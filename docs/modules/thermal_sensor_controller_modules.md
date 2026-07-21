# Thermal Sensor Controller Modules

**Directory:** `framework/core/thermalSensorControllerModules`

**Purpose:**

The thermal sensor controller modules provide a pluggable set of implementations for simulating or interacting with thermal sensor hardware during L3 testing. Each implementation conforms to a common interface, allowing the factory (`ThermalSensorController`) to select the appropriate backend based on rack configuration without any changes to test logic.

---

**Key Classes:**

* **ThermalSensorControllerInterface** (`ThermalSensorControllerInterface.py`):
   * Abstract base class that all thermal sensor controller implementations must inherit.
   * Defines the two mandatory methods:
      * `triggerThermalStateChange(state, sensorName, temperatureCelsius, timestampMonotonicMs)` — directly commands a state transition.
      * `injectTemperatureUpdate(sensorName, temperatureCelsius, timestampMonotonicMs)` — injects a raw temperature reading and lets the vcomponent derive the state.

* **virtualThermalSensorController** (`virtualThermalSensorController.py`):
   * Used in vDevice (software-only) test flows.
   * Posts YAML command payloads to the vcomponent control-plane endpoint (`/api/postKVP`).
   * See [`thermalSensorControllerModules/virtual_commands.md`](thermalSensorControllerModules/virtual_commands.md) for full YAML payload definitions.

* **actualThermalSensorController** (`actualThermalSensorController.py`):
   * Used for real hardware flows where thermal events are raised by platform firmware.
   * Prompts the test operator via `utUserResponse` to manually trigger the required thermal condition and confirm the result.

* **programmableThermalChamber** (`programmableThermalChamber.py`):
   * Drives a programmable thermal chamber through configured shell command templates.
   * Supports a dedicated SSH control session to the chamber if an `address` is provided.

* **smartSwitchThermalController** (`smartSwitchThermalController.py`):
   * Controls a heater or blower via a smart power switch (Kasa, Tapo, APC, etc.) using the RAFT `powerControlClass` abstraction.
   * Timed heating/cooling pulses are derived from per-sensor configuration keys such as `heating_duration_seconds` and `seconds_per_degree_celsius`.

---

**How to Use:**

1. **Rack Configuration:** Add a `thermalSensorController` block to the device entry in the rack YAML:

   ```yaml
   thermalSensorController:
     type: virtual           # vdevice | actual | programmable-thermal-chamber | smartswitch_thermalcontroller
     control_port: 8081
   ```

2. **Initialization:** The helper class instantiates `ThermalSensorController` (factory in `thermalSensorController.py`), which resolves the correct implementation automatically.

3. **Triggering Events in Tests:**

   ```python
   # Inject a temperature reading (vDevice flow)
   self.thermalSensorDevice.injectTemperatureUpdate(
       sensorName="SoC Die",
       temperatureCelsius=100.0)

   # Force a direct state transition
   self.thermalSensorDevice.triggerThermalStateChange(
       state="CRITICAL_TEMPERATURE_EXCEEDED",
       sensorName="SoC Die",
       temperatureCelsius=97.0)
   ```

---

**Related Documents:**

* [`thermalSensorControllerModules/virtual_commands.md`](thermalSensorControllerModules/virtual_commands.md) — YAML payload reference for the virtual controller.
