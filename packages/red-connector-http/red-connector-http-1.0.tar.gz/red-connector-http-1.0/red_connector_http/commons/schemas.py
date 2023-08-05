from copy import deepcopy


_HTTP_METHODS = ['Get', 'Put', 'Post']
_HTTP_METHODS_ENUMS = deepcopy(_HTTP_METHODS) + [m.lower() for m in _HTTP_METHODS] + [m.upper() for m in _HTTP_METHODS]

_AUTH_METHODS = ['Basic', 'Digest']
_AUTH_METHODS_ENUMS = deepcopy(_AUTH_METHODS) + [m.lower() for m in _AUTH_METHODS] + [m.upper() for m in _AUTH_METHODS]

SCHEMA = {
    'type': 'object',
    'properties': {
        'url': {'type': 'string'},
        'method': {'enum': _HTTP_METHODS_ENUMS},
        'auth': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'},
                'method': {'enum': _AUTH_METHODS_ENUMS}
            },
            'additionalProperties': False,
            'required': ['username', 'password']
        },
        'disableSSLVerification': {'type': 'boolean'}
    },
    'additionalProperties': False,
    'required': ['url']
}

MOUNT_DIR_SCHEMA = {
    'type': 'object',
    'properties': {
        'url': {'type': 'string'},
        'auth': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'},
            },
            'additionalProperties': False,
            'required': ['username', 'password']
        },
        'cache': {'type': 'boolean'}
    },
    'additionalProperties': False,
    'required': ['url']
}

ARCHIVE_SCHEMA = deepcopy(SCHEMA)
ARCHIVE_SCHEMA['properties']['archiveFormat'] = {'enum': ['zip', 'tar', 'gztar', 'bztar', 'xztar']}
ARCHIVE_SCHEMA['required'].append('archiveFormat')
