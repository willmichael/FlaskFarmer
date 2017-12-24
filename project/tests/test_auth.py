# server/tests/test_auth.py

import unittest
import json

from tests.base import BaseTestCase

class TestAuth(BaseTestCase):
    def test_no_auth(self):
        test_auth = self.client.get(
            '/api/test'
        )
        data = json.loads(test_auth.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'public')

    def test_auth(self):
        # registered user access data
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

        test_auth = self.client.get(
            '/api/test_auth',
            headers=dict(
                Authorization='Bearer ' + data['auth_token']
            )
        )
        data = json.loads(test_auth.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'private')

