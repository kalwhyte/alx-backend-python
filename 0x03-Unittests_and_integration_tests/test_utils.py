#!/usr/bin/env python3
""" Parameterize a unit test """


from parameterized import parameterized, parameterized_class
import unittest
import utils


class TestAccessNestedMap(unittest.TestCase):
    """ Class for testing AccessNestedMap function """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test that the method returns what it is supposed to """
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """ Test that a KeyError is raised for the following inputs """
        with self.assertRaises(KeyError) as error:
            utils.access_nested_map(nested_map, path)
            self.assertEqual(error.exception, expected)
