import unittest
from lib_costs import get_montly_costs, get_costs

class test_get_montly_costs(unittest.TestCase):
    def test_daily(self):
        costs = get_montly_costs(1,"d")
        self.assertEqual(costs, 30)
    def test_hourly(self):
        costs = get_montly_costs(1,"h")
        self.assertEqual(costs, 720)
    def test_minutely(self):
        costs = get_montly_costs(1,"m")
        self.assertEqual(costs, 43200)
    def test_secondly(self):
        costs = get_montly_costs(1,"s")
        self.assertEqual(costs, 2592000)
    def test_invalid(self):
        costs = get_montly_costs(1,"x")
        self.assertEqual(costs, -1)


class test_get_costs(unittest.TestCase):
    def test_kms(self):
        res = {"type":"aws_kms_key"}
        costs = get_costs(res)
        self.assertEqual(costs, 1)

if __name__ == '__main__':
    unittest.main()