import unittest
# import this so it's seen by coverage metrics
from sqla_vertica_python import vertica_python  # noqa


class TestNothing(unittest.TestCase):
    # It shouldn't be too hard to increase coverage from here!
    def test_true(self):
        self.assertTrue(True)
