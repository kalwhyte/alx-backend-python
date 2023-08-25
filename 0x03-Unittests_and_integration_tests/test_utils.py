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


class TestGetJson(unittest.TestCase):
    """ Class for testing get_json function """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @unittest.mock.patch('requests.get')
    def test_get_json(self, test_url, test_payload):
        """ Test that utils.get_json returns the expected result """
        mock_response = unittest.mock_get.return_value
        mock_response.json.return_value = test_payload

        result = utils.get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_response.get.assert_called_once_with()


class TestMemoize(unittest.TestCase):
    """ Class for testing memoize decorator """

    def test_memoize(self):
        """ Test that when calling a_property twice, the correct result is
        returned but a_method is only called once using assert_called_once
        """
        class TestClass:
            """ TestClass that inherits from BaseClass """

            def a_method(self):
                """ Returns the attribute 'a' """
                return 42

            @utils.memoize
            def a_property(self):
                """ Returns memoized property """
                return self.a_method()

        with unittest.mock.patch.object(TestClass, 'a_method') as mock:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
