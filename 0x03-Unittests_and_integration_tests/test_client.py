#!/usr/bin/env python3
""" Parameterize and patch as decorators """


import unittest
from fixtures import TEST_PAYLOAD
from typing import Dict
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from client import GithubOrgClient
from unittest.mock import (
    patch,
    Mock,
    PropertyMock,
    MagicMock
)
from utils import get_json, access_nested_map, memoize


class TestGithubOrgClient(unittest.TestCase):
    """ Class for testing GithubOrgClient """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, test_org: str, resp: Dict, mocked_whyte: MagicMock) -> None:
        """ Test GithubOrgClient.org method 

        Args:
            mocked_whyte (MagicMock): [description]
        """
        mocked_whyte.return_value = MagicMock(return_value=resp)
        test_class = GithubOrgClient(test_org)
        self.assertEqual(test_class.org(), resp)
        mocked_whyte.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(test_org)
        )

    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org: MagicMock) -> None:
        """ Test GithubOrgClient._public_repos_url

        Args:
            mock_public_repos_url (MagicMock): [description]
        """
        mock_payload = {
            "repos_url": 'http://api.github.com/orgs/testorg/repos'}
        mock_org.return_value = mock_payload

        test_class = GithubOrgClient("testorg")
        result = test_class._public_repos_url()

        expected_url = 'https://api.github.com/orgs/testorg/repos'
        self.assertEqual(result, expected_url)

    @patch('client.GithubOrgClient.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos(self, mock_org: MagicMock, mock_get: MagicMock) -> None:
        """ Test GithubOrgClient.public_repos method 

        Args:
            mock_org (MagicMock): [description]
            mock_get (MagicMock): [description]
        """
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get.return_value = mock_payload

        test_class = GithubOrgClient('testorg')
        result = test_class.public_repos()

        expected = ["repo1", "repo2", "repo3"]
        self.assertEqual(result, mock_payload)
        mock_org.assert_called_once_with()
        mock_get.assert_called_once_with(mock_org.return_value)


if __name__ == '__main__':
    unittest.main()
