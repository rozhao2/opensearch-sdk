# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'barycenter'

import unittest
from opensearchsdk.core.client import OpensearchClientFactory
from opensearchsdk.service.suggest import SuggestMgr

class TestSuggest(unittest.TestCase):
    """
    please ensure there is a application with name "F7xBML" and this applicaiton has a suggest rule: "suggest_rule1"
    and make this rule valid
    """

    def setUp(self):
        client = OpensearchClientFactory.create_client("hangzhou", "external", "XVqTa2Rl5fGpml7c", "ZRXQN8Azm15Z7bWKgD0zVzS0OJR6A9")
        self.suggest = SuggestMgr(client)

    def test_suggest_P1(self):
        resp = self.suggest.suggest("title", "F7xBML", "suggest_rule1")
        self.assertTrue(resp.success())
        self.assertTrue(len(resp.suggests) > 0)
        self.assertIn("this is the new title", resp.suggests)