
import sys
import os
import unittest

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

print("sys.path:", sys.path)

from framework.core.unittestTestControl import unittestTestControl

class TestSingle(unittestTestControl):

    def test_example_one(self):
        print("Running test example one")
        self.assertTrue(True)

    def test_example_two(self):
        print("Running test example two")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
    # unittest.main(exit=False)

