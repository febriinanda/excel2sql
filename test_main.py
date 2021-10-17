from unittest import TestCase

import utility


class Test(TestCase):
    def test_convert(self):
        exp = "01-Jan-70"

        self.assertEqual(utility.convert("19700101"), exp, "Should be {0}".format(exp))
