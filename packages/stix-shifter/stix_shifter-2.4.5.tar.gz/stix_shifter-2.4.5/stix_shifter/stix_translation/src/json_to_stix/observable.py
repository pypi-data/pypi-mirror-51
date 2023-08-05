REGEX = {
    'date': '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(.\d+)?Z',
    'ipv4': ('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'),  # noqa: E501
    'ipv6': ('(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'),
    'mac': ('^(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})|([0-9a-fA-F]{3}[\.]){3}([0-9a-fA-F]{3}))$'),
    'ipv4_cidr': ('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/[0-2][0-5]?$'),  # noqa: E501
    'domain_name': ('^([a-z0-9]+(-[a-z0-9]+)*)*[\.a-z]*$')
}

properties = {
    'first_observed': {
        'valid_regex': REGEX['date']
    },
    'last_observed': {
        'valid_regex': REGEX['date']
    },
    'ipv4-addr.value': {
        'valid_regex': REGEX['ipv4']
    },
    'ipv6-addr.value': {
        'valid_regex': REGEX['ipv6']
    },
    'created': {
        'valid_regex': REGEX['date']
    },
    'modified': {
        'valid_regex': REGEX['date']
    },
    'domain-name.value': {
        'valid_regex': REGEX['domain_name']
    }
}
