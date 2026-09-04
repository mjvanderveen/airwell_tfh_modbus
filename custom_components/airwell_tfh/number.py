"""Number platform for airwell_tfh — writable holding-register setpoints.

Range comments mark values this project could not confirm against a
manufacturer register table and derived instead from a live installation's
own Home Assistant helpers or from general heat-pump-water-heater practice.
Adjust them to your controller's documented limits before relying on them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import EntityCategory, UnitOfTemperature, UnitOfTime

from .entity import AirwellTFHEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AirwellTFHDataUpdateCoordinator
    from .data import AirwellTFHConfigEntry


@dataclass(frozen=True, kw_only=True)
class AirwellTFHNumberDescription(NumberEntityDescription):
    """Describes a number entity writing one Settings holding register."""

    attribute: str


ENTITY_DESCRIPTIONS: tuple[AirwellTFHNumberDescription, ...] = (
    AirwellTFHNumberDescription(
        key="target_temperature",
        name="Target temperature",
        attribute="target_temperature",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=30,
        native_max_value=75,
        native_step=1,
        mode=NumberMode.BOX,
    ),
    AirwellTFHNumberDescription(
        key="temperature_difference",
        name="Temperature hysteresis",
        attribute="temperature_difference",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=1,
        native_max_value=20,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="stop_ambient_temperature",
        name="Stop ambient temperature",
        attribute="stop_ambient_temperature",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=-20,
        native_max_value=30,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="max_heatpump_temperature",
        name="Max heat pump temperature",
        attribute="max_heatpump_temperature",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=40,
        native_max_value=75,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="electric_heater_start_temperature",
        name="Electric heater start temperature",
        attribute="electric_heater_start_temperature",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=0,
        native_max_value=75,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="sterilization_cycle_hours",
        name="Sterilization cycle interval",
        attribute="sterilization_cycle_hours",
        native_unit_of_measurement=UnitOfTime.HOURS,
        native_min_value=1,
        native_max_value=720,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="temperature_correction",
        name="Water tank sensor correction",
        attribute="temperature_correction",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=-10,
        native_max_value=10,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="compressor_start_delay",
        name="Compressor start delay",
        attribute="compressor_start_delay",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        native_min_value=0,
        native_max_value=30,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="defrost_start_temperature",
        name="Defrost start temperature",
        attribute="defrost_start_temperature",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=-30,
        native_max_value=10,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="defrost_finish_temperature",
        name="Defrost finish temperature",
        attribute="defrost_finish_temperature",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=-10,
        native_max_value=30,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="defrost_start_time",
        name="Defrost start time",
        attribute="defrost_start_time",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        native_min_value=0,
        native_max_value=120,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="defrost_max_time",
        name="Defrost max time",
        attribute="defrost_max_time",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        native_min_value=1,
        native_max_value=30,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    AirwellTFHNumberDescription(
        key="electric_heater_mode",
        name="Electric heater mode (raw)",
        attribute="electric_heater_mode",
        native_min_value=0,
        native_max_value=10,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AirwellTFHConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(AirwellTFHNumber(coordinator, d) for d in ENTITY_DESCRIPTIONS)


class AirwellTFHNumber(AirwellTFHEntity, NumberEntity):
    """A single writable holding register on the Settings component."""

    entity_description: AirwellTFHNumberDescription

    def __init__(
        self,
        coordinator: AirwellTFHDataUpdateCoordinator,
        entity_description: AirwellTFHNumberDescription,
    ) -> None:
        """Initialize the number class."""
        super().__init__(coordinator, entity_description.key, "settings")
        self.entity_description = entity_description

    @property
    def native_value(self) -> float | None:
        """Return the current setpoint."""
        return getattr(self._subsystem, self.entity_description.attribute)

    async def async_set_native_value(self, value: float) -> None:
        """Write the new setpoint and refresh."""
        await self._subsystem.write(self.entity_description.attribute, int(value))
        await self.coordinator.async_request_refresh()
