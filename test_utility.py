from unittest import TestCase

import utility


class Test(TestCase):
    def test_convert(self):
        exp = "01-Jan-70"

        self.assertEqual(utility.convert("19700101"), exp, "Should be {0}".format(exp))

    def test_non_leap_year(self):
        data = "20250229"
        exp = "20250228"
        result = utility.tz_checking(data)
        self.assertEqual(result, exp, "Should be {0}".format(exp))

    def test_leap_year(self):
        data = "20240229"
        exp = "20240229"
        result = utility.tz_checking(data)
        self.assertEqual(result, exp, "Should be {0}".format(exp))
