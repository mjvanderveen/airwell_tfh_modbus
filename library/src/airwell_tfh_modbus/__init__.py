"""airwell-tfh-modbus — read and control an Airwell TFH-series heat pump water heater over Modbus.

Covers the TFHA, TFHW, TFHX and TFHZ model families, which share one Modbus
register map.

Construct :class:`AirwellTFH` with a ``modbus_connection.ModbusUnit``, call
``await device.async_update()``, then read its sub-systems as plain Python
objects::

    device.sensors.water_tank_temperature
    device.controller.operation_mode
    device.relays.compressor

Write a setting or the operating mode with ``await component.write(name, value)``,
e.g. ``await device.controller.write("operation_mode", OperationMode.ECO)``.

Sub-systems live in :mod:`airwell_tfh_modbus.subsystems`. Controller identity
lives in :mod:`airwell_tfh_modbus.device_info`. The public sub-system classes
remain available while :class:`AirwellTFH` exposes stable, named slots.
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
