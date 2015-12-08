# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import unittest
from opensearchsdk.authentication import Signature

__author__ = 'barycenter'


class TestAuthentication(unittest.TestCase):
    def setUp(self):

        pass

    def test_signature(self):
        params = dict()
        params['Version'] = 'v2'
        params['AccessKeyId'] = 'testid'
        params['SignatureMethod'] = 'HMAC-SHA1'
        params['SignatureVersion'] = '1.0'
        params['SignatureNonce'] = '14053016951271226'
        params['Timestamp'] = '2014-07-14T01:34:55Z'
        params['query'] = "config=format:json,start:0,hit:20&&query:'的'"
        params['index_name'] = 'ut_3885312'
        params['format'] = 'json'
        params['fetch_fields'] = "title;gmt_modified"

        sig = Signature(params)

        signature = sig.get_signature("testsecret")

        self.assertEqual("fxGidmIYSsx2AMa8onxuavOijuE=", signature)
