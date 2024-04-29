## Device Manager

**Module Name:** `deviceManager.py`

**Directory:** `framework/core/deviceManager.py`

**Purpose:**

* **Centralized Device Management:** Provides a structured way to organize and access information about multiple devices within your test environment.
* **Abstraction Layer:** Offers a unified interface to control devices, regardless of their specific communication protocols (e.g., SSH, Telnet, Serial) or power control methods.
* **Encapsulation:** Keeps the details of individual device configurations and control mechanisms together, reducing complexity in the rest of your test code.

**Key Classes:**

1. **`consoleClass`**
   * **Purpose:** Represents a single console connection (SSH, Telnet, or Serial) to a device.
   * **Key Functions:**
      * `__init__(self, log, logPath, configElements)`: Initializes a console object based on the provided configuration.
   * **Stores:** The underlying session object (`sshConsole`, `telnet`, or `serialSession`).

2. **`deviceClass`**
   * **Purpose:** Models a single device under test.
   * **Key Functions:**
      * `__init__(self, log, logPath, devices)`:  Initializes a device object with its consoles, power control, etc.
      * `getField(self, fieldName)`:  Retrieves a specific configuration field value from the device's configuration data.
      * `getConsoleSession(self, consoleName)`: Returns a console session object for the specified console.
   * **Manages:**
      * `consoles` (dictionary): Stores available consoles for the device.
      * `powerControl` (`powerControlClass` object): Handles power cycling.
      * `outBoundClient` (`outboundClientClass` object):  Handles outbound connections from the device.
      * `remoteController` (`commonRemoteClass` object):  Manages remote control actions.

3.  **`deviceManager`**
    * **Purpose:** The main interface for managing all devices in your test setup.
    * **Key Functions:**
       * `__init__(self, deviceConfig, log, logPath)`: Initializes the device manager with the configuration.
       * `getDevice(self, deviceName)`: Retrieves a `deviceClass` object representing the specified device.

**How It Works**

1. **Configuration:** You provide a configuration file (dictionary) that defines your devices and their properties:
   ```yaml
   devices:
     dut:
       consoles:
         - ssh:
             type: ssh
             ip: 192.168.0.10
             username: myuser
             password: mypassword
       powerSwitch:
         # Power control details...
   ```

2. **Initialization:**  
   * The `deviceManager` is created, loading the configuration.
   * For each device, it creates `deviceClass` objects.
   * Within each `deviceClass`, it creates `consoleClass` objects for each defined console.

3. **Device Interaction**
   ```python
   my_device_manager = deviceManager(device_config, my_logger, log_path)
   dut = my_device_manager.getDevice("dut")

   ssh_session = dut.getConsoleSession("ssh")  
   ssh_session.send("ls -l")  # Send a command over SSH

   dut.powerControl.powerOff() # Power off the device
   ```

**Benefits**

* **Organization:** Improves code readability and maintainability by separating device management logic.
* **Flexibility:** Supports various communication protocols and power control mechanisms.
* **Ease of Use:** Provides a clear API for interacting with devices in your tests.
