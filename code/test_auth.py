import unittest
import os
import json

from helpers import setup_s3
setup_s3()

os.environ["KEY"] = "CheckMe"

from auth import create_policy, lambda_handler

class test_create_policy(unittest.TestCase):
    def test_allow(self):
        policy = create_policy("test","test")
        self.assertEqual(policy["policyDocument"]["Statement"][0]["Effect"], "Deny")

class test_lambda_handler(unittest.TestCase):
    def test_lambda_handler_ok(self):
        event = {"headers":{"Authorization":"Basic YWRtaW46Q2hlY2tNZQ=="}, "methodArn": "test"}
        policy = lambda_handler(event,{})
        self.assertEqual(policy["policyDocument"]["Statement"][0]["Effect"], "Allow")
    def test_lambda_handler_invalid(self):
        event = {"headers":{"Authorization":"Basic YWRtaW46SnNrZGF3aGRqa2FoZA=="}, "methodArn": "test"}
        with self.assertRaises(Exception):
            lambda_handler(event,{})

if __name__ == '__main__':
    unittest.main()