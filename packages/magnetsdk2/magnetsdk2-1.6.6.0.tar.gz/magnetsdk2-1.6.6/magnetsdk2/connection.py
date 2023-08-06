# -*- coding: utf-8 -*-
"""
This module implements the Connection class, which is used for low-level interaction with the
Niddel Magnet v2 API.
"""
import logging
import os
import sys

import six
from uuid import UUID
from requests import request
from six.moves.configparser import RawConfigParser
from six.moves.urllib.parse import urlsplit, quote_plus

from magnetsdk2 import __version__ as magnetsdk_version
from magnetsdk2.time import UTC
from magnetsdk2.validation import is_valid_uuid, is_valid_uri, is_valid_port, \
     is_valid_alert_sortBy, is_valid_alert_status, parse_date

# Default values used for the configuration
_CONFIG_DIR = os.path.expanduser('~/.magnetsdk')
_CONFIG_FILE = os.path.join(_CONFIG_DIR, "config")
_DEFAULT_CONFIG = {'endpoint': 'https://api.[region].niddel.com/v2'}
_API_KEY_HEADER = 'X-Api-Key'
_PAGE_SIZE = 100

class Connection(object):
    """ This class encapsulates accessing the Niddel Magnet v2 API (https://api.[region].niddel.com/v2)
     using a particular configuration profile from ~/.magnetsdk/config, and is wrapper around
     the requests library that is used for all accesses.
    """

    def __init__(self, profile='default', api_key=None, endpoint=None, user_agent=None):
        """ Initializes the connection with the proper configuration data.
        :param profile: the profile name to use in ~/.magnetsdk/config
        :param api_key: if provided, this API key is used instead of the one on the
        configuration file
        :param endpoint: if provided this endpoint URL is used instead of the one on the
        configuration file
        """
        # initialize logger and credential cache
        self._logger = logging.getLogger('magnetsdk2')
        self._org_creds_cache = {}

        # initially get configuration from environment
        self.endpoint = os.getenv('MAGNETSDK_API_ENDPOINT', _DEFAULT_CONFIG['endpoint'])
        self.api_key = os.getenv('MAGNETSDK_API_KEY')

        # read from configuration file and profile
        if profile and os.path.isfile(_CONFIG_FILE):
            parser = RawConfigParser(_DEFAULT_CONFIG)
            parser.read(_CONFIG_FILE)
            if not parser.has_section(profile):
                raise ValueError('profile %s not found in %s' % (profile, _CONFIG_FILE))
            self.api_key = parser.get(profile, 'api_key')
            self.endpoint = parser.get(profile, 'endpoint')

        # explicit parameters override whatever was read previously
        if api_key is not None:
            if not isinstance(api_key, six.string_types):
                raise ValueError("API key must be a string")
            self.api_key = api_key
        if endpoint is not None:
            if not is_valid_uri(endpoint):
                raise ValueError("endpoint must be a string containing a valid URL")
            self.endpoint = endpoint

        # ensure we have an API key to work with
        if not self.api_key:
            raise ValueError('no API key to use')

        # parse endpoint data and ensure it ends with a slash
        endpoint = urlsplit(self.endpoint, 'https')
        self.endpoint = endpoint.geturl()
        if not self.endpoint.endswith('/'):
            self.endpoint += '/'

        # check for certificate pinning for the destination server
        if os.path.isfile(os.path.join(_CONFIG_DIR, endpoint.hostname + '.pem')):
            self.verify = os.path.join(_CONFIG_DIR, endpoint.hostname + '.pem')
        else:
            self.verify = True

        self._logger.debug('%s: endpoint=%r, verify=%r', self.__class__.__name__, self.endpoint,
                           self.verify)
        self._proxies = None

        # support passing user-agent as Splunk TA or App version
        # so we can identify in backend the client version installed
        if user_agent:
            self.user_agent = "Magnet SDK Python/v%s; %s" % (magnetsdk_version, user_agent) 
        else:
            self.user_agent = "Magnet SDK Python/v%s" % magnetsdk_version

    def __del__(self):
        self.close()

    def set_proxy(self, proxy, proxy_port=None, proxy_user=None, proxy_pass=None,
                  proxy_proto='https'):
        """Configure this connection to use an HTTPS proxy to access the API endpoint.
        :param proxy: string containing the proxy hostname or iP address
        :param proxy_port: integer containing the proxy port to connect to (optional)
        :param proxy_user: string containing the username to use for basic authentication to the
        proxy (optional)
        :param proxy_pass: string containing the password to use for basic authentication to the
        proxy (optional)
        :param proxy_proto: string containing the proxy protocol equal to either 'http' or 'https'
        :return: the proxy URL
        """
        if not isinstance(proxy_proto, six.string_types) or proxy_proto not in ('http', 'https'):
            raise ValueError("proxy protocol must be a string")
        proxy_url = proxy_proto + '://'
        proxy_url_sanitized = proxy_proto + '://'
        if proxy_user and proxy_pass:
            if not isinstance(proxy_user, six.string_types):
                raise ValueError("proxy username must be a string")
            if not isinstance(proxy_pass, six.string_types):
                raise ValueError("proxy password must be a string")
            proxy_url += quote_plus(proxy_user) + ':' + quote_plus(proxy_pass) + '@'
            proxy_url_sanitized += quote_plus(proxy_user) + ':' + ('*' * len(proxy_pass)) + '@'
        elif proxy_user:
            if not isinstance(proxy_user, six.string_types):
                raise ValueError("proxy username must be a string")
            proxy_url += quote_plus(proxy_user) + '@'
            proxy_url_sanitized += quote_plus(proxy_user) + '@'
        if not isinstance(proxy, six.string_types):
            raise ValueError("proxy hostname or IP address must be a string")
        proxy_url += proxy
        proxy_url_sanitized += proxy
        if proxy_port:
            if isinstance(proxy_port, six.string_types):
                proxy_port = int(proxy_port)
            if not is_valid_port(proxy_port):
                raise ValueError("invalid proxy port")
            proxy_url += ":%i" % proxy_port
            proxy_url_sanitized += ":%i" % proxy_port
        self.set_proxy_url(proxy_url)
        self._logger.debug('using proxy URL ' + proxy_url_sanitized)
        return proxy_url

    def set_proxy_url(self, proxy_url):
        """Configure this connection to use an HTTPS proxy to access the API endpoint using a
        URL as per http://docs.python-requests.org/en/master/user/advanced/#proxies
        :param proxy_url: string containing the proxy URL
        """
        self._proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

    def clear_proxy(self):
        """Removes the existing proxy configuration so that """
        if self._proxies:
            self.close()
            self._proxies = None

    def close(self):
        """ Closes the Connection object.
        """
        pass

    def _request(self, method, path, params=None, body=None, region=None):
        """ Performs an HTTP operation using the base API endpoint, API key and SSL validation /
        cert pinning obtained from the configuration file.
        :param method: string with the the HTTP method to use ('GET', 'PUT', etc.)
        :param path: string with the path to append to the base API endpoint
        :param params: dict with the query parameters to submit
        :return: the requests.Response object
        """
        endpoint=""

        if region:
            endpoint = self.endpoint.replace("[region]", region)
        else:
            endpoint = self.endpoint.replace("[region]", "global")

        response = request(method=method, url=endpoint + path, params=params, json=body,
                           verify=self.verify,
                           proxies=self._proxies, timeout=(5, 60),
                           headers={_API_KEY_HEADER: self.api_key,
                                    "Accept-Encoding": "gzip, deflate",
                                    "User-Agent": self.user_agent,
                                    "Accept": "application/json"})
        if response.request.body:
            msg = '{0:s} {1:s} ({2:d} bytes in body)'.format(response.request.method,
                                                             response.request.url,
                                                             len(response.request.body))
            self._logger.debug(msg)
        else:
            self._logger.debug('{0:s} {1:s}'.format(response.request.method, response.request.url))
        self._logger.debug("got {0:d} response".format(response.status_code))
        return response

    def _request_retry(self, method, path, params=None, body=None, ok_status=(200, 404), retries=5, region=None):
        """ Wrapper around self._request that retries on exceptions and unexpected status codes.
        """
        i = 1
        while True:
            try:
                response = self._request(method, path, params, body, region)
                if i >= retries or response.status_code in ok_status:
                    return response
            except:
                self._logger.exception('error at try %i of %s request for %s with params=%s', i,
                                       method, path, repr(params))
                if i >= retries:
                    six.reraise(*sys.exc_info())
            i += 1

    def iter_organizations(self):
        """ Generator that allows iteration over all of the organizations that this connections's
        API key has access to.
        :return: an iterator over the decoded JSON objects that represent organizations.
        """
        params = {
            'page': 1,
            'size': _PAGE_SIZE
        }
        while True:
            response = self._request_retry("GET", path='organizations', params=params)
            if response.status_code == 200:
                organization_list = response.json()
                for organization in organization_list:
                    yield organization
                if len(organization_list) < _PAGE_SIZE:
                    return
            elif response.status_code == 404:
                return
            else:
                response.raise_for_status()
            params['page'] += 1

    def get_organization(self, organization_id):
        """ Retrieves detailed data from an organization this API key has accessed to based on its
        ID.
        :param organization_id: string with the UUID-style unique ID of the organization
        :return: decoded JSON objects that represents the organization or None if not found
        """
        region=None
        if not is_valid_uuid(organization_id):
            raise ValueError("organization id should be a string in UUID format")
        for org in self.iter_organizations():
            if str(organization_id) == org['id']:
                region = org['region']
        response = self._request_retry("GET", path='organizations/%s' % organization_id,region=region)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()

    def get_organization_topology(self, organization_id):
        """Retrieves detailed data from the organization topology this API key has accessed to based on its
        ID.
        :param organization_id: string with the UUID-style unique ID of the organization
        :return: decoded JSON objects that represents the organization topology or None if not found
        """
        region=None
        if not is_valid_uuid(organization_id):
            raise ValueError("organization id should be a string in UUID format")
        for org in self.iter_organizations():
            if str(organization_id) == org['id']:
                region = org['region']
        response = self._request_retry("GET", path='organizations/%s/settings' % organization_id,region=region)
        if response.status_code == 200:
            yield response.json()
            return
        elif response.status_code == 404:
            return
        else:
            response.raise_for_status()

    def get_organization_credentials(self, organization_id, cache=True):
        """ Retrieves a new set of temporary AWS credentials to allow access to an organization's
        S3 bucket. Typically used to upload log files. Will cache the response and return the same
        credentials if they have at least 10 minutes before expiration.
        :param organization_id: string with the UUID-style unique ID of the organization
        :param cache: boolean controlling whether credentials are cached in this connection
        :return: decoded JSON objects that represents the credentials
        """
        region=None
        if not is_valid_uuid(organization_id):
            raise ValueError("organization id should be a string in UUID format")
        for org in self.iter_organizations():
            if str(organization_id) == org['id']:
                region = org['region']

        # try cached response first, must have at least 10 minutes validity
        if cache:
            cached_response = self._org_creds_cache.get(organization_id, None)
            if cached_response:
                exp = iso8601.parse_date(cached_response['expiration'])
                if exp >= (datetime.datetime.now(UTC) + datetime.timedelta(minutes=10)):
                    return cached_response
                else:
                    del self._org_creds_cache[organization_id]

        # get a new credential
        response = self._request_retry("GET", path='organizations/%s/credentials' % organization_id,region=region)
        if response.status_code == 200:
            cached_response = response.json()
            if cache:
                self._org_creds_cache[organization_id] = cached_response
            return cached_response
        else:
            response.raise_for_status()

    def iter_organization_alerts(self, organization_id, fromDate=None, toDate=None,
                                 sortBy="logDate", status=None):
        """ Generator that allows iteration over an organization's alerts, with optional filters.
        :param organization_id: string with the UUID-style unique ID of the organization
        :param fromDate: only list alerts with dates >= this parameter
        :param toDate: only list alerts with dates <= this parameter
        :param sortBy: one of 'logDate' or 'batchDate', controls which date field fromDate and
        toDate apply to
        :param status: a list or set containing one or more of 'new', 'under_investigation',
        'rejected', 'resolved'
        :return: an iterator over the decoded JSON objects that represent alerts.
        """
        region=None
        if not is_valid_uuid(organization_id):
            raise ValueError("organization id should be a string in UUID format")
        for org in self.iter_organizations():
            if str(organization_id) == org['id']:
                region = org['region']
        if not is_valid_alert_sortBy(sortBy):
            raise ValueError("sortBy must be either 'logDate' or 'batchDate'")
        if status is not None and not is_valid_alert_status(status):
            raise ValueError(
                "status must be an iterable with one or more of 'new', 'under_investigation', " +
                "'rejected' or 'resolved'")

        # loop over alert pages and yield them
        params = {
            'page': 1,
            'size': _PAGE_SIZE,
            'sortBy': sortBy
        }
        if fromDate:
            params['fromDate'] = parse_date(fromDate)
        if toDate:
            params['toDate'] = parse_date(toDate)
        if status:
            params['status'] = status

        while True:
            response = self._request_retry("GET", path='organizations/%s/alerts' % organization_id,
                                           params=params,region=region)
            if response.status_code == 200:
                alert_list = response.json()
                for alert in alert_list:
                    yield alert
                if len(alert_list) < _PAGE_SIZE:
                    return
            elif response.status_code == 404:
                return
            else:
                response.raise_for_status()
            params['page'] += 1


    def iter_organization_alerts_stream(self, organization_id, latest_api_cursor=None, 
                                        latest_batch_date=None, persistence=False):
        """ Generator that allows iteration over an organization's alerts, with optional filters.
        :param organization_id: string with the UUID-style unique ID of the organization
        :param latest_api_cursor: string with API cursor representing the latest alert ID retrived
        :param latest_batch_date: string with YYYY-MM-DD format representing the latest alert batch date retrived
        :param persistence: boolean indicating if the alerts will be persisted. If so, the API cursor should be returned
        :return: an iterator over the decoded JSON objects that represent alerts.
        """
        region=None
        if not is_valid_uuid(organization_id):
            raise ValueError("organization id should be a string in UUID format")
        for org in self.iter_organizations():
            if str(organization_id) == org['id']:
                region = org['region']
    
        # loop over alert pages and yield them
        params = {}

        if latest_api_cursor:
            params['cursor'] = latest_api_cursor

        elif latest_batch_date and not latest_api_cursor:
            params['batchDate'] = parse_date(latest_batch_date)

        while True:
            
            response = self._request_retry("GET", 
                                        path='organizations/%s/alerts/stream' % organization_id,
                                        params=params,region=region)
            
            if response.status_code == 200:
                alert_response = response.json()

                if 'paging' not in alert_response:
                    return

                if 'cursor' not in alert_response['paging']:
                    return
                
                params['cursor'] = alert_response['paging']['cursor']

                if 'batchDate' in params:
                    del params['batchDate']

                for alert in alert_response['data']:
                    if persistence:
                        yield {'cursor': params['cursor'], 'alert':alert}
                    else:
                        yield alert
                if persistence:
                    return
            else:
                response.raise_for_status()


    def list_organization_alert_dates(self, organization_id, sortBy="logDate"):
        """ Lists all log or batch dates for which alerts exist on the organization.
        :param organization_id: string with the UUID-style unique ID of the organization
        :param sortBy: one of 'logDate' or 'batchDate', controls which date field to return
        :return: a set of ISO 8601 dates for which alerts exist
        """
        region=None
        if not is_valid_uuid(organization_id):
            raise ValueError("organization id should be a string in UUID format")
        for org in self.iter_organizations():
            if str(organization_id) == org['id']:
                region = org['region']
        if not is_valid_alert_sortBy(sortBy):
            raise ValueError("sortBy must be either 'logDate' or 'batchDate'")

        response = self._request_retry("GET",
                                       path='organizations/%s/alerts/dates' % organization_id,
                                       params={'sortBy': sortBy},region=region)
        if response.status_code == 200:
            return set(response.json())
        elif response.status_code == 404:
            return set()
        else:
            response.raise_for_status()

    def get_me(self):
        """Queries the API about the user that owns the API key in use.
        :return: a dict representing the user details
        """
        response = self._request_retry("GET", path="me", ok_status=(200,))
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def _list_organization_wblists(self, scope, organization_id):
        if not scope in ('white', 'black',):
            raise ValueError('scope should be either white or black')
        region=None
        if not is_valid_uuid(organization_id):
            raise ValueError("organization id should be a string in UUID format")
        for org in self.iter_organizations():
            if str(organization_id) == org['id']:
                region = org['region']

        path = 'organizations/%s/%slists' % (organization_id, scope)
        response = self._request_retry("GET", path=path,region=region)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            response.raise_for_status()

    def list_organization_whitelists(self, organization_id):
        """
        Lists the white list entries of an organization.
        :param organization_id: the organization ID
        :return: a list of dicts representing white list entries
        """
        return self._list_organization_wblists('white', organization_id)

    def list_organization_blacklists(self, organization_id):
        """
        Lists the black list entries of an organization.
        :param organization_id: the organization ID
        :return: a list of dicts representing black list entries
        """
        return self._list_organization_wblists('black', organization_id)

    def _get_organization_wblist_entry(self, scope, organization_id, id):
        if not scope in ('white', 'black',):
            raise ValueError('scope should be either white or black')
        region=None
        if not is_valid_uuid(organization_id):
            raise ValueError("organization id should be a string in UUID format")
        for org in self.iter_organizations():
            if str(organization_id) == org['id']:
                region = org['region']

        path = 'organizations/%s/%slists/%s' % (organization_id, scope, id)
        response = self._request_retry("GET", path=path,region=region)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_organization_whitelists(self, organization_id, id):
        """
        Retrieves the details of a the white list entry.
        :param organization_id: the organization ID
        :param id: the white list entry ID
        :return: a dict representing a white list entry
        """
        return self._get_organization_wblist_entry('white', organization_id, id)

    def get_organization_blacklists(self, organization_id, id):
        """
        Retrieves the details of a the black list entry.
        :param organization_id: the organization ID
        :param id: the black list entry ID
        :return: a dict representing a black list entry
        """
        return self._get_organization_wblist_entry('black', organization_id, id)
