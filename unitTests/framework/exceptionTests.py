#! /bin/python3
import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.testControl import testController
from framework.core.logModule import logModule

class framework_test1(testController):
 
    def __init__(self, log=None, exitOnError=False):
        self.exitOnError = exitOnError
        super().__init__("framework_test", "1", log=log)
        self.run()

    def waitForBoot(self):
        self.log.step("waitForBoot Removed")
        return True

    def testFunction(self):
        if self.exitOnError == True:
            self.log.stepStart("UnitTest 2 Started", "This test will fail")
            raise Exception("I want to raise an exception")
            self.utils.wait( 1 )
            return False
        self.log.stepStart("UnitTest 2 Started", "This test will pass")
        self.log.step("unit_test2 Completed.")
        self.log.stepResult( True, "Happy with this stage")
        self.utils.wait( 2 )
        return True

    def testExceptionCleanUp(self):
        # Although this function is available, each test should setup it's requirements for operation
        # But if a test would do something out of the ordinary, e.g. erase some part of the serialsation data, or change the retry count to large value
        # Then in this case you would use this function to reprogram the defaults, if an exception occurs.
        # The descrive test should already be cleaning up, after it's passed without an excpetion
        self.log.warn("testExceptionCleanUp()-> Only to be used for major test recovery")
        #quit

if __name__ == '__main__':

    # Run a group test, this will cause all the tests to be grouped under the same parent
    #├── framework_test-1
    #│   ├── test-1.log
    #│   ├── test-2.log
    #│   └── test-3.log
    #└── test_summary.log

    summary = logModule("GroupTest1", level=logModule.INFO)
    summary.testStart("GroupTest1", qcId = "1234" )

    framework_test1(summary, exitOnError=True)
    framework_test1(summary)
    framework_test1(summary, exitOnError=True)

    summary.testResult("GroupTest1 Completed")

    # Perform a test on a single run on it's own, this will cause a new root directory
    #└── framework_test-1
        #├── test-0.log
        #└── test_summary.log

    framework_test1()





