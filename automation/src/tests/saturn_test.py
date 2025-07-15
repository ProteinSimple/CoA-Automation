import unittest
from datetime import datetime, timedelta
import saturn
import os

class TestSaturn(unittest.TestCase):

    def test_auth(self):
        user = os.getenv("API_USER")
        passkey = os.getenv("API_PASS")
        test_args = lambda:0
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

    def test_fetch(self):
        user = os.getenv("API_USER")
        passkey = os.getenv("API_PASS")
        end_dt = datetime.today()
        start_dt = end_dt - timedelta(days=1)
        enddate = end_dt.strftime("%Y-%m-%d")
        startdate = start_dt.strftime("%Y-%m-%d")
        
        res = list(saturn.saturn_get(startdate, enddate, user, passkey))
        for val in res:
            for f in ["id", "type", "b_date"]:
                self.assertIn(f, val)
                self.assertIsNotNone(val[f])
            

            
        
        
        
