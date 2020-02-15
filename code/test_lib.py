import unittest
import os
import json
from moto import mock_s3

from helpers import setup_s3

setup_s3()

from lib import (
    randomString,
    create_response,
    redirect,
    write_key,
    read_key_or_default,
    read_file,
    get_tf_res,
    get_tf_metadata,
    get_post_parameter,
    new_project,
    get_config,
    render_template,
    gen_report,
    get_report,
    get_reports,
    gen_test_project,
)


class test_randomString(unittest.TestCase):
    def test_len(self):
        random_string = randomString(20)
        self.assertEqual(len(random_string), 20)


class test_create_response(unittest.TestCase):
    def test_result(self):
        result = create_response("test", code=401)
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
        write_key("test_write.txt", "test_write")
        data = read_key_or_default("test_write.txt", "Failed")
        self.assertEqual(data, b"test_write")

    def test_overwrite(self):
        write_key("test_overwrite.txt", "TextBefore")
        write_key("test_overwrite.txt", "test_overwrite")
        data = read_key_or_default("test_overwrite.txt", "Failed")
        self.assertEqual(data, b"test_overwrite")


@mock_s3
class test_read_key_or_default(unittest.TestCase):
    def test_real(self):
        write_key("test_real.txt", "test_real")
        data = read_key_or_default("test_real.txt", "Failed")
        self.assertEqual(data, b"test_real")

    def test_default(self):
        data = read_key_or_default("test_default.txt", "test_default")
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
        self.assertEqual(len(tf_res), 1)
        self.assertEqual(tf_res[0]["id"], "state_bucket")

    def test_res_raw(self):
        tf_raw_state = read_file("test_data/terraform.teststate")
        tf_res = get_tf_res(tf_raw_state, True)
        self.assertEqual(len(tf_res), 1)

    def test_res_raw_invalid(self):
        tf_res = get_tf_res("SOME_TEXT", True)
        self.assertEqual(len(tf_res), 0)


class test_get_tf_metadata(unittest.TestCase):
    def test_res(self):
        tf_raw_state = read_file("test_data/terraform.teststate")
        tf_state = json.loads(tf_raw_state)
        tf_meta = get_tf_metadata(tf_state)
        self.assertEqual(tf_meta["version"], 4)
        self.assertEqual(tf_meta["terraform_version"], "0.12.9")
        self.assertEqual(tf_meta["serial"], 360)

    def test_res_raw(self):
        tf_raw_state = read_file("test_data/terraform.teststate")
        tf_meta = get_tf_metadata(tf_raw_state, True)
        self.assertEqual(tf_meta["version"], 4)
        self.assertEqual(tf_meta["terraform_version"], "0.12.9")
        self.assertEqual(tf_meta["serial"], 360)

    def test_res_raw_invalid(self):
        tf_meta = get_tf_metadata("SOME_TEXT", True)
        self.assertEqual(tf_meta["version"], -1)
        self.assertEqual(tf_meta["terraform_version"], "invalid")
        self.assertEqual(tf_meta["serial"], -1)


class test_get_post_parameter(unittest.TestCase):
    def test_parse(self):
        params = get_post_parameter(
            {"body": "name=test&owner=test%40test.de&token=sometoken"}
        )
        self.assertEqual(params["name"], "test")
        self.assertEqual(params["owner"], "test@test.de")
        self.assertEqual(params["token"], "sometoken")

    def test_parse_invalid(self):
        params = get_post_parameter({"body": "name&"})
        self.assertEqual(len(params), 0)

    def test_parse_invalid2(self):
        params = get_post_parameter({"none": "invalid"})
        self.assertEqual(len(params), 0)


@mock_s3
class test_new_project(unittest.TestCase):
    def test_create(self):
        project_id = new_project(
            name="test", owner="test@test.de"
        )
        raw_tf = read_key_or_default(f"{project_id}/terraform.tfstate", "EMPTY")
        config = get_config(project_id)
        self.assertTrue(raw_tf.startswith(b"{"))
        self.assertEqual(config["name"], "test")


@mock_s3
class test_get_config(unittest.TestCase):
    def test_load(self):
        project_id = gen_test_project()
        config = get_config(project_id)
        self.assertEqual(config["name"], "test")

    def test_load_invalid(self):
        config = get_config("notexistingid")
        self.assertEqual(config["name"], "invalid")


class test_render_template(unittest.TestCase):
    def test_load(self):
        output = render_template("project_form.html", name="test")
        self.assertTrue(output.startswith("<!doctype"))


@mock_s3
class test_gen_report(unittest.TestCase):
    def test_report(self):
        project_id = gen_test_project()

        report = gen_report(project_id)
        report_from_s3 = json.loads(
            read_key_or_default(f"{project_id}/report.json", "")
        )

        self.assertEqual(report["config"]["name"], "test")
        self.assertEqual(report_from_s3["config"]["name"], "test")

@mock_s3
class test_get_report(unittest.TestCase):
    def test_report(self):
        project_id = gen_test_project()

        report = gen_report(project_id)
        report_from_s3 = get_report(project_id)

        self.assertEqual(report["config"]["name"], "test")
        self.assertEqual(report_from_s3["config"]["name"], "test")

@mock_s3
class test_get_reports(unittest.TestCase):
    def test_report(self):
        project_id_1 = gen_test_project()
        gen_report(project_id_1)
        project_id_2 = gen_test_project()
        gen_report(project_id_2)

        reports = get_reports()

        self.assertGreaterEqual(len(reports), 2)


@mock_s3
class test_gen_test_project(unittest.TestCase):
    def test_generated(self):
        project_id = gen_test_project()
        config = get_config(project_id)
        self.assertEqual(config["name"], "test")
