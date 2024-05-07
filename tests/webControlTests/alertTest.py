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

class alertTest(testController):
    def __init__(self, testName="alertTest", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):
        testClass = self
        webpageControl = testClass.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        webpageControl.navigateTo("alerts_page")

        self.log.stepStart("Creating alert")
        webpageControl.performAction("create_alert")
        self.log.stepResult(True, "Alert created")

        self.log.stepStart("Reading content of alert")
        if webpageControl.getAlertText() == "I am an alert box!":
            self.log.stepResult(True, "Alert text matched what was expected")
        else:
            self.log.stepResult(False, "Alert text did not match what was expected")

        self.log.stepStart("Confirming alert")
        webpageControl.performAction("confirm_alert")
        self.log.stepResult(True, "Alert accepted")

        self.log.stepStart("Creating confirm alert")
        webpageControl.performAction("create_confirm_alert")
        self.log.stepResult(True, "Alert created")

        self.log.stepStart("Reading content of alert")
        if webpageControl.getAlertText() == "I am a confirm alert":
            self.log.stepResult(True, "Alert text matched what was expected")
        else:
            self.log.stepResult(False, "Alert text did not match what was expected")

        self.log.stepStart("Confirming alert")
        webpageControl.performAction("confirm_alert")
        self.log.stepResult(True, "Alert accepted")

        self.log.stepStart("Checking alert was confirmed")
        if webpageControl.getTextOfElement("confirm_result") == "true":
            self.log.stepResult(True, "Alert was confirmed")
        else:
            self.log.stepResult(False, "Alert was not confirmed")

        self.log.stepStart("Creating confirm alert")
        webpageControl.performAction("create_confirm_alert")
        self.log.stepResult(True, "Alert created")

        self.log.stepStart("Reading content of alert")
        if webpageControl.getAlertText() == "I am a confirm alert":
            self.log.stepResult(True, "Alert text matched what was expected")
        else:
            self.log.stepResult(False, "Alert text did not match what was expected")

        self.log.stepStart("Dismissing alert")
        webpageControl.performAction("dismiss_alert")
        self.log.stepResult(True, "Alert dismissed")

        self.log.stepStart("Checking alert was dismissed")
        if webpageControl.getTextOfElement("confirm_result") == "false":
            self.log.stepResult(True, "Alert was dismissed")
        else:
            self.log.stepResult(False, "Alert was not dismissed")



    

if __name__ == "__main__":
    test = alertTest()

    
