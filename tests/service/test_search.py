# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'barycenter'

import unittest
from opensearchsdk.core.client import OpensearchClientFactory
from opensearchsdk.service.search import Search, Q, FQ

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.client = OpensearchClientFactory.create_client("hangzhou", "external", "XVqTa2Rl5fGpml7c", "ZRXQN8Azm15Z7bWKgD0zVzS0OJR6A9")

    def test_search_P1(self):
        """
        plain query string, just title
        :return:
        """
        self.search = Search(self.client)
        self.search.query("title").index_name("F7xBML")
        results = self.search.results()
        self.assertTrue(results.success())
        self.assertEqual("query=default:'title'", self.search.query_string)

    def test_search_P2(self):
        """
        using Q to combine complex query condition
        and support rank
        :return:
        """
        self.search = Search(self.client)
        self.search.query(Q(default="title"), Q(default="中文")|Q(default="title3")).rank("校长").index_name("F7xBML")
        results = self.search.results()
        self.assertTrue(results.success())
        expected_query_string = "query=(default:'title' AND (default:'中文' OR default:'title3')) RANK default:'校长'"
        self.assertEqual(expected_query_string, self.search.query_string)

    def test_search_P3(self):
        """
        test query_raw string
        please notice query_raw must be last call
        :return:
        """
        self.search = Search(self.client)
        expected_query_string = "query=(default:'title' AND (default:'中文' OR default:'title3')) RANK default:'校长'"
        results = self.search.index_name("F7xBML").query_raw(expected_query_string)
        self.assertTrue(results.success())

    def test_search_P4(self):
        """
        using Q to combine complex query condition
        and support rank
        :return:
        """
        self.search = Search(self.client)
        self.search.query(Q(default="title"), ~Q(default="中文")).rank("校长").index_name("F7xBML")
        results = self.search.results()
        self.assertTrue(results.success())
        expected_query_string = "query=(default:'title' ANDNOT default:'中文') RANK default:'校长'"
        self.assertEqual(expected_query_string, self.search.query_string)

    def test_config_P1(self):
        """
        I don't know why I set result_format is xml, but it still return json
        :return:
        """
        self.search = Search(self.client)
        self.search.query("title").index_name("F7xBML").config(start=1, hit=5, result_format='xml', rerank_size=100)
        results = self.search.results()
        expected_query_string = "query=default:'title'&&config=start:1;hit:5;rerank_size:100;result_format:xml"
        self.assertTrue(results.success())
        self.assertEqual(expected_query_string, self.search.query_string)

    def test_filter_N1(self):
        """
        filter is a little like query, you could use FQ to combine complex filter
        of course, you could use plaintext
        :return:
        """
        self.search = Search(self.client)
        self.search.query("title").index_name("F7xBML").filter("a>1", FQ("a+b<2") & FQ("c+d>3"))
        results = self.search.results()
        expected_query_string = "query=default:'title'&&filter=a>1 AND ('a+b<2' AND 'c+d>3')"
        self.assertFalse(results.success())
        self.assertEqual(expected_query_string, self.search.query_string)
        self.assertEqual("6127/Attribute not exist.", results.msg)

    def test_sort_P1(self):
        """
        :return:
        """
        self.search = Search(self.client)
        self.search.query("title").index_name("F7xBML").sort("+RANK")
        results = self.search.results()
        expected_query_string = "query=default:'title'&&sort=+RANK"
        self.assertTrue(results.success())
        self.assertEqual(expected_query_string, self.search.query_string)

    def test_aggregate_N1(self):
        self.search = Search(self.client)
        self.search.query("title").index_name("F7xBML").aggregate(group_key="group_id", agg_fun="sum(price)#max(price)")
        self.search.aggregate(group_key="group_id2", agg_fun="sum(price)#max(price)")
        results = self.search.results()
        self.assertFalse(results.success())
        self.assertEqual("6127/Attribute not exist.", results.msg)

    def test_distinct_N1(self):
        self.search = Search(self.client)
        self.search.query("title").index_name("F7xBML")
        self.search.distinct(dist_key="title")
        results = self.search.results()
        self.assertFalse(results.success())
        self.assertEqual("6127/Attribute not exist.", results.msg)

    def test_kvpairs_P1(self):
        self.search = Search(self.client)
        self.search.query("title").index_name("F7xBML")
        self.search.kvpairs(a="b", c="d")
        results = self.search.results()
        self.assertTrue(results.success())
        expected_string = "query=default:'title'&&kvpairs=a:b,c:d"
        self.assertEqual(expected_string, self.search.query_string)



