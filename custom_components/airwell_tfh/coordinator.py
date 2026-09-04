"""DataUpdateCoordinator for airwell_tfh."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from modbus_connection import ModbusError

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .airwell_tfh_modbus import AirwellTFH
    from .data import AirwellTFHConfigEntry

# A domestic hot water heat pump changes slowly, but we poll aggressively and fixed.
SCAN_INTERVAL = timedelta(seconds=30)


class AirwellTFHDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the controller."""

    config_entry: AirwellTFHConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: AirwellTFHConfigEntry,
        device: AirwellTFH,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
            config_entry=config_entry,
        )
        self.device = device

    async def _async_update_data(self) -> Any:
        """Poll every sub-system of the device."""
        try:
            await self.device.async_update()
        except ModbusError as exception:
            raise UpdateFailed(exception) from exception
        return self.device
