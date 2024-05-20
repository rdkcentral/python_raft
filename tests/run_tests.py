
import sys
import unittest

# Discover all test cases in the current directory and subdirectories
test_loader = unittest.TestLoader()
test_suite = test_loader.discover(start_dir='.', pattern='test_*.py')

# Run the test suite
test_runner = unittest.TextTestRunner(verbosity=2)
test_runner.run(test_suite)

# python run_tests.py
# pytest test_device_management.py --junitxml=path/to/report.xml



