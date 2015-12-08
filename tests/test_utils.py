# -*- encoding: utf-8 -*-
import unittest
import string
import re

from opensearchsdk import utils

__author__ = 'barycenter'


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_random_str_P1(self):
        """
        test length
        :return:
        """
        a = utils.get_random_str()
        print a
        self.assertEqual(32, len(a))
        a = utils.get_random_str(128)
        self.assertEqual(128, len(a))

    def test_get_random_str_P2(self):
        """
        test collision
        random 10000 strings with len 32, no reduplication, so, the collision probability is very small!
        :return:
        """
        test_num = 10000

        number_set = set()

        for i in range(0, test_num):
            number_set.add(utils.get_random_str())

        self.assertEqual(test_num, len(number_set))

    def test_get_random_str_P3(self):
        """
        test sample characters
        :return:
        """
        a = utils.get_random_str(sample_characters=string.digits)
        self.assertTrue(re.match("^[0-9]{32}$", a))
