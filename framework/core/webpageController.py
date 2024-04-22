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
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @file        : webpageControl.py
#*   ** @date        : 13/04/2022
#*   **
#*   ** @brief : webpage control method to web page interaction
#*   **
#* ******************************************************************************

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

from framework.core.webpageModules.seleniumDriver import seleniumDriver

class webpageController():

    def __init__(self, log, webDriverConfig, baseUrl = None, webpageConfig = None):
        """
        Initializes a WebpageController instance.

        Args:
            log (logModule): The log module instance.
            webDriverConfig (dict): Configuration for the web driver.
            baseUrl (str, optional): The base URL to navigate to the pages. Defaults to None.
            webpageConfig (dict, optional): Configuration containing the pages. Defaults to None.
        """
        self._pages = None
        self.webDriver = None
        self.log = log

        if not os.path.exists(f"{log.logPath}browser"):
            os.mkdir(f"{log.logPath}browser")

        if webDriverConfig == None:
            return

        if webDriverConfig.get("controlType") == "selenium":
            self.webDriver = seleniumDriver(log, webDriverConfig)

        if webpageConfig:
            self._setWebpageConfig(webpageConfig)

        if baseUrl:
            self._setBaseUrl(baseUrl)

        self.currentTab = "default"
        self.currentPage = None
        self.currentPageName = None
        self.currentView = None
        self.defaultView = None
        self.tabs = {}

    def _setBaseUrl(self, baseUrl):
        """Sets the base url for the controller to use.

        Args:
            base_url (str): Base url to navigate to the pages.
        """
        if "http://" in baseUrl or "https://" in baseUrl:
            self.url = baseUrl
        else:
            self.url = "http://" + baseUrl

    def _setWebpageConfig(self, webpageConfig): 
        """
        Sets the pages that the webpage controller has access to from the webpage config.

        Args:
            webpageConfig (dict): Dictionary config containing the pages.
        """
        self.webpageConfig = webpageConfig
        self._pages = webpageConfig.get("pages")
        self.globalActions = webpageConfig.get("global_actions")

    def configureWebpages(self, baseUrl, webpageConfig):  
        """
        Sets the webpage base url as well as the webpage config if they were not set in the constructor.

        Args:
            base_url (str): Base url to navigate to the pages.
            webpageConfig (dict): Dictionary config containing the pages.
        """
        self._setBaseUrl(baseUrl)
        self._setWebpageConfig(webpageConfig)

    def setWebpage(self, pageName):
        """Tells the controller that the browser is on a different page than what is set in the controller. For use after a redirect.

        Args:
            pageName (str): Name of the page that the browser is now on.
        """
        self.tabs[self.currentTab] = {"pageName":pageName, "windowId":self._getwindowId(), "baseUrl": self.url, "webpageConfig":self.webpageConfig}
        if not pageName:
            self.currentPage = None
            self.currentPageName = None
            return
        page = self._getPage(pageName)
        self.removeTemporaryWebElements()
        self.currentPage = page
        self.currentPageName = pageName
        if page.get("views"):
            self.defaultView = page.get("views").get("default")
        else:
            self.defaultView = None
            self.currentView = None
        
        self._validateView()

    def _isConfigured(self):
        """Checks that the controller is configured with a url and dictionary of pages.

        Raises:
            Exception: If not configured.
        """
        if not self.url and self._pages:
            raise Exception("Base url and / or webpageConfig not configured in webpageController")

    def _isOnPage(self):
        """Checks that the controller is on a page.

        Raises:
            Exception: If not on a page.
        """
        if not self.currentPage:
            raise Exception("No page has been navigated too")


    def navigateTo(self, pageName):
        """
        Navigates to the pageName specified based on the pages config. Then checks that the expected elements are present.

        Args:
            pageName (str): Name of the page to navigate to based on a key in the pages config.
        """
        self._isConfigured()
        self.removeTemporaryWebElements()
        page = self._getPage(pageName)
        self.log.debug("Navigating to page '" + pageName + "' and checking elements")
        urlExtension = page.get("url_extension")

        if urlExtension:
            self.webDriver.navigateTo(self.url + page.get("url_extension"))
        else:
            navigationSequence = page.get("sequence")
            if navigationSequence is None:
                raise Exception("No url extension or sequence to navigate to page: " + pageName)
            self._navigateSequence(navigationSequence)

        self.setWebpage(pageName)

    def _navigateSequence(self, sequence):
        """
        Navigates through a sequence that is passed in.

        Args:
            sequence (dict): A dictionary containing the webpage to navigate to and sequence of interactions within that webpage to perform.
        """
        for page, action in sequence.items():
            self.navigateTo(page)
            self.performAction(action)


    def _checkElements(self, elements):
        """
        Checks that the browser has all of the elements expected based on the current page.

        Raises:
            Exception: If the webpageController does not have a current page.
        """
        if not self.currentPage:
            raise Exception("Not on a page to check elements for")

        notFound = []
        for name, element  in elements.items():
            try:
                self.webDriver.waitForElement(element)
                self.log.debug("Found element " + name)
            except:
                self.log.debug(f"Could not find element '{name}'")
                notFound.append((name, element))

        if notFound.__len__() > 0:
            error = f"Elements: '{repr(notFound)}' could not be found in page: '{self.currentPageName}'"
            self.log.error(error)
            raise Exception(error)

        self.log.info("All elements found for page: " + self.currentPageName)


    def _validateView(self, viewName = "default"):
        """Validates all the elements in the view. If no views exist will validate all elements on page

        Args:
            viewName (str, optional): The name of the view to validate. Defaults to "default".

        Raises:
            Exception: If the view doesn't exist for the page.
        """
        views = self.currentPage.get("views")
        if views:
            view = views.get(viewName)
            if view is None:
                error = f"View: '{viewName}' could not be found in page: '{self.currentPageName}'"
                self.log.error(error)
                raise Exception(error)
        else:
            view = self.currentPage

        elements = {}
        for elementName in view.get("elements"):
            elements[elementName] = self._getElement(elementName)
                    
        self._checkElements(elements)

    def _getPage(self, pageName):
        """
        Gets the page based on the page name

        Args:
            pageName (str): Page name based on a webpage config keys.

        Raises:
            Exception: If page name does not match any of those in the associated webpage config.

        Returns:
            dict: A dictionary representing the page.
        """
        page = self.pages.get(pageName)
        if not page:
            raise Exception("Page:" + pageName + " is not a valid page in the webpage config")
        return page

    def _getElement(self, elementName):
        """
        Gets an element based on the element name from the current page.

        Args:
            elementName (str): Name of the element to get.

        Raises:
            Exception: If the element name does not match any of those for the current page.

        Returns:
            dict: A dictionary representing the element.
        """
        self._isOnPage()
        element = self.currentPage.get("elements").get(elementName)
        if not element:
            error = "Element '" + elementName + "' is not a valid element for page '" + self.currentPageName + "'"
            self.log.error(error)
            raise Exception(error)

        if self.defaultView:
            if elementName in self.defaultView.get("elements"):
                return element

            viewName = self._getViewForElement(elementName)
            view = self._getView(viewName)
            if self.currentView != view and self.defaultView != view:
                self._activateView(viewName)

        return element

    def _getViewForElement(self, elementName):
        """Gets the name of the first view that the element belongs to.

        Args:
            elementName (str): Name of element.

        Raises:
            Exception: If element does not belong to any view.

        Returns:
            str: Name of view.
        """
        views = self.currentPage.get("views")
        for viewName, viewContent in views.items():
            if elementName in viewContent.get("elements"):
                return viewName
        error = "Element '" + elementName + "' is not a valid element for any view on page '" + self.currentPageName + "'"
        self.log.error(error)
        raise Exception(error)

    def _getView(self, viewName):
        """Returns the config for the view.

        Args:
            viewName (str): Name of view from the config.

        Raises:
            Exception: If page contains no views.
            Exception: If view does not exist for page.

        Returns:
            dict: Dictionary of the view's elements and sequence to activate it. 
        """
        views = self.currentPage.get("views")
        if views is None:
            error = f"Cannot get view '{viewName}' for page '{self.currentPageName}' as no views exist on it"
            self.log.error(error)
            raise Exception(error)
        view = views.get(viewName)
        if view is None:
            error = f"View '{viewName}' is not a valid view for page '{self.currentPageName}'"
            self.log.error(error)
            raise Exception(error)
        return view

    def _activateView(self, viewName):
        """Activates a view based on the view name passed.

        Args:
            viewName (str): Name of view from config.
        """
        self.log.info(f"Activating view '{viewName}'")
        view = self._getView(viewName)
        sequence = view.get("sequence")
        if sequence:
            self.performAction(sequence)
        self.currentView = view
        self._validateView(viewName)

    def _getAction(self, actionName):
        """
        Gets an action based on the action name from the current page.

        Args:
            actionName (str): Name of the action to get.

        Raises:
            Exception: If the action name does not match any of those for the current page.

        Returns:
            dict: A dictionary representing the action.
        """
        self._isOnPage()
        action = self.currentPage.get("actions").get(actionName)
        if not action:
            raise Exception("Action: " + actionName + " is not a valid action for page: " + self.currentPageName)
        return action

    @property
    def pages(self):
        """Gets the dictionary of the pages that the webpage config has provided.

        Returns:
            dict: Dictionary of the pages that the webpage config has provided.
        """
        return self._pages.copy()

    def performAction(self, actionName, **kwargs):
        """
        Performs the action that is passed in action name, any additional arguments are subbed into any args values starting with $.

        Args:
            actionName (str): The name of the action to perform.
        """
        action = self._getAction(actionName)
        for interactions in action:
            for interactionType, interactionVars in interactions.items():
                args = None
                elementName = None

                if  interactionVars:
                    if interactionVars.get("args"):
                        args = self._interactionArgsSub(interactionVars.get("args"), kwargs)
                    if interactionVars.get("element"):
                        elementName = interactionVars.get("element")
                self.performInteraction(interactionType, elementName, args)

    def getTextOfElement(self, elementName):
        """
        Gets the text content of a specified element on the webpage.

        Args:
            elementName (str): The name of the element to get text from.

        Returns:
            str: The text content of the specified element.
        """
        return self.webDriver.getText(self._getElement(elementName))


    def performInteraction(self, interactionName, elementName=None, args=None):
        """
        Performs a single interaction with the browser based on the type passed.

        Args:
            interaction (str): The interaction to perform.
            args (dict): Any arguments to substitute into the interaction.
        """ 
        debugInfo = f"Performing interaction '{interactionName}'"
        if elementName:
            debugInfo = debugInfo + f" on element '{elementName}'"
            element = self._getElement(elementName)
        if args:
            debugInfo = debugInfo + f" with args '{repr(args)}'"

        self.log.debug(debugInfo)

        if interactionName == "send_keys":
            self.webDriver.sendKeys(element, args.get("keys"))
        elif interactionName == "click":
            self.webDriver.click(element)
        elif interactionName == "accept_alert":
            self.webDriver.acceptAlert()
        elif interactionName == "clear":
            self.webDriver.clear(element)
        elif interactionName == "refresh":
            self.log.info("Refreshing and checking elements on page: " + self.currentPageName)
            self.webDriver.refresh()
            self.removeTemporaryWebElements()
            self._validateView()
        elif interactionName == "select":
            self.webDriver.selectFromDropdown(element, args.get("selectVal"))
        elif interactionName == "dismiss_alert":
            self.webDriver.dismissAlert()
        
        
    def _interactionArgsSub(self, interactionArgs, args):
        """
        Substitutes in any arguments passed in args into interactionArgs based on any args in interactionArgs starting with $.

        Example:
        interactionArgs = ["admin","$password"]
        args = {password:"superSecretPassword98"}

        returns = ["admin","superSecretPassword98"]

        Args:
            interactionArgs (dict): Dictionary of arguments with potential arguments needing to be substituted
            args (dict): _description_

        Returns:
            list: List of arguments
        """
        newArgs = {}
        for key, arg in interactionArgs.items():
            subVal = arg
            if arg[0] == '$':
                subVal = args.get(arg[1:])
                if not subVal:
                    error = "Did not pass an argument to substitute arg '" + arg + "'. Passed args are: " + repr(args)
                    self.log.error(error)
                    raise Exception(error)
            newArgs[key] = subVal
        return newArgs

    def performGlobalAction(self, globalActionName, **kwargs):
        """Performs a global action.

        Args:
            globalActionName (String): Name of the action to perform.
            kwargs: Variable number of optional arguments for the actions.

        Raises:
            Exception: If webpage config does not contain any global action.
        """
        if not self.globalActions:
            raise Exception("Webpage config does not contain global actions")
        
        globalAction = self.globalActions.get(globalActionName)


        for action in globalAction:
            for page, actionName in action.items():
                self.navigateTo(page)
                self.performAction(actionName, **kwargs)


    def getElementAttribute(self, elementName, attributeName):
        """Gets the value of the element attribute specified.

        Args:
            elementName (String): Name of element.
            attributeName (String): Name of attribute.

        Returns:
            String: Value of attribute.
        """
        return self.webDriver.getElementAttribute(self._getElement(elementName), attributeName)

    def isElementSelected(self, elementName):
        """Returns whether the element is selected or not. 

        Args:
            elementName (String): Name of element.

        Returns:
            Boolean: Whether the element is selected or not.
        """
        return self.webDriver.isElementSelected(self._getElement(elementName))

    def getSelectedOptions(self, elementName):
        """Gets all of the options of the select element that are currently selected.

        Args:
            elementName (String): Name of element.

        Returns:
            List of Strings: Text content of the elements that are selected.
        """
        return self.webDriver.getSelectedOptions(self._getElement(elementName))

    def getFirstSelectedOption(self, elementName):
        """Gets the first option that is selected.

        Args:
            elementName (String): Name of element.

        Returns:
            Strings: Text content of the first element selected.
        """
        return self.webDriver.getFirstSelectedOption(self._getElement(elementName))

    def getSelectAvailableOptions(self, elementName):
        """Gets the list of all of the available options that could be selected.

        Args:
            elementName (String): Name of element.

        Returns:
            List of Strings: Text content of all elements that could be selected.
        """
        return self.webDriver.getSelectAvailableOptions(self._getElement(elementName))

    def getUrl(self):
        """Gets the url of the current webpage open.

        Returns:
            String: Url of the webpage that is open.
        """
        return self.webDriver.browser.current_url  

    def getAlertText(self):
        """Gets the text of an open web alert box.

        Returns:
            String: Content of the alert box if it is open, None otherwise.
        """
        return self.webDriver.getAlertText()

    def closeBrowser(self):
        """Ends webdriver session and closes browser.
        """
        self.log.debug("Closing the browser")
        if self.webDriver != None:
            self.webDriver.browser.close()

    def saveScreenshot(self, fileName):
        """Saves a screenshot of the current browser view to the fileName specified the tests log folder.

        Args:
            fileName (String): The fileName to save the screenshot to. It will be saved as a .png file.
        """

        self.log.debug(f"Saving screenshot to {self.log.logPath}browser/{fileName}.png")
        self.webDriver.saveScreenshot(f"{self.log.logPath}browser/", fileName)

    def saveHtmlSnapshot(self, fileName):
        """Saves a copy of the html of the current page the webpageController is on to the test log folder.

        Args:
            fileName (String): The fileName to save the html to.
        """
        self.log.debug(f"Saving html snapshot to {self.log.logPath}browser/{fileName}.html")
        with open(f'{self.log.logPath}browser/{fileName}.html', 'w') as f:
            f.write(self.webDriver.getHtml())
    
    def getDynamicTable(self, elementName, text = None):
        """Gets the  elements of the table as a list of lists.

        Args:
            elementName (String):  dynamic table name.
            text(bool): Text attribute indicator of the web element. Set to True to retrieve text attribute of the webelement, defaults to None.
        Returns:
            list: list of list of dictionaries with element details.
        """
        
        #Remove temporary dynamic elements if already present in current page elements dictionary
        self.removeTemporaryWebElements()
        
        element = self._getElement(elementName)
        if element["dynamic_element"]:
            tableData = self.webDriver.getTableElements(element, elementName, text)
        else:
            raise TypeError ("Expecting a dynamic web element")

        #Adding dynamic table cell elements to the current page 'elements' dictionary
        for row in tableData:
            for column in row:
                self.currentPage["elements"][column["elementName"]] = column
                     
        return tableData
    

    def getDynamicTableText(self, elementName):
        """Gets the text of elements in the table as a list of list of dictionaries, with corresponding element details.

        Args:
            elementName (String): dynamic table name.

        Returns:
            list:  list of list of dictionaries with element details - type, value, text, elementName.
        """
        self.log.warn("METHOD getDynamicTableText() SOON TO BE DEPRECIATED DO NOT USE")
        return self.getDynamicTable(elementName, text = True)
    
    
    def removeTemporaryWebElements(self):
        """Removes  list of temporary elements added to page's elements dictionary.
        
        """  
        temporaryElementList = []
        if self.currentPage != None:
            for elementName, elementDict in self.currentPage["elements"].items():
                if elementDict.get("temporaryFlag"):
                    temporaryElementList.append(elementName)
            
            for tempElement in temporaryElementList:
                self.currentPage["elements"].pop(tempElement)
                    
    def createNewTab(self, tabName, baseUrl, webpageConfig):
        """Creates a new tab and switches the webpageController to that tab.

        Args:
            tabName (String): Name of the tab to create. Will be used to switch back to it.
            baseUrl (String): Base url for the webpage config.
            webpageConfig (Dict): A dictionary of the webpage config ymls.
        """
        self.log.info(f"Creating new tab {tabName} with baseUrl: {baseUrl}")
        self.webDriver.newTab()
        self.configureWebpages(baseUrl, webpageConfig)
        self.currentTab = tabName
        self.setWebpage(None)

    def switchTab(self, tabName):
        """Switches the browser and webpageController to the tab specified. The original tab is named `default`.

        Args:
            tabName (String): Name of the tab to switch to.
        """
        self.log.info(f"Switching to tab {tabName} from tab {self.currentTab}")
        tab = self.tabs.get(tabName)
        self.webDriver.switchTab(tab["windowId"])
        self.currentTab = tabName
        self.configureWebpages(tab["baseUrl"], tab["webpageConfig"])
        self.setWebpage(tab["pageName"])

    def getTabs(self):
        """Returns a list of the tab names that have been created.

        Returns:
            List(String): A list of tab names that have been created.
        """
        return list(self.tabs.keys())
    
    def getTab(self, tabName):
        """Gets a dictionary of the pageName and windowId of the tab specified by name.

        Args:
            tabName (String): Name of tab.

        Returns:
            Dict: A dictionary with `pageName` and `windowId` keys.
        """
        return self.tabs[tabName] 
    
    def _getwindowId(self):
        """Gets the window handle from the webDriver.

        Returns:
            String: windowId of the current window.
        """
        return self.webDriver.getWindowId()

    def getSubElements(self, elementName):
        """Returns a list of elementNames for the subElements of the element passed.

        Args:
            elementName (String): Name of element.

        Returns:
            list: A list of element names that will now be included in as temporary elements in the webpageControllers config.
            
        """
        element = self._getElement(elementName)
        listDicts = self.webDriver.getSubElements(element, elementName)
        listNames = []
        for subElement in listDicts:
            self.currentPage["elements"][subElement["elementName"]] = subElement
            listNames.append(subElement["elementName"])

        return listNames
        