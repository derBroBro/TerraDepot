import unittest
import os
import json
from moto import mock_s3

from helpers import setup_s3

setup_s3()


from state import lambda_handler
from lib import read_key_or_default, new_project, read_file, get_tf_metadata


@mock_s3
class test_lambda_handler(unittest.TestCase):
    def test_request_get(self):
        # create project
        project_id = new_project(name="test", owner="test@test.de", token="test123")

        # get state
        event = {
            "httpMethod": "GET",
            "pathParameters": {"projectId": project_id},
            "requestContext": {"domainName": "test.local"},
        }
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 200)
        self.assertTrue(result["body"].startswith("{"))

    def test_request_get_na(self):
        event = {
            "httpMethod": "GET",
            "pathParameters": {"projectId": "notexistingproject"},
            "requestContext": {"domainName": "test.local"},
        }
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 404)
        self.assertTrue(result["body"].startswith("No "))

    def test_request_post(self):
        # create project
        project_id = new_project(name="test", owner="test@test.de", token="test123")

        # post state
        raw_tf = read_file("test_data/terraform.teststate")
        event = {
            "httpMethod": "POST",
            "body": raw_tf,
            "pathParameters": {"projectId": project_id},
            "requestContext": {"domainName": "test.local"},
        }
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 200)
        self.assertTrue(result["body"].startswith("{"))

        s3_data = read_key_or_default(f"{project_id}/terraform.tfstate", "NONE")
        tf_meta = get_tf_metadata(s3_data, True)
        self.assertNotEqual(tf_meta["terraform_version"], "invalid")

    def test_request_post_invalid(self):
        # create project
        project_id = new_project(name="test", owner="test@test.de", token="test123")

        # post state
        event = {
            "httpMethod": "POST",
            "body": "test",
            "pathParameters": {"projectId": project_id},
            "requestContext": {"domainName": "test.local"},
        }
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 500)


if __name__ == "__main__":
    unittest.main()
