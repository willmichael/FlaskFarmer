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
from bson import Binary
import bson

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
                'message': 'please login'
            }
            return make_response(jsonify(responseObject)), 401
        if auth_token:
            userid = User.decode_auth_token(auth_token)
            return f(userid, *args, **kws)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'no auth token'
            }
            return make_response(jsonify(responseObject)), 401
    return decorate_function


@app.route('/auth/login', methods = ['POST'])
def login():
    '''
    User Login
    '''
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
    '''
    User registration
    '''
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

            # Copy file to Directory
            store_files(uid)

            responseObject = {
                'status': 'success',
                'message': 'Registered User',
                'auth_token': auth_token
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            # TODO: logging error

            print e
            result = mongo.db.users.delete_one(user_json)
            print result.deleted_count
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


# Helper Function
def getNextSequence(name):
    '''
    Gets next user id
    '''
    ret = mongo.db.counters.find_one_and_update(
            { "_id": name },
            { "$inc": { "seq": 1 } },
            return_document = ReturnDocument.AFTER
    )
    return ret["seq"]

def store_files(userid):
    '''
    Copies files from local computer to mongo database
    '''
    oldcwd = os.getcwd()
    os.chdir("/Users/WillMichael/Documents/git/FlaskFarmer/project/server/auth")
    file_paths = [
        "../files/test.csv",
        "../files/Mock/1/APPENDIX A- Recall Team_MR.xlsx",
        "../files/Mock/1/APPENDIX B-Agency-Press-Supplier-Customer Contact List_MR.xlsx",
        "../files/Mock/1/APPENDIX D-General Communication Log_MR.xlsx",
        "../files/Mock/1/APPENDIX H-Ingredients Receipts Record_MR.xlsx",
        "../files/Mock/1/APPENDIX I-Production Batch Sheet_MR.xlsx",
        "../files/Mock/1/APPENDIX K-Product Distribution record_MR.xlsx",
        "../files/Mock/1/APPENDIX N-Product Reconciliation_MR.xlsx",
        "../files/Mock/1/Mock Recall/APPENDIX G1-Mock Recall Record_MR.xlsx",
        "../files/Mock/1/Mock Recall/APPENDIX G2-Mock Recall Log_MR.xlsx",
        "../files/Mock/1/Mock Recall/APPENDIX O3-Recall Notification via Phone_MR.docx"
    ]
    for idx, fp in enumerate(file_paths):
        fo = open(fp, 'r')
        bin_file = fo.read()

        data = {
            "userid": userid,
            "docid": idx,
            "data": Binary(bin_file)
        }
        mongo.db.documents.insert_one(data)
    os.chdir(oldcwd)
