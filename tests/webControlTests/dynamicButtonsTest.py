#! /bin/python3
import os
import sys



# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../../")

from framework.core.testControl import testController

class dynamicButtonsTest(testController):
    def __init__(self, testName="dynamicButtonsTest", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):
        webpageControl = self.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        webpageControl.navigateTo("dynamic_buttons_page")

        self.log.stepStart("Getting button1 from view1")
        button = webpageControl.getTextOfElement("button1")
        if button != 'One':
            self.log.stepResult(False, "Button did not match input of form")
        else:    
            self.log.stepResult(True, "Button did match input of form")

        self.log.stepStart("Getting button2 from view2")
        button = webpageControl.getTextOfElement("button2")
        if button != 'Two':
            self.log.stepResult(False, "Button did not match input of form")
        else:    
            self.log.stepResult(True, "Button did match input of form")

        self.log.stepStart("Getting button3 from view3")
        button = webpageControl.getTextOfElement("button3")
        if button != 'Three':
            self.log.stepResult(False, "Button did not match input of form")
        else:    
            self.log.stepResult(True, "Button did match input of form")

        print(webpageControl.webDriver.browser.current_url)

if __name__ == "__main__":
    test = dynamicButtonsTest()

    
