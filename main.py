#!/usr/bin/python

"""
Main script for setting parameters and looping through batch of data.
"""

__author__ = "Sergio Galvez"
__version__ = "1.0"

import logging
import os
import json
import argparse

from github import GitHub
from config import SUPPORTED_RESOURCES

logging.basicConfig(level=logging.INFO)


def parse_command_line_args(argv):
    """ This function parses required arguments needed to run the program.
        :param argv: The command-line arguments for this call of this script.
        :returns args: dictionary of parsed know args.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--owner', dest='owner', required=True,
                        help='A string representing the Owner name.')
    parser.add_argument('--repositories', dest='repositories', required=True,
                        help='A list of strings representing repository names.')
    parser.add_argument('--resources', dest='resources', required=True,
                        help='A list of desired resource names. \n' 
                             'Here is a list of supported resources:  \n'
                             '{supported_resources}'.format(
                                supported_resources=SUPPORTED_RESOURCES
                             ))

    return parser.parse_known_args(argv)


def write_to_file(data):
    """ Write results to a file.
        :param data: (str) contains data to write on the file.
        :returns None
    """
    # file_format: resources/<datetime>/request_<page>.json
    filename = 'resources/{filename}.json'.format(
        filename=data['filename']
    )

    logging.info('Writing resource to %s ... ' % filename)

    if data is not None:

        # check if file/dir is existing, else create it automatically
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(file=filename, mode='a+') as result_file:
            json.dump(data['data'], result_file, sort_keys=True, indent=4)


def run(argv=None):
    """Main code body
        :returns None
    """

    known_args, extra = parse_command_line_args(argv)

    # set parameters for github object
    gh = GitHub(
        owner=known_args.owner,
        repositories=known_args.repositories.split(','),
        resources=known_args.resources.split(',')
    )

    # read until data is depleted
    data = gh.read()
    while data is not None:

        # do something with the data
        write_to_file(data=data)

        # read next batch of data
        data = gh.read()


if __name__ == '__main__':
    run()
