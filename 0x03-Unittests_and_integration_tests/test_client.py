#!/usr/bin/env python3
""" Parameterize and patch as decorators """


from parameterized import parameterized
from unittest.mock import patch
import unittest
from client import GithubOrgClient
from utils import get_json, access_nested_map, memoize


""" In a new test_client.py file, declare the TestGithubOrgClient(unittest.TestCase) class and implement the test_org method.

This method should test that GithubOrgClient.org returns the correct value.

Use @patch as a decorator to make sure get_json is called once with the expected argument but make sure it is not executed.

Use @parameterized.expand as a decorator to parametrize the test with a couple of org examples to pass to GithubOrgClient, in this order:

google
abc
Of course, no external HTTP calls should be made.
"""


class TestGithubOrgClient(unittest.TestCase):
    """ Class for testing GithubOrgClient
    """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, test_org, mock_get_json):
        """ Test that GithubOrgClient.org returns the correct value
        """
        test_class = GithubOrgClient(test_org)
        test_class.org()
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{test_org}'
        )

    # @patch('client.GithubOrgClient.org')
    # def test_public_repos_url(self, mock_org):
        """ Test that the result of _public_repos_url is the expected one
            based on the mocked payload
        """
        ''' org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_org.return_value = org_payload

        client = GithubOrgClient("google")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """ Test that the list of repos is what you expect from the chosen
        payload
        """
        mock_get_json.return_value = [
            {'name': 'google'},
            {'name': 'abc'},
        ]
        test_class = GithubOrgClient("test")
        self.assertEqual(
            test_class.public_repos(),
            ['google', 'abc']
        )
        mock_get_json.assert_called_once_with(
            'https://api.github.com/orgs/test/repos'
        )

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """ Test that the list of repos is what you expect from the chosen
        payload
        """
        mock_get_json.return_value = [
            {'name': 'google', 'license': {'key': 'a'}},
            {'name': 'abc', 'license': {'key': 'b'}},
            {'name': 'abc', 'license': {'key': 'c'}},
        ]
        test_class = GithubOrgClient("test")
        self.assertEqual(
            test_class.public_repos('a'),
            ['google']
        )
        self.assertEqual(
            test_class.public_repos('c'),
            ['abc', 'abc']
        )
        mock_get_json.assert_called_once_with(
            'https://api.github.com/orgs/test/repos'
        )

    @patch('client.get_json')
    def test_public_repos_url(self, mock_get_json):
        """ Test that the result of _public_repos_url is the expected one
            based on the mocked payload
        """
        org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_get_json.return_value = org_payload
        """
'''


if __name__ == '__main__':
    unittest.main()
