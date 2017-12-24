# server/tests/test_register.py

import unittest
import json

from tests.base import BaseTestCase

class TestRegister(BaseTestCase):
    def test_register(self):
        with self.client:
            register_res = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username = "new0",
                    email='test@gmail.com',
                    password='test'
                )),
                content_type='application/json',
            )

            data = json.loads(register_res.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['auth_token'])

            register_res = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username = "new0",
                    email='test@gmail.com',
                    password='test'
                )),
                content_type='application/json',
            )

            data = json.loads(register_res.data.decode())
            self.assertTrue(data['status'] == 'fail')


