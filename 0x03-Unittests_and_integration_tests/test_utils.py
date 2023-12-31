#!/usr/bin/env python3
""" Parameterize a unit test """


from unittest import mock
from parameterized import parameterized, parameterized_class
import unittest
import utils
from utils import (
    access_nested_map,
    get_json,
    memoize
)
import requests
from unittest.mock import patch, Mock


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


class TestGetJson(unittest.TestCase):
    """ Class for testing get_json function
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @mock.patch('requests.get')
    def test_get_json(self, test_url, expected, mock_get):
        """ Test that utils.get_json returns the expected result
            for the mocked requests.get

        Args:
            test_url ([type]): [description]
            test_payload ([type]): [description]

        Returns:
            [type]: [description]
        """
        mock_response = mock.MagicMock()
        mock_response.json = lambda: expected
        with mock.patch("requests.get", create=True,
                        return_value=mock_response) as mock_get:
            self.assertEqual(get_json(test_url), expected)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """ Class for testing memoize decorator """

    def test_memoize(self) -> None:
        """ Test memoize decorator """
        class TestClass:
            """ TestClass that inherits from BaseClass """

            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                """ Returns memoized property """
                return self.a_method()

        with patch.object(
            TestClass,
            'a_method', return_value=lambda: 42,
        ) as whyte:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            whyte.assert_called_once()


if __name__ == '__main__':
    unittest.main()
