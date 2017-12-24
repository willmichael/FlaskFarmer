# server/tests/test_login.py

import unittest
import json

from tests.base import BaseTestCase

class TestLogin(BaseTestCase):
    def test_user_login(self):
        # registered user login
        register_res = self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            username = "test0",
            email='test@gmail.com',
            password='test'
            )),
            content_type='application/json'
        )

        response = self.client.post(
            '/auth/login',
            data=json.dumps(dict(
                username = "test0",
                email='test@gmail.com',
                password='test'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)



