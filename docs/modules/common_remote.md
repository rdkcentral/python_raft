## Common Remote

**Module Name:** `commonRemote.py`

**Directory:** `framework/core/CommonRemote.py`

**Purpose:**

* **Remote Control Abstraction:** Provides a consistent way to send remote control commands to various devices, regardless of the specific remote's type or technology.
* **Key Mapping:** Allows you to customize and translate key presses for different remotes, ensuring your test scripts use a unified set of commands across devices.

**Key Classes:**

1. **`remoteControllerMapping`**
   * **Purpose:** Manages translations between your standard test key names and the actual codes different remotes use.
   * **Key Functions:**
     * **`getMappedKey(key)`:** Takes a standard key name (e.g., "POWER") and returns the corresponding, translated key for the currently active remote.
     * **`getKeyMap()`** Returns the complete currently active key map.
     * **`setKeyMap(newMapName)`:** Switches to a different key map.

2. **`commonRemoteClass`**
   * **Purpose:** The core remote control object your tests interact with. Wraps other remote-specific classes and handles key mappings.
   * **Key Functions:**
     * **`sendKey(keycode, delay=1, repeat=1, randomRepeat=0)`**
        * Translates the standard `keycode` using the key map.
        * Sends the mapped code to the actual remote control device.
        * Handles repeats and delays if needed.
     * **`setKeyMap(name)`:**  Switches to the key map specified by `name`.
     * **`getKeyMap()`** Retrieves the currently active key map.

**How Key Mapping Works**

1. **Remote Configuration:** In a configuration file (`remoteConfig`), you specify:
   * `type`: The remote type (e.g., "olimex", "sky_proc", "arduino")
   * `map`:  The name of the key map you want to use with this remote.

2. **Key Map Files:** Separate files hold your key maps (e.g., `olimex_map.yml`). A typical map file looks like this:
   ```yaml
   - name: "MyOlimexMap"
     codes:
       UP: "0x20"
       DOWN: "0x21"
       POWER: "0x0C"
     prefix: "OLIMEX_"  # Optional - Adds a prefix to all translated keys
   ```

2. **Translating Keycodes:**
   * When you call `sendKey("POWER")`, the `commonRemoteClass` does the following:
      * Looks up "POWER" in the currently active key map.
      * Finds the mapped code (e.g., "0x0C" with a prefix of "OLIMEX_").
      * Issues the command "OLIMEX_0x0C" to the underlying remote implementation.

**Example Usage:**

```python
from framework.core.webpageModules.commonRemote import commonRemoteClass

# ... your test setup ...

my_remote = commonRemoteClass(my_logger, remote_config)  # Load from your configuration

# Assuming the key map translates "OK" to "ENTER" on the remote
my_remote.sendKey(rc.OK) 

# Switch to a different remote
new_remote_config = ...  # Load configuration for a different remote device
my_remote.remoteConfig = new_remote_config  
```

**Key Benefits:**

* **Decouples Test Logic:** Your test scripts don't need to know about the specifics of each remote control.
* **Manageability:**  Changing key translations can be done in configuration files rather than modifying your test code.

