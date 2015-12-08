# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import copy

from opensearchsdk.base import Base
from opensearchsdk.core.httputil import HttpConnection
from opensearchsdk import log
from opensearchsdk.config import Config
from opensearchsdk.authentication import SignatureBuilder


__author__ = 'barycenter'

def singleton(cls, *args, **kw):
    """
    singleton mode to create client
    :param cls:
    :param args:
    :param kw:
    :return:
    """
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class OpenSearchClient(Base):

    def __init__(self, zone, url_type, access_id, access_key, proxy_host=None, proxy_port='80'):
        self.__zone = zone
        self.__zone_url = Config.get_zone_url(zone, url_type)
        self.__access_id = access_id
        self.__access_key = access_key
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port

    def build_signature(self, params, method='GET'):

        params_send = copy.deepcopy(params)
        builder = SignatureBuilder(params_send)
        params_send = builder.build_signature(access_key_id=self.__access_id,
                                              secret_key=self.__access_key,
                                              request_method=method)
        return params_send

    def get_connection(self):
        """
        create a http connection
        :return:
        """
        return HttpConnection(proxy_host=self.__proxy_host, proxy_port=self.__proxy_port)

    def send_message(self, url, method='GET', params=dict(), files=dict()):
        conn = self.get_connection()
        params_send = self.build_signature(params, method)
        url = self.__zone_url + url
        conn.build_request(url, params=params_send, files=files, method=method)
        resp = conn.execute_request()
        return resp


class OpensearchClientFactory(Base):
    @classmethod
    def create_client(cls, zone, url_type, access_id, access_key, proxy_host=None, proxy_port='80'):
        return OpenSearchClient(zone, url_type, access_id, access_key, proxy_host, proxy_port)


