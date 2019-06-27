#!/usr/bin/python

"""
Library for processing Github's API.
"""

__author__ = "Sergio Galvez"
__version__ = "1.0"

import requests

from config import GITHUB_TOKEN

HEADER = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'token {}'.format(GITHUB_TOKEN)
}


class GitHub:
    """A helper class which contains the logic for calling Github v3 API."""

    def __init__(self, owner, repositories, resources):
        """Instantiate Github class
            :param owner: string representing the owner's name.
            :param repositories: list of repository names.
            :param resources: list desired resource names
            :returns: data (dict) processed by api or None
        """
        self.owner = owner
        self.repositories = repositories
        self.resources = resources
        self.counter = 1

    def read(self):
        """Read Github's API data
            :param self: instantiated class
            :returns: data (dict) processed by api or None
        """

        repository_dict = dict()

        for repository in self.repositories:

            resources_dict = dict()
            for resource in self.resources:

                combination = '{user}/{repo}/{resource}'.format(
                    user=self.owner,
                    repo=repository,
                    resource=resource,
                )
                url = 'https://api.github.com/repos/{combination}' \
                    '?page={page}'.format(
                        combination=combination,
                        page=self.counter
                    )

                response = requests.get(url, headers=HEADER)
                if response.status_code == 200:  # check status if ok

                    if response.json():
                        resources_dict[resource] = {
                            'url': url,
                            'data': response.json()
                        }

            # if data available for resource, enclose it to another dict
            if resources_dict:
                repository_dict[repository] = resources_dict

        # format filename
        filename = '{owner}/{repositories}/response_{counter}'.format(
            owner=self.owner,
            repositories='_'.join(self.repositories),
            counter=str(self.counter)
        )

        # increment page for iteration
        self.counter += 1

        if repository_dict:
            return {
                'filename': filename,
                'data': repository_dict
            }

        else:
            return None
