# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


import urllib
import hmac
import hashlib
import copy

from opensearchsdk.utils import Constants
from opensearchsdk.base import Base
from opensearchsdk import utils

__author__ = 'barycenter'


class Signature(Base):
    """
    Signature class
    """
    def __init__(self, params):
        self.params = params

    def get_signature(self, secret_key, request_method="GET"):
        params = self.params
        sorted_params = sorted(params.items(), key=lambda params : params[0])

        #canonicalized_query_string = "&".join(
        #    map(lambda (k, v): "%s=%s" % (self.encode_str(k), self.encode_str(v)), sorted_params))
        canonicalized_query_string = "&".join(
            ["%s=%s" % (self.encode_str(item[0]), self.encode_str(item[1])) for item in sorted_params])

        canonicalized_query_string = self.encode_str(canonicalized_query_string)

        string_to_sign = request_method + "&%2F&" + canonicalized_query_string

        return self.cal_signature(string_to_sign, secret_key)

    @staticmethod
    def encode_str(param):
        result = urllib.quote_plus(param.encode(Constants.DEFAULT_ENCODE)).replace("%7E", '~') \
            .replace("/", "%2F") \
            .replace('+', '%20') \
            .replace('*', '%2A')
        return result

    @staticmethod
    def cal_signature(string_to_sign, secret_key):
        secret_key += "&"
        secret_key = secret_key.encode(Constants.DEFAULT_ENCODE)
        string_to_sign = string_to_sign.encode(Constants.DEFAULT_ENCODE)
        return hmac.new(secret_key, string_to_sign, hashlib.sha1).digest().encode('base64').strip()


'''
SignatureBuilder class
'''
class SignatureBuilder(Base):
    def __init__(self, params):
        # shallow copy, cannot change to deep copy
        self.params = copy.copy(params)
        pass

    def add_param(self, key, value):
        self.params[str(key)] = str(value)

    def __add_common_params(self):
        """
        common params: Version, SignatureVersion, SignatureMethod, SignatureNonce, Timestamp

              Timestamp: UTC format：%Y-%m-%dT%H:%M:%SZ

        About common parameters, please refer to
        https://docs.aliyun.com/?spm=5176.1980653.30105.11.KzfKTo#/pub/opensearch/api-reference/call-method&common-params
        """
        self.add_param("Version", "v2")
        self.add_param("SignatureVersion", "1.0")
        self.add_param("SignatureMethod", "HMAC-SHA1")
        self.add_param("SignatureNonce", utils.get_random_timestamp())
        self.add_param("Timestamp", utils.get_datetime_str(utils.Constants.TIME_FORMAT_UTC))

    def build_signature(self, access_key_id, secret_key, request_method="GET"):
        """
        add signature and common params
        :param access_key_id:
        :param secret_key:
        :param request_method:
        :return:
        """

        self.__add_common_params()
        self.add_param("AccessKeyId", access_key_id)

        sig = Signature(self.params)
        signature = sig.get_signature(secret_key, request_method)
        self.add_param("Signature", signature)
        return self.params
