# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import unittest
from opensearchsdk.core.client import OpensearchClientFactory
from opensearchsdk.service.application import ApplicationMgr
from opensearchsdk import utils

__author__ = 'barycenter'

class TestApplication(unittest.TestCase):
    """
    You need create template manually, create templates with name default and default2
    """

    def setUp(self):
        client = OpensearchClientFactory.create_client("hangzhou", "external", "XVqTa2Rl5fGpml7c", "ZRXQN8Azm15Z7bWKgD0zVzS0OJR6A9")
        self.app = ApplicationMgr(client)

    def test_create_duplicate_N1(self):

        app_name = utils.get_random_str(6)
        result = self.app.create(app_name, "default2")
        self.assertEqual("OK", result.status)

        result = self.app.create(app_name, "default2")
        self.assertEqual("FAIL", result.status)

    def test_delete_P1(self):
        app_name = utils.get_random_str(6)
        result = self.app.create(app_name, "default")
        self.assertEqual("OK", result.status)

        result = self.app.delete(app_name)
        self.assertEqual("OK", result.status)

    def test_delete_noexists_P1(self):
        result = self.app.delete("not_exists")
        self.assertEqual("FAIL", result.status)

    def test_multiple_thread(self):
        pass

    def test_view(self):
        result = self.app.view("test1")
        self.assertEqual("OK", result.status)

