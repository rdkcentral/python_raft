#!/usr/bin/env python3

from io import IOBase
from threading import Thread
from os import path


class StreamToFile():

    def __init__(self):
        self._file_handles = {}

    def writeStreamToFile(self, inputStream: IOBase, outFileName: str) -> None:
        """
        Starts a new thread to write the contents of an input stream to a file.

        Args:
            inputStream (IOBase): The input stream to be read from.
            outFileName (str): The path of the output file where the stream data will be written.
                                If only a file name is given, the file will be written in the current tests log directory.
        """
        outFileHandle = open(outFileName, 'a+', encoding='utf-8')
        newThread = Thread(target=self._writeLogFile,
                                        args=[inputStream, outFileHandle],
                                        daemon=True)
        
        self._file_handles.update({outFileName: newThread})
        newThread.start()

    def stopStreamedLog(self, outFileName: str) -> None:
        """
        Stops a previously started thread that is writing to a log file.

        Args:
            outFileName (str): The path of the output file associated with the thread to be stopped.

        Raises:
            AttributeError: If the specified thread cannot be found.
        """
        log_thread = self._loggingThreads.get(outFileName)
        if log_thread:
            log_thread.join(timeout=30)
        else:
            raise AttributeError(f'Could not find requested logging thread to stop. [{outFileName}]')

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

    def readUntil(self, fileName:str, searchString:str, retries: int = 5) -> None:
        """
        Reads the monitoring log until the specified message is found.

        Opens the monitoring log file and checks for the message within a specified retry limit.

        Args:
            message (str): The message to search for in the monitoring log.
            retries (int, optional): The maximum number of retries before giving up (default: 5).

        Returns:
            bool: True if the message was found, False otherwise.
        """
        out_file_dict = self._file_handles.get(fileName, None)
        if out_file_dict is None:
            raise FileNotFoundError(fileName)
        out_file_handle = out_file_dict.get('handle')
        result = False
        retry = 0
        max_retries = retries
        while retry != max_retries and not result:
            read_line = out_file_dict.get('read_line')
            out_file_handle.seek(read_line)
            out_lines = out_file_handle.readlines()
            write_line = len(out_lines)
            while read_line != write_line:
                if searchString in out_lines[read_line]:
                    result = True
                    break
                read_line+=1
            retry += 1
        out_file_dict['read_line'] = read_line
        return result

    def __del__(self):
        for handle in self._file_handles.values():
            handle.close()