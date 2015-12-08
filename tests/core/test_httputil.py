# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from opensearchsdk.core.httputil import HttpConnection

__author__ = 'barycenter'


class TestHttputil(unittest.TestCase):
    def setUp(self):
        self.conn = HttpConnection()
        self.http_url = ""

    def test_http_get_P1(self):
        self.conn.build_request("http://www.aliyun.com/")
        response = self.conn.execute_request()
        self.assertTrue(response.ok())
        self.assertIn("云服务器、云主机、云存储、开放存储、数据库、RDS", response.response_text())

    def test_http_post_P1(self):
        self.conn.build_request("http://www.aliyun.com/", method="POST")
        response = self.conn.execute_request()
        self.assertTrue(response.ok())
        self.assertIn("阿里云-打造数据第一平台", response.response_text())

    def test_http_get_proxy_P1(self):
        self.conn1 = HttpConnection(proxy_host="proxy.jsjngf.com", proxy_port="3128")
        self.conn1.build_request("http://www.aliyun.com/")
        response = self.conn1.execute_request()
        self.assertTrue(response.ok())
        self.assertIn("云服务器、云主机、云存储、开放存储、数据库、RDS", response.response_text())

    def test_http_post_proxy_P1(self):
        self.conn1 = HttpConnection(proxy_host="proxy.jsjngf.com", proxy_port="3128")
        self.conn1.build_request("http://www.aliyun.com/", method="POST")
        response = self.conn1.execute_request()
        self.assertTrue(response.ok())
        self.assertIn("阿里云-打造数据第一平台", response.response_text())

    def test_https_get_P1(self):
        self.conn.build_request("https://account.aliyun.com/login/login.htm")
        response = self.conn.execute_request()
        self.assertTrue(response.ok())
        self.assertIn("阿里云-帐号登录", response.response_text())

    def test_https_post_P1(self):
        self.conn.build_request("https://account.aliyun.com/login/login.htm", method="POST")
        response = self.conn.execute_request()
        self.assertTrue(response.ok())
        self.assertIn("阿里云-帐号登录", response.response_text())

