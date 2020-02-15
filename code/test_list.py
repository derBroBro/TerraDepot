import unittest
import os
import json
from moto import mock_s3

from helpers import setup_s3

setup_s3()


from list import lambda_handler
from lib import read_key_or_default, new_project, gen_report, read_file, write_key, gen_test_project


@mock_s3
class test_lambda_handler(unittest.TestCase):
    def test_request_get(self):
        # create project
        project_id_1 = gen_test_project()
        gen_report(project_id_1)
        project_id_2 = gen_test_project()
        gen_report(project_id_2)
        project_id_3 = gen_test_project()
        # get state
        event = {
            "httpMethod": "GET",
            "requestContext": {"domainName": "test.local"},
        }
        result = lambda_handler(event, {})
        print(result["body"])
        self.assertEqual(result["statusCode"], 200)
        self.assertTrue(result["body"].startswith("<!doctype"))


if __name__ == "__main__":
    unittest.main()
