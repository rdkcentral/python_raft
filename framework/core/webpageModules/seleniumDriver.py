#!/usr/bin/env python3
import os
#** *****************************************************************************
#* Copyright (C) 2019 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.webpageModules
#*   ** @file        : webpageControl.py
#*   ** @date        : 13/04/2022
#*   **
#*   ** @brief : webdriver to support & wrap the selenium driver
#*   **
#* ******************************************************************************

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service

class seleniumDriver():
    def __init__(self, log, webDriverConfig):
        self.log = log
        self._setWebdriver(webDriverConfig)

    def _setWebdriver(self, webDriverConfig):
        """Provides the webDriver config to properly configure the selenium webdriver

        Args:
            webDriverConfig (dict): Dictionary containing appropriate config for selenium webdriver
        """
        options = Options()
        options.headless = True
        windowSize = webDriverConfig.get("windowSize")
        if windowSize == None:
            self.log.info("windowSize variable not set in web driver config, defaulting to 1920x1080")
            windowSize = "1920x1080"
        options.add_argument(f'window-size={windowSize}')
        webdriverDownloadPath = webDriverConfig.get("webdriverDownloadPath")
        if webdriverDownloadPath:
            downloadLocation = os.path.join(self.log.logPath, webdriverDownloadPath)
            if not os.path.exists(downloadLocation):
                os.makedirs(downloadLocation)
            chrome_prefs = {"download.default_directory": downloadLocation}
            options.experimental_options["prefs"] = chrome_prefs
            self.log.info(f"Set webdrive download path to {downloadLocation}")
        else:
            self.log.warn("No 'webdriverDownloadPath' found in config. Has not been set")
        if webDriverConfig.get('supportedBrowser') == 'chrome':
            webDriverLocation = webDriverConfig.get("webdriverLocation")
            if webDriverLocation:
                service = Service(executable_path= webDriverLocation)
                self.browser = webdriver.Chrome(service=service, options=options)
            else:
                self.browser = webdriver.Chrome(options=options)

        return 

    def navigateTo(self, url):
        """Naviagates to the url

        Args:
            url (str): The url to be navigated to
        """
        self.browser.get(url)
    
    def getElementType(self, elementType: str):
        """Gives the selenium element type based on the config type passed

        Args:
            elementType (str): The type of element in the config

        Returns:
            Selenium Element Type: _description_
        """
        elementTypes = {
            'LINK_TEXT' : By.LINK_TEXT,
            'XPATH' : By.XPATH,
            'CLASS_NAME' : By.CLASS_NAME,
            'NAME' : By.NAME,
            'ID' : By.ID,
            'TAG_NAME' : By.TAG_NAME,
            'PARTIAL_LINK_TEXT' : By.PARTIAL_LINK_TEXT
        }
        element = elementTypes.get(elementType)
        if element:
            return element
        self.log.error('routerPage.UNSUPPORTED browser element - {}'.format(elementType))


    def waitForElement(self, element, timeout = 10):
        """Wait for presence of element in the webpage

        Args:
            element ({type: str, value: str}): A dictionary containing a type and value, which can be used to determine the element in the webpage
        """
        elementType = self.getElementType(element.get("type"))
        elementValue = element.get("value")

        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((elementType, elementValue)))
        except:
            self.log.error("Element cannot be found")
            raise Exception("Element cannot be found")

    def sendKeys(self, element, keys):
        """Send keys to an element on the webpage

        Args:
            element ({type: str, value: str}): A dictionary containing a type and value, which can be used to determine the element in the webpage
            keys (str): The keys to be sent to the element
        """
        self._getElement(element).send_keys(keys)

    def click(self, element):
        """Click an element on the webpage (Ex: button, hyperlink)

        Args:
            element ({type: str, value: str}): A dictionary containing a type and value, which can be used to determine the element in the webpage
        """  
        self._getElement(element).click()
        return True

    def selectFromDropdown(self, element, value):
        """Selects a value from a element which represents a dropdown list

        Args:
            element ({type: str, value: str}): A dictionary containing a type and value, which can be used to determine the element in the webpage
            value (str): The option to select
        """
        select = Select(self._getElement(element))
        select.select_by_visible_text(value)

    def _getElement(self, element):
        """Gets an element object from the selenium webdriver based on the dict passed

        Args:
            element ({type: str, value: str}): A dictionary containing a type and value, which can be used to determine the element in the webpage
        
        Returns:
            WebElement 
        """
        elementType = self.getElementType(element.get("type"))
        elementValue = element.get("value")

        return self.browser.find_element(elementType, elementValue)

    def getText(self, element):
        return self._getElement(element).text

    def clear(self, element):
        """
        Resets the content of an element 

        Args:
            element ({type: str, value: str}): A dictionary containing a type and value, which can be used to determine the element in the webpage
        """
        self._getElement(element).clear()


    def acceptAlert(self):
        """Accepts an alert if one is present on the webpage
        """
        alert = Alert(self.browser)
        try:
            alert.accept()
        except:
            error = "Attempted to accept alert which does not exist"
            self.log.error(error)
            raise Exception(error)

    def refresh(self):
        """Refreshes the webpage
        """
        self.browser.refresh()

    def getElementAttribute(self, element, attribute):
        return self._getElement(element).get_attribute(attribute)

    def isElementSelected(self, element):
        return self._getElement(element).is_selected()

    def getSelectedOptions(self, element):
        select = Select(self._getElement(element))
        selectedOptions = []
        for ele in select.all_selected_options:
            selectedOptions.append(ele.text)
        return selectedOptions

    def getFirstSelectedOption(self, element):
        select = Select(self._getElement(element))
        return select.first_selected_option.text

    def getSelectAvailableOptions(self, element):
        select = Select(self._getElement(element))
        options = []
        for ele in select.options:
            options.append(ele.text)
        return options

    def getAlertText(self):
        alert = Alert(self.browser)
        try:
            return alert.text
        except:
            error = "Attempted to read alert which does not exist"
            self.log.error(error)
            return None
        
    def dismissAlert(self):
        alert = Alert(self.browser)
        try:
            return alert.dismiss()
        except:
            error = "Attempted to dismiss alert which does not exist"
            self.log.error(error)
            raise Exception(error)

    def saveScreenshot(self, directory, fileName):
        self.browser.save_screenshot(f"{directory}/{fileName}.png")

    def getHtml(self):
        return self.browser.page_source
        
    
    def getTableElements(self, element, elementName, text = None):
        """Gets the elements of dynamic table as a list of list of dictionaries 

        Args:
            element (dictionary): A dictionary representing the dynamic element
            elementName (string): Name of the dynamic element
            text (bool, optional): Text attribute indicator of the web element. Set to True to retreive text attribute of the webelement. Defaults to None.

        Returns:
            list: list of list of dictionaries with element details - element locator type, element locator value , text (if text=true)
        """
        elementTable = []
          
        table = self._getElement(element)
        rows = table.find_elements(By.XPATH, ".//tr")
        rowCount = 0
        for row in rows:
            tableRow = []
            tableColumns = [] 
            columnCount = 0
                      
            tableColumns += row.find_elements(By.TAG_NAME, "th")
            tableColumns  +=  row.find_elements(By.TAG_NAME, "td")
                        
            for cell in tableColumns:
                elementsName = f"{elementName}_r{rowCount}_c{columnCount}"
                elementLocatorType = "XPATH"
                temporaryFlag = True
                xpathValue = self.getXpath(cell)              
                tableRow.append(self._createElementsDictionary(elementName = elementsName, elementLocatorType = elementLocatorType, elementLocatorValue = xpathValue, temporaryFlag = temporaryFlag, text = text))
                columnCount = columnCount+1
                
            elementTable.append(tableRow)    
            rowCount = rowCount + 1
        
        return  elementTable

    def  getXpath(self, element):
        """Returns the xpath of a webelement
        """
        elementXpath = self.browser.execute_script(
            """function getAbsolutePath(element){
                if (element.tagName === 'HTML')
                  return '/HTML[1]';
                if (element === document.body) 
                  return '/HTML[1]/BODY[1]';
                var index = 0; 
                var siblings = element.parentNode.childNodes;
                for (var i = 0; i<siblings.length; i++)
                   { 
                    var sibling = siblings[i]; 
                    if (sibling === element) 
                      return getAbsolutePath(element.parentNode)+'/'+element.tagName+'['+(index+1)+']';
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) 
                      index++; 
                    } 
                } return getAbsolutePath(arguments[0]).toLowerCase();""", element)
        
        return elementXpath
    
    def _createElementsDictionary( self, elementName, elementLocatorType, elementLocatorValue, **kwargs):
        """Creates a dictonary of element's details

        Args:
            elementName (String): The name of the web element
            elementLocatorType (String): The locator type for the web element (Eg: XPATH, ID, TAG etc)
            elementLocatorValue (String): Actual value of the locator for the web element
            text (bool, optional): Text attribute indicator of the web element. Set to True to retreive text attribute of the webelement. Defaults to None.
            temporaryFlag(bool, optional) : Indicates if the webelement is temporary or not. Set to True for temporary element. Defaults to False.
        Returns:
            dict:  A dictionary representing the attributes of element
        """
        elementsDictionary = {}
        elementsDictionary["elementName"] = elementName
        elementsDictionary["type"] = elementLocatorType
        elementsDictionary["value"] = elementLocatorValue
        for key, value in kwargs.items():
            if key == 'text':
                elementsDictionary["text"] = self.getText(elementsDictionary)
            else:
                elementsDictionary[key] = value
            
        return elementsDictionary

    def newTab(self):
        """Creates a new tab on the selenium driver

        Returns:
            (String, String): A tuple of the original tab and the new tab window handles
            
        """
        originalTab = self.browser.current_window_handle
        self.browser.switch_to.new_window("tab")
        newTab = self.browser.current_window_handle
        return originalTab, newTab

    def switchTab(self, tab):
        """Switchs tab on the selenium driver

        Args:
            tab (String): Window handle for tab

        Returns:
            (String, String): A tuple of the original tab and the new tab window handles
            
        """
        originalTab = self.browser.current_window_handle
        self.browser.switch_to.window(tab)
        newTab = self.browser.current_window_handle
        return originalTab, newTab
    
    def getWindowId(self):
        """Gets the current window handle of the browser

        Returns:
            String: Window handle of the current tab/window
        """
        return self.browser.current_window_handle

    def getSubElements(self, element, elementName):
        webElement = self._getElement(element)
        subElements = webElement.find_elements(By.XPATH, "./child::*")
        subElementsList = []
        for count, subElement in enumerate(subElements):
            subElementName = f"{elementName}_e{count}"
            subElementValue = self.getXpath(subElement)

            subElementsList.append(self._createElementsDictionary(subElementName, "XPATH", subElementValue, temporaryFlag = True))

        return subElementsList