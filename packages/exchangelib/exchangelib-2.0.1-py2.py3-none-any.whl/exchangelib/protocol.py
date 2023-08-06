# coding=utf-8
"""
A protocol is an endpoint for EWS service connections. It contains all necessary information to make HTTPS connections.

Protocols should be accessed through an Account, and are either created from a default Configuration or autodiscovered
when creating an Account.
"""
from __future__ import unicode_literals

import datetime
import logging
from multiprocessing.pool import ThreadPool
import os
from threading import Lock

from cached_property import threaded_cached_property
import requests.adapters
import requests.sessions
from future.utils import with_metaclass, python_2_unicode_compatible
from future.moves.queue import LifoQueue, Empty, Full
from six import string_types

from .errors import TransportError, SessionPoolMinSizeReached
from .properties import FreeBusyViewOptions, MailboxData, TimeWindow, TimeZone
from .services import GetServerTimeZones, GetRoomLists, GetRooms, ResolveNames, GetUserAvailability, \
    GetSearchableMailboxes, ExpandDL
from .transport import get_auth_instance, get_service_authtype, DEFAULT_HEADERS
from .util import split_url
from .version import Version, API_VERSIONS

log = logging.getLogger(__name__)


def close_connections():
    CachingProtocol.clear_cache()


class BaseProtocol(object):
    # Base class for Protocol which implements the bare essentials

    # The maximum number of sessions (== TCP connections, see below) we will open to this service endpoint. Keep this
    # low unless you have an agreement with the Exchange admin on the receiving end to hammer the server and
    # rate-limiting policies have been disabled for the connecting user.
    SESSION_POOLSIZE = 4
    # We want only 1 TCP connection per Session object. We may have lots of different credentials hitting the server and
    # each credential needs its own session (NTLM auth will only send credentials once and then secure the connection,
    # so a connection can only handle requests for one credential). Having multiple connections ser Session could
    # quickly exhaust the maximum number of concurrent connections the Exchange server allows from one client.
    CONNECTIONS_PER_SESSION = 1
    # Timeout for HTTP requests
    TIMEOUT = 120

    # The adapter class to use for HTTP requests. Override this if you need e.g. proxy support or specific TLS versions
    HTTP_ADAPTER_CLS = requests.adapters.HTTPAdapter

    def __init__(self, config):
        from .configuration import Configuration
        if not isinstance(config, Configuration):
            raise ValueError("'config' %r must be a Configuration instance" % config)
        if not config.service_endpoint:
            raise AttributeError("'config.service_endpoint' must be set")
        self.config = config
        self._session_pool_size = self.SESSION_POOLSIZE
        self._session_pool = None  # Consumers need to fill the session pool themselves
        self._session_pool_lock = None

    @property
    def service_endpoint(self):
        return self.config.service_endpoint

    @property
    def auth_type(self):
        return self.config.auth_type

    @property
    def credentials(self):
        return self.config.credentials

    @property
    def retry_policy(self):
        return self.config.retry_policy

    @threaded_cached_property
    def server(self):
        return split_url(self.service_endpoint)[1]

    def __del__(self):
        # pylint: disable=bare-except
        try:
            self.close()
        except:  # nosec
            # __del__ should never fail
            pass

    def close(self):
        log.debug('Server %s: Closing sessions', self.server)
        while True:
            try:
                self._session_pool.get(block=False).close()
            except Empty:
                break

    @classmethod
    def get_adapter(cls):
        # We want just one connection per session. No retries, since we wrap all requests in our own retry handler
        return cls.HTTP_ADAPTER_CLS(
            pool_block=True,
            pool_connections=cls.CONNECTIONS_PER_SESSION,
            pool_maxsize=cls.CONNECTIONS_PER_SESSION,
            max_retries=0,
        )

    @property
    def session_pool_size(self):
        return self._session_pool_size

    def decrease_poolsize(self):
        """Decreases the session pool size in response to error messages from the server requesting to rate-limit
        requests. We decrease by one session per call.
        """
        # Take a single session from the pool and discard it. We need to protect this with a lock while we are changing
        # the pool size variable, to avoid race conditions. We must keep at least one session in the pool.
        if self._session_pool_size <= 1:
            raise SessionPoolMinSizeReached('Session pool size cannot be decreased further')
        with self._session_pool_lock:
            if self._session_pool_size <= 1:
                log.debug('Session pool size was decreased in another thread')
                return
            log.warning('Lowering session pool size from %s to %s', self._session_pool_size,
                        self._session_pool_size - 1)
            self.get_session().close()
            self._session_pool_size -= 1

    def get_session(self):
        _timeout = 60  # Rate-limit messages about session starvation
        while True:
            try:
                log.debug('Server %s: Waiting for session', self.server)
                session = self._session_pool.get(timeout=_timeout)
                log.debug('Server %s: Got session %s', self.server, session.session_id)
                return session
            except Empty:
                # This is normal when we have many worker threads starving for available sessions
                log.debug('Server %s: No sessions available for %s seconds', self.server, _timeout)

    def release_session(self, session):
        # This should never fail, as we don't have more sessions than the queue contains
        log.debug('Server %s: Releasing session %s', self.server, session.session_id)
        try:
            self._session_pool.put(session, block=False)
        except Full:
            log.debug('Server %s: Session pool was already full %s', self.server, session.session_id)

    def retire_session(self, session):
        # The session is useless. Close it completely and place a fresh session in the pool
        log.debug('Server %s: Retiring session %s', self.server, session.session_id)
        session.close()
        del session
        self.release_session(self.create_session())

    def renew_session(self, session):
        # The session is useless. Close it completely and place a fresh session in the pool
        log.debug('Server %s: Renewing session %s', self.server, session.session_id)
        session.close()
        del session
        return self.create_session()

    def create_session(self):
        session = requests.sessions.Session()
        # Add some extra info
        session.session_id = sum(map(ord, str(os.urandom(100))))  # Used for debugging messages in services
        session.protocol = self
        session.auth = get_auth_instance(credentials=self.credentials, auth_type=self.auth_type)
        # Create a copy of the headers because headers are mutable and session users may modify headers
        session.headers.update(DEFAULT_HEADERS.copy())
        session.mount('http://', adapter=self.get_adapter())
        session.mount('https://', adapter=self.get_adapter())
        log.debug('Server %s: Created session %s', self.server, session.session_id)
        return session

    @classmethod
    def raw_session(cls):
        s = requests.sessions.Session()
        s.mount('http://', adapter=cls.get_adapter())
        s.mount('https://', adapter=cls.get_adapter())
        return s

    def __repr__(self):
        return self.__class__.__name__ + repr((self.service_endpoint, self.credentials, self.auth_type))


class CachingProtocol(type):
    _protocol_cache = {}
    _protocol_cache_lock = Lock()

    def __call__(cls, *args, **kwargs):
        # Cache Protocol instances that point to the same endpoint and use the same credentials. This ensures that we
        # re-use thread and connection pools etc. instead of flooding the remote server. This is a modified Singleton
        # pattern.
        #
        # We ignore auth_type from kwargs in the cache key. We trust caller to supply the correct auth_type - otherwise
        # __init__ will guess the correct auth type.

        # We may be using multiple different credentials and changing our minds on TLS verification. This key
        # combination should be safe.
        _protocol_cache_key = kwargs['config'].service_endpoint, kwargs['config'].credentials

        protocol = cls._protocol_cache.get(_protocol_cache_key)
        if isinstance(protocol, Exception):
            # The input data leads to a TransportError. Re-throw
            raise protocol
        if protocol is not None:
            return protocol

        # Acquire lock to guard against multiple threads competing to cache information. Having a per-server lock is
        # probably overkill although it would reduce lock contention.
        log.debug('Waiting for _protocol_cache_lock')
        with cls._protocol_cache_lock:
            protocol = cls._protocol_cache.get(_protocol_cache_key)
            if isinstance(protocol, Exception):
                # Someone got ahead of us while holding the lock, but the input data leads to a TransportError. Re-throw
                raise protocol
            if protocol is not None:
                # Someone got ahead of us while holding the lock
                return protocol
            log.debug("Protocol __call__ cache miss. Adding key '%s'", str(_protocol_cache_key))
            try:
                protocol = super(CachingProtocol, cls).__call__(*args, **kwargs)
            except TransportError as e:
                # This can happen if, for example, autodiscover supplies us with a bogus EWS endpoint
                log.warning('Failed to create cached protocol with key %s: %s', _protocol_cache_key, e)
                cls._protocol_cache[_protocol_cache_key] = e
                raise e
            cls._protocol_cache[_protocol_cache_key] = protocol
        return protocol

    @classmethod
    def clear_cache(mcs):
        for key, protocol in mcs._protocol_cache.items():
            if isinstance(protocol, Exception):
                continue
            service_endpoint = key[0]
            log.debug("Service endpoint '%s': Closing sessions", service_endpoint)
            protocol.close()
        mcs._protocol_cache.clear()


@python_2_unicode_compatible
class Protocol(with_metaclass(CachingProtocol, BaseProtocol)):
    def __init__(self, *args, **kwargs):
        super(Protocol, self).__init__(*args, **kwargs)

        # Autodetect authentication type if necessary
        # pylint: disable=access-member-before-definition
        if self.config.auth_type is None:
            name = self.credentials.username if self.credentials and self.credentials.username else 'DUMMY'
            self.config.auth_type, version_hint = get_service_authtype(
                service_endpoint=self.service_endpoint, versions=API_VERSIONS, name=name
            )
        else:
            version_hint = None

        # Try to behave nicely with the Exchange server. We want to keep the connection open between requests.
        # We also want to re-use sessions, to avoid the NTLM auth handshake on every request.
        self._session_pool = self._create_session_pool()
        self._session_pool_lock = Lock()

        if not self.config.version:
            # Version.guess() needs auth objects and a working session pool
            self.config.version = Version.guess(self, hint=version_hint)

    @property
    def version(self):
        return self.config.version

    def _create_session_pool(self):
        # Create a pool to reuse sessions containing connections to the server
        session_pool = LifoQueue(maxsize=self._session_pool_size)
        for _ in range(self._session_pool_size):
            session_pool.put(self.create_session(), block=False)
        return session_pool

    @threaded_cached_property
    def thread_pool(self):
        # Used by services to process service requests that are able to run in parallel. Thread pool should be
        # larger than the connection pool so we have time to process data without idling the connection.
        # Create the pool as the last thing here, since we may fail in the version or auth type guessing, which would
        # leave open threads around to be garbage collected.
        thread_poolsize = 4 * self._session_pool_size
        return ThreadPool(processes=thread_poolsize)

    def get_timezones(self, timezones=None, return_full_timezone_data=False):
        """ Get timezone definitions from the server

        :param timezones: A list of EWSDateTime instances. If None, fetches all timezones from server
        :param return_full_timezone_data: If true, also returns periods and transitions
        :return: A list of (tz_id, name, periods, transitions) tuples
        """
        return GetServerTimeZones(protocol=self).call(
            timezones=timezones, return_full_timezone_data=return_full_timezone_data
        )

    def get_free_busy_info(self, accounts, start, end, merged_free_busy_interval=30, requested_view='DetailedMerged'):
        """ Returns free/busy information for a list of accounts

        :param accounts: A list of (account, attendee_type, exclude_conflicts) tuples, where account is an Account
               object, attendee_type is a MailboxData.attendee_type choice, and exclude_conflicts is a boolean.
        :param start: The start datetime of the request
        :param end: The end datetime of the request
        :param merged_free_busy_interval: The interval, in minutes, of merged free/busy information
        :param requested_view: The type of information returned. Possible values are defined in the
               FreeBusyViewOptions.requested_view choices.
        :return: A generator of FreeBusyView objects
        """
        from .account import Account
        for account, attendee_type, exclude_conflicts in accounts:
            if not isinstance(account, Account):
                raise ValueError("'accounts' item %r must be an 'Account' instance" % account)
            if attendee_type not in MailboxData.ATTENDEE_TYPES:
                raise ValueError("'accounts' item %r must be one of %s" % (attendee_type, MailboxData.ATTENDEE_TYPES))
            if not isinstance(exclude_conflicts, bool):
                raise ValueError("'accounts' item %r must be a 'bool' instance" % exclude_conflicts)
        if start >= end:
            raise ValueError("'start' must be less than 'end' (%s -> %s)" % (start, end))
        if not isinstance(merged_free_busy_interval, int):
            raise ValueError("'merged_free_busy_interval' value %r must be an 'int'" % merged_free_busy_interval)
        if requested_view not in FreeBusyViewOptions.REQUESTED_VIEWS:
            raise ValueError(
                "'requested_view' value %r must be one of %s" % (requested_view, FreeBusyViewOptions.REQUESTED_VIEWS))
        _, _, periods, transitions, transitions_groups = list(self.get_timezones(
            timezones=[start.tzinfo],
            return_full_timezone_data=True
        ))[0]
        return GetUserAvailability(self).call(
                timezone=TimeZone.from_server_timezone(
                    periods=periods,
                    transitions=transitions,
                    transitionsgroups=transitions_groups,
                    for_year=start.year
                ),
                mailbox_data=[MailboxData(
                    email=account.primary_smtp_address,
                    attendee_type=attendee_type,
                    exclude_conflicts=exclude_conflicts
                ) for account, attendee_type, exclude_conflicts in accounts],
                free_busy_view_options=FreeBusyViewOptions(
                    time_window=TimeWindow(start=start, end=end),
                    merged_free_busy_interval=merged_free_busy_interval,
                    requested_view=requested_view,
                ),
        )

    def get_roomlists(self):
        return GetRoomLists(protocol=self).call()

    def get_rooms(self, roomlist):
        from .properties import RoomList
        return GetRooms(protocol=self).call(roomlist=RoomList(email_address=roomlist))

    def resolve_names(self, names, return_full_contact_data=False, search_scope=None, shape=None):
        """ Resolve accounts on the server using partial account data, e.g. an email address or initials

        :param names: A list of identifiers to query
        :param return_full_contact_data: If True, returns full contact data
        :param search_scope: The scope to perform the search. Must be one of SEARCH_SCOPE_CHOICES
        :param shape:
        :return: A list of Mailbox items or, if return_full_contact_data is True, tuples of (Mailbox, Contact) items
        """
        from .items import SHAPE_CHOICES, SEARCH_SCOPE_CHOICES
        if search_scope:
            if search_scope not in SEARCH_SCOPE_CHOICES:
                raise ValueError("'search_scope' %s must be one if %s" % (search_scope, SEARCH_SCOPE_CHOICES))
        if shape:
            if shape not in SHAPE_CHOICES:
                raise ValueError("'shape' %s must be one if %s" % (shape, SHAPE_CHOICES))
        return list(ResolveNames(protocol=self).call(
            unresolved_entries=names, return_full_contact_data=return_full_contact_data, search_scope=search_scope,
            contact_data_shape=shape,
        ))

    def expand_dl(self, distribution_list):
        """ Expand distribution list into it's members

        :param distribution_list: SMTP address of the distribution list to expand, or a DLMailbox representing the list
        :return: List of Mailbox items that are members of the distribution list
        """
        from .properties import DLMailbox
        if isinstance(distribution_list, string_types):
            distribution_list = DLMailbox(email_address=distribution_list, mailbox_type='PublicDL')
        return list(ExpandDL(protocol=self).call(distribution_list=distribution_list))

    def get_searchable_mailboxes(self, search_filter=None, expand_group_membership=False):
        """This method is only available to users who have been assigned the Discovery Management RBAC role. See
        https://docs.microsoft.com/en-us/exchange/permissions-exo/permissions-exo

        :param search_filter: Is set, must be a single email alias
        :param expand_group_membership: If True, returned distribution lists are expanded
        :return: a list of SearchableMailbox, FailedMailbox or Exception instances
        """
        return list(GetSearchableMailboxes(protocol=self).call(
            search_filter=search_filter,
            expand_group_membership=expand_group_membership,
        ))

    def __getstate__(self):
        # The thread and session pools cannot be pickled
        state = self.__dict__.copy()
        try:
            del state['thread_pool']
        except KeyError:
            # thread_pool is a cached property and may not exist
            pass
        del state['_session_pool']
        del state['_session_pool_lock']
        return state

    def __setstate__(self, state):
        # Restore the session pool. The thread pool is a property and will recreate itself
        self.__dict__.update(state)
        self._session_pool = self._create_session_pool()
        self._session_pool_lock = Lock()

    def __str__(self):
        return '''\
EWS url: %s
Product name: %s
EWS API version: %s
Build number: %s
EWS auth: %s''' % (
            self.service_endpoint,
            self.version.fullname,
            self.version.api_version,
            self.version.build,
            self.auth_type,
        )


class NoVerifyHTTPAdapter(requests.adapters.HTTPAdapter):
    # An HTTP adapter that ignores TLS validation errors. Use at own risk.
    def cert_verify(self, conn, url, verify, cert):
        # pylint: disable=unused-argument
        # We're overiding a method so we have to keep the signature
        super(NoVerifyHTTPAdapter, self).cert_verify(conn=conn, url=url, verify=False, cert=cert)


class RetryPolicy(object):
    """Stores retry logic used when faced with errors from the server
    """
    @property
    def fail_fast(self):
        # Used to choose the error handling policy. When True, a fault-tolerant policy is used. False, a fail-fast
        # policy is used.
        raise NotImplementedError()

    @property
    def back_off_until(self):
        raise NotImplementedError()

    @back_off_until.setter
    def back_off_until(self, value):
        raise NotImplementedError()


class FailFast(RetryPolicy):
    """Fail immediately on server errors
    """
    @property
    def fail_fast(self):
        return True

    @property
    def back_off_until(self):
        return None


class FaultTolerance(RetryPolicy):
    """Enables fault-tolerant error handling. Tells internal methods to do an exponential back off when requests start
    failing, and wait up to max_wait seconds before failing.
    """
    def __init__(self, max_wait=3600):
        self.max_wait = max_wait
        self._back_off_until = None
        self._back_off_lock = Lock()

    def __getstate__(self):
        # Locks cannot be pickled
        state = self.__dict__.copy()
        del state['_back_off_lock']
        return state

    def __setstate__(self, state):
        # Restore the lock
        self.__dict__.update(state)
        self._back_off_lock = Lock()

    @property
    def fail_fast(self):
        return False

    @property
    def back_off_until(self):
        """Returns the back off value as a datetime. Resets the current back off value if it has expired."""
        if self._back_off_until is None:
            return None
        with self._back_off_lock:
            if self._back_off_until is None:
                return None
            if self._back_off_until < datetime.datetime.now():
                self._back_off_until = None  # The back off value has expired. Reset
                return None
            return self._back_off_until

    @back_off_until.setter
    def back_off_until(self, value):
        with self._back_off_lock:
            self._back_off_until = value

    def back_off(self, seconds):
        if seconds is None:
            seconds = 60  # Back off 60 seconds if we didn't get an explicit suggested value
        value = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        with self._back_off_lock:
            self._back_off_until = value
