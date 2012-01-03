__author__ = 'vladg'

import unittest
import contacts.lookup
import contacts.config

class TestLookupFunctions(unittest.TestCase):
    def setUp(self):
        self.query = contacts.lookup.Query(
                        username=contacts.config.username,
                        password=contacts.config.password,
                        environment=contacts.config.environment,
                        ssl_verify=contacts.config.ssl_verify)

    def test_init(self):
        self.assertTrue(self.query.request)

    def test_query_ipv4(self):
        result = self.query.query_ip(contacts.config.ipv4_test)
        print result
        self.assertEqual(result["Status"], "Success")

    def test_query_ipv6(self):
        result = self.query.query_ipv6(contacts.config.ipv6_test)
        print result
        self.assertEqual(result["Status"], "Success")

    def test_query_fqdn(self):
        result = self.query.query_fqdn(contacts.config.fqdn_test)
        print result
        self.assertEqual(result["Status"], "Success")

    def test_query_netid(self):
        result = self.query.query_netid(contacts.config.netid_test)
        print result
        self.assertEqual(result["Status"], "Success")

    def test_query_net_name(self):
        result = self.query.query_net_name(contacts.config.net_name_test)
        print result
        self.assertEqual(result["Status"], "Success")

if __name__ == '__main__':
    unittest.main()