# project/server/api/views.py

import os
import json
from flask import Flask, request, make_response, jsonify
from flask import send_file

from server.auth.views import authorize
from bson import Binary
import bson

import jwt
import StringIO

import datetime

from server import app, auth, mongo


@app.route('/api/test', methods = ['GET'])
def test():
    responseObject = {
        'status': 'success',
        'message': 'public',
    }
    return make_response(jsonify(responseObject)), 200


@app.route('/api/test_auth', methods = ['GET'])
@authorize
def test_auth(userid):
    responseObject = {
        'status': 'success',
        'message': 'private',
    }
    return make_response(jsonify(responseObject)), 200


@app.route('/api/store_file', methods = ['POST'])
@authorize
def store_file(userid):
    post_data = request.get_json()
    try:
        previous_result = mongo.db.documents.find_one({"userid": userid, "docid": post_data["docid"]})
        if previous_result != None:
            # Update previous documents then add new document
            mongo.db.prev_documents.insert_one(
                {
                    "userid": previous_result.userid,
                    "docid": previous_result.docid,
                    "date": datetime.datetime.now(),
                    "data": previous_result.data
                }
            )
            mongo.db.documents.find_one_and_update(
                {"userid": userid, "docid": post_data["docid"]},
                {"data": post_data["data"]}
            )
        else:
            mongo.db.documents.insert_one(
                {
                    "userid": previous_result.userid,
                    "docid": previous_result.docid,
                    "data": previous_result.data
                }
            )
        responseObject = {
            'status': 'success',
            'message': 'file updated in database',
        }
        return make_response(jsonify(responseObject)), 200
    except Exception as e:
        print e
        responseObject = {
            'status': 'fail',
            'message': 'unknown error try again',
        }
        return make_response(jsonify(responseObject)), 400


@app.route('/api/get_file', methods = ['POST'])
@authorize
def get_file(userid):
    post_data = request.get_json()
    try:
        result = mongo.db.documents.find_one({"userid": userid, "docid": post_data["docid"]})
        if result != None:
            res_bytes = bytes(result["data"])
            strIO = StringIO.StringIO()
            strIO.write(res_bytes)
            strIO.seek(0)
            return make_response(send_file(strIO, attachment_filename="testing.txt", as_attachment=True)), 200
            # responseObject = {
                # 'status': 'success',
                # 'message': 'documentX',
            # }
            # print "not none"
            # return make_response(jsonify(responseObject)), 200

        else:
            print "none"
            print post_data["docid"]
            print "this", userid

            responseObject = {
                'status': 'fail',
                'message': 'documentX not found'
            }
            return make_response(jsonify(responseObject)), 202
    except Exception as e:
        print post_data["docid"]
        print e
        responseObject = {
            'status': 'fail',
            'message': 'unknown error try again' + str(e),
        }
        return make_response(jsonify(responseObject)), 400


### MARK: Helper

def store_files_db(userid):
    oldcwd = os.getcwd()
    os.chdir("/Users/WillMichael/Documents/git/FlaskFarmer/project/tests")
    file_paths = [
        "../server/files/Mock/1/APPENDIX A- Recall Team_MR.xlsx",
        "../server/files/Mock/1/test.txt",
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
