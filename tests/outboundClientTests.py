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
#*   ** @addtogroup  : unittests
#*   ** @date        : 08/10/2026
#*   **
#*   ** @brief : outbound client test application
#*   **
#*
#* ******************************************************************************/

import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

from framework.core.outboundClient import outboundClientClass


class FakeResponse:
    def __init__(self, chunks=None, headers=None, error=None):
        self.chunks = chunks or []
        self.headers = headers or {}
        self.error = error
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.closed = True

    def raise_for_status(self):
        if self.error is not None:
            raise self.error

    def iter_content(self, chunk_size):
        yield from self.chunks


class TestOutboundClient(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.client = outboundClientClass(
            log=Mock(),
            workspaceDirectory=self.workspace.name,
            upload_url="sftp://example.test/upload",
            httpProxy="None",
        )

    def tearDown(self):
        self.workspace.cleanup()

    def test_downloads_chunked_https_response(self):
        response = FakeResponse(chunks=[b"first", b"", b"second"])

        with patch("framework.core.outboundClient.requests.get", return_value=response):
            result = self.client.downloadFile("https://example.test/video.bin")

        self.assertEqual("video.bin", result)
        self.assertTrue(response.closed)
        with open(os.path.join(self.workspace.name, "video.bin"), "rb") as downloaded:
            self.assertEqual(b"firstsecond", downloaded.read())

    def test_downloads_http_response_with_content_length(self):
        response = FakeResponse(chunks=[b"test data"], headers={"content-length": "9"})

        with patch("framework.core.outboundClient.requests.get", return_value=response) as get:
            result = self.client.downloadFile("http://example.test/test.bin")

        self.assertEqual("test.bin", result)
        self.assertTrue(response.closed)
        get.assert_called_once_with(
            "http://example.test/test.bin", proxies=None, stream=True
        )
        with open(os.path.join(self.workspace.name, "test.bin"), "rb") as downloaded:
            self.assertEqual(b"test data", downloaded.read())

    def test_downloads_to_requested_filename(self):
        response = FakeResponse(chunks=[b"image"], headers={"content-length": "5"})

        with patch("framework.core.outboundClient.requests.get", return_value=response):
            result = self.client.downloadFile(
                "https://example.test/source.bin", "renamed.bin"
            )

        self.assertEqual("renamed.bin", result)
        self.assertTrue(response.closed)
        with open(os.path.join(self.workspace.name, "renamed.bin"), "rb") as downloaded:
            self.assertEqual(b"image", downloaded.read())

    def test_http_error_removes_stale_file(self):
        destination = os.path.join(self.workspace.name, "build.yml")
        with open(destination, "wb") as stale_file:
            stale_file.write(b"stale: true")
        response = FakeResponse(error=requests.HTTPError("404 Client Error"))

        with patch("framework.core.outboundClient.requests.get", return_value=response):
            result = self.client.downloadFile("https://example.test/build.yml")

        self.assertFalse(result)
        self.assertTrue(response.closed)
        self.assertFalse(os.path.exists(destination))

    def test_empty_response_removes_destination(self):
        response = FakeResponse()

        with patch("framework.core.outboundClient.requests.get", return_value=response):
            with self.assertRaisesRegex(Exception, "zero length"):
                self.client.downloadFile("http://example.test/empty.bin")

        self.assertTrue(response.closed)
        self.assertFalse(os.path.exists(os.path.join(self.workspace.name, "empty.bin")))


if __name__ == "__main__":
    unittest.main()