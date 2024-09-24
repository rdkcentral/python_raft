#!/usr/bin/env python3
#/* *****************************************************************************
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
#*   ** @date        : 05/07/2021
#*   **
#*   ** @brief : outboundClient.py
#*   **
#*
#* ******************************************************************************/
import os
import sys
import re
import requests
import inspect
from paramiko import SSHClient
from fabric import Connection
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs

# Add the framework path to system
from framework.core.logModule import logModule as logModule

class outboundClientClass():

    def __init__(self, log:logModule=None, workspaceDirectory:str=None, upload_url:str=None, httpProxy:str="", **kwargs):
        """Initialize the class.

        Args:
            log (logModule, optional): Logging class from parent if required. Defaults to None.
            workspaceDirectory (str, optional): Local workspace folder to download files to. Defaults to None.
            upload_url (str, optional): Upload URL. Defaults to None.
            httpProxy (str, optional): HTTP proxy if required, used for downloading via HTTP. Defaults to "".
        """
        self.log = log
        self.logBase = False
        if log == None:
            self.log = logModule( "outboundClientClass" );
            self.logBase = True
        self.workspaceDirectory = workspaceDirectory
        if not os.path.isdir(workspaceDirectory):
            self.log.info('creating [{}]'.format(workspaceDirectory))
            os.mkdirdirs( workspaceDirectory, exist_ok=True )
        self.upload_url = upload_url
        self.uploadPath = ""
        self.httpProxy = httpProxy
        self.__configureUploadProtocol__( upload_url )
    
    def __del__(self):
        """Destructor method."""
        if self.logBase == True:
            self.log.log.removeHandler(self.log.log.handlers[0])

    def __configureUploadProtocol__(self, upload_url:str):
        """Configure the upload protocol if required.

        Args:
            upload_url (str): Upload folder including the protocol requirements.

        Returns:
            bool: True on success, otherwise False.
        """
        parse = urlparse( upload_url )
        if parse.scheme == "sftp":
            self.uploadPort = int(22) # Standard Port for ssh
            location = parse.path
        else:
            self.log.error("Unsupported Upload Folder Method [{}]".format(parse.scheme))
            return False

          # URL for xftp://servername:69/dir/filename.blah
        self.uploadAddress = parse.hostname
        if parse.port != None:
            self.uploadPort = parse.port
        self.uploadPath = parse.path

    def downloadFile(self, url:str, filename:str = None):
        """Download a file from the URL and save it to the workspace.

        Args:
            url (str): URL of the file to be downloaded.
            filename (str, optional): Optional name of the downloaded file.

        Returns:
            bool: True on success, otherwise False.
        """
        if not os.path.exists(self.workspaceDirectory):
            os.makedirs(self.workspaceDirectory)  # create folder if it does not exist

        if filename == None:
            filename = os.path.basename(url)
        file_path = os.path.join(self.workspaceDirectory, filename)

        if url.startswith("http://") == True:
            return self.__downloadHTTP__( url, filename )

        if url.startswith("sftp://") == True:
            return self.__downloadSFTP__( url, filename )

        self.log.error("Unsupported URL [{}]", url)
        return False

    def prepareOutboundWithImageFromUrl( self, imageType:str, url:str):
        """Program the given image name from the provided URL.

        Args:
            imageType (str): Type of image (e.g., 'image', 'PCI1', 'PCI2').
            url (str): URL for the source image (HTTP or SFTP).

        Returns:
            bool: True on success, otherwise False.
        """
        try:
            imageFilename = self.translateImageTypeToImageFilename( imageType )
            if self.downloadFile( url, imageFilename ) == False:
                self.log.error("Error downloading filename: [{}]".format(imageFilename))
                return False
            return self.uploadFile( imageFilename )
        except Exception as e:
            self.log.error('Exception occurred')
            self.log.error(e)
            raise Exception('Failed to prepareOutboundWithImageFromUrl - {} url {}'.format(imageType, url))

    def translateImageTypeToImageFilename(self, imageType:str):
        """Convert imageType to imageFilename.

        Args:
            imageType (str): Image type (e.g., 'PCI1', 'PCI2', 'PDRI', 'BDRI').

        Returns:
            str: Filename returned with extension.
        """

        imageFilename = imageType+".bin" 
        return imageFilename;

    def getSizeInHumanReadable(self, size:int):
        """Get size in human-readable form.

        Args:
            size (int): Size in bytes.

        Returns:
            str: Size string.
        """
        units = ['B', 'KB', 'MB', 'GB']
        index = 0
        size = int(size)
        while size >= 1024:
            size /= 1024
            index += 1
        return f'{size} {units[index]}'

    def __downloadSFTP__(self, url:str, filename:str=None ):
        """Download the given URL via SFTP protocol.

        Args:
            url (str): Source URL.
            filename (str, optional): Optional destination filename.

        Returns:
            bool: True on success, otherwise False.
        """
        parse = urlparse( url )
        port = int(22)
        if parse.port != None:
            port = parse.port
        try:
            ssh = Connection( parse.hostname, port=port)
        except Exception as e:
            self.log.error(str(e))
            return False

        location = parse.path

        filePath = self.workspaceDirectory
        if filename != None:
            filePath = filePath + os.path.basename(filename)
        self.log.info("SFTP Downloading url:[{}] to filename:[{}]".format(url, filePath))
        try:
            result = ssh.get(location, local=filePath)
        except Exception as e:
            self.log.error(str(e))
            return False
        return True

    def cleanWorkspace(self):
        """Clean the workspace folder."""
        self.log.info("Clean workspace folder [{}]")


    def __uploadSFTP__(self, filename:str):
        """Upload the specified file via sftp protocol
            Note: This function will create directories as required

        Args:
            filename ([str]): [filename from workspace]

        Returns:
            [bool]: [True - on success, otherwise False]
        """
        fileSize = os.path.getsize(filename)
        humanSize = self.getSizeInHumanReadable(fileSize)
        if fileSize == 0:
            self.log.info("SFTP Uploading Zero Length filename:[sftp://{}] Length:[{}] to Path:[{}]".format(filename, humanSize, self.uploadPath))
            return False
        self.log.info("SFTP Uploading filename:[sftp://{}] Length:[{}] to Path:[{}]".format(filename, humanSize, self.uploadPath))

        try:
            ssh = Connection( self.uploadAddress, port=self.uploadPort)
        except Exception as e:
            self.log.error(str(e))
            return False

        try:
            command="mkdir -p {}".format(self.uploadPath)
            ssh.run(command)
        except Exception as e:
            self.log.error(str(e))
            return False

        try:
            result = ssh.put(filename, remote=self.uploadPath)
        except Exception as e:
            self.log.error(str(e))
            return False
        return True

    def progressSFTP(self, filename:str, size:int, sent:int):
        """SSH Progress callback.

        Args:
            filename (str): Filename.
            size (int): Total size.
            sent (int): Current sent.
        """
        done = int(50 * sent / size)
        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )

    def __downloadHTTP__(self, url:str, filename:str=None ):
        """Download the given URL via HTTP protocol.

        Args:
            url (str): Source URL.
            filename (str, optional): Optional destination filename.

        Returns:
            bool: True on success, otherwise False.
        """
        httpProxy = None
        if self.httpProxy != 'None':
            httpProxy = { 'http':self.httpProxy,
                          'https':self.httpProxy }
        if filename == None:
            filename = url.rsplit("/")
        filePath = os.path.join(self.workspaceDirectory, filename)
        with open(filePath, 'wb') as fHandle:
            try:
                response = requests.get(url, proxies=httpProxy, stream=True)
            except Exception as e:
                self.log.error(str(e))
                return e

            totalLength = response.headers.get('content-length')
            humanSize = self.getSizeInHumanReadable(totalLength)
            self.log.info("HTTP Downloading url:[{}] to filename:[{}] Length:[{}]".format(url, filePath, humanSize))
            if totalLength is None: # no content length header
                fHandle.write(response.content)
                self.log.error("File is of zero length [{}]".format(filePath))
                raise Exception ("File is of zero length")
            else:
                downloadLength = 0
                totalLength = int(totalLength)
                for dataRead in response.iter_content(chunk_size=4096):
                    downloadLength += len(dataRead)
                    fHandle.write(dataRead)
                    done = int(50 * downloadLength / totalLength)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()
                sys.stdout.write("\n")
        return filename

    def  uploadFile(self,filename:str):
        """Upload the file specified from the workspace to the output folder.

        Args:
            filename (str): File to be uploaded.

        Returns:
            bool: True on success, otherwise False.
        """
        sourceFilename = os.path.join(self.workspaceDirectory, filename)
        if os.path.isfile(sourceFilename) == False:
            # If the folder or the file doesn't exist, we can't proceed
            self.log.error("File not found [{}]".format(sourceFilename))
            raise Exception ("File not found")
            return False

        if self.upload_url.startswith("sftp://") == True:
            return self.__uploadSFTP__( sourceFilename )

        self.log.error("File Upload Type not supported [{}]".format(filename))
        raise Exception ("File upload type not supported")
        return False

    def retrieveListofFilenamesFromUrl(self, inputUrl:str):
        """Retrieve a list of build/image names using the input URL.

        Args:
            inputUrl (str): URL of the build binaries.

        Returns:
            list: List of image names available in the binaries folder.
        """
        self.log.step("outboundClient.retrieveListofFilenamesFromUrl")
        if inputUrl.startswith("http://") or inputUrl.startswith("https://"):
            # Retrive binaries details
            try:
                httpProxy = { 'http': self.httpProxy, 'https': self.httpProxy }
                outputHtml = requests.get(inputUrl, proxies=httpProxy, stream=True)
                outputHtmlText = outputHtml.text

                # Get binaries details
                soup = bs(outputHtmlText, 'html.parser')
                imageList = []
                for link in soup.find_all('a'):
                    imageList.append(link.get('href'))
            except Exception as e:
                raise Exception("outboundClient.retrieveListofFilenamesFromUrl returns error - {}".format(e))
        else:
            raise Exception('UNSUPPORTED format - Currently http or https methods are supported')
        return imageList