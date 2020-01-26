import unittest
import os
import json
from moto import mock_s3

from helpers import setup_s3
setup_s3()

from new import lambda_handler
from lib import read_key_or_default

@mock_s3
class test_lambda_handler(unittest.TestCase):
    def test_request_post_complete(self):
        event = {"httpMethod":"POST", "body":"name=test&owner=test%40test.de&token=test"}
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 301)
        project_id  = result["headers"]["Location"].split("/")[-2]
        state = json.loads(read_key_or_default(f"{project_id}/terraform.tfstate","NA"))
        self.assertEqual(state["serial"],0)
        config = json.loads(read_key_or_default(f"{project_id}/config.json","NA"))
        self.assertEqual(config["name"],"test")
    def test_request_post_incomplete(self):
        event = {"httpMethod":"POST", "body":"name=test&token=test"}
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 500)
    def test_request_get(self):
        event = {"httpMethod":"GET"}
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 200)

if __name__ == '__main__':
    unittest.main()