# python_raft AI Brief

> Single-file reference for AI tools. Covers architecture, API surface, configuration schemas, and common patterns for the Rapid Application Framework for Test (RAFT).

## 1. Purpose

python_raft is a Python 3.10+ test-automation framework for engineering-level device testing, primarily targeting RDK (Reference Design Kit) set-top boxes and embedded Linux devices. It provides:

- YAML-driven rack/slot/device configuration (no test-code changes per environment)
- Unified console abstraction (SSH, Serial, Telnet)
- Power control across 8 switch types
- IR/RF remote control with key-mapping
- HDMI-CEC send/receive
- A/V sync measurement
- Video capture and OCR
- Two test harness styles: `testController` (custom lifecycle) and `RAFTUnitTestCase` (stdlib `unittest`)

Repository: `rdkcentral/python_raft`, default branch `develop`.

---

## 2. Directory Layout

```
python_raft/
  framework/
    core/
      testControl.py          # testController class (custom test lifecycle)
      deviceManager.py        # deviceManager, deviceClass, consoleClass
      rackController.py       # rackController, rack, rackSlot
      configParser.py         # configParser (device/CPE config)
      configParserBase.py     # Base class for config parsing
      decodeParams.py         # CLI argument parser (argparse)
      logModule.py            # Logging wrapper with custom levels
      singleton.py            # Singleton shared state for unittest path
      raftUnittest.py         # RAFTUnitTestCase, RAFTUnitTestSuite
      rcCodes.py              # rcCode enum (remote control key constants)
      commonRemote.py         # commonRemoteClass, remoteControllerMapping
      powerControl.py         # powerControlClass (delegates to modules)
      hdmiCECController.py    # HDMICECController
      avSyncController.py     # AVSyncController (SyncONE2)
      utPlaneController.py    # utPlaneController (ut-core integration)
      outboundClient.py       # File download/upload client
      capture.py              # Video capture engine
      webpageController.py    # Selenium web driver wrapper
      utilities.py            # Shell command helpers, wait, etc.
      streamToFile.py         # Stream-to-file utility
      commandModules/
        consoleInterface.py   # Abstract base class for consoles
        sshConsole.py         # SSH via paramiko
        serialClass.py        # Serial via pyserial
        telnetClass.py        # Telnet via telnetlib
      powerModules/
        none.py               # No-op power
        hs100.py              # TP-Link HS100
        apc.py                # APC (telnet-based)
        apcAos.py             # APC AOS firmware
        olimex.py             # Olimex relay board
        kasaControl.py        # TP-Link Kasa smart plugs/strips
        tapoControl.py        # TP-Link Tapo smart plugs
        SLP.py                # Server Technology SLP PDU
      remoteControllerModules/
        remoteInterface.py    # Abstract base for remotes
        none.py               # No-op remote
        olimex.py             # Olimex IR blaster
        skyProc.py            # Sky proprietary IR
        arduino.py            # Arduino-based IR
        keySimulator.py       # RDK middleware key simulator
        redrat.py             # RedRat IR hub
      hdmicecModules/         # CEC-client, remote-cec-client, virtual-cec-client
      avSyncModules/          # SyncONE2 serial driver
      audioAmplifier/         # Audio amplifier controller
  examples/
    code/
      example_ssh.py          # testController example
      example_ssh_unittest.py # RAFTUnitTestCase example
    configs/
      getting_started_rack_config.yml
      example_rack_config.yml
      example_device_config.yml
      example_keymap.yml
      example_olimex_keys.yml
      example_redrat_keymap.yml
  installation/
    install_requirements.sh
  requirements.txt
```

---

## 3. Core Classes

### 3.1 testController (`framework/core/testControl.py`)

The original test harness. Tests subclass `testController` and override lifecycle hooks.

```python
class testController:
    def __init__(self, testName="", qcId="", maxRunTime=TEST_MAX_RUN_TIME,
                 level=logModule.STEP, loop=1, log=None)
```

**Constructor flow:**
1. Creates `logModule` for this test
2. Parses CLI args via `decodeParams`
3. Decodes rack config via `rackController`
4. Decodes device config via `configParser`
5. Selects rack and slot (from CLI `--rack` / `--slot` / `--slotName`)
6. Constructs log paths under `logs/<rack>/<slot>/<timestamp>/`
7. Creates `deviceManager` from slot device list
8. Sets up shortcut attributes: `self.dut`, `self.session`, `self.powerControl`, `self.commonRemote`, `self.hdmiCECController`
9. Optionally sets up `capture` (video), `webpageController` (Selenium)

**Key attributes available in tests:**
- `self.session` -- default console session (SSH/Serial/Telnet) for the DUT
- `self.dut` -- `deviceClass` instance for "dut"
- `self.powerControl` -- `powerControlClass`
- `self.commonRemote` -- `commonRemoteClass`
- `self.hdmiCECController` -- `HDMICECController` or None
- `self.capture` -- `capture` instance or None
- `self.log` -- `logModule` instance
- `self.cpe` -- device config CPE entry (dict)
- `self.slotInfo` -- `rackSlot` instance
- `self.config` -- `decodeParams` instance

**Lifecycle hooks (override in subclass):**

| Method | When | Default |
|---|---|---|
| `testPrepareFunction()` | Before test loop | returns True |
| `testFunction()` | Each loop iteration | returns True |
| `testEndFunction(powerOff=True)` | After all loops complete | closes session, powers off |
| `testExceptionCleanUp()` | On exception in testFunction | no-op |
| `waitForBoot()` | Before testPrepareFunction | returns True |

**`run(powerOff=True)` execution order:**
1. `session.open()`
2. `waitForBoot()`
3. `testPrepareFunction()`
4. Loop `testFunction()` up to `self.loopCount` times (or until False/exception/maxRunTime)
5. `testEndFunction(powerOff)`

**Other useful methods:**
- `pingTest(deviceName="dut")` -- ICMP ping check
- `waitForPrompt(prompt=None)` -- wait for shell prompt on session
- `syscmd(cmd)` -- run command on the local host
- `runHostCommand(command)` -- run command on host via subprocess

### 3.2 deviceManager (`framework/core/deviceManager.py`)

```python
class deviceManager:
    def __init__(self, deviceConfig: dict, log: logModule, logPath: str = "")
    def getDevice(self, deviceName: str = "dut") -> deviceClass
```

Iterates over the device list from slot config, creating a `deviceClass` for each.

### 3.3 deviceClass

Represents a single device. Created from the per-device dict in the rack config.

```python
class deviceClass:
    def __init__(self, log, logPath, devices: dict)
```

**Attributes:**
- `consoles` -- dict of `consoleClass` instances keyed by name (e.g. "default", "ssh")
- `powerControl` -- `powerControlClass` or None
- `outBoundClient` -- `outboundClientClass` or None
- `remoteController` -- `commonRemoteClass` or None
- `hdmiCECController` -- `HDMICECController` or None
- `avSyncController` -- `AVSyncController` or None
- `session` -- default console session

**Key methods:**
- `getConsoleSession(consoleName="default")` -- returns the underlying console session object
- `getField(fieldName)` -- recursive dict search for a field in raw config
- `pingTest(logPingTime=False)` -- ICMP reachability check

### 3.4 consoleClass

Factory that creates the right console type based on `type` field in config.

Supported types: `ssh`, `serial`, `telnet`.

### 3.5 rackController / rack / rackSlot (`framework/core/rackController.py`)

```python
class rackController:
    def __init__(self, config)
    def getRackByName(self, rackName) -> rack
    def getRackByIndex(self, rackIndex) -> rack

class rack:
    def getSlot(self, slotIndex) -> rackSlot        # 1-based index
    def getSlotByName(self, slotName) -> rackSlot

class rackSlot:
    def getDevice(self, deviceName) -> dict
    def getPlatform(deviceName="dut") -> str
    def getDeviceAddress(deviceName="dut") -> str
    def getRemoteKeyType(deviceName="dut") -> str
```

### 3.6 decodeParams (`framework/core/decodeParams.py`)

Parses CLI arguments via argparse. The `--config` argument is **required**.

| Argument | Description |
|---|---|
| `--config` / `-config` | **Required.** Path to rack config YAML |
| `--deviceConfig` / `-deviceConfig` / `--testConfig` | Device config YAML (overrides `includes.deviceConfig` in rack config) |
| `--rack` | Rack name to use |
| `--slot` | Slot number (1-based int) |
| `--slotName` | Slot name (string alternative to `--slot`) |
| `--loop` | Override loop count |
| `--debug` / `-debug` | Enable DEBUG log level |
| `--test` / `-test` | Enable test mode |
| `--buildInfo` | URL to build info YAML |
| `--overrideDeviceConfig` | URL to CPE config override YAML |
| `--job_id` | Optional job identifier |
| `--rack_job_execution_id` | Optional rack job execution identifier |

### 3.7 logModule (`framework/core/logModule.py`)

Wraps Python `logging` with custom levels and structured test output.

**Custom log levels (in ascending order):**

| Level | Name | Numeric |
|---|---|---|
| DEBUG | DEBUG | 10 |
| INFO | INFO | 20 |
| STEP | STEP | 21 |
| STEP_START | STEP_START | 22 |
| TEST_START | TEST_START | 23 |
| STEP_RESULT | STEP_RESULT | 24 |
| TEST_RESULT | TEST_RESULT | 25 |
| TEST_SUMMARY | TEST_SUMMARY | 26 |
| WARNING | WARNING | 30 |
| ERROR | ERROR | 40 |
| CRITICAL | CRITICAL | 50 |
| FATAL | FATAL | 100 |

**Key methods:**
- `stepStart(message, expected=None)` -- begin a numbered test step
- `step(message)` -- log within a step
- `stepResult(result: bool, message)` -- record pass/fail for a step
- `testStart(testName, qcId, loops, maxRunTime)` -- begin test timing
- `testResult(message)` -- end test, compute pass/fail summary
- `setFilename(logPath, logFileName)` -- attach file handler + CSV logger
- `indent()` / `outdent()` -- visual indentation in log output
- `fatal(message)` -- logs and calls `os._exit(1)`

**Log output format:** `YYYY-MM-DD HH:MM:SS, <module>, <LEVEL>: <message>`

Parallel CSV output: `QcId, TestName, Result, Failed Step, Failure, Duration`

**Log directory structure:**
```
logs/<rackName>/<slotName>/<YYYYMMDD-HH-MM-SS>/
    test_summary.log
    test_summary.log.csv
    <testName>-<qcId>/
        test-0.log
        test-0.log.csv
        screenImages/
        captureImages/
```

### 3.8 Singleton (`framework/core/singleton.py`)

Shared state for the `RAFTUnitTestCase` path. Created once at module import time as `SINGLETON`.

```python
class Singleton:
    # Class-level attributes shared by all tests:
    config          # decodeParams
    _rackController # rackController
    deviceConfig    # configParser
    rack            # selected rack
    slotInfo        # selected slot
    summaryLog      # logModule for summary
    testLog         # logModule for test detail
    devices         # deviceManager (lazy init)
```

---

## 4. Console Types

All consoles implement `consoleInterface` (abstract base class):

```python
class consoleInterface(ABC):
    def open(self) -> bool
    def close(self) -> bool
    def read_until(self, value: str, timeout: int = 10) -> str
    def read_all(self) -> str
    def write(self, message: list|str, lineFeed="\n", wait_for_prompt=False) -> bool
    def waitForPrompt(self, prompt=None, timeout=10) -> bool
    # property: timeout (int, seconds)
```

### 4.1 SSH (`sshConsole`)

Uses `paramiko.SSHClient`. Supports key-based and password auth.

Config fields: `type: "ssh"`, `address`/`ip`, `username`, `password`, `port` (default 22), `known_hosts`, `prompt`.

Extra method: `open_interactive_shell()`, `read(timeout=10)`.

### 4.2 Serial (`serialSession`)

Uses `pyserial`.

Config fields: `type: "serial"`, `port` (e.g. "/dev/ttyUSB0"), `baudRate` (default 115200), `dataBits` (8), `stopBits` (1), `parity` ("None"), `flowControl` (False), `prompt`.

### 4.3 Telnet (`telnet`)

Uses `telnetlib`.

Config fields: `type: "telnet"`, `address`/`ip`, `username`, `password`, `port` (default 23), `username_prompt`, `password_prompt`, `prompt`.

---

## 5. Power Modules

`powerControlClass` delegates to a specific module based on `type` in config.

```python
class powerControlClass:
    def powerOn(self) -> bool
    def powerOff(self) -> bool
    def reboot(self) -> bool
    def getPowerLevel(self) -> float     # Watts
    def getVoltageLevel(self) -> float   # Volts
    def getCurrentLevel(self) -> float   # Amps
```

All operations support retry via `retryCount` (default 1) and `retryDelay` (default 30s) config fields.

| Type | Module | Config fields |
|---|---|---|
| `"none"` | `powerNone` | (none) |
| `"hs100"` | `powerHS100` | `ip`, `port` |
| `"apc"` | `powerAPC` | `ip`, `username`, `password`, `outlet` |
| `"apcAos"` | `powerApcAos` | `ip`, `username`, `password`, `port` (23), `outlet` |
| `"olimex"` | `powerOlimex` | `ip`, `port`, `relay` |
| `"kasa"` | `powerKasa` | `ip`, `options` ("--plug" or "--strip"), `args` ("--index N") |
| `"tapo"` | `powerTapo` | `ip`, `username`, `password`, `outlet` |
| `"SLP"` | `powerSLP` | `ip`, `username`, `password`, `outlet_id`, `port` (23) |

---

## 6. Remote Control

`commonRemoteClass` provides a unified remote-control interface with key mapping.

```python
class commonRemoteClass:
    def sendKey(self, keycode: rcCode, delay=1, repeat=1, randomRepeat=0)
    def setKeyMap(self, name)
    def getKeyMap(self) -> dict
```

**Key codes** are defined in `rcCodes.py` as the `rcCode` enum:
```python
from framework.core.rcCodes import rcCode as rc
rc.ARROW_UP, rc.ARROW_DOWN, rc.OK, rc.BACK, rc.HOME, rc.POWER,
rc.NUM_0 .. rc.NUM_9, rc.RED, rc.GREEN, rc.BLUE, rc.YELLOW, etc.
```

**Remote types:**

| Type | Module | Config fields |
|---|---|---|
| `"olimex"` | `remoteOlimex` | `ip`, `port`, `map`, `config` |
| `"sky_proc"` | `remoteSkyProc` | `map`, `config` |
| `"arduino"` | `remoteArduino` | `map`, `config` |
| `"keySimulator"` | `remoteKeySimulator` | `ip`, `port`, `username`, `password`, `map`, `config` |
| `"redrat"` | `remoteRedRat` | `hub_ip`, `hub_port`, `netbox_ip`, `netbox_name`, `netbox_mac`, `output`, `map`, `config` |
| (default) | `remoteNone` | -- |

**Key mapping** is loaded from a YAML file specified by `config` field. Maps contain named translation tables with a `codes` dict and optional `prefix`. The `map` field selects which mapping to activate.

---

## 7. HDMI-CEC Controller

```python
class HDMICECController:
    def __init__(self, log, config: dict)
    def start(self)
    def stop(self)
    def sendMessage(self, sourceAddress, destAddress, opCode, payload=None)
    def checkMessageReceived(self, sourceAddress, destAddress, opCode,
                              timeout=10, payload=None) -> bool
    def listDevices(self) -> list[dict]
```

**CEC controller types:**

| Type | Config fields |
|---|---|
| `"cec-client"` | `adaptor` (e.g. "/dev/ttyACM0") |
| `"remote-cec-client"` | `adaptor`, `address`, `username`, `password`, `port` (22), `prompt` |
| `"virtual-cec-client"` | `adaptor`, `address`, `username`, `password`, `port`, `prompt`, `control_port` (8080), `device_network_configuration` |

---

## 8. A/V Sync Controller

```python
class AVSyncController:
    def __init__(self, log, config: dict)
    def calibrate(self)
    def start_measurements(self)
    def stop_measurements(self)
    def clear_results(self)
    def get_results(self) -> list[dict]
    # Properties: audio_trigger_level, video_trigger_level, frame_rate, mask_length, offset
```

Config: `type: "SyncOne2"`, `port`, `extended_mode` (bool), `audio_input` ("AUTO"|"EXTERNAL"|"INTERNAL"), `speaker_distance`.

Results dict keys: `milliseconds`, `frames`, `avg_milliseconds`, `avg_frames`, `span_milliseconds`, `span_frames`.

---

## 9. utPlaneController (ut-core Integration)

Sends YAML commands to a ut-controller HTTP endpoint running on the DUT.

```python
class utPlaneController:
    def __init__(self, session, port=8080, log=None)
    def sendMessage(self, yamlInput: str, isFile: bool = False) -> bool
```

Sends via `curl -X POST` to `http://localhost:<port>/api/postKVP`. When `isFile=True`, uses `--data-binary @<path>` for a file on the DUT; otherwise sends the YAML string inline.

---

## 10. Configuration Schemas

### 10.1 Rack Config YAML (the `--config` file)

```yaml
globalConfig:
    includes:
        deviceConfig: "path/to/device_config.yml"  # auto-loaded device config
    local:
        log:
            directory: "./logs"
            delimiter: "/"
    # Optional sections:
    # capture:
    #     ocrEnginePath: "/usr/bin/tesseract"
    #     resolution: "1080p"
    #     input: 0
    # webpageDriver:
    #     <Selenium driver config>

rackConfig:
    rack1:
        name: "rack1"
        description: "my test rack"
        slot1:
            name: "slot1"
            devices:
                - dut:
                    ip: "192.168.1.100"
                    description: "Device under test"
                    platform: "llama"
                    consoles:
                        - default:
                            type: "ssh"          # or "serial" or "telnet"
                            ip: "192.168.1.100"
                            port: 22
                            username: "root"
                            password: ""
                            prompt: "root@device:~#"
                        - serial:
                            type: "serial"
                            port: "/dev/ttyUSB0"
                            baudRate: 115200
                    powerSwitch:
                        type: "kasa"
                        ip: "192.168.1.50"
                        options: "--plug"
                        retryCount: 2
                        retryDelay: 15
                    remoteController:
                        type: "olimex"
                        ip: "192.168.1.60"
                        port: 7
                        map: "llama_rc6"
                        config: "remote_commander.yml"
                    hdmiCECController:
                        type: "cec-client"
                        adaptor: "/dev/ttyACM0"
                    avSyncController:
                        type: "SyncOne2"
                        port: "/dev/ttyACM1"
                    outbound:
                        download_url: "http://server/images/"
                        upload_url: "http://server/uploads/"
                        workspaceDirectory: "~/workspace"
                - pi2:
                    ip: "192.168.1.101"
                    platform: "pi4"
                    consoles:
                        - default:
                            type: "ssh"
                            port: 22
                            username: "pi"
```

### 10.2 Device Config YAML

```yaml
deviceConfig:
    cpe1:
        platform: "llama"
        model: "ModelX"
        prompt: "root@device:~#"
        screenRegions: "path/to/screen_regions.yml"
        validImage:
            baseLocation: "http://images.example.com/"
            image1: "firmware_v1.bin"
            image2: "firmware_v2.bin"
```

The `platform` field links a CPE entry to a device in the rack config.

### 10.3 Config include mechanism

The `configParser.processIncludes()` method supports an `include` key at any level:

```yaml
include:
    - "path/to/extra_config.yml"
    - "https://remote.server/config.yml"
```

Included files are merged into the parent dict. Supports local files and HTTP URLs.

---

## 11. Test Lifecycle

### 11.1 testController style

```
__init__()
  |
  v
run(powerOff=True)
  |-> session.open()
  |-> waitForBoot()
  |-> testPrepareFunction()        # override this
  |-> loop 1..N:
  |     testFunction()             # override this
  |     (break on False or exception)
  |-> testEndFunction(powerOff)    # override for cleanup
```

### 11.2 RAFTUnitTestCase style (unittest)

```python
class MyTest(RAFTUnitTestCase):
    def setUp(self):       # standard unittest setUp
        self.dut.session.open()

    def test_something(self):
        self.dut.session.write("echo hello")
        output = self.dut.session.read_all()
        self.assertIn("hello", output)

    def tearDown(self):    # standard unittest tearDown
        self.dut.session.close()

if __name__ == '__main__':
    RAFTUnitTestMain()
```

`RAFTUnitTestCase` provides `self.log`, `self.devices`, `self.dut`, `self.cpe`, `self.utils` automatically via the `Singleton`.

Run with: `python my_test.py --config rack_config.yml`

---

## 12. CLI Usage

```bash
# testController style
python my_test.py --config rack_config.yml [--rack rack1] [--slot 1] [--debug] [--loop 5]

# unittest style
python my_test.py --config rack_config.yml [--rack rack1] [--slot 1] [--debug]
```

---

## 13. Dependencies (requirements.txt highlights)

| Package | Purpose |
|---|---|
| `paramiko` | SSH console |
| `pyserial` | Serial console |
| `PyYAML` | Config parsing |
| `requests` | HTTP operations, remote YAML loading |
| `python-kasa` | Kasa smart plug control |
| `opencv-python` | Video capture |
| `pytesseract` / `pillow` | OCR |
| `selenium` | Web page control |
| `numpy` | Image processing |
| `fabric` / `invoke` | Remote execution utilities |
| `boto3` | AWS S3 integration |

---

## 14. Common Test Patterns

### 14.1 Basic SSH command execution (testController)

```python
class MyTest(testController):
    def __init__(self):
        super().__init__(testName="my_test", qcId="TC001")

    def testPrepareFunction(self):
        self.session.prompt = self.cpe.get("prompt")
        return True

    def testFunction(self):
        self.log.stepStart("Run command on DUT")
        self.session.write("cat /proc/version")
        output = self.session.read_until(self.session.prompt)
        result = "Linux" in output
        self.log.stepResult(result, "Verify Linux kernel version string")
        return result

    def testEndFunction(self, powerOff=False):
        return super().testEndFunction(powerOff)

if __name__ == "__main__":
    test = MyTest()
    test.run()
```

### 14.2 Power cycle and verify boot

```python
def testFunction(self):
    self.log.stepStart("Power cycle DUT")
    self.powerControl.reboot()
    self.log.step("Wait for device to come back")
    time.sleep(30)
    alive = self.pingTest()
    self.log.stepResult(alive, "DUT responds to ping after reboot")
    return alive
```

### 14.3 Send remote control keys

```python
from framework.core.rcCodes import rcCode as rc

def testFunction(self):
    self.log.stepStart("Navigate to settings menu")
    self.commonRemote.sendKey(rc.HOME, delay=2)
    self.commonRemote.sendKey(rc.ARROW_DOWN, repeat=3, delay=1)
    self.commonRemote.sendKey(rc.OK, delay=2)
    return True
```

### 14.4 HDMI-CEC message exchange

```python
def testFunction(self):
    self.log.stepStart("Send CEC standby and verify acknowledgement")
    self.hdmiCECController.sendMessage("0", "4", "0x36")  # standby
    received = self.hdmiCECController.checkMessageReceived(
        "4", "0", "0x90", timeout=5, payload=["0x01"]
    )
    self.log.stepResult(received, "Device acknowledged standby")
    return received
```

### 14.5 Using utPlaneController

```python
from framework.core.utPlaneController import utPlaneController

def testFunction(self):
    controller = utPlaneController(self.session, port=8080, log=self.log)
    yaml_cmd = "key: value\ncommand: test_start"
    result = controller.sendMessage(yaml_cmd)
    self.log.stepResult(result, "Sent command to ut-controller")
    return result
```

### 14.6 unittest style with assertions

```python
from framework.core.raftUnittest import RAFTUnitTestCase, RAFTUnitTestMain

class TestNetwork(RAFTUnitTestCase):
    def setUp(self):
        self.dut.session.open()

    def test_ping(self):
        self.assertTrue(self.dut.pingTest(), "DUT should be reachable")

    def test_hostname(self):
        self.dut.session.write("hostname")
        output = self.dut.session.read_all()
        self.assertIn("mydevice", output)

    def tearDown(self):
        self.dut.session.close()

if __name__ == "__main__":
    RAFTUnitTestMain()
```

### 14.7 Multiple devices in one slot

```python
# Access non-DUT device
pi_device = self.devices.getDevice("pi2")
pi_session = pi_device.getConsoleSession("default")
pi_session.open()
pi_session.write("ifconfig eth0")
output = pi_session.read_all()
```

### 14.8 Named console access

```python
# Use a specific console on the DUT
serial_session = self.dut.getConsoleSession("serial")
serial_session.open()
serial_session.write("reboot")
```

---

## 15. License

Apache License 2.0. Copyright 2023 RDK Management.
