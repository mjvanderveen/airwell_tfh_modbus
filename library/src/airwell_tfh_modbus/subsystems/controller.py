"""Controller-wide status, alarm codes, and operating mode (holding registers 1101-1106)."""

from __future__ import annotations

from modbus_connection.model import Component, enum, integer

from ..enums import AlarmCode1, AlarmCode2, ControllerStatus, OperationMode


class Controller(Component):
    """Read-only status plus the writable operating-mode selector."""

    controller_status = enum(1101, ControllerStatus, signed=False)
    """Overall state machine position."""

    alarm_register_1 = enum(1102, AlarmCode1, signed=False)
    """Primary active alarm, if any."""

    alarm_register_2 = enum(1103, AlarmCode2, signed=False)
    """Secondary active alarm, if any."""

    operation_mode = enum(1104, OperationMode, signed=False, writable=True)
    """User-selected operating mode."""

    eev_opening = integer(1106, signed=False)
    """Electronic expansion valve position. Raw units (percentage vs. steps) not documented."""
