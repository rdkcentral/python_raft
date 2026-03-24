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
#*   ** @file        : __init__.py
#*   ** @date        : 17/01/2019
#*   **
#*   **
#* ******************************************************************************
#!/usr/bin/env python3

#__all__ = ["testControl", "logModule", "rcCodes", "rackController", "slotInfo" ]
#expose only the components required for the upper classes to operate
try:
  from . capture import capture
except ModuleNotFoundError as e:
  # Only treat known optional image-processing dependencies as optional.
  _optional_capture_deps = {"cv2", "pytesseract", "PIL"}
  if e.name in _optional_capture_deps:
    class _CaptureMissingDependency:
      def __call__(self, *args, **kwargs):
        raise ImportError(
          "Image capture functionality is unavailable because optional "
          "dependencies (cv2, pytesseract, PIL) are not installed."
        ) from e
    capture = _CaptureMissingDependency()
  else:
    # Unexpected missing module (e.g., bug inside capture.py) - do not hide it.
    raise
from . commonRemote import commonRemoteClass
from . deviceManager import deviceManager
from . logModule import logModule
from . logModule import DEBUG, INFO, WARNING, ERROR, CRITICAL
from . testControl import testController
try:
  from . webpageController import webpageController
except ModuleNotFoundError:
  webpageController = None  # selenium not installed (e.g. Docker)
from . rcCodes import rcCode as rc
from . utilities import utilities

#print("framework.core-> __init__.py")
