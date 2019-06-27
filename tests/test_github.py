import json
import logging
import unittest

from github import GitHub


class TestGitHub(unittest.TestCase):
    """The test cases are focused on the business logic.
    In this case, this is how we parse the data, transform the data
    and output to dictionary."""

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_data(self):
        """Test the api output of github.py"""

        with open('tests/actual_data.json', 'r') as json_file:
            expected_dict_output = json.load(json_file)

        gh = GitHub(
            owner='moby',
            repositories=['moby', 'toolkit', 'tool'],
            resources=['issues', 'commits', 'pull_requests']
        )
        actual_dict_outut = gh.read()

        # check if matched
        self.assertEqual(actual_dict_outut['data'], expected_dict_output)


if __name__ == '__main__':
    unittest.main()
