## Test Control

**Module Name:** `testControl.py`

**Directory:** `framework/core/testControl.py`

**Purpose:**

* Serves as the central control point for orchestrating and running rack-based tests.
* Manages the lifecycle of a test,  including setup, execution, and cleanup.
* Abstracts away details of interacting with devices, networking, and other test infrastructure. 
* Provides a layer for common test actions and reporting to make your test scripts simpler and more readable. 

**Key Features:**

1. **Test Configuration:**
   * **Modular Structure:**  Tests are based on the configuration files you provide (e.g., `test_config.yml`, `device_config.yml`). These files define parameters, devices, and other settings.
   * **Flexibility:** Supports running tests on different racks and with different slot configurations.
   * **Logs and Results:** Organizes logs and test results into a clear, timestamped directory structure for easy analysis.

2.  **Device Control:**
    * **Centralized Management:** Provides methods to power devices on/off and interact with their consoles (e.g., sending commands, reading output).
    * **Remote Control:** Supports controlling devices using various remote control technologies (IR, Bluetooth, etc.). You would configure this in your device configuration files.

3. **Test Execution:**
   * **Main Test Function (`testFunction`)** Implement your core test logic and actions within this function in your test script.
   * **Setup and Cleanup (`testPrepareFunction`, `testEndFunction`)** Functions to handle pre-test configuration (e.g., preparing devices, setting up network connections) and post-test cleanup actions.
   * **Looping:** Executes `testFunction` multiple times based on a loop count you provide for stress testing. 
   * **Exception Handling:** Catches exceptions during your test execution and performs necessary cleanup (via `testExceptionCleanUp`). This helps maintain test stability.

4. **Additional Functionality:**
   * **Image Programming:**  Can automatically fetch and program valid device images based on your configuration.
   * **Web Page Control:**  Supports automating interactions with web interfaces on your devices using a web driver.
   * **Video Capture:** Can integrate with video capture devices to record screen activity during tests. Useful for UI testing and analyzing test failures.

**How to Use:**

1.  **Create Test Scripts:**
    *  Extend the `testControl` class within your test scripts.
    *  Override the key functions:
        * **`testPrepareFunction`**:  Set up the necessary environment for your test.
        * **`testFunction`**:  Implement the core logic of your test (device interactions, verifications, assertions).
        * **`testEndFunction`**:  Clean up after your test, such as powering down devices, closing browser sessions, etc. 

2. **Provide Configuration Files:**
     * **Rack Configuration:**  Defines racks, slots, devices, and their properties.
     * **Test Configuration:** Specifies test parameters, loop count, device images, etc.

3. **Run Tests:**
    * Execute your test script, potentially passing command-line arguments to control settings like rack and slot selection.

**Example Workflow**

```python
# MyTestScript.py
from framework.core.testControl import testController

class MyTest(testController):
    def testPrepareFunction(self):
        # Connect to devices, set initial state, etc.

    def testFunction(self):
        # 1. Send commands to the device
        # 2. Read response from the device
        # 3. Verify the expected behavior

    def testEndFunction(self):
        # Close connections, reset devices, etc. 

# Instantiate and run the test
test = MyTest("TestName", "QC12345")
test.run()
```   
