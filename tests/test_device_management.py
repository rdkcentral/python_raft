
import sys
import os
import unittest

# Add the directory containing the framework package to the Python path
# framework_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'framework'))
framework_path = '/home/FKC01/python_raft'

sys.path.append(framework_path)

from framework.core.unittestTestControl import unittestTestControl

class DeviceManagementTests(unittestTestControl):

# def test_initial(self):
#     print("initial test")

    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_subtraction(self):
        self.assertTrue(5 - 3, 2)


if __name__ == '__main__':
    unittest.main()