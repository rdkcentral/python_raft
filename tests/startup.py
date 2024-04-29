#! /bin/python3
import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.testControl import testController

class framework_test1(testController):
 
    def __init__(self):
        print('unit2 - Initializing test controller')
        super().__init__("framework_test", "1")
        self.run()

    def testFunction(self):
        print("unit_test2 called.")
        return True

if __name__ == '__main__':

    test = framework_test1()
  

    