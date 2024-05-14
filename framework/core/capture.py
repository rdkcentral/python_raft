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
#*   ** @date        : 03/04/2022
#*   **
#*   ** @brief : ocr capture module 
#*   **
#* ******************************************************************************

import cv2, os
from datetime import datetime, timedelta
from pytesseract import pytesseract
from PIL import Image, ImageFilter
from framework.core.utilities import utilities as utils
from framework.core.logModule import logModule

class capture(utils):
    def __init__(self, log:logModule, captureImagesPath:str, ocrEnginePath:str, resolution:str, input:str, **kwargs:dict):
        """Initialise the OCR capture engine

        Args:
            log (logModule): logging module
            captureImagesPath (str): output capture images path
            ocrEnginePath (str): ocr binary path
            resolution (str): input resolution
            input (str): input number for capture
        """
        utils.__init__(self, log)
        self.log = log
        self.resolution = resolution
        self.captureImagesPath = captureImagesPath
        self.ocrEnginePath = ocrEnginePath
        self.captureInput = input
        self.captureImagesCount = 1
        self.videoApi = None
        self.regionDetails = None
        self.screenRegions = None

    def setRegions( self, regionsConfig:dict ):
        """Set the capture regions dictionary to operate with

        Args:
            regionsConfig (dict): capture regions dictionary
        """
        self.screenRegions = regionsConfig

    def start(self):
        """Initialise capturing video output from capture card
        """
        self.log.info("capture.initaliseVideoCapture")
        try:
            self.log.step("Initializing OCR Engine. This may take upto 60secs..,")
            pytesseract.tesseract_cmd = r"{}".format(self.ocrEnginePath)
            self.videoApi = cv2.VideoCapture(int(self.captureInput))
        except Exception as e:
            self.log.error(e)
            raise Exception('Failed to start Video Capture')

        # set Frame resolution to self.resolution
        if self.resolution == '1080p':
            self.videoApi.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.videoApi.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        elif self.resolution == '720p':
            self.videoApi.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.videoApi.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        else:
            self.log.error('UNSUPPORTED Video Resolution')
        self.log.info("Frame resolution set as: " + str(self.videoApi.get(cv2.CAP_PROP_FRAME_WIDTH))+ " x " +str(self.videoApi.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return True

    def stop(self):
        """Stop videocapture and release the resources
        """
        self.videoApi.release()
        cv2.destroyAllWindows()
        self.log.info("Successfully released Video capture resources")
        return True

    def startImageCapture(self):
        """Capture current video frame from video input and return a PIL Image
        """
        self.log.info("capture.startImageCapture")
        _, frame = self.videoApi.read()
        imgPath = os.path.join(self.captureImagesPath, "image{}.png".format(self.captureImagesCount))
        cv2.imwrite(imgPath, frame)
        image = Image.open(imgPath)
        self.captureImagesCount += 1
        return image

    def getRegionCoords(self, regionName):
        """Get region co ordinates and ocr filters for the given region name

        Args:
            regionName (str) - Name of the region

        Returns:
            regionsDict (dict) - Dictionary of region co-ordinates and filters
            Ex: regionsDict = {co_ords: (730, 410, 1155, 650), filters: "None"}
        """
        self.log.info("capture.getRegionCoords for - {}".format(regionName))
        regionsDict = {}
        for k, v in self.screenRegions.items():
            if k == regionName:
                for key, val in v.items():
                    if key == 'co_ords':
                        regionsDict[key] = eval(val)
                    else:
                        regionsDict[key] = val

        return regionsDict

    def applyOcrImageFilter(self, inputImage, filterName):
        """Applied ocr filters on the input image

        Args:
            inputImage (PIL Image)
            filterName (str) - Filter to be applied on the image

        Returns:
            outputImage (PIL Image)            
        """
        self.log.info('capture.applyOcrImageFilter - {}'.format(filterName))
        if filterName == 'edge_enhance':
            outputImage = inputImage.filter(ImageFilter.EDGE_ENHANCE)
        elif filterName == 'gaussian_blur':
            outputImage = inputImage.filter(ImageFilter.GaussianBlur)
        elif filterName == 'smooth':
            outputImage = inputImage.filter(ImageFilter.SMOOTH)
        elif filterName == 'edge_enhance_more':
            outputImage = inputImage.filter(ImageFilter.EDGE_ENHANCE_MORE)
        elif filterName == 'None':
            return inputImage
        else:
            self.log.info('Invalid OCR filter - {}'.format(filterName))
        return outputImage

    def __getOCRText__(self, regionName):
        """Get text from device screen video output

        Args:
            regionName (str) - refer screen_regions.yml

        Returns:
            ocrText (str) - Text extracted from the screen region
        """
        self.log.info("capture.getOCRText")
        image = self.startImageCapture()
        self.regionDetails = self.getRegionCoords(regionName)
        croppedImage = image.crop(self.regionDetails['co_ords'])
        if self.regionDetails['filters'] != 'None':
            croppedImage = self.applyOcrImageFilter(croppedImage, self.regionDetails['filters'])
        ocrText = pytesseract.image_to_string(croppedImage)
        self.log.info(ocrText)
        return ocrText

    def checkOcrText(self, regionName, expectedText=""):
        """Check expected text against the OCRed text from screen for given region and return the result

        Args:
            expectedText (str) - Expected text on the screen
            regionName (str) - stb screen region (refer screen_regions.yml)

        Returns:
            result (boolean)
        """
        self.log.info("capture.checkOcrText")
        ocrText = self.__getOCRText__(regionName)
        if expectedText == "": # If script didn't send expectedText then check the platforms screen_regions.yml
            if self.regionDetails['ocr_text']:
                expectedText = self.regionDetails['ocr_text']
        if expectedText == "":
            self.log.error('Please pass expectedText for OCR region - {}'.format(regionName))
            raise Exception('ExpectedText is missing')
        result = self.fuzzyCompareText(expectedText, ocrText)
        return result

    def waitForDisplayedScreen(self, regionName, waitBetweenChecks=1, maxWaitTime=10):
        """Wait until a screen is displayed on the device

        Args:
            regionName (str) - Region where text is expected on the screen
            expectedText (str) - Expected text on the screen. If empty, uses ocr_text of regionName from xx.xx.screen_regions.yml
            waitBetweenChecks (int) - Wait in secs after every check
            maxWaitTime (int) - Maximum wait time to check for the expected screen

        Returns:
            result (bool)
        """
        self.log.info("capture.waitForDisplayedScreen - {}".format(regionName))
        result = False
        currentTime = datetime.now()
        waitUntil = currentTime+timedelta(seconds=maxWaitTime)
        self.log.info("Waiting until - {}".format(waitUntil))
        while currentTime < waitUntil:
            result = self.checkOcrText(regionName)
            if result:
                break
            self.wait(waitBetweenChecks)
            currentTime = datetime.now()
        resultLog = 'Screen was NOT displayed'
        if result:
            resultLog = 'Screen displayed at - {}'.format(currentTime)
        self.log.info(resultLog)
        return result
