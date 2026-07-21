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

import time

from raft.framework.plugins.ut_raft.utUserResponse import utUserResponse

from framework.core.commandModules.sshConsole import sshConsole
from framework.core.logModule import logModule
from framework.core.thermalSensorControllerModules.ThermalSensorControllerInterface import ThermalSensorControllerInterface


class programmableThermalChamber(ThermalSensorControllerInterface):
    """
    Thermal controller that drives a programmable chamber through configured
    shell command templates.

    Supported config keys:
            address: optional chamber host/IP for a dedicated SSH control session
            username: SSH username for the chamber session
            password: SSH password for the chamber session
            ssh_port: optional SSH port for the chamber session
            port: accepted as an alias for ssh_port
            prompt: optional shell prompt for the chamber session
      set_temperature_command: optional command template for raw temperature injection
      trigger_state_command: optional command template for direct state changes
      stabilization_delay_seconds: optional wait after sending a command
      prompt_for_confirmation: ask the operator to confirm the chamber action
    """

    DEFAULT_SET_TEMPERATURE_COMMAND = "chamberctl set --temperature {temperatureCelsius}"
    DEFAULT_TRIGGER_STATE_COMMAND = (
        "chamberctl set-state --state {state} --sensor {sensorName}"
    )
    DEFAULT_STABILIZATION_DELAY_SECONDS = 30

    def __init__(self, session, prompt: str = "~#", port: int = 8080, config: dict = None):
        super().__init__(session, prompt, port)
        self.config = config or {}
        self.testUserResponse = utUserResponse(session, prompt)
        self._log = logModule(self.__class__.__name__)
        self._log.setLevel(self._log.INFO)
        self.commandSession = self._createCommandSession(session, prompt)
        self.setTemperatureCommand = self.config.get(
            "set_temperature_command", self.DEFAULT_SET_TEMPERATURE_COMMAND)
        self.triggerStateCommand = self.config.get(
            "trigger_state_command", self.DEFAULT_TRIGGER_STATE_COMMAND)
        self.promptForConfirmation = bool(self.config.get("prompt_for_confirmation", False))
        self.stabilizationDelaySeconds = float(
            self.config.get(
                "stabilization_delay_seconds",
                self.DEFAULT_STABILIZATION_DELAY_SECONDS,
            )
        )

    def _createCommandSession(self, defaultSession, defaultPrompt: str):
        address = self.config.get("address", "")
        if not address:
            return defaultSession

        username = self.config.get("username", "")
        password = self.config.get("password", "")
        sshPort = int(self.config.get("ssh_port", self.config.get("port", 22)))
        sessionPrompt = self.config.get("prompt", defaultPrompt)

        return sshConsole(
            self._log,
            address,
            username,
            password,
            port=sshPort,
            prompt=sessionPrompt,
        )

    def _buildCommand(self, commandTemplate: str, state: str = "", sensorName: str = "",
                      temperatureCelsius: float = 0.0, timestampMonotonicMs: int = 0) -> str:
        if not commandTemplate:
            return ""
        return commandTemplate.format(
            state=state,
            sensorName=sensorName,
            temperatureCelsius=temperatureCelsius,
            timestampMonotonicMs=timestampMonotonicMs,
            port=self.port,
        ).strip()

    def _sendCommand(self, commandTemplate: str, state: str = "", sensorName: str = "",
                     temperatureCelsius: float = 0.0, timestampMonotonicMs: int = 0) -> bool:
        command = self._buildCommand(
            commandTemplate,
            state=state,
            sensorName=sensorName,
            temperatureCelsius=temperatureCelsius,
            timestampMonotonicMs=timestampMonotonicMs,
        )
        if not command:
            return False

        self.commandSession.write(command)
        if self.stabilizationDelaySeconds > 0:
            time.sleep(self.stabilizationDelaySeconds)
        return True

    def _confirm(self, message: str) -> bool:
        if not self.promptForConfirmation:
            return True
        return self.testUserResponse.getUserYN(message)

    def triggerThermalStateChange(self, state: str, sensorName: str = "",
                                  temperatureCelsius: float = 0.0,
                                  timestampMonotonicMs: int = 0):
        if timestampMonotonicMs == 0:
            timestampMonotonicMs = int(time.time() * 1000)

        if self._sendCommand(
            self.triggerStateCommand,
            state=state,
            sensorName=sensorName,
            temperatureCelsius=temperatureCelsius,
            timestampMonotonicMs=timestampMonotonicMs,
        ):
            return self._confirm(
                f"Verify the chamber drove state '{state}' for sensor '{sensorName}'. Continue? (Y/N):"
            )

        if self._sendCommand(
            self.setTemperatureCommand,
            state=state,
            sensorName=sensorName,
            temperatureCelsius=temperatureCelsius,
            timestampMonotonicMs=timestampMonotonicMs,
        ):
            return self._confirm(
                f"Verify the chamber reached {temperatureCelsius} Celsius for sensor '{sensorName}'. Continue? (Y/N):"
            )

        return self.testUserResponse.getUserYN(
            f"No programmable chamber command is configured for state '{state}'. "
            f"Apply it manually for sensor '{sensorName}' and continue? (Y/N):"
        )

    def injectTemperatureUpdate(self, sensorName: str, temperatureCelsius: float,
                                timestampMonotonicMs: int = 0):
        if timestampMonotonicMs == 0:
            timestampMonotonicMs = int(time.time() * 1000)

        if self._sendCommand(
            self.setTemperatureCommand,
            sensorName=sensorName,
            temperatureCelsius=temperatureCelsius,
            timestampMonotonicMs=timestampMonotonicMs,
        ):
            return self._confirm(
                f"Verify the chamber reached {temperatureCelsius} Celsius for sensor '{sensorName}'. Continue? (Y/N):"
            )

        return self.testUserResponse.getUserYN(
            f"No programmable chamber command is configured. Set sensor '{sensorName}' "
            f"to {temperatureCelsius} Celsius manually and continue? (Y/N):"
        )