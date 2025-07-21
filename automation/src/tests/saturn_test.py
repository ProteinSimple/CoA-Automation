import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock
import saturn


class TestSaturn(unittest.TestCase):

    def test_auth(self):
        user = os.getenv("API_USER")
        passkey = os.getenv("API_PASS")
        test_args = Mock()
        test_args.user = user
        test_args.passkey = passkey
        self.assertEqual(saturn.auth(test_args), (user, passkey))
        self.assertEqual(saturn.auth({}), (user, passkey))
        test_args.user = "jiber"
        test_args.passkey = "ish"
        self.assertRaises(Exception, saturn.auth, test_args)

    def test_check(self):
        user = os.getenv("API_USER")
        passkey = os.getenv("API_PASS")
        self.assertIsInstance(saturn.saturn_check(user, passkey), bool)
        self.assertTrue(saturn.saturn_check(user, passkey))
        self.assertFalse(saturn.saturn_check("jiber", "ish"))

    def test_bundle(self):
        user = os.getenv("API_USER")
        passkey = os.getenv("API_PASS")
        end_dt = datetime.today()
        start_dt = end_dt - timedelta(days=1)
        enddate = end_dt.strftime("%Y-%m-%d")
        startdate = start_dt.strftime("%Y-%m-%d")
        res = saturn.saturn_get_bundle(user, passkey, startdate, enddate)

        self.assertIsInstance(res, list)
        for val in res:
            self.assertIsInstance(val, saturn.CartridgeData)
            self.assertIn(val.class_code, saturn.CartridgeData.code_map)
            self.assertIsNotNone(val.batch_num)
            self.assertIsNotNone(val.build_date)
            self.assertIsNotNone(val.build_time)
            self.assertIsNotNone(val.exp_date)
            self.assertIsNotNone(val.class_name)
            self.assertIsNotNone(val.class_code)
            self.assertIsNotNone(val.id)
            self.assertIsNotNone(val.qc_status)
