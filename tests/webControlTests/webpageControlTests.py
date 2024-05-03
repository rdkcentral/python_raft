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

from cgi import test
import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.logModule import logModule
from unitTests.framework.webControlTests.accessElementsTests import accessElementsTest
from unitTests.framework.webControlTests.performActionsTests import performActionsTests
from unitTests.framework.webControlTests.dynamicButtonsTest import dynamicButtonsTest
from unitTests.framework.webControlTests.alertTest import alertTest
from unitTests.framework.webControlTests.sequenceTest import sequenceTest
from unitTests.framework.webControlTests.elementAttributeTest import elementAttributeTest
from unitTests.framework.webControlTests.selectOptionsTests import selectOptionsTests
from unitTests.framework.webControlTests.globalActionTest import globalActionTest
from unitTests.framework.webControlTests.downloadTest import downloadTest
from unitTests.framework.webControlTests.saveScreenshotTest import saveScreenshotTest
from unitTests.framework.webControlTests.dynamicTablesTest import dynamicTablesTest


    

if __name__ == "__main__":
    summary = logModule("WebpageControlTests", level=logModule.INFO)
    summary.testStart("WebpageControlTests", "1")

    accessElementsTest(log=summary)
    performActionsTests(log=summary)
    dynamicButtonsTest(log=summary)
    alertTest(log=summary)
    sequenceTest(log=summary)
    elementAttributeTest(log=summary)
    selectOptionsTests(log=summary)
    globalActionTest(log=summary)
    downloadTest(log=summary)
    saveScreenshotTest(log=summary)
    dynamicTablesTest(log=summary)