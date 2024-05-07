#! /bin/python3
import os
import sys



# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.testControl import testController

class elementAttributeTest(testController):
    def __init__(self, testName="elementAttributeTest", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):
        webpageControl = self.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        webpageControl.navigateTo("attributes_page")

        self.log.stepStart("Getting attribute from element")
        attributeVal = webpageControl.getElementAttribute("paragraph", "title")
        if attributeVal == "a paragraph to test attributes on":
            self.log.stepResult(True, "Attribute was as expected")
        else:
            self.log.stepResult(False, "Attribute was not as expected")




if __name__ == "__main__":
    test = elementAttributeTest()

    
