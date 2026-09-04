"""airwell_tfh_modbus — vendored copy for the airwell_tfh HACS custom integration.

This is a verbatim copy of the standalone ``airwell-tfh-modbus`` device
library (see the sibling ``airwell-tfh-modbus`` project), bundled here so
this custom component installs cleanly via HACS without depending on an
unpublished PyPI package. Do not edit this sub-package directly — port
changes to the standalone library first, then re-vendor.

Construct ``AirwellTFH(unit)`` with a ``modbus_connection.ModbusUnit``, call
``await device.async_update()``, then read its sub-systems as plain Python
objects::

    device.sensors.water_tank_temperature
    device.controller.operation_mode
    device.relays.compressor
"""

from __future__ import annotations

from .device import AirwellTFH
from .device_info import DeviceInformation
from .enums import AlarmCode1, AlarmCode2, ControllerStatus, OperationMode
from .subsystems import Alarms, Controller, Relays, Sensors, Settings

__all__ = [
    "AirwellTFH",
    "AlarmCode1",
    "AlarmCode2",
    "Alarms",
    "Controller",
    "ControllerStatus",
    "DeviceInformation",
    "OperationMode",
    "Relays",
    "Sensors",
    "Settings",
]
