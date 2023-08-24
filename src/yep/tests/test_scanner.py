import unittest

from yep.scanner import Scanner

class TestScanner(unittest.TestCase):
    def test_scanner1(self):
        scanner = Scanner('print "Hello, World!"')