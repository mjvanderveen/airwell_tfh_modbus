"""The Airwell TFH heat pump water heater integration.

SPECULATIVE / NOT CURRENTLY FUNCTIONAL: this depends on
``homeassistant.components.modbus_connection``, which core added on
2026-07-05 (#175407) and removed again on 2026-07-16 (#176618). It is not
present in current core. For something installable today, use the
vendorized, connection-owning version in ``../../../custom_components/airwell_tfh``
instead.

Airwell TFH is a Modbus device. This integration does not own its
connection: it borrows a ``ModbusUnit`` from a ``modbus_connection`` config
entry (chosen in the config flow) and hands it to the ``airwell_tfh_modbus``
library. The ``modbus_connection`` entry owns the connection lifecycle; this
integration reloads when the connection drops so it re-borrows on the
rebuilt connection.
"""

from __future__ import annotations

from airwell_tfh_modbus import AirwellTFH

from homeassistant.components.modbus_connection import async_get_unit
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_CONNECTION, CONF_UNIT_ID
from .coordinator import AirwellTFHConfigEntry, AirwellTFHCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: AirwellTFHConfigEntry) -> bool:
    """Set up Airwell TFH from a config entry.

    ``async_get_unit`` raises ``ConnectionNotReady`` (a ``ConfigEntryNotReady``)
    if the shared connection is missing or not loaded; letting it propagate
    gives Home Assistant's setup retry.
    """
    unit = async_get_unit(hass, entry.data[CONF_CONNECTION], int(entry.data[CONF_UNIT_ID]))
    device = AirwellTFH(unit)
    coordinator = AirwellTFHCoordinator(hass, entry, device)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    # The borrowed unit is bound to modbus_connection's current connection.
    # When that connection drops, modbus_connection rebuilds it; reload so
    # we re-borrow a unit on the fresh connection instead of holding a dead one.
    entry.async_on_unload(
        unit.on_connection_lost(
            lambda: hass.config_entries.async_schedule_reload(entry.entry_id)
        )
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: AirwellTFHConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
