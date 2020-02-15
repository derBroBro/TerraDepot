import unittest
import os
import json
from moto import mock_s3

from helpers import setup_s3

setup_s3()


from info import lambda_handler
from lib import read_key_or_default, new_project, gen_report, read_file, write_key, gen_test_project


@mock_s3
class test_lambda_handler(unittest.TestCase):
    def test_request_get(self):
        # create project
        project_id = gen_test_project()
        tf_raw_state = read_file("test_data/terraform.teststate")
        write_key(f"{project_id}/terraform.tfstate", tf_raw_state)
        report = gen_report(project_id)
        print(report)
        # get state
        event = {
            "httpMethod": "GET",
            "pathParameters": {"projectId": project_id},
            "requestContext": {"domainName": "test.local"},
        }
        result = lambda_handler(event, {})
        print(result["body"])
        self.assertEqual(result["statusCode"], 200)
        self.assertTrue(result["body"].startswith("<!doctype"))

    def test_request_get_na(self):
        event = {
            "httpMethod": "GET",
            "pathParameters": {"projectId": "notexistingproject"},
            "requestContext": {"domainName": "test.local"},
        }
        result = lambda_handler(event, {})
        self.assertEqual(result["statusCode"], 404)
        self.assertTrue(result["body"].startswith("No "))


if __name__ == "__main__":
    unittest.main()
