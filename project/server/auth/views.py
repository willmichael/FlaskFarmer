# project/server/auth/views.py

import os
import json
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import Binary
from flask import send_file
from flask_httpauth import HTTPBasicAuth

import jwt

from server import app, auth



### Setup db connections
client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection

@app.route('/api/test', methods = ['GET'])
def test():
    return "un-restricted ea"

@app.route('/api/test_auth', methods = ['GET'])
# @auth.login_required
def test_auth():
    return "restricted area"

### MARK: Login/Authentication
# @auth.verify_password
def verify_password(username, password):
    # TODO: implement verify password (do hashing first)
    result = db.test_collection.find_one({"user_name": username})
    if result != None:
        if result["pass"] == password:
            return True
    return False

def json_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'fileinfo':
        return FileInfo(obj['file'], obj['stage'])
    elif '__type__' in obj and obj['__type__'] == 'newuser':
        uid = generate_uid()
        return UserInfo(uid, obj['user_name'], obj['user_pass'], obj['name'], obj['user_type'], obj['email'])
    elif '__type__' in obj and obj['__type__'] == 'userinfo':
        return UserInfo(obj['uid'], obj['user_name'], obj['user_pass'], obj['name'], obj['user_type'], obj['email'])
    return obj

