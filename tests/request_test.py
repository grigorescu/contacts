__author__ = 'vladg'

import unittest
import contacts.lookup
import secret_data # I'd rather not share the details on GitHub...

class TestLookupFunctions(unittest.TestCase):
    def setUp(self):
        self.query = contacts.lookup.Query(username=secret_data.username,
                                           password=secret_data.password,
                                           environment=secret_data.environment,
                                           ssl_verify=secret_data.ssl_verify)

    def test_init(self):
        self.assertTrue(self.query.request)

    def test_query_ipv4(self):
        result = self.query.query_ip(secret_data.ipv4_test)
        print result
        self.assertEqual(result["Status"], "Success")

    def test_query_ipv6(self):
        result = self.query.query_ipv6(secret_data.ipv6_test)
        print result
        self.assertEqual(result["Status"], "Success")

    def test_query_fqdn(self):
        result = self.query.query_fqdn(secret_data.fqdn_test)
        print result
        self.assertEqual(result["Status"], "Success")

    def test_query_netid(self):
        result = self.query.query_netid(secret_data.netid_test)
        print result
        self.assertEqual(result["Status"], "Success")

    def test_query_net_name(self):
        result = self.query.query_net_name(secret_data.net_name_test)
        print result
        self.assertEqual(result["Status"], "Success")

if __name__ == '__main__':
    unittest.main()