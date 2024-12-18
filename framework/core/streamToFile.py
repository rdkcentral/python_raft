#!/usr/bin/env python3

from io import IOBase
from threading import Thread
from os import path


class StreamToFile():

    def __init__(self, outputPath):
        self._filePath = outputPath
        self._fileHandle = None
        self._activeThread = None
        self._readLine = 0

    def writeStreamToFile(self, inputStream: IOBase) -> None:
        """
        Starts a new thread to write the contents of an input stream to a file.

        Args:
            inputStream (IOBase): The input stream to be read from.
            outFileName (str): The path of the output file where the stream data will be written.
                                If only a file name is given, the file will be written in the current tests log directory.
        """
        self._fileHandle = open(self._filePath, 'a+', encoding='utf-8')
        newThread = Thread(target=self._writeLogFile,
                                        args=[inputStream, self._fileHandle],
                                        daemon=True)
        
        self._activeThread =  newThread
        newThread.start()

    def stopStreamedLog(self) -> None:
        """
        Stops a previously started thread that is writing to a log file.

        Args:
            outFileName (str): The path of the output file associated with the thread to be stopped.

        Raises:
            AttributeError: If the specified thread cannot be found.
        """
        if self._activeThread:
            self._activeThread.join(timeout=30)
        else:
            raise AttributeError(f'Could not find requested logging thread to stop. [{self._filePath}]')

    def _writeLogFile(self,streamIn: IOBase, ioOut: IOBase) -> None:
        """
        Writes the input stream to a log file.

        Args:
            stream_in (IOBase): The stream from a process.
            logFilePath (str): File path to write the log out to.
        """
        while True:
            chunk = streamIn.readline()
            if chunk == '':
                break
            ioOut.write(chunk)

    def readUntil(self, searchString:str, retries: int = 5) -> None:
        """
        Read lines from a file until a specific search string is found, with a specified
        number of retries.
        
        Args:
          searchString (str): The string that will be search for.
          retries (int): The maximum number of times the method will attempt to find the `searchString`.
                          Defaults to 5
        
        Returns:
            boolean : True when the `searchString` is found. False otherwise.
        """
        result = False
        retry = 0
        max_retries = retries
        while retry != max_retries and not result:
            read_line = self._readLine
            self._fileHandle.seek(read_line)
            out_lines = self._fileHandle.readlines()
            write_line = len(out_lines)
            while read_line != write_line:
                if searchString in out_lines[read_line]:
                    result = True
                    break
                read_line+=1
            retry += 1
        self._readLine = read_line
        return result

    def __del__(self):
        self.stopStreamedLog()
        if self._fileHandle:
            self._fileHandle.close()