import unittest
from check_security import run, gen_review, get_test, STATE


class test_gen_review(unittest.TestCase):
    def test_generate(self):
        tests = []
        tests.append(get_test(STATE.CRITICAL, "a tests message"))
        tests.append(get_test(STATE.WARNING, "a tests message"))
        review = gen_review(tests)
        self.assertEqual(review["state"], 2)
        self.assertEqual(len(review["tests"]), 2)


class test_get_test(unittest.TestCase):
    def test_generate(self):
        result = get_test(STATE.WARNING, "a tests message")
        self.assertEqual(result["state"], 1)
        self.assertEqual(result["message"], "a tests message")


class test_get_security(unittest.TestCase):
    def test_s3_enabled(self):
        res = {
            "type": "aws_s3_bucket",
            "instances": [{"attributes": {"logging": ["somebucket"]}}],
        }
        sec = run(res)
        self.assertEqual(sec["state"], 0)

    def test_s3_disabled(self):
        res = {"type": "aws_s3_bucket", "instances": [{"attributes": {"logging": []}}]}
        sec = run(res)
        self.assertEqual(sec["state"], 2)

    def test_s3_emtpy(self):
        res = {"type": "aws_s3_bucket", "instances": []}
        sec = run(res)
        self.assertEqual(sec["state"], -1)

    def test_other_emtpy(self):
        res = {"type": "aws_other_bucket", "instances": []}
        sec = run(res)
        self.assertEqual(sec["state"], -1)


if __name__ == "__main__":
    unittest.main()
