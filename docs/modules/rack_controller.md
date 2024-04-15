## Rack Controller

**Module Name:** `rackController.py`

**Directory:** `framework/core/rackController.py`

**Purpose:**

* Defines the structure and configuration of a testing rack.
* Manages slots within a rack, each slot potentially representing a device under test (DUT).
* Provides methods to access and retrieve information about racks and their associated devices.

**Key Classes:**

* **configDecoderClass:**
   * Base class that handles decoding of configuration settings.
   * Checks for required fields in the configuration.
   * Maps configuration items to specific handling functions.

* **rackSlot:**
   * Represents a single slot within a rack.
   * Stores configuration details about the device in that slot:
      * Device Name
      * Remote control type
      * IP address or hostname
      * Platform type 
      * Outbound upload/download directories (for file exchange)

* **rack:**
   * Represents an entire testing rack.
   * Contains a list of `rackSlot` objects.
   * Provides methods to get slots by index or name.

* **rackController:**
   * Top-level class managing multiple racks within the system.
   * Decodes the main rack configuration file.
   * Provides methods to get racks by index or name.

**How to Use:**

1. **Configuration File:** Create a configuration file (likely in YAML format) that defines the following:
   * Racks: Each rack has a name and contains slots.
   * Slots: Each slot defines the device within it, including its name, address, platform, etc.

2. **Initialization:**  Include the `racks.py` module and load the configuration. This initializes the `rackController` and its internal representation of your racks.

3. **Accessing Information:**
   * Use methods of the `rackController` to retrieve specific racks:
      * `getRackByName()` 
      * `getRackByIndex()`
   * Once you have a `rack` object:
      * Use `getSlot()` or `getSlotByName()` to get a `rackSlot` object.
      * Access device information from the `rackSlot` object.

**Example:**

**YAML Configuration:**

```yaml
rack1:
  name: MyTestingRack
  slot1:
    name: DUT1
    deviceType: STB
    address: 192.168.1.100  
    platform: XYZ
```

**Python Code:**

```python
import racks

config = # Load your YAML configuration
racks_obj = racks.rackController(config)

my_rack = racks_obj.getRackByName("MyTestingRack")
device_slot = my_rack.getSlotByName("DUT1")

ip_address = device_slot.getDeviceIp()
platform = device_slot.getPlatform()

print("Device IP:", ip_address)
print("Device Platform:", platform)
```
