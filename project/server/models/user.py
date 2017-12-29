# server/models/user.py

import jwt
import datetime
import logging

from server import app

class User():
    def __init__(self, _id, username, password, email, form_type=0):
        self._id = _id
        self.username = username
        self.password = password
        self.email = email
        self.form_type = form_type

    @staticmethod
    def encode_auth_token(user_id):
        '''
        Generates Authentication Token for user based on JSON Web Tokens
        https://realpython.com/blog/python/token-based-authentication-with-flask/
        :return: string
        '''
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        https://realpython.com/blog/python/token-based-authentication-with-flask/
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            # is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            # if is_blacklisted_token:
                # return 'Token blacklisted. Please log in again.'
            # else:
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

