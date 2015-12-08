# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'barycenter'

import unittest
from opensearchsdk.core.client import OpensearchClientFactory
from opensearchsdk.service.reference import ReferenceMgr


class TestReference(unittest.TestCase):
    """
    please ensure there is a application with name "F7xBML" and have table named main
    and make this rule valid
    """

    def setUp(self):
        client = OpensearchClientFactory.create_client("hangzhou", "external", "XVqTa2Rl5fGpml7c", "ZRXQN8Azm15Z7bWKgD0zVzS0OJR6A9")
        self.app = ReferenceMgr(client)

    def test_create_task_P1(self):
        resp = self.app.create_task("F7xBML")
        self.assertTrue(resp.success())

    def test_create_task_P2(self):
        resp = self.app.create_task("F7xBML", True, ["main"])
        self.assertTrue(resp.success())
