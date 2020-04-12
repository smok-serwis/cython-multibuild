from example_module.test import times_two
from example_module.test2 import times_three, times_five
from example_module.test3.test3 import times_four
from example_module.test3.test2 import times_seven
from example2.example import test
from example3.example3.example3.test import test as test_three
import unittest


class TestExample(unittest.TestCase):
    def test_seven(self):
        self.assertEqual(times_seven(4), 4*7)

    def test_three(self):
        self.assertEqual(test_three(2, 3), 5)

    def test_test(self):
        self.assertEqual(test(2, 3), 5)

    def test_five(self):
        self.assertEqual(times_five(2), 10)

    def test_two(self):
        self.assertEqual(times_two(2), 4)

    def test_three(self):
        self.assertEqual(times_three(2), 6)

    def test_four(self):
        self.assertEqual(times_four(2), 8)
