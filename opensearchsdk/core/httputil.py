# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from requests import Request, Session
from requests.adapters import HTTPAdapter

from opensearchsdk import UserAgent
from opensearchsdk import log
from opensearchsdk import utils
from opensearchsdk import set_stream_logger
from opensearchsdk.base import Base
from opensearchsdk.config import Config

__author__ = 'barycenter'


class HttpConnection(Base):
    """Base HTTP connection"""

    def __init__(self, method="GET", proxy_host=None, proxy_port=80, timeout=Config.DEFAULT_HTTP_TIMEOUT, async=False, **kwargs):
        if Config.DEBUG:
            set_stream_logger()
            pass

        self.response = None
        self.request = None
        self.method = method
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.timeout = timeout
        self.async = async

        self.proxies = dict()

        if self.proxy_host:
            proxy = "http://%s:%s" % (proxy_host, proxy_port)
            self.proxies['http'] = proxy
            self.proxies['https'] = proxy

        self.session = Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))

        self._reset()

    def build_request(self, url, params=dict(), headers=dict(), files=dict(), method='GET'):
        self._reset();
        self.method = method
        self.url = self._build_url(url)
        self.headers = self._build_header(headers,  files, method)
        self.request_data = self._build_data(params, method)

        if method == "GET":
            self.request = Request(self.method,
                                   self.url,
                                   params=self.request_data,
                                   headers=self.headers,
                                   )
        else:
            self.request = Request(self.method,
                                   self.url,
                                   data=self.request_data,
                                   headers=self.headers,
                                   files=files,
                                   )

        self.request = self.request.prepare()
        self._request_id = utils.get_uuid()

    def _build_url(self, url):
        return url

    def _build_header(self, headers=dict(), files=dict(), method='GET'):
        headers.update({
            "User-Agent": UserAgent
        })

        if method.upper() == 'POST':
            if not files:
                headers.update({
                    "Content-Type": "application/x-www-form-urlencoded"
                })
            else:
                headers.update({
                    "Content-Type": "multipart/form-data"
                })
        return headers

    def _build_data(self, params=dict(), method='GET'):
        """
        do nothing...
        :param params:
        :param method:
        :return:
        """
        return params

    def execute_request(self):

        log.debug("Request %s url=%s; method=%s" % (self._request_id, self.url, self.method))
        log.debug("Request %s headers=%s" % (self._request_id, self.request.headers))
        log.debug("Request %s param=%s" % (self._request_id, self.request_data))

        if self.async:
            # async http request stay blank
            raise Exception("async http request not support yet")
            return None
        else:
            self.response = self.session.send(self.request,
                                              verify=True,
                                              proxies=self.proxies,
                                              timeout=self.timeout,
                                              allow_redirects=True)
            log.debug("Response %s status_code=%s" % (self._request_id, self.response.status_code))
            log.debug("Response %s headers=%s" % (self._request_id, self.response.headers))
            log.debug("Response %s content=%s" % (self._request_id, self.response.text))

        return ResponseInfo(self.response)

    def _reset(self):
        # request_id for async requests
        self._request_id = None

        # request related
        self.url = None
        self.headers = None
        self.request_data = None
        self.method='GET'
        pass


class ResponseInfo(Base):

    def __init__(self, response, exception=None):

        if Config.DEBUG:
            set_stream_logger()
            pass

        self.__response = response
        self.__exception = exception

        if not self.__response:
            self.status_code = -1
            self.response_content = None
            self.error_msg = str(self.__exception)
            log.debug("Response exception: %s " % self.error_msg)
        else:
            self.status_code = response.status_code
            self.response_content = response.text

            if self.status_code >= 400:
                # error...
                self.response_content = "invalid response"
                self.__exception = Exception("invalid response %s" % self.status_code)
                pass

    def ok(self):
        return self.status_code == 200

    def response_code(self):
        return self.status_code

    def response_json(self):
        return self.__response.json()

    def response_text(self):
        return self.response_content


class HttpConnectionPool(Base):
    """
    HttpConnectionPool for async http request
    """
    def __init__(self):
        pass
