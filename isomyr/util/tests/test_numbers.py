from unittest import TestCase

from isomyr.util.numbers import getOrdinal


class OrdinalTestCase(TestCase):

    def test_stNumbers(self):
        numbers = [1, 21, 31, 101]
        expectedOrdinals = ["1st", "21st", "31st", "101st"]
        for number, expected in zip(numbers, expectedOrdinals):
            self.assertEquals(getOrdinal(number), expected)
        for number in [11, 111, 1011]:
            self.assertFalse(getOrdinal(number).endswith("st"))

    def test_ndNumbers(self):
        numbers = [2, 22, 32, 102]
        expectedOrdinals = ["2nd", "22nd", "32nd", "102nd"]
        for number, expected in zip(numbers, expectedOrdinals):
            self.assertEquals(getOrdinal(number), expected)
        for number in [12, 112, 1012]:
            self.assertFalse(getOrdinal(number).endswith("nd"))

    def test_rdNumbers(self):
        numbers = [3, 23, 33, 103]
        expectedOrdinals = ["3rd", "23rd", "33rd", "103rd"]
        for number, expected in zip(numbers, expectedOrdinals):
            self.assertEquals(getOrdinal(number), expected)
        for number in [13, 113, 1013]:
            self.assertFalse(getOrdinal(number).endswith("rd"))

    def test_thNumbers(self):
        numbers = range(4, 21) + [1011, 1012, 1013, 1014]
        for number in numbers:
            self.assertTrue(getOrdinal(number).endswith("th"))
