import unittest
from lib_security import get_security


class test_get_security(unittest.TestCase):
    def test_s3_enabled(self):
        res = {"type":"aws_s3_bucket", "instances":[{"attributes":{"logging":["somebucket"]}}] }
        sec = get_security(res)
        self.assertEqual(sec, 0)
    def test_s3_disabled(self):
        res = {"type":"aws_s3_bucket", "instances":[{"attributes":{"logging":[]}}] }
        sec = get_security(res)
        self.assertEqual(sec, 2)
    def test_s3_emtpy(self):
        res = {"type":"aws_s3_bucket", "instances":[] }
        sec = get_security(res)
        self.assertEqual(sec, 3)

if __name__ == '__main__':
    unittest.main()

