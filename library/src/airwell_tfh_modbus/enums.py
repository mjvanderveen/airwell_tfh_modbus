"""Enumerations decoded from Airwell TFH controller registers.

The numeric values below are reverse-engineered from an installer's own,
already-working Home Assistant Modbus configuration for a TFHA 300L unit
(templates that translated the raw register values into human-readable
labels), not from an official Airwell Modbus register table. They match the
"Modbus Table TFHW/TFHX/TFHZ" family this device shares its register map
with. Treat any value not listed here as unknown rather than assuming it
does not occur.
"""

from __future__ import annotations

from enum import IntEnum


class ControllerStatus(IntEnum):
    """Overall controller state machine position (holding register 1101)."""

    POWER_OFF = 0
    STANDBY = 1
    PREHEATING = 2
    HEATING = 3
    BEFORE_DEFROST = 4
    DEFROSTING = 5
    AFTER_DEFROST = 6
    ADDING_REFRIGERANT = 7
    ALARM = 8


class OperationMode(IntEnum):
    """User-selectable operating mode (holding register 1104, writable)."""

    AUTO = 0
    ECO = 1
    ELECTRIC_HEATER = 2
    STERILIZATION = 3


class AlarmCode1(IntEnum):
    """Primary alarm code (holding register 1102)."""

    NONE = 0
    HIGH_PRESSURE = 1
    LOW_PRESSURE = 2
    TEMPERATURE_SENSOR_FAULT = 3


class AlarmCode2(IntEnum):
    """Secondary alarm code (holding register 1103)."""

    NONE = 0
    WATER_TANK_SENSOR_FAULT = 1
    AMBIENT_SENSOR_FAULT = 2
    DEFROST_FAULT = 3
