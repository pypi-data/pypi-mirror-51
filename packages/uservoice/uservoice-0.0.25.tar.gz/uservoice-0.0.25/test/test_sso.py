from __future__ import print_function
import yaml
import unittest
import uservoice

class TestSso(unittest.TestCase):
    def setUp(self):
        super(TestSso, self).setUp()
        with open('test/config.yml') as f:
            self.config = yaml.load(f)

    def test_generating_with_validity(self):
        sso_token = uservoice.generate_sso_token(self.config['subdomain_name'], self.config['sso_key'], {
            'email': 'myemail@example.com',
            'guid': 'code-myemail@example.com-1'
        }, 10)
        print("{protocol}://{subdomain}.{domain}?sso={sso}".format(protocol=self.config.get('protocol', 'https'),domain=self.config.get('uservoice_domain', 'uservoice.com'),subdomain=self.config['subdomain_name'],sso=sso_token))
        self.assertTrue(len(sso_token) > 10)
