"""Select platform for airwell_tfh — the user-selectable operating mode."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.select import SelectEntity, SelectEntityDescription

from .airwell_tfh_modbus import OperationMode
from .entity import AirwellTFHEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AirwellTFHDataUpdateCoordinator
    from .data import AirwellTFHConfigEntry

_MODE_OPTIONS = [mode.name.lower() for mode in OperationMode]

ENTITY_DESCRIPTION = SelectEntityDescription(
    key="operation_mode",
    name="Operating mode",
    options=_MODE_OPTIONS,
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AirwellTFHConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    async_add_entities([AirwellTFHModeSelect(entry.runtime_data.coordinator)])


class AirwellTFHModeSelect(AirwellTFHEntity, SelectEntity):
    """The controller's Auto / Eco / Electric heater / Sterilization mode."""

    entity_description = ENTITY_DESCRIPTION

    def __init__(self, coordinator: AirwellTFHDataUpdateCoordinator) -> None:
        """Initialize the select class."""
        super().__init__(coordinator, ENTITY_DESCRIPTION.key, "controller")

    @property
    def current_option(self) -> str | None:
        """Return the current mode."""
        mode = self._subsystem.operation_mode
        return mode.name.lower() if mode is not None else None

    async def async_select_option(self, option: str) -> None:
        """Write the new mode and refresh."""
        await self._subsystem.write("operation_mode", OperationMode[option.upper()])
        await self.coordinator.async_request_refresh()
