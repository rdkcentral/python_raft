#!/usr/bin/env python3
#** *****************************************************************************
# *
# * Copyright 2026 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# * http://www.apache.org/licenses/LICENSE-2.0
# *
#* ******************************************************************************

from framework.core.thermalSensorControllerModules.actualThermalSensorController import actualThermalSensorController
from framework.core.thermalSensorControllerModules.programmableThermalChamber import programmableThermalChamber
from framework.core.thermalSensorControllerModules.smartSwitchThermalController import smartSwitchThermalController
from framework.core.thermalSensorControllerModules.virtualThermalSensorController import virtualThermalSensorController


class ThermalSensorController:
    """
    Factory class that selects the appropriate thermal sensor implementation.

    The first argument may be either the legacy platform string or a controller
    configuration dictionary from the rack config. This keeps the existing
    vDevice flow intact while allowing explicit controller types such as a
    programmable thermal chamber.
    """

    VIRTUAL_CONTROLLER_TYPES = {
        "vdevice",
        "virtual",
        "virtual-thermalsensor-client",
    }

    PROGRAMMABLE_CHAMBER_TYPES = {
        "programmable-thermal-chamber",
        "thermal-chamber",
        "chamber",
    }

    SMART_SWITCH_CONTROLLER_TYPES = {
        "smartswitch_thermalcontroller",
        "smartswitch-thermalcontroller",
        "smart-switch-thermalcontroller",
    }

    ACTUAL_CONTROLLER_TYPES = {
        "actual",
        "actual-thermalsensor-client",
        "hardware",
        "manual",
    }

    def __new__(cls, controllerConfig, session, prompt: str = "~#", port: int = 8080):
        controllerType, controllerSettings, prompt, port = cls._normaliseControllerConfig(
            controllerConfig, prompt, port)
        if controllerType in cls.VIRTUAL_CONTROLLER_TYPES:
            return virtualThermalSensorController(session, prompt, port)
        if controllerType in cls.PROGRAMMABLE_CHAMBER_TYPES:
            return programmableThermalChamber(session, prompt, port, controllerSettings)
        if controllerType in cls.SMART_SWITCH_CONTROLLER_TYPES:
            return smartSwitchThermalController(session, prompt, port, controllerSettings)
        return actualThermalSensorController(session, prompt, port)

    @classmethod
    def _normaliseControllerConfig(cls, controllerConfig, prompt: str, port: int):
        if isinstance(controllerConfig, dict):
            controllerSettings = dict(controllerConfig)
            controllerType = str(
                controllerSettings.get("type") or controllerSettings.get("platform") or ""
            ).strip().lower()
            prompt = controllerSettings.get("prompt", prompt)
            port = controllerSettings.get(
                "control_port",
                controllerSettings.get("port", port),
            )
            return controllerType, controllerSettings, prompt, port

        controllerType = str(controllerConfig or "").strip().lower()
        return controllerType, {}, prompt, port
