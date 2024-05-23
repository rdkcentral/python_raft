
import sys
import unittest
import pytest

if __name__ == '__main__':
    pytest.main(['--junitxml=report.xml'])



# # # Discover all test cases in the current directory and subdirectories
# # test_loader = unittest.TestLoader()
# # test_suite = test_loader.discover(start_dir='.', pattern='test_*.py')

# # # Run the test suite
# # test_runner = unittest.TextTestRunner(verbosity=2)
# # test_runner.run(test_suite)

# def main():
#     if len(sys.argv) < 3 or sys.argv[1] != '--config':
#         print("ERROR: missing --config <url> argument")
#         sys.exit(1)

#     config_url = sys.argv[2]

#     # Set up any necessary configuration using config_url
#     # For example, you might want to set an environment variable or
#     # pass this config to your test classes

#     # Discover and run tests
#     loader = unittest.TestLoader()
#     suite = loader.discover('tests')

#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(suite)

# if __name__ == '__main__':
#     main()

# # if __name__ == '__main__':
# #     # Discover all tests in the 'tests' directory
# #     loader = unittest.TestLoader()
# #     suite = loader.discover('tests')

# #     runner = unittest.TextTestRunner(verbosity=2)
# #     runner.run(suite)
    
# # python run_tests.py
# # pytest test_device_management.py --junitxml=path/to/report.xml



