# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'barycenter'

import unittest
from opensearchsdk.core.client import OpensearchClientFactory
from opensearchsdk.service.error_log import ErrorLog

class TestErrorLog(unittest.TestCase):
    def setUp(self):
        client = OpensearchClientFactory.create_client("hangzhou", "external", "XVqTa2Rl5fGpml7c", "ZRXQN8Azm15Z7bWKgD0zVzS0OJR6A9")
        self.app = ErrorLog(client)

    def test_log_P1(self):
        resp = self.app.get_log("F7xBML", 1, 10)
        self.assertTrue(resp.success())
        self.assertEqual(0, len(resp.logs))
        self.assertEqual(list, type(resp.logs))

    def test_log_N1(self):
        try:
            self.app.get_log("F7xBML", 0, -1)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_log_N2(self):
        resp = self.app.get_log("noexist", 1, 100)

        self.assertFalse(resp.success())
