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
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'}),
    ])
    @patch('client.get_json')
    def test_org(self, test_org: str, resp: Dict,
                 mocked_whyte: MagicMock) -> None:
        """ Test GithubOrgClient.org method """
        mocked_whyte.return_value = MagicMock(return_value=resp)
        whyte_class = GithubOrgClient(test_org)
        self.assertEqual(whyte_class.org(), resp)
        mocked_whyte.assert_called_once_with(
            'https://api.github.com/orgs/{}'.format(test_org)
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
        result.assert_called_once_with()
        self.assertEqual(result, expected_url)

    @patch('client.get_json', return_value=[{'name': 'google'},
                                            {'name': 'abc'}])
    def test_public_repos(self, mock_get):
        """ Test GithubOrgClient.public_repos method """
        test_class = GithubOrgClient('test')
        self.assertEqual(
            test_class.public_repos(),
            ['google', 'abc']
        )
        mock_get.assert_called_once_with(
            'https://api.github.com/orgs/test/repos')

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False),
    ])
    @patch('client.get_json')
    def test_has_license(self, repo: Dict, license_key: str,
                         expected: bool, mock_get: MagicMock) -> None:
        """ Test GithubOrgClient.has_license method """
        mock_get.return_value = repo
        test_class = GithubOrgClient('test')
        self.assertEqual(
            test_class.has_license(repo, license_key), expected)
        mock_get.assert_called_once_with(
            'https://api.github.com/orgs/test/repos')


@parameterized_class([
    {'org_payload': {'repos_url': 'https://api.github.com/orgs/google/repos'},
     'repos_payload': [{'name': 'google'}],
     'expected_repos': ['google'],
     'apache2_repos': ['google']},
    {'org_payload': {'repos_url': 'https://api.github.com/orgs/google/repos'},
     'repos_payload': [{'name': 'abc'}],
     'expected_repos': ['abc'],
     'apache2_repos': ['abc']},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Class for testing GithubOrgClient """

    def setUpClass(self) -> None:
        """ Set up for testing """
        config = {
            'return_value.json.side_effect': [
                self.org_payload, self.repos_payload,
                self.org_payload, self.repos_payload
            ]
        }
        self.get_patcher = patch('requests.get', **config)
        self.mocked_get = self.get_patcher.start()

    def tearDownClass(self) -> None:
        """ Tear down for testing """
        self.get_patcher.stop()

    def test_public_repos(self) -> None:
        """ Test GithubOrgClient.public_repos method """
        whyte_class = GithubOrgClient('google')
        self.assertEqual(whyte_class.public_repos(), self.expected_repos)
        self.assertEqual(whyte_class.public_repos(
            'apache-2.0'), self.apache2_repos)
        self.mocked_get.assert_called()

    def test_public_repos_with_license(self) -> None:
        """ Test GithubOrgClient.public_repos method implement logic to
        test the public_repos method with the argument license="apache-2.0"
        """
        whyte_class = GithubOrgClient('google')
        self.assertEqual(whyte_class.public_repos(
            'apache-2.0'), self.apache2_repos)
        self.assertEqual(whyte_class.public_repos(
            'bsd'), [])
        self.mocked_get.assert_called()


if __name__ == '__main__':
    unittest.main()
