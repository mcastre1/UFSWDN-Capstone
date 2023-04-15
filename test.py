import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

import app
from models import setup_db, Job, Inventory, Sink


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.server = app
        self.server.test = True
        self.app = self.server.app
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        self.jwt = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdlWnQxR0JZY25jZkJ2eVpheEVIMCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ubXl4azdoZnRvbWVmbHJkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMTEyOTU4NTM3MDUyNDQzMjgyOCIsImF1ZCI6ImNhcHN0b25lQVBJIiwiaWF0IjoxNjgxNTgyNjA5LCJleHAiOjE2ODE1ODk4MDksImF6cCI6IlBZRVByYmNTbldQbFRySUFqdlRqcDJjYW5pSm5Tb3RUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6aW52ZW50b3J5X2l0ZW0iLCJjcmVhdGU6am9iIiwiY3JlYXRlOnNpbmsgIiwiZGVsZXRlOmludmVudG9yeV9pdGVtIiwiZGVsZXRlOmpvYiIsInBhdGNoOmludmVudG9yeV9pdGVtIiwicGF0Y2g6am9iIiwicGF0Y2g6c2luayIsInJlYWQ6aW52ZW50b3J5IiwicmVhZDppbnZlbnRvcnlfaXRlbSIsInJlYWQ6am9iLWRldGFpbHMiLCJyZWFkOmpvYnMiLCJyZWFkOnNpbmsiLCJyZWFkOnNpbmtzIl19.AqgbnDlxMgjnQ3l5XqmwZfPXwZDAh1T7ryzPdxRX5H_2fxNSJdBkh1GwWg16sPFiY8UqQuiNVHeGT2Ga11i2OSgq7zzSh3pA81w1mmBsQJEUHSIX5cqa3LyfsqAiYLjnsHe2YRQmCEdAfub7vh6K8vqJ729ulSu-50p_nxlvepnGydGHBli2dbWvDWle68aMyhKdv_amTdm_vJ3VOpZfOfuBp9nwof1KFb5sMPfWXTq5PyGrhJxiEsECiyCvmdTZpUrTMgcU70nxNf2OUn9jVHECHBnv1GsPo73vPGAfiA96UMjcrMKSNLBjZ5KqNJI5uBoV14FGbgl4DOr0s-XRMg"
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test
    for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/sinks', headers={'Authorization':self.jwt})
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
