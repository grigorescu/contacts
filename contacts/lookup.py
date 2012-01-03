
__author__ = 'vladg'

import getpass
import requests
import json
from contacts import config

class Query:

    CDB_PROD = config.prod
    CDB_DEV = config.dev
    CDB_TEST = config.test
    PATH = config.path

    def __init__(self, username=None, password=None, environment="Prod",
                 ssl_verify=True):
        """Makes sure the parameters are valid, and sets up the Query."""

        if not username: username = getpass.getuser()
        if not password: password = getpass.getpass()

        if environment.lower() == "prod": self.url = self.CDB_PROD + self.PATH
        elif environment.lower() == "dev": self.url = self.CDB_DEV + self.PATH
        elif environment.lower() == "test": self.url = self.CDB_TEST + self.PATH
        else: raise ValueError("Unknown CDB environment. Options are prod, "
                               "dev, or test.")

        self.request = requests.session(auth=(username, password),
                                        verify=ssl_verify)
        response = self.request.get(self.url)
        if response.status_code != 200:
            raise IOError("Error logging in to Contacts Database.")

    def _query(self, data):
        return self.request.post(url=self.url, data=json.dumps([data]))

    def _build_param_list(self, search_value, search_field,
                          search_operation, include_data=None):
        """Builds a CDB-compatible list of parameters, given a value,
        a field, and an optional operation."""

        if not isinstance(search_value, list):
            search_value = [search_value]
        if not isinstance(search_field, list):
            search_field = [search_field]

        include_types = {"contacts": "contact_info",
                         "dependencies": "model_dependencies",
                         "permissions": "model_permissions",
                         "models": "contact_models"}
        include_fields = []
        if include_data is None:
            include_data = include_types["contacts"]
        if not isinstance(include_data, list):
            include_data = [include_data]
        include_data = [d.lower() for d in include_data]
        for d in include_data:
            try:
                include_fields += [include_types[d]]
            except KeyError:
                raise ValueError("Unknown include request: '%s'. Allowed "
                                 "includes are: '%s'." %
                                 (d, include_types.keys()))

        if not isinstance(search_operation, list):
            search_operation = [search_operation.lower()]
        else:
            search_operation = [op.lower() for op in search_operation]
        valid_operations = ("=", "like", "begins with", "ends with")
        for op in search_operation:
            if op not in valid_operations:
                raise ValueError("Unknown operation: '%s'. Allowed "
                                 "operations are: '%s'." %
                                 (op, valid_operations))

        parameters = {"search_value": search_value,
                      "search_field": search_field,
                      "search_operation": search_operation,
                      "include": include_fields}

        return parameters

    def _build_query(self, function, param_list):
        valid_functions = ("find", "search", "update", "create",
                           "manage_contacts", "manage_permissions",
                           "manage_dependencies")
        function = function.lower()
        if function not in valid_functions:
            raise ValueError("Unknown function: '%s'. Allowed functions are:"
                             " '%s'." % (function, valid_functions))

        query = {"function": function,
                 "params": param_list}

        return query

    def call(self, search_value, search_field, search_operation="=",
             search_function="find"):
        param_list = self._build_param_list(search_value, search_field,
                                            search_operation)
        data = self._build_query(search_function, param_list)
        return json.loads(self._query(data).content)

    query_ip = lambda self, ip: self.call(ip, "ip_address")
    # TODO: merge query_ipv6 with query_ip
    query_ipv6 = lambda self, ip: self.call(ip, "ip6_address")
    query_fqdn = lambda self, fqdn: self.call(fqdn, "host_name")
    query_net_name = lambda self, name: self.call(name, "network_name")
    query_netid = lambda self, netid: self.call(netid, "netid")


