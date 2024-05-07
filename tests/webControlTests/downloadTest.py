#! /bin/python3
import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.testControl import testController

class downloadTest(testController):
    def __init__(self, testName="downloadTest", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):  
        testClass = self
        webpageControl = testClass.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)
        webpageControl.navigateTo("download_page")

        self.log.stepStart("Downloading file and checking it exists")
        webpageControl.performAction("download")

        self.utils.wait(10)

        path = os.path.join(self.log.logPath,"downloads/textfile.txt")
        if os.path.isfile(path):
            self.log.stepResult(True, "File does exist")
        else:
            self.log.stepResult(False, "File does not exist")
            return

        self.log.stepStart("Checking contents of file are as expected")
        expectedText = """This is a text file.

Downloaded from https://testapps.heroku.com

Remember to visit https://EvilTester.com for all your testing edufication.
"""
        with open(path) as textFile:
            text = textFile.read()
            if text == expectedText:
                self.log.stepResult(True, "Content of file was as expected")
            else:
                self.log.stepResult(False, f"Content of file was not as expected. Actual content was:\n{text}")


    

    

if __name__ == "__main__":
    test = downloadTest()

    
