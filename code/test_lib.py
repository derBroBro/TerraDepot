import unittest
import os
import json
from moto import mock_s3

from helpers import setup_s3
setup_s3()

from lib import randomString, create_response, redirect, write_key, read_key_or_default, read_file, get_tf_res, get_tf_metadata

class test_randomString(unittest.TestCase):
    def test_len(self):
        random_string = randomString(20)
        self.assertEqual(len(random_string), 20)
    
class test_create_response(unittest.TestCase):
    def test_result(self):
        result = create_response("test",code=401)
        self.assertEqual(result["body"], "test")
        self.assertEqual(result["statusCode"], 401)

class test_redirect(unittest.TestCase):
    def test_result(self):
        result = redirect("http://test.local")
        self.assertEqual(result["headers"]["Location"], "http://test.local")
        self.assertEqual(result["statusCode"], 301)

@mock_s3
class test_write_key(unittest.TestCase):
    def test_write(self):
        write_key("test_write.txt","test_write")
        data = read_key_or_default("test_write.txt","Failed")
        self.assertEqual(data, b"test_write")
    def test_overwrite(self):
        write_key("test_overwrite.txt","TextBefore")
        write_key("test_overwrite.txt","test_overwrite")
        data = read_key_or_default("test_overwrite.txt","Failed")
        self.assertEqual(data, b"test_overwrite")

@mock_s3
class test_read_key_or_default(unittest.TestCase):
    def test_real(self):
        write_key("test_real.txt","test_real")
        data = read_key_or_default("test_real.txt","Failed")
        self.assertEqual(data, b"test_real")
    def test_default(self):
        data = read_key_or_default("test_default.txt","test_default")
        self.assertEqual(data, b"test_default")


class test_read_file(unittest.TestCase):
    def test_real(self):
        data = read_file("test_data/terraform.teststate")
        self.assertTrue(data.startswith("{"))


class test_get_tf_res(unittest.TestCase):
    def test_res(self):
        tf_raw_state = read_file("test_data/terraform.teststate")
        tf_state = json.loads(tf_raw_state)
        tf_res = get_tf_res(tf_state)
        self.assertEqual(len(tf_res),1)
        self.assertEqual(tf_res[0]["id"], "test-res")

class test_get_tf_metadata(unittest.TestCase):
    def test_res(self):
        tf_raw_state = read_file("test_data/terraform.teststate")
        tf_state = json.loads(tf_raw_state)
        tf_meta = get_tf_metadata(tf_state)
        self.assertEqual(tf_meta["version"],4)
        self.assertEqual(tf_meta["terraform_version"],"0.12.9")
        self.assertEqual(tf_meta["serial"], 360)
