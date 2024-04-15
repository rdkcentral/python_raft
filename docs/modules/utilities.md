## Utilities

**Module Name:** `utilities.py`

**Directory:** `framework/core/utilities.py`

**Purpose:**

* Provides a collection of helper functions to simplify common tasks within your test scripts.
* Makes your test code cleaner and more focused on the test logic itself.
* Enhances flexibility to handle common challenges in testing

**Key Features:**

1. **Time Management:**
    * **`wait(seconds, minutes=0, hours=0)`:**  Pauses your test execution for a specified time. This is essential for waiting for devices to respond, processes to complete, or introducing delays to synchronize actions.

2. **Text Handling:**

    * **`fuzzyCompareText(expText, actualText, exactMatch=False)`:** Compares two strings flexibly, allowing you to check if an expected text pattern is present within a larger text output.  Especially useful for handling dynamic responses or when you only need to verify a portion of the output.

3. **Value Comparison:**

    * **`value1HigherThanValue2(value1, value2)`:**  Designed to compare version numbers or other dot-separated numerical values (e.g., "1.2.5" vs. "1.2.3").  Important for determining if one software version is newer than another.

**How to Use:**

1. **Import the module:**
   ```python
   from framework.core.utilities import utilities
   ```

2. **Instantiate a 'utilities' object:**
   ```python
   my_utils = utilities(my_log)  # Pass in your logging object
   ```

3. **Use the utility functions:**
   * **Waiting:**
      ```python
      my_utils.wait(5, minutes=1)  # Wait for 1 minute and 5 seconds
      ```
   * **Text Comparison:**
      ```python
      is_match = my_utils.fuzzyCompareText("Welcome*", "Welcome to the system!", exactMatch=False)
      ```
   * **Value Comparison:**
      ```python
      is_newer = my_utils.value1HigherThanValue2("2.5.1", "2.4.8")
      ```

**Example Use Case:**

```python
# ... your test script setup ...

# Wait for a device to reboot before continuing
my_utils.wait(120)  # Wait for 2 minutes

# Capture output from the device console 
device_output = device_console.read_output()  

# Verify that a success message is displayed
if not my_utils.fuzzyCompareText("operation successful", device_output):
   # Handle the case where the operation may have failed
   ... 
```
