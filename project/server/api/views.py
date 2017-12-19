# project/server/api/views.py

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

# Basic Setup
# app = Flask(__name__)
# auth = HTTPBasicAuth()

# Properties
prefix = "/api/"
test_dir = "./files/"
user_dir = "./users"
template_dir = "./templates/"

template_X = "recall_1/template.txt"
# File info
file_name = "test.csv"
file_path = test_dir + file_name

class UserPaths():
    ''' Path Class'''
    def __init__(self, uid):
        self.stage1_files = [
            "file1",
            "file2",
            "file3" ]
        self.stage2_files = [
            "file1",
            "file2",
            "file3" ]
        self.stage3_files = [
            "file1",
            "file2",
            "file3" ]
        self.stage_dir = [
            ["stage1", self.stage1_files ],
            ["stage2", self.stage2_files ],
            ["stage3", self.stage3_files ] ]

        self.stages = []
        self.file_paths = []
        for i, dirs in enumerate(self.stage_dir):
            sd = "%s/%s/%s" % (user_dir, uid, dirs[0])
            self.stages.append([sd])
            for file_dirs in dirs[1]:
                self.stages[i].append("%s/%s" % (sd,file_dirs))


class UserInfo():
    ''' User information'''
    def __init__(self, uid, user_name, user_pass, name, user_type, email):
        self.uid = uid
        self.user_name = user_name
        self.password = user_pass
        self.name = name
        self.type = user_type
        self.email = email


class FileInfo():
    ''' File information'''
    def __init__(self, file_n, stage):
        self.file = file_n
        self.stage = stage


#get binary file data
# fileo = open(file_path, 'r')
# bin_file = fileo.read()


### Setup db connections
client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection

### insert binary into db
# post = {"file_name": file_name,
        # "data": bin_file}

# post_id = collection.insert_one(post).inserted_id

@app.route('/api/test', methods = ['GET'])
def test():
    return "un-restricted ea"

@app.route('/api/test_auth', methods = ['GET'])
@auth.login_required
def test_auth():
    return "restricted area"


@app.route('/api/get_file', methods = ['POST'])
@auth.login_required
def get_file():
    # TODO: user authentication somehow to get uid
    # JSON test
    json_test = '{ "__type__":"fileinfo", "file": 1, "stage": 2 }'
    up = UserPaths(1)

    # Decide which file the user wants from JSON
    fi = json.loads(json_test, object_hook = json_decoder)

    # Find file if it exists
    # Return file or return DNE
    stage = fi.stage - 1
    if len(up.stages) >= stage and len(up.stages[stage]) > fi.file:
        all_files = os.listdir(up.stages[stage][fi.file])
        # TODO: Choose which file to send
        return send_file("%s/%s" % (up.stages[stage][fi.file], all_files[0]))
    else:                                # File Doesnt exist
         return jsonify({'error':'no dir found'})
    return "1"


@app.route(prefix + "create_user", methods = ['POST'])
def create_user():
    ''' Create all relevant user information

    Create an entry for the user in Mongo database
    populate user files with templates on the filestorage server
    '''

    # TODO: Grab user information from POST call 
    json = request.get_json()
    user_info = json.loads(json, object_hook = json_decoder)

    # User information
    # TODO: Check database to make sure UID is unique
    uid = generate_uid()
    user_name = "userName"
    user_pass = "password"
    name = "Jack"
    user_type = 1
    email = "test@gmail.com"

    # TODO: Generate user information and add info to DB
    # TODO: Hash password
    ui = UserInfo(uid, user_name, user_pass, name, user_type, email)
    ui = json.dumps(ui.__dict__)

    insert_user_id = collection.insert_one(ui).inserted_id
    recall_1 = generate_recall_json(uid)
    recall_1_id = collection.insert_one(recall_1).inserted_id

    # TODO: Create File Space
    up = UserPaths(uid)

    for fp in up.stages:
        if not os.path.exists(fp):
            os.makedirs(fp)

    return "1"


### MARK: Login/Authentication
@auth.verify_password
def verify_password(username, password):
    # TODO: implement verify password (do hashing first)
    result = db.test_collection.find_one({"user_name": username})
    if result != None:
        if result["pass"] == password:
            return True
    return False

### MARK: Token authenication


### MARK: Helper functions
def generate_uid():
    ''' Helper function create user ID or get userID in future'''

    # TODO: implement generating unique userid's

    return 1

def generate_recall_json(uid):
    recall_1 = {
        "uid": uid,
        "form_X": template_dir + template_X
    }

    return recall_1

def json_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'fileinfo':
        return FileInfo(obj['file'], obj['stage'])
    elif '__type__' in obj and obj['__type__'] == 'newuser':
        uid = generate_uid()
        return UserInfo(uid, obj['user_name'], obj['user_pass'], obj['name'], obj['user_type'], obj['email'])
    elif '__type__' in obj and obj['__type__'] == 'userinfo':
        return UserInfo(obj['uid'], obj['user_name'], obj['user_pass'], obj['name'], obj['user_type'], obj['email'])
    return obj








# TODO: what are these

# 3
# app.db = mongo.develop_database
# 4
# api = Api(app)

if __name__ == '__main__':
    app.run(debug = True)
