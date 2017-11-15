from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import Binary
from flask import send_file

# Basic Setup
# 1
app = Flask(__name__)
# 2

#file info
test_dir = "./files/"
file_name = "test.csv"
file_path = test_dir + file_name

#get binary file data
# fileo = open(file_path, 'r')
# bin_file = fileo.read()


#setup db connections
# client = MongoClient('localhost', 27017)

# db = client.test_database
# collection = db.test_collection

#insert binary into db
# post = {"file_name": file_name,
        # "data": bin_file}

# post_id = collection.insert_one(post).inserted_id

@app.route('/api/get_file', methods = ['POST'])
def get_file():
    json = request.get_json()
    if json['user'] == 'larry':
        return send_file(file_path)
    else:
        return jsonify({'error':'no user found'})

# 3
# app.db = mongo.develop_database
# 4
# api = Api(app)

if __name__ == '__main__':
    app.run(debug = True)
