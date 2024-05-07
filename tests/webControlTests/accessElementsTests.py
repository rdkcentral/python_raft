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

class accessElementsTest(testController):
    def __init__(self, testName="accessElementsTest", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):
        testClass = self
        webpageControl = testClass.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        webpageControl.navigateTo("test_locator")

        testClass.log.stepStart("Get element by XPATH")
        paragraphA = webpageControl.getTextOfElement("paragraph_a_XPATH")
        if paragraphA != "This is a paragraph text":
            testClass.log.stepResult(False, "Text of element did not match expected text")
        else:
            testClass.log.stepResult(True, "Text of element did match expected text")

        testClass.log.stepStart("Get element by ID")
        paragraphA = webpageControl.getTextOfElement("paragraph_a_ID")
        if paragraphA != "This is a paragraph text":
            testClass.log.stepResult(False, "Text of element did not match expected text")
        else:
            testClass.log.stepResult(True, "Text of element did match expected text")

        testClass.log.stepStart("Get element by NAME")
        paragraphA = webpageControl.getTextOfElement("paragraph_a_NAME")
        if paragraphA != "This is a paragraph text":
            testClass.log.stepResult(False, "Text of element did not match expected text")
        else:
            testClass.log.stepResult(True, "Text of element did match expected text")

        testClass.log.stepStart("Get element by CLASS_NAME")
        paragraphA = webpageControl.getTextOfElement("paragraph_a_CLASS_NAME")
        if paragraphA != "This is a paragraph text":
            testClass.log.stepResult(False, "Text of element did not match expected text")
        else:
            testClass.log.stepResult(True, "Text of element did match expected text")

        testClass.log.stepStart("Get element by TAG_NAME")
        paragraphA = webpageControl.getTextOfElement("paragraph_a_TAG_NAME")
        if paragraphA != "This is a paragraph text":
            testClass.log.stepResult(False, "Text of element did not match expected text")
        else:
            testClass.log.stepResult(True, "Text of element did match expected text")


    

if __name__ == "__main__":
    test = accessElementsTest()

    
