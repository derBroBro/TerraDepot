import unittest
import os
import json
from moto import mock_s3

from helpers import setup_s3
setup_s3()


from state import lambda_handler
from new import lambda_handler as new_lambda_handler
from lib import read_key_or_default

@mock_s3
class test_lambda_handler(unittest.TestCase):
    def test_request_get(self):
        # create project
        new_event = {"httpMethod":"POST", "body":"name=test&owner=test%40test.de&token=test"}
        new_result = new_lambda_handler(new_event,{})
        project_id  = new_result["headers"]["Location"].split("/")[-2]

        # get state
        event = {"httpMethod":"GET","pathParameters":{"projectId":project_id}, "requestContext":{"domainName":"test.local"}}
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 200)
        self.assertTrue(result["body"].startswith("{"))

    def test_request_get_na(self):
        event = {"httpMethod":"GET","pathParameters":{"projectId":"notexistingproject"}, "requestContext":{"domainName":"test.local"}}
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 200)
        self.assertTrue(result["body"].startswith("No "))


    def test_request_post(self):
        # create project
        new_event = {"httpMethod":"POST", "body":"name=test&owner=test%40test.de&token=test"}
        new_result = new_lambda_handler(new_event,{})
        project_id  = new_result["headers"]["Location"].split("/")[-2]

        # post state
        event = {"httpMethod":"POST", "body": "test","pathParameters":{"projectId":project_id}, "requestContext":{"domainName":"test.local"}}
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["body"], "test")

        s3_data = read_key_or_default(f"{project_id}/terraform.tfstate","NONE")
        self.assertEqual(s3_data,b"test")


if __name__ == '__main__':
    unittest.main()