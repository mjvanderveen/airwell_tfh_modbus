"""Select platform — the user-selectable operating mode."""

from __future__ import annotations

from airwell_tfh_modbus import OperationMode

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AirwellTFHConfigEntry, AirwellTFHCoordinator
from .entity import AirwellTFHEntity

_MODE_OPTIONS = [mode.name.lower() for mode in OperationMode]

_DESCRIPTION = SelectEntityDescription(
    key="operation_mode",
    name="Operating mode",
    options=_MODE_OPTIONS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AirwellTFHConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Airwell TFH operating-mode select entity."""
    async_add_entities([AirwellTFHModeSelect(entry.runtime_data)])


class AirwellTFHModeSelect(AirwellTFHEntity, SelectEntity):
    """The controller's Auto / Eco / Electric heater / Sterilization mode."""

    entity_description = _DESCRIPTION

    def __init__(self, coordinator: AirwellTFHCoordinator) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator, _DESCRIPTION.key, "controller")

    @property
    def current_option(self) -> str | None:
        """Return the current mode."""
        mode = self._subsystem.operation_mode
        return mode.name.lower() if mode is not None else None

    async def async_select_option(self, option: str) -> None:
        """Write the new mode and refresh."""
        await self._subsystem.write("operation_mode", OperationMode[option.upper()])
        await self.coordinator.async_request_refresh()
