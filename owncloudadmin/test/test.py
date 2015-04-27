__author__ = 'walter'

import unittest
from owncloudadmin import Client, StatusCodeException
import requests
from xml.etree import ElementTree as ET
from config import Config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.client = Client(Config['owncloud_url'],Config['owncloud_username'],Config['owncloud_password'])


    def test_get_404_error_request(self):
        """Test getting HTTPerror 4040 exception"""
        with self.assertRaises(requests.exceptions.HTTPError) as e:
            self.client.url = Config['owncloud_url'] + 'nourl'
            self.client.getUsers()
        self.assertEquals(e.exception.response.status_code, 404)

    def test_get_owncloudadmin_response_instance(self):
        pass

    def test_owncloudadmin_status_exception(self):
        with self.assertRaises(StatusCodeException) as e:
            self.client.getUser('bbbbbbbbbbbbbbbb')
        self.assertEqual(e.exception.status,'failure')
        self.assertIn(e.exception.statusCode,[101,102,103,104,105,998,999])

    def test_get_users(self):
        #get data from verbose procedure
        res = requests.get(self.client.url+'/users',auth=self.client.auth)
        xml = ET.fromstring(res.text)
        data = xml.find('data')
        toConf = []
        for u in list(data.find('users')):
            toConf.append(u.text)

        users = self.client.getUsers()
        self.assertListEqual(users,toConf)


if __name__ == '__main__':
    unittest.main()