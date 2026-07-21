# Thermal Sensor YAML Command Definitions

**Directory:** `framework/core/thermalSensorControllerModules`

## Overview

This document consolidates Thermal Sensor YAML command definitions used by the virtual controller (`virtualThermalSensorController`). The payloads are posted to the vcomponent control-plane endpoint (`/api/postKVP`) with top-level node `IThermalSensor`.

---

## 1. temperature_update

### Purpose

This command injects a raw temperature reading. The vcomponent evaluates per-sensor thresholds and automatically emits thermal state transitions. This is the supported control-plane command for thermal event simulation.

### YAML Content

```yaml
IThermalSensor:
  command: temperature_update
  sensorName: SoC Die
  temperatureCelsius: 100.0
  timestampMonotonicMs: 1710000000000
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `command` | string | Must be `temperature_update`. |
| `sensorName` | string | Sensor name providing the reading. |
| `temperatureCelsius` | float | Temperature value in Celsius. |
| `timestampMonotonicMs` | int | Reading timestamp in milliseconds. |

### Auto-transition Behavior

Based on current state and configured thresholds, `temperature_update` drives transitions such as:

- `NORMAL` → `CRITICAL_TEMPERATURE_EXCEEDED`
- `CRITICAL_TEMPERATURE_EXCEEDED` → `CRITICAL_TEMPERATURE_RECOVERED`
- `CRITICAL_TEMPERATURE_RECOVERED` → `NORMAL`
- `CRITICAL_TEMPERATURE_EXCEEDED` or `CRITICAL_TEMPERATURE_RECOVERED` → `CRITICAL_SHUTDOWN_IMMINENT`

> **Note:** Once in `CRITICAL_SHUTDOWN_IMMINENT`, recovery is intentionally suppressed by policy.

---

## Summary

Thermal Sensor controller uses one YAML command payload:

- **Temperature Update (`temperature_update`)**: Threshold logic computes transitions automatically.

These definitions are used for thermal event simulation and validation in vDevice test flows.
