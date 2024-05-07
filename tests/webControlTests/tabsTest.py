#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2023 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *
# http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *
#* ******************************************************************************

import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.testControl import testController

class tabsTest(testController):
    def __init__(self, testName="tabsTest", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):  
        testClass = self
        webpageControl = testClass.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        self.log.stepStart("Navigating to test_locatorPage on first tab and checking contents of elements")
        webpageControl.navigateTo("test_locator")

        paragraphA = webpageControl.getTextOfElement("paragraph_a_XPATH")

        if paragraphA == "This is a paragraph text":
            self.log.stepResult(True, "Content of element was as expected")
        else:
            self.log.stepResult(False, "Content of element was not as expected")

        self.log.stepStart("Creating new tab and navigating to attributes page")

        altWebpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTestAlternative.yml")
        webpageControl.createNewTab("tab2", "https://testpages.herokuapp.com", altWebpageConfig)
        webpageControl.navigateTo("attributes_page")   

        attributesParagraph = self.webpageController.getTextOfElement("paragraph")

        if attributesParagraph == "This paragraph has attributes":
            self.log.stepResult(True, "Content of element was as expected")
        else:
            self.log.stepResult(False, "Content of element was not as expected")

        self.log.stepStart("Returning to orignal tab and checking if it is on correct page")

        webpageControl.switchTab("default")
        paragraphA = webpageControl.getTextOfElement("paragraph_a_XPATH")

        if paragraphA == "This is a paragraph text":
            self.log.stepResult(True, "Content of element was as expected")
        else:
            self.log.stepResult(False, "Content of element was not as expected")

        self.log.stepStart("Navigating to another webpage and checking if on correct page")

        webpageControl.navigateTo("index_page")
        linkText = webpageControl.getTextOfElement("link_to_redirect_page")

        if linkText == "Redirect (JavaScript) Test Page":
            self.log.stepResult(True, "Content of element was as expected")
        else:
            self.log.stepResult(False, "Content of element wsa not as expected")

        self.log.stepStart("Switching tabs and expecting to still be on the same page")

        webpageControl.switchTab("tab2")

        attributesParagraph = self.webpageController.getTextOfElement("paragraph")

        if attributesParagraph == "This paragraph has attributes":
            self.log.stepResult(True, "Content of element was as expected")
        else:
            self.log.stepResult(False, "Content of element was not as expected")

        self.log.stepStart("Checking the tabs are all named as expected")

        tabs = list(webpageControl.getTabs())
        if tabs == ["default", "tab2"]:
            self.log.stepResult(True, "Tabs were named as expected")
        else:
            self.log.stepResult(False, "Tabs were not named as expected")
            





    

    

if __name__ == "__main__":
    test = tabsTest()

    
