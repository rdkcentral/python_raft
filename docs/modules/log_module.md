## Log Module

**Module Name:** `logModule`

**Directory:** `framework/core/logModule.py`

**Purpose:**

* Provides a structured, flexible logging mechanism for test cases and scripts.
* Organizes log output with clear visual separation for different levels of information and execution steps.
* Supports both console output and file logging.
* Tracks test statistics, step counts, and results for easy reporting. 

**Key Features:**

1. **Logging Levels:** 
   * Employs standard logging levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
   * Adds custom levels for clarity:
     * `STEP`: General step within a test.
     * `STEP_START`: Marks the beginning of a step.
     * `STEP_RESULT`: Indicates step completion and outcome (pass/fail).
     * `TEST_START`: Signals the start of a test case.
     * `TEST_RESULT`: Summarizes the overall test result (pass/fail).
     * `TEST_SUMMARY`: Provides aggregated results of multiple tests.

2. **Output Formatting**
    * Uses visual separators (e.g., `----`, `****`) to delineate tests, steps, and results.
    * Includes timestamps and module names for each log entry.
    * Allows customization of indentation for nested steps.

3. **Test Tracking:**
    * Maintains counters for steps (total, passed, failed).
    * Records start/end times of tests and overall execution durations.
    * Manages test names and associated QC IDs (for integration with test management platforms).
    * Logs test statistics and outcomes in a CSV format for reporting.

**How to Use:**

1. **Initialization:** Create a `logModule` object, providing a module name and optionally a desired logging level:
   ```python
    my_logger = logModule("my_test_module", logModule.INFO)  
   ```

2. **Logging Messages:**  Use the provided methods to log messages at appropriate levels:
  ```python
   my_logger.info("Starting initialization")
   my_logger.debug("Detailed configuration value: X")
   my_logger.error("Connection failed")
  ```

3. **Test and Step Management:** 
   * `testStart()`: Marks the beginning of a test, logs metadata (name, QC ID).
   * `stepStart()`: Marks the beginning of a step, includes a description.
   * `stepResult()`: Logs the step outcome (pass/fail) and any messages.
   * `testResult()`: Summarizes the test result and generates CSV log entry.

**Example Workflow:**

```python  
my_logger.testStart("Device Reboot Test", "QC-1234")

my_logger.stepStart("Power cycle device")
   # ... code to power cycle the device ...
my_logger.stepResult(True, "Device rebooted successfully") 

my_logger.stepStart("Verify connectivity")
   # .... code to check connectivity ...
my_logger.stepResult(False, "Connection timeout")  

my_logger.testResult("Test failed due to connectivity issues")
```

