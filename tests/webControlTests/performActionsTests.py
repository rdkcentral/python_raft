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

class performActionsTests(testController):
    def __init__(self, testName="performActionTests", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):
        webpageControl = self.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        webpageControl.navigateTo("form_page")

        self.log.stepStart("Starting action fill_form")
        webpageControl.performAction("fill_form",
            password="password123",
            path=os.path.abspath("unitTests/framework/webControlTests/mockUploadFile.txt"),
            multi_1="Selection Item 2",
            multi_2="Selection Item 4",
            dropdown="Drop Down Item 6")
        self.log.stepResult(True, "Finished action fill_form")

        print(webpageControl.webDriver.browser.current_url)

        webpageControl.setWebpage("form_results_page")

        self.log.stepStart("Checking username")
        username = webpageControl.getTextOfElement("username_value")
        if username != 'admin':
            self.log.stepResult(False, "Username did not match input of form")
        else:    
            self.log.stepResult(True, "Username did match input of form")

        self.log.stepStart("Checking password")
        password = webpageControl.getTextOfElement("password_value")
        if password != 'password123':
            self.log.stepResult(False, "Password did not match input of form")
        else:
            self.log.stepResult(True, "Password did match input of form")

        self.log.stepStart("Checking filename")
        filename = webpageControl.getTextOfElement("filename_value")
        if filename != 'mockUploadFile.txt':
            self.log.stepResult(False, "Filename did not match input of form")
        else:
            self.log.stepResult(True, "Filename did match input of form")

        self.log.stepStart("Checking checkbox 2")
        checkbox = webpageControl.getTextOfElement("checkbox_1_value")
        if checkbox != 'cb2':
            self.log.stepResult(False, "Checkbox did not match input of form")
        else:
            self.log.stepResult(True, "Checkbox did match input of form")
    
        self.log.stepStart("Checking checkbox 3")
        checkbox = webpageControl.getTextOfElement("checkbox_2_value")
        if checkbox != 'cb3':
            self.log.stepResult(False, "Checkbox did not match input of form")
        else:
            self.log.stepResult(True, "Checkbox did match input of form")

        self.log.stepStart("Checking radio button")
        radioButton = webpageControl.getTextOfElement("radio_button_value")
        if radioButton != 'rd3':
            self.log.stepResult(False, "Radio button did not match input of form")
        else:
            self.log.stepResult(True, "Radio button did match input of form")

        self.log.stepStart("Checking multiselect 1")
        multiSelect = webpageControl.getTextOfElement("multiselect_1_value")
        if multiSelect != 'ms2':
            self.log.stepResult(False, "Multiselect did not match input of form")
        else:
            self.log.stepResult(True, "Multiselect did match input of form")

        self.log.stepStart("Checking multiselect 2")
        multiSelect = webpageControl.getTextOfElement("multiselect_2_value")
        if multiSelect != 'ms4':
            self.log.stepResult(False, "Multiselect did not match input of form")
        else:
            self.log.stepResult(True, "Multiselect did match input of form")

        self.log.stepStart("Checking dropdown")
        dropdown = webpageControl.getTextOfElement("dropdown_value")
        if dropdown != 'dd6':
            self.log.stepResult(False, "Dropdown did not match input of form")
        else:
            self.log.stepResult(True, "Dropdown did match input of form")

if __name__ == "__main__":
    test = performActionsTests()

    
