#!/usr/bin/python

"""
Library for processing Github's API.
"""

__author__ = "Sergio Galvez"
__version__ = "1.0"

import requests

from config import GITHUB_TOKEN, SUPPORTED_RESOURCES, API_URL

HEADER = {'Accept': 'application/vnd.github.v3+json'}

# use github token, if existing
if GITHUB_TOKEN:
    HEADER['Authorization'] = \
        'token {}'.format(GITHUB_TOKEN)


class GitHub(object):
    """A helper class which contains the logic for calling Github v3 API."""

    def __init__(self, owner, repositories, resources):
        """Instantiate Github class
            :param owner: string representing the owner's name.
            :param repositories: list of repository names.
            :param resources: list desired resource names
            :returns: data (dict) processed by api or None
        """
        self._owner = owner
        self._repositories = repositories
        self._resources = resources
        self.counter = 1

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        if not owner:
            raise Exception("Owner cannot be empty.")
        if not self.is_owner_valid(owner):
            raise Exception("Owner is not existing/valid.")
        self._owner = owner

    @property
    def repositories(self):
        return self._repositories

    @repositories.setter
    def repositories(self, repositories):
        if not repositories:
            raise Exception("Repositories cannot be empty.")
        self._repositories = repositories

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, resources):
        if not resources:
            raise Exception("Resources cannot be empty.")
        if not isinstance(resources, list):
            raise Exception("Resources should be a list.")
        if not all(elem in resources for elem in SUPPORTED_RESOURCES):
            raise Exception("Some resources listed are not supported.")

        self._resources = resources

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
                url = '{repository_url}/{combination}?page={page}'.format(
                        repository_url=API_URL['repositories'],
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

    @staticmethod
    def is_owner_valid(owner):
        """Validate owner name
            :param owner: github's owner name
            :returns: boolean: true if valid, else False
        """
        url = '{users_url}/{owner}'.format(
            users_url=API_URL['users'],
            owner=owner
        )
        response = requests.get(url, headers=HEADER)
        if response.status_code == 200:  # check status if ok
            return True

        return False
