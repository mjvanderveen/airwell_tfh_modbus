"""Switch platform for airwell_tfh — writable boolean holding registers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import EntityCategory

from .entity import AirwellTFHEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AirwellTFHDataUpdateCoordinator
    from .data import AirwellTFHConfigEntry


@dataclass(frozen=True, kw_only=True)
class AirwellTFHSwitchDescription(SwitchEntityDescription):
    """Describes a switch writing one boolean Settings holding register."""

    attribute: str


ENTITY_DESCRIPTIONS: tuple[AirwellTFHSwitchDescription, ...] = (
    AirwellTFHSwitchDescription(
        key="sterilization_heater_enable",
        name="Sterilization enabled",
        attribute="sterilization_heater_enable",
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHSwitchDescription(
        key="econ_mode_heater_enable",
        name="Eco mode backup heater enabled",
        attribute="econ_mode_heater_enable",
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHSwitchDescription(
        key="heatpump_enable",
        name="Heat pump enabled",
        attribute="heatpump_enable",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AirwellTFHConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(AirwellTFHSwitch(coordinator, d) for d in ENTITY_DESCRIPTIONS)


class AirwellTFHSwitch(AirwellTFHEntity, SwitchEntity):
    """A single writable boolean register on the Settings component."""

    entity_description: AirwellTFHSwitchDescription

    def __init__(
        self,
        coordinator: AirwellTFHDataUpdateCoordinator,
        entity_description: AirwellTFHSwitchDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator, entity_description.key, "settings")
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool | None:
        """Return true if the register is set."""
        return getattr(self._subsystem, self.entity_description.attribute)

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        await self._subsystem.write(self.entity_description.attribute, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        await self._subsystem.write(self.entity_description.attribute, False)
        await self.coordinator.async_request_refresh()
