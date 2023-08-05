import json
from argparse import ArgumentParser

import jsonschema

from red_connector_http.commons.schemas import SCHEMA
from red_connector_http.commons.helpers import http_method_func, auth_method_obj, fetch_file, graceful_error,\
    DEFAULT_TIMEOUT

RECEIVE_FILE_DESCRIPTION = 'Receive input file from HTTP(S) server.'
RECEIVE_FILE_VALIDATE_DESCRIPTION = 'Validate access data for receive-file.'

SEND_FILE_DESCRIPTION = 'Send output file to HTTP(S) server.'
SEND_FILE_VALIDATE_DESCRIPTION = 'Validate access data for send-file.'


def _receive_file(access, local_file_path):
    with open(access) as f:
        access = json.load(f)

    http_method = http_method_func(access, 'GET')
    auth_method = auth_method_obj(access)

    verify = True
    if access.get('disableSSLVerification'):
        verify = False

    fetch_file(local_file_path, access['url'], http_method, auth_method, verify)


def _receive_file_validate(access):
    with open(access) as f:
        access = json.load(f)

    jsonschema.validate(access, SCHEMA)


def _send_file(access, local_file_path):
    with open(access) as f:
        access = json.load(f)

    http_method = http_method_func(access, 'POST')
    auth_method = auth_method_obj(access)

    verify = True
    if access.get('disableSSLVerification'):
        verify = False

    with open(local_file_path, 'rb') as f:
        r = http_method(
            access['url'],
            data=f,
            auth=auth_method,
            verify=verify,
            timeout=DEFAULT_TIMEOUT
        )
        r.raise_for_status()


def _send_file_validate(access):
    with open(access) as f:
        access = json.load(f)
    
    jsonschema.validate(access, SCHEMA)


@graceful_error
def receive_file():
    parser = ArgumentParser(description=RECEIVE_FILE_DESCRIPTION)
    parser.add_argument(
        'access', action='store', type=str, metavar='ACCESSFILE',
        help='Local path to ACCESSFILE in JSON format.'
    )
    parser.add_argument(
        'local_file_path', action='store', type=str, metavar='LOCALFILE',
        help='Local input file path.'
    )
    args = parser.parse_args()
    _receive_file(**args.__dict__)


@graceful_error
def receive_file_validate():
    parser = ArgumentParser(description=RECEIVE_FILE_VALIDATE_DESCRIPTION)
    parser.add_argument(
        'access', action='store', type=str, metavar='ACCESSFILE',
        help='Local path to ACCESSFILE in JSON format.'
    )
    args = parser.parse_args()
    _receive_file_validate(**args.__dict__)


@graceful_error
def send_file():
    parser = ArgumentParser(description=SEND_FILE_DESCRIPTION)
    parser.add_argument(
        'access', action='store', type=str, metavar='ACCESSFILE',
        help='Local path to ACCESSFILE in JSON format.'
    )
    parser.add_argument(
        'local_file_path', action='store', type=str, metavar='LOCALFILE',
        help='Local output file path.'
    )
    args = parser.parse_args()
    _send_file(**args.__dict__)


@graceful_error
def send_file_validate():
    parser = ArgumentParser(description=SEND_FILE_VALIDATE_DESCRIPTION)
    parser.add_argument(
        'access', action='store', type=str, metavar='ACCESSFILE',
        help='Local path to ACCESSFILE in JSON format.'
    )
    args = parser.parse_args()
    _send_file_validate(**args.__dict__)
