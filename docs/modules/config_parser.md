## Config Parser

**Module Name:** `configParser.py`

**Directory:** `framework/core/configParser.py`

**Purpose:**

* **Organize Configuration:**  Manages your test configuration files in a structured way.
* **Handle Multiple Platforms:** Parses configuration settings that are specific to different device platforms.
* **Image Management:** Helps you locate and work with the correct image files (e.g., firmware) for different devices.
* **Memory Map Support:** Enables you to work with memory maps, which describe where specific data is stored within a device's memory.

**Key Sections:**

1. **`local`**
   * General test configuration settings.
   * **Example:**
       * `workspaceDirectory`: Location to store logs and temporary files.

2. **`cpe`**
   * Device-specific configurations. Entries are typically named after platforms (e.g., "cpeSTB123").
   * **Important Fields:**
     * `platform`: The platform identifier this configuration entry is for.
     * `validImage`: Defines available valid image files and their locations.
     * `negativeImageLocation`: Location of a negative image (used for testing failure states).
     * `memoryMap`: Specifies the name of the memory map configuration to use with this platform.
     * `alternative_platform`: A list of other platforms that can be treated as compatible with this one.

3. **`memoryMap`**
    * Describes the layout of a device's memory. Entries are also typically named after platforms.
    * **Important Fields:**
        *  `offsets`:  Defines names and memory addresses of specific data elements you might reference in tests (e.g., "bootStatus" at address 0x12345678).

**How to Use It:**

1. **Loading Configuration:**
   ```python
   import configParser as cp

   my_config = cp.configParser(config_file)  # Load from your configuration file
   ```

2. **Retrieving Values:**
   ```python
   # General Setting
   workspace = my_config.getWorkspaceDirectory()

   # Platform-Specific
   platform = "STB123"
   valid_image_url = my_config.getValidImageUrlViaPlatform("PCI1_image", platform)
   memory_map_offset = my_config.getMemoryMapValueViaPlatform(platform, "bootStatus") 
   ```

3. **Image Handling**
   ```python
   image_name = "PCI2_image"
   platform = "STB456"
   image_url = my_config.getImageField(image_name, "platform", platform)
   ```

**Example Configuration Structure:**

```yaml
local:
  workspaceDirectory: /home/user/raft-tests

cpeSTB123:
  platform: STB123
  validImage:
    PCI1_image: http://images/stb123/PCI1.img 
    PCI2_image: http://images/stb123/PCI2.img
  negativeImageLocation: http://images/stb123/negative.img
  memoryMap: memoryMapSTB123

memoryMapSTB123:
  offsets:
    bootStatus: 0x12345678
```


## Config Parser Base

**Module Name:** `configParserBase.py`

**Directory** `framework/core/configParseBase.py`

**Purpose:**

* **Foundation for Parsers:** Provides the basic building blocks for creating more specialized configuration file parsers within your test system.
* **Handles Common Structures:** Defines how to extract and store configuration parameters that are likely to be present across different types of test configuration files.

**Key Functions:**

* **`__init__(self, config, log=None)`**
   * **Constructor:** Initializes the parser object.
     * `config`:  The configuration data, typically loaded from a file and represented as a dictionary.
     * `log`:  An optional logging object to use for reporting.

* **`decodeTable(self, parent, config)`**
   * **Processes Tables:** Handles cases where your configuration file contains nested tables (i.e., dictionaries within dictionaries).
   * `parent`: The dictionary where the decoded table should be stored.
   * `config`: The table (as a dictionary) to be parsed  

* **`decodeParam(self, parent, name, value)`**
   * **Handles Individual Parameters:** Extracts single key-value pairs from the configuration.
   * Updates the `parent` dictionary with the `name` and `value` extracted. 

**How It Relates to Your Test Framework**

Think of the `configParserBase` module as a blueprint for creating parsers that understand the specific formats of your configuration files. Let's illustrate this with a hypothetical example:

**Scenario:**

* You have a `rack_config.yaml` file that defines test environments  (e.g., racks, devices).
* You need to load settings from this file into your test scripts. 

**Steps:**

1. **Create a Subclass:**
   ```python
   from configParserBase import configParserBase 

   class RackConfigParser(configParserBase): 
       # ... your specific parser logic here ...
   ```

2. **Customize Parsing:** In your `RackConfigParser` class, you would override the `decodeTable` and `decodeParam` methods to match the structure of your `rack_config.yaml` file.

**Benefits**

* **Code Structure:**  Provides a consistent way to handle different configuration file formats throughout your framework.
* **Centralized Logic:** Common parsing tasks are handled in the base class, reducing code duplication.

**Note:** The `configParserBase` itself is usually not used directly. It's the specialized subclasses (like the hypothetical `RackConfigParser`) that are integrated into your test scripts.