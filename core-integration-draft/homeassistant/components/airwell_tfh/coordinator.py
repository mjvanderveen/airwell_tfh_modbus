"""DataUpdateCoordinator that polls the Airwell TFH controller."""

from __future__ import annotations

import logging

from airwell_tfh_modbus import AirwellTFH
from modbus_connection import ModbusError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

type AirwellTFHConfigEntry = ConfigEntry[AirwellTFHCoordinator]


class AirwellTFHCoordinator(DataUpdateCoordinator[AirwellTFH]):
    """Refreshes every sub-system on a schedule.

    The ``modbus_connection`` entry owns the connection; this coordinator only reads.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        entry: AirwellTFHConfigEntry,
        device: AirwellTFH,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=SCAN_INTERVAL,
        )
        self.device = device

    async def _async_update_data(self) -> AirwellTFH:
        """Poll every sub-system of the device."""
        try:
            await self.device.async_update()
        except ModbusError as err:
            raise UpdateFailed(f"Error communicating with Airwell TFH: {err}") from err
        return self.device
