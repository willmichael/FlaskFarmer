# project/server/auth/views.py

import os
import json
import sys
from functools import wraps

import jwt

from flask import request, make_response, jsonify
from pymongo import ReturnDocument

from server import app, auth, mongo
from server.models.user import User

def authorize(f):
    @wraps(f)
    def decorate_function(*args, **kws):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'no auth'
            }
            return make_response(jsonify(responseObject)), 401
        if auth_token:
            userid = User.decode_auth_token(auth_token)
            return f(userid, *args, **kws)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'no auth'
            }
            return make_response(jsonify(responseObject)), 401
    return decorate_function


@app.route('/auth/login', methods = ['POST'])
def login():
    post_data = request.get_json()
    try:
        result = mongo.db.users.find_one({'username': post_data["username"]})
        if result != None:
            if result["password"] == post_data["password"]:
                auth_token = User.encode_auth_token(result["_id"])
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Logged in',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(responseObject)), 200
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': 'login failed',
        }
        return make_response(jsonify(responseObject)), 400
    responseObject = {
        'status': 'fail',
        'message': 'login failed',
    }
    return make_response(jsonify(responseObject)), 400


@app.route('/auth/register', methods = ['POST'])
def register():
    post_data = request.get_json()
    result = mongo.db.users.find_one({'username': post_data["username"]})
    if result == None:
        try:
            # Create user
            uid = getNextSequence("userid")
            user = User(
                _id = uid,
                username = post_data["username"],
                email = post_data["email"],
                password = post_data["password"]
            )

            user_json = user.__dict__
            mongo.db.users.insert_one(user_json)
            auth_token = user.encode_auth_token(uid)

            responseObject = {
                'status': 'success',
                'message': 'Registered User',
                'auth_token': auth_token
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            # TODO: logging error
            responseObject = {
                'status': 'fail',
                'message': 'error registering, please try again'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'user already exists'
        }
        return make_response(jsonify(responseObject)), 202


### MARK: Login/Authentication
# @auth.verify_password
def verify_password(username, password):
    # TODO: implement verify password (do hashing first)
    result = mongo.db.test_collection.find_one({"user_name": username})
    if result != None:
        if result["pass"] == password:
            return True
    return False


### MARK: Helpers
def json_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'fileinfo':
        return FileInfo(obj['file'], obj['stage'])
    elif '__type__' in obj and obj['__type__'] == 'newuser':
        uid = generate_uid()
        return UserInfo(uid, obj['user_name'], obj['user_pass'], obj['name'], obj['user_type'], obj['email'])
    elif '__type__' in obj and obj['__type__'] == 'userinfo':
        return UserInfo(obj['uid'], obj['user_name'], obj['user_pass'], obj['name'], obj['user_type'], obj['email'])
    return obj


def getNextSequence(name):
   ret = mongo.db.counters.find_one_and_update(
            { "_id": name },
            { "$inc": { "seq": 1 } },
            return_document = ReturnDocument.AFTER
   )
   return ret["seq"]

