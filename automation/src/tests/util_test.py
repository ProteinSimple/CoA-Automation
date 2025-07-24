import unittest

import util


class UtilTest(unittest.TestCase):
    def test_get_initial(self):
        """Test get_initial function with various scenarios"""
        cases = [
            ("John Doe", "jd"),
            ("John Michael Smith", "jms"),
            ("JOHN DOE", "jd"),
            ("  Arvin Asgharian", "aa")
        ]
        for name, exp in cases:
            self.assertEqual(util.get_initial(name), exp)

    def test_format_date(self):
        cases = [
            ("03/15/2023", "15MAR2023"),
            ("1/5/2023", "5JAN2023"),
            ("12/31/2023", "31DEC2023"),
        ]
        for given, expected in cases:
            self.assertEqual(util.format_date(given), expected)
