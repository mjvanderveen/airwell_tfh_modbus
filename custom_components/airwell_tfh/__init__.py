"""
Custom integration to integrate Airwell TFH with Home Assistant.

Vendors its own copy of the `airwell-tfh-modbus` device library (see the
`airwell_tfh_modbus/` sub-package) so this installs cleanly via HACS without
depending on an unpublished PyPI package or Home Assistant's (not yet
released) `modbus_connection` shared-connection integration. This
integration therefore owns its Modbus connection directly, one per config
entry.

For more details about this integration, please refer to
https://github.com/mjvanderveen/airwell_tfh_modbus
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.loader import async_get_loaded_integration
from modbus_connection import ModbusTcpParams
from modbus_connection.tmodbus import ModbusConnection

from .airwell_tfh_modbus import AirwellTFH
from .const import CONF_UNIT_ID
from .coordinator import AirwellTFHDataUpdateCoordinator
from .data import AirwellTFHData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import AirwellTFHConfigEntry

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: AirwellTFHConfigEntry) -> bool:
    """Set up this integration using UI."""
    connection = ModbusConnection(
        ModbusTcpParams(host=entry.data[CONF_HOST], port=entry.data[CONF_PORT], framer="rtu"),
    )
    unit = connection.for_unit(int(entry.data[CONF_UNIT_ID]))
    device = AirwellTFH(unit)

    coordinator = AirwellTFHDataUpdateCoordinator(
        hass=hass,
        config_entry=entry,
        device=device,
    )

    entry.runtime_data = AirwellTFHData(
        connection=connection,
        coordinator=coordinator,
        integration=async_get_loaded_integration(hass, entry.domain),
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: AirwellTFHConfigEntry) -> bool:
    """Handle removal of an entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.connection.close()
    return unloaded
