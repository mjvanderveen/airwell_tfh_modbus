"""The top-level Airwell TFH device object."""

from __future__ import annotations

from typing import TYPE_CHECKING

from modbus_connection.model import ComponentGroup

from .device_info import DeviceInformation
from .subsystems import Alarms, Controller, Relays, Sensors, Settings

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit


class AirwellTFH:
    """An Airwell TFHA/TFHW/TFHX/TFHZ heat pump water heater, reached through a ``ModbusUnit``."""

    def __init__(self, unit: ModbusUnit) -> None:
        """Construct every sub-system against the given unit."""
        self._unit = unit
        self.info = DeviceInformation(unit)
        self.sensors = Sensors(unit)
        self.relays = Relays(unit)
        self.alarms = Alarms(unit)
        self.settings = Settings(unit)
        self.controller = Controller(unit)

        # One device, one register map: everything pools into as few reads
        # as the planner can manage, regardless of the gap between e.g.
        # holding registers 10-33 and 1101-1106.
        self._group = ComponentGroup(unit, list(self.components))
        self._identity_read = False

    @property
    def components(self) -> tuple[Sensors, Relays, Alarms, Settings, Controller]:
        """Return every actively polled subsystem."""
        return (self.sensors, self.relays, self.alarms, self.settings, self.controller)

    async def async_update(self) -> None:
        """Refresh identity (once) and every polled sub-system."""
        if not self._identity_read:
            await self.info.async_update()
            self._identity_read = True
        await self._group.async_update()

    async def async_read_raw(self) -> dict[str, dict[int, int | bool]]:
        """Every register this device reads, undecoded — for diagnostics."""
        raw: dict[str, dict[int, int | bool]] = {}
        for component in (self.info, *self.components):
            read = await component.async_read_raw(notify=False)
            for space, values in read.items():
                raw.setdefault(space, {}).update(values)
        return raw
