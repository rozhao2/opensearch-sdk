# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import codecs

from opensearchsdk.core.client import OpensearchClientFactory
from opensearchsdk.service.data import DataMgr
from opensearchsdk import utils

__author__ = 'barycenter'

class TestData(unittest.TestCase):
    def setUp(self):
        client = OpensearchClientFactory.create_client("hangzhou", "external", "XVqTa2Rl5fGpml7c", "ZRXQN8Azm15Z7bWKgD0zVzS0OJR6A9")
        self.data_mgr = DataMgr(client)

    def test_upload_P1(self):
        with codecs.open("../files/test4_main.txt") as ifh:
            json_str = ifh.read()
        resp = self.data_mgr.upload("test5", "main", json_str)
        self.assertTrue(resp.success())

    def test_upload_P2(self):
        json_str = """
        [
            {
                "cmd": "add",
                "timestamp": 1401342874777,
                "fields": {
                    "id": "1",
                    "title": "This is the title",
                    "body": "This is the body"
                }
            },
            {
                "cmd": "update",
                "timestamp": 1401342874778,
                "fields": {
                    "id": "2",
                    "title": "This is the new title"
                }
            },
            {
                "cmd": "delete",
                "fields": {
                    "id": "3"
                }
            }
        ]
        """
        resp = self.data_mgr.upload("F7xBML", "main", json_str)
        self.assertTrue(resp.success())
