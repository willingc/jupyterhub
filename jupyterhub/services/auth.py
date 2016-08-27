"""Authenticating services with JupyterHub

Hub receives cookies sent for verification. Hub replies with a JSON model
describing the authenticated user.

HubAuth can be used in any application, even outside tornado.

HubAuthenticated is a mixin class for tornado handlers that should
authenticate with the Hub.
"""

import socket
import time
from urllib.parse import quote

import requests

from tornado.log import app_log
from tornado.web import HTTPError

from traitlets.config import Configurable
from traitlets import Unicode, Integer, Instance, default

from ..utils import url_path_join


class _ExpiringDict(dict):
    """Cache for the Hub API requests

    A dict-like cache where values will expire after ``max_age`` seconds.

    Uses a monotonic timer (``time.monotonic``) to count forward in time and
    is unaffected by system clock changes.

    Attributes
    ----------
    max_age : Number of seconds before cached values will expire.
              ``max_age = 0`` means keep the cache forever.
    """

    max_age = 0

    def __init__(self, max_age=0):
        self.max_age = max_age
        self.timestamps = {}
        self.values = {}

    def __setitem__(self, key, value):
        """Store key and record timestamp"""
        self.timestamps[key] = time.monotonic()
        self.values[key] = value

    def _check_age(self, key):
        """Check a key's timestamp"""
        if key not in self.values:
            # not registered, nothing to do
            return
        now = time.monotonic()
        timestamp = self.timestamps[key]
        if self.max_age > 0 and timestamp + self.max_age < now:
            self.values.pop(key)
            self.timestamps.pop(key)

    def __contains__(self, key):
        """Check dict for `key in dict`"""
        self._check_age(key)
        return key in self.values

    def __getitem__(self, key):
        """Check age of cache before returning value"""
        self._check_age(key)
        return self.values[key]

    def get(self, key, default=None):
        """Returns value for a given key"""
        try:
            return self[key]
        except KeyError:
            return default


class HubAuth(Configurable):
    """A class for authenticating with JupyterHub

    This class can be used by any application.

    If using tornado, use via :class:`HubAuthenticated` mixin.
    If using manually, use the ``.user_for_cookie(cookie_value)`` method
    to identify the user corresponding to a given cookie value.

    The following config MUST be set:

    - api_token: token for authenticating with JupyterHub's REST API
    - cookie_name: the name of the cookie I should be using
    - login_url: the *public* ``/hub/login`` URL for the Hub

    The following config may be set:

    - api_url: the base URL of the Hub's internal API
    - cookie_cache_max_age: the number of seconds responses
      from the Hub should be cached.
    """

    # where is the hub
    api_url = Unicode('http://127.0.0.1:8081/hub/api',
        help="""The base API URL of the Hub.

        Typically http://hub-ip:hub-port/hub/api
        """
    ).tag(config=True)

    login_url = Unicode('https://127.0.0.1:8000/hub/login',
        help="""The login URL of the Hub
        
        Typically https://public-hub-host/hub/login
        """
    ).tag(config=True)

    api_token = Unicode('',
        help="""API key for accessing Hub API.

        Generate with `jupyterhub token [username]` or add to JupyterHub.api_tokens config.
        """
    ).tag(config=True)

    cookie_name = Unicode(
        help="""The name of the cookie I should be looking for"""
    ).tag(config=True)
    cookie_cache_max_age = Integer(300,
        help="""The maximum time (in seconds) to cache the Hub's response for cookie authentication.

        A larger value reduces load on the Hub and occasional response lag.
        A smaller value reduces propagation time of changes on the Hub (rare).

        Default: 300 (five minutes)
        """
    ).tag(config=True)
    cookie_cache = Instance(_ExpiringDict, allow_none=False)
    @default('cookie_cache')
    def _cookie_cache(self):
        return _ExpiringDict(self.cookie_cache_max_age)

    def user_for_cookie(self, encrypted_cookie, use_cache=True):
        """Ask the Hub to identify the user for a given cookie.

        Args:
            encrypted_cookie (str): the cookie value (pass the encrypted
                                    cookie value and the Hub will decrypt)
            use_cache (bool): determines whether cached values are used.
                              Default: True. Specify ``use_cache=False`` to
                              ignore cached cookie values.

        Returns:
            user_model (dict): The user model, if a user is identified.
                               None, if authentication fails.

            The 'name' field of user_model contains the user's name.
        """
        if use_cache:
            cached = self.cookie_cache.get(encrypted_cookie)
            if cached is not None:
                return cached
        try:
            r = requests.get(
                url_path_join(self.api_url,
                              "authorizations/cookie",
                              self.cookie_name,
                              quote(encrypted_cookie, safe=''),
                ),
                headers = {
                    'Authorization' : 'token %s' % self.api_token,
                },
            )
        except requests.ConnectionError:
            msg = "Failed to connect to Hub API at %r." % self.api_url
            msg += "  Is the Hub accessible at this URL (from host: %s)?" % socket.gethostname()
            if '127.0.0.1' in self.api_url:
                msg += "  Make sure to set c.JupyterHub.hub_ip to an IP accessible to" + \
                       " single-user servers if the servers are not on the same host as the Hub."
            raise HTTPError(500, msg)

        if r.status_code == 404:
            data = None
        elif r.status_code == 403:
            app_log.error("I don't have permission to verify cookies, my auth token may have expired: [%i] %s", r.status_code, r.reason)
            raise HTTPError(500, "Permission failure checking authorization, I may need a new token")
        elif r.status_code >= 500:
            app_log.error("Upstream failure verifying auth token: [%i] %s", r.status_code, r.reason)
            raise HTTPError(502, "Failed to check authorization (upstream problem)")
        elif r.status_code >= 400:
            app_log.warn("Failed to check authorization: [%i] %s", r.status_code, r.reason)
            raise HTTPError(500, "Failed to check authorization")
        else:
            data = r.json()
        self.cookie_cache[encrypted_cookie] = data
        return data

    def get_user(self, handler):
        """Get the Hub user for a given tornado handler.

        Checks cookie with the Hub to identify the current user.

        Args:
            handler (tornado.web.RequestHandler): the current request handler

        Returns:
            user_model (dict): The user model, if a user is identified.
                               None, if authentication fails.

            The 'name' field contains the user's name.
        """

        # only allow this to be called once per handler
        # avoids issues if an error is raised,
        # since this may be called again when trying to render the error page
        if hasattr(handler, '_cached_hub_user'):
            return handler._cached_hub_user

        handler._cached_hub_user = None
        encrypted_cookie = handler.get_cookie(self.cookie_name)
        if encrypted_cookie:
            user_model = self.user_for_cookie(encrypted_cookie)
            handler._cached_hub_user = user_model
            return user_model
        else:
            app_log.debug("No token cookie")
            return None


class HubAuthenticated(object):
    """Mixin for tornado handlers that are authenticated with JupyterHub

    A handler that mixes this in must have these attributes/properties:

    - .hub_auth: A HubAuth instance
    - .hub_users: A set of usernames to allow.
      If left unspecified or None, any Hub user will be allowed.

    Examples::

        class MyHandler(HubAuthenticated, web.RequestHandler):
            hub_users = {'inara', 'mal'}

            def initialize(self, hub_auth):
                self.hub_auth = hub_auth

            @web.authenticated
            def get(self):
                ...
    """
    hub_users = None  # set of allowed users
    hub_auth = None   # must be a HubAuth instance

    def check_hub_user(self, user_model):
        """Check whether Hub-authenticated user should be allowed.

        Returns the input if the user should be allowed, None otherwise.

        Override if you want to check additional parameters other than the
        username's presence in hub_users list.

        Args:
            user_model (dict): the user model returned from :class:`HubAuth`
        Returns:
            user_model (dict): The user model if the user should be allowed.
                               None otherwise.
        """
        if self.hub_users is None:
            # no users specified, allow any authenticated Hub user
            return user_model
        name = user_model['name']
        if name in self.hub_users:
            return user_model
        else:
            app_log.warn("Not allowing Hub user %s" % name)
            return None

    def get_current_user(self):
        """Tornado's authentication method

        Returns:
            user_model (dict): The user model, if a user is identified.
                               None, if authentication fails.
        """
        user_model = self.hub_auth.get_user(self)
        if not user_model:
            return
        return self.check_hub_user(user_model)
