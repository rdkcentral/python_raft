## Decode Params

**Module Name:** `decodeParams.py`

**Directory:** `framework/core/decodeParams.py`

**Purpose:**

* **Process Command-Line Arguments:**  Parses the arguments you provide when you run your test script, allowing you to set up the test environment dynamically.
* **Interpret Configuration Files:** Reads configuration files (usually in YAML format) and stores the settings in a usable format. 
* **Provide Test Parameters:** Makes these parameters easily accessible to your test scripts, enabling customization and flexibility.

**Key Features:**

1. **Argument Parsing:**

   * Leverages the Python `argparse` library.
   * Supports a mix of required arguments (`--config`), optional arguments (`--slotName`, `--job_id`), and flags (`--test`, `--debug`).
   * Handles both short (`-config`) and long (`--configFile`) argument forms.

2. **Configuration File Handling**

   * Loads YAML configuration files.
   * Works with paths that are either absolute or relative to the script's location.
   * Handles both the main configuration file (`rackConfig`) and device-specific configurations (`deviceConfig`).

3. **Additional Functionality**

   * **Debug Mode:** Enables debug logging with the `--debug` flag.
   * **Test Mode:** Activates test-specific behaviors with the `--test` flag.
   * **Loopback Override:**   Allows overriding loopback settings with the `--loop` argument.

**How It Works**

1. **Initialization:** When you create a `decodeParams` object, the `__init__` method does the following:
   * Parses the command-line arguments using  `argparse`.
   * Loads the main configuration file (`rackConfig`).
   * Optionally, loads the device configuration file (`deviceConfig`).
   * Processes build info and override configuration files (if specified).
   * Sets flags for debug and test mode.

2. **Accessing Parameters:** Your test scripts can access the parsed parameters as attributes of the `decodeParams` object:
   * `rackConfig` (dictionary)
   * `deviceConfig` (dictionary)
   * `args` (from `argparse`)
   * `testMode` (boolean)
   * `debug` (boolean)

**Example Usage**

```python
from decodeParams import decodeParams

my_params = decodeParams(log) # Assuming you have a logging object

rack_name = my_params.args.rackName 
test_mode = my_params.testMode
device_ip = my_params.deviceConfig["devices"]["dut"]["deviceAddress"] 
```

**Benefits**

* **Clarity:** Separates the handling of test parameters from the test logic itself, improving code readability.
* **Flexibility:** Gives you the ability to customize test runs without modifying the core test code.
* **Centralization:** Provides a unified way to deal with configuration and command-line arguments across different test scripts. 

