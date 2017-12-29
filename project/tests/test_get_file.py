# server/tests/test_get_file.py

import unittest
import json
import os

from tests.base import BaseTestCase
from server.models.user import User
from server import mongo
from bson import Binary

class TestGetFile(BaseTestCase):
    def test_get_file(self):
        register_res = self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            username = "test0",
            email='test@gmail.com',
            password='test'
            )),
            content_type='application/json'
        )
        data = json.loads(register_res.data.decode())
        userid = User.decode_auth_token(data["auth_token"])
        store_files(userid)

        doc_result = self.client.post(
            'api/get_file',
            data=json.dumps(dict(
                docid = 0,
            )),
            content_type="application/json",
            headers = dict(
                Authorization='Bearer ' + data["auth_token"]
            )
        )
        print doc_result

        # doc_data = json.loads(doc_result.data.decode())
        # self.assertTrue(doc_data['status'] == 'success')
        # self.assertTrue(doc_data['message'] == 'documentX')
        # self.assertTrue(doc_data['data'])


def store_files(userid):
    oldcwd = os.getcwd()
    os.chdir("/Users/WillMichael/Documents/git/FlaskFarmer/project/tests")
    file_paths = [
        "../server/files/Mock/1/APPENDIX A- Recall Team_MR.xlsx",
        "../server/files/Mock/1/APPENDIX B-Agency-Press-Supplier-Customer Contact List_MR.xlsx",
        "../server/files/Mock/1/APPENDIX D-General Communication Log_MR.xlsx",
        "../server/files/Mock/1/APPENDIX H-Ingredients Receipts Record_MR.xlsx",
        "../server/files/Mock/1/APPENDIX I-Production Batch Sheet_MR.xlsx",
        "../server/files/Mock/1/APPENDIX K-Product Distribution record_MR.xlsx",
        "../server/files/Mock/1/APPENDIX N-Product Reconciliation_MR.xlsx",
        "../server/files/Mock/1/Mock Recall/APPENDIX G1-Mock Recall Record_MR.xlsx",
        "../server/files/Mock/1/Mock Recall/APPENDIX G2-Mock Recall Log_MR.xlsx",
        "../server/files/Mock/1/Mock Recall/APPENDIX O3-Recall Notification via Phone_MR.docx"
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

