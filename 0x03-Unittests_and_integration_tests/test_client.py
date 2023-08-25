#!/usr/bin/env python3
""" Parameterize and patch as decorators """
from parameterized import parameterized
from unittest.mock import patch
import unittest
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ Class for testing GithubOrgClient """

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, test_org, mock_get_json):
        """ Test that GithubOrgClient.org returns the correct value """
        test_class = GithubOrgClient(test_org)
        test_class.org()
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{test_org}'
        )

    def test_public_repos_url(self):
        """ Test that the result of _public_repos_url is the expected one
        based on the mocked payload
        """
        test_class = GithubOrgClient("test")
        test_class.org = TEST_PAYLOAD
        self.assertEqual(
            test_class._public_repos_url,
            TEST_PAYLOAD['repos_url']
        )

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
