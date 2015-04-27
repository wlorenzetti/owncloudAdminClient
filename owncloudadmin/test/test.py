__author__ = 'walter'

import unittest
from owncloudadmin import Client
from requests.exceptions import HTTPError
from config import Config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.client = Client(Config['owncloud_url'],Config['owncloud_username'],Config['owncloud_password'])


    def test_get_404_error_request(self):
        """Test getting HTTPerror 4040 exception"""
        with self.assertRaises(HTTPError) as e:
            self.client.url = Config['owncloud_url'] + 'nourl'
            self.client.getUsers()
        self.assertEquals(e.exception.response.status_code, 404)

    def test_get_owncloudadmin_response_instance(self):
        pass

if __name__ == '__main__':
    unittest.main()