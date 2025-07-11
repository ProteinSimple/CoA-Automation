import unittest
import util


class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_util(self):
        self.assertEqual(util.exec_c("TEST"), "Filled")
