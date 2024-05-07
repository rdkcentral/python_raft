#! /bin/python3
import os
import sys



# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../../")

from framework.core.testControl import testController

class selectOptionsTests(testController):
    def __init__(self, testName="selectOptionsTests", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):
        webpageControl = self.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        webpageControl.navigateTo("form_page")

        self.log.stepStart("Getting selected options of dropdown")
        selected = webpageControl.getSelectedOptions("dropdown_select")
        if selected[0] == "Drop Down Item 3" and len(selected) == 1:
            self.log.stepResult(True, "First item was as expected and was only of length one")
        else:
            self.log.stepResult(False, "First item was not as expected and was not of expected length. Actual first item: " + selected[0] + " Actual length: " + len(selected))

        self.log.stepStart("Getting options of dropdown")
        options = webpageControl.getSelectAvailableOptions("dropdown_select")
        if len(options) == 6:
            self.log.stepResult(True, "Options are as expected")
        else:
            self.log.stepResult(False, "Options are not of expected length")

        self.webpageController.performInteraction("select", "multi_select", args = {"selectVal": "Selection Item 1"})
        self.webpageController.performInteraction("select", "multi_select", args = {"selectVal": "Selection Item 2"})

        self.log.stepStart("Getting selected options of multi select")
        selected = webpageControl.getSelectedOptions("multi_select")
        if selected[0] == "Selection Item 1" and selected[1] == "Selection Item 2" and selected[2] == "Selection Item 4" and len(selected) == 3:
            self.log.stepResult(True, "Selected items were as expected")
        else:
            self.log.stepResult(False, "Selected items were not as expected. Actual: " + repr(selected))

        self.log.stepStart("Seeing if checkbox 3 is selected")
        if webpageControl.isElementSelected("checkbox_3"):
            self.log.stepResult(True, "Checkbox was selected as expected")
        else:
            self.log.stepResult(False, "Checkbox was not selected when not expected to be")

        self.log.stepStart("Seeing if radiobutton 3 is selected")
        if webpageControl.isElementSelected("radio_button_3"):
            self.log.stepResult(False, "Radio button was selected when not expected to be")
        else:
            self.log.stepResult(True, "Radio button was not selected as expected")

if __name__ == "__main__":
    test = selectOptionsTests()

    
