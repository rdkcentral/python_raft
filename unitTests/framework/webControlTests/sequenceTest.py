#! /bin/python3
import os
import sys



# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../../")

from framework.core.testControl import testController

class sequenceTest(testController):
    def __init__(self, testName="sequenceTest", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):
        webpageControl = self.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        self.log.stepStart("Navigating through sequence to sequence_page")
        webpageControl.navigateTo("sequence_page")

        self.utils.wait(10)

        text = webpageControl.getTextOfElement("content")
        if text == "You have been successfully redirected.":
            self.log.stepResult(True, "Text is as expected")
        else:
            self.log.stepResult(False, "Text is not as expected")




if __name__ == "__main__":
    test = sequenceTest()

    
