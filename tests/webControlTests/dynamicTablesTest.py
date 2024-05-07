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
import json



# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.testControl import testController

class dynamicTablesTest(testController):
    def __init__(self, testName="dynamicTablesTest", log=None):
        super().__init__(testName=testName, log=log)
        self.run()

    def testFunction(self):
        webpageControl = self.webpageController

        webpageConfig = self.config.decodeConfigIntoDictionary("./unitTests/framework/webControlTests/webPageTest.yml")
        webpageControl.configureWebpages("https://testpages.herokuapp.com/styled", webpageConfig)

        webpageControl.navigateTo("dynamic_tables_page")
             
        self.log.stepStart("Display the text content of dynamic table")
        tableContent = webpageControl.getDynamicTableText("dynamic_table")
        tableContentText = []
        for row in range(0, len(tableContent)):
            tableContentText.append([])
            for column in range(0, len(tableContent[row])):
                tableContentText[row].append(tableContent[row][column]["text"])
                
        if len(tableContent) != 0:
            self.log.stepResult(True, f"Table data displayed successfully.  Table length: {len(tableContent)} Table text contents: {tableContentText}")
        else:
            self.log.stepResult(False, f"Table data not displayed successfully")
        
                                    
        self.log.stepStart("Verify that 'George' is the value in second row first column in the table")
        tableContent = webpageControl.getDynamicTableText("dynamic_table")
        if tableContent[2][0]["text"] == "George":
            self.log.stepResult(True, f"George is found at expected location - second row first column in the table")
        else:
            self.log.stepResult(False, f"George is not found at expected location -second row first column in the table")
           
            
        self.log.stepStart("Add new row to dynamic table")  
        inputRow = {}
        inputRow["name"] = "Zara"
        inputRow["age"] = 22
        
        #eval is creating a  list of dictionaries from the json
        tableElementValue = eval(webpageControl.getElementAttribute("text_area", "value"))
        #Append new dictionary item to existing one
        tableElementValue.append(inputRow)
        jsonInputString  = json.dumps(tableElementValue)
        
        #update the table input with new row
        webpageControl.performAction("update_table", input_row = jsonInputString)
        self.utils.wait(5)
        existingTableLength = len(tableContent)
        tableContent = webpageControl.getDynamicTableText("dynamic_table")
        newTableLength = len(tableContent)    
         
        if newTableLength > existingTableLength:
            self.log.stepResult(True, f"New row successfully added to the table. Table length - new : {newTableLength}, old : {existingTableLength}")
        else:
            self.log.stepResult(False, f"New row not  added to the table. Table length - new :{newTableLength} , old :{existingTableLength}")
        
        
        self.log.stepStart("Verify that 'Zara' is the value in third row first column in the table")
        tableContent = webpageControl.getDynamicTableText("dynamic_table")
        
        if tableContent[3][0]["text"] == "Zara":
            self.log.stepResult(True, f"Zara is found at expected location - third row first column in the table")
        else:
            self.log.stepResult(False, f"Zara is not found at expected location -third row first column in the table")
        
        
        self.log.stepStart("Verify the table length updates when page is refreshed")                 
        webpageControl.performAction("page_refresh")               
        tableContent = webpageControl.getDynamicTableText("dynamic_table")
        existingTableLength = newTableLength        
        newTableLength = len(tableContent)
        
        if newTableLength < existingTableLength :
            self.log.stepResult(True, f"Table refreshed successfully. Table length - new : {newTableLength}, old : {existingTableLength}")
        else:
            self.log.stepResult(False, f" Table refresh not successful. Table length - new :{newTableLength} , old :{existingTableLength}")
        
        
        ##navigation
        self.log.stepStart("Check if temporary elements are removed form the elements dictionary on navigating to another webpage")
        dynamicElements = webpageControl.getDynamicTable("dynamic_table")
        dynamicElementsList = self.getTemporaryElementList(webpageControl._getPage("dynamic_tables_page")["elements"])
                        
        webpageControl.navigateTo("dynamic_buttons_page")
        
        temporaryList = self.getTemporaryElementList(webpageControl._getPage("dynamic_tables_page")["elements"])
                        
        if dynamicElementsList != temporaryList and len(temporaryList) == 0 :
            self.log.stepResult(True, f"Temporary elements have been removed successfully. Temporary Elements before navigation :{dynamicElementsList}. Temporary Elements after navigation :{temporaryList}")
        else:
            self.log.stepResult(False, "Temporary elements  removal unsuccessful")
            
        ##Redirection   
        self.log.stepStart("Check if temporary elements are removed form the elements dictionary on redirecting to another webpage")
        webpageControl.navigateTo("dynamic_tables_page")
        dynamicElements = webpageControl.getDynamicTable("dynamic_table")
        
        dynamicElementsList = self.getTemporaryElementList(webpageControl._getPage("dynamic_tables_page")["elements"])
               
        webpageControl.performAction("return_to_index_page")
        webpageControl.setWebpage("index_page")
        temporaryList = self.getTemporaryElementList(webpageControl._getPage("dynamic_tables_page")["elements"])
                        
        if dynamicElementsList != temporaryList and len(temporaryList) == 0 :
            self.log.stepResult(True, f"Temporary elements have been removed successfully on redirection. Temporary Elements before redirection :{dynamicElementsList}. Temporary Elements after redirection :{temporaryList}")
        else:
            self.log.stepResult(False, "Temporary elements  removal unsuccessful")
        
        ##Refresh
        self.log.stepStart("Check if temporary elements are removed form the elements dictionary on page refresh")
        webpageControl.navigateTo("dynamic_tables_page")
        webpageControl.performAction("update_table", input_row = jsonInputString) ## adding back 3rd row
        dynamicElements = webpageControl.getDynamicTable("dynamic_table")
        dynamicElementsList = self.getTemporaryElementList(webpageControl._getPage("dynamic_tables_page")["elements"])
        
        webpageControl.performAction("page_refresh")
        dynamicElements = webpageControl.getDynamicTable("dynamic_table")
        temporaryList = self.getTemporaryElementList(webpageControl._getPage("dynamic_tables_page")["elements"])
                        
        if dynamicElementsList != temporaryList:
            self.log.stepResult(True, f"Temporary elements have been removed successfully on page refresh. Temporary Elements before refresh :{dynamicElementsList}. Temporary Elements after refresh :{temporaryList}")
        else:
            self.log.stepResult(False, "Temporary elements  removal unsuccessful")
    
    def getTemporaryElementList(self, pageElementDict):
        temporaryElementsList = []
        for elementName, elementDict in  pageElementDict.items():
            if  elementDict.get("temporaryFlag"):
                temporaryElementsList.append(elementName)
        
        return temporaryElementsList
        
        
if __name__ == "__main__":
    test = dynamicTablesTest()

    