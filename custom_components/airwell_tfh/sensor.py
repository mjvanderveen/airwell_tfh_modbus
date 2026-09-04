"""Sensor platform for airwell_tfh — diagnostic readings."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory, UnitOfTemperature

from .airwell_tfh_modbus import AlarmCode1, AlarmCode2, ControllerStatus
from .entity import AirwellTFHEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AirwellTFHDataUpdateCoordinator
    from .data import AirwellTFHConfigEntry


@dataclass(frozen=True, kw_only=True)
class AirwellTFHSensorDescription(SensorEntityDescription):
    """Describes a sensor reading one attribute of one component."""

    component: str
    attribute: str


def _temp(
    component: str, attribute: str, name: str, *, enabled: bool = True
) -> AirwellTFHSensorDescription:
    return AirwellTFHSensorDescription(
        key=f"{component}_{attribute}",
        name=name,
        component=component,
        attribute=attribute,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=enabled,
    )


def _enum(
    component: str, attribute: str, name: str, options: list[str]
) -> AirwellTFHSensorDescription:
    return AirwellTFHSensorDescription(
        key=f"{component}_{attribute}",
        name=name,
        component=component,
        attribute=attribute,
        device_class=SensorDeviceClass.ENUM,
        options=options,
        entity_category=EntityCategory.DIAGNOSTIC,
    )


_STATUS_OPTIONS = [status.name.lower() for status in ControllerStatus]
_ALARM_1_OPTIONS = [code.name.lower() for code in AlarmCode1]
_ALARM_2_OPTIONS = [code.name.lower() for code in AlarmCode2]

ENTITY_DESCRIPTIONS: tuple[AirwellTFHSensorDescription, ...] = (
    _temp("sensors", "water_tank_temperature", "Water tank temperature"),
    _temp("sensors", "defrost_temperature", "Defrost temperature", enabled=False),
    _temp("sensors", "ambient_temperature", "Ambient temperature"),
    _temp("sensors", "exhaust_temperature", "Exhaust gas temperature", enabled=False),
    _temp("sensors", "return_gas_temperature", "Return gas temperature", enabled=False),
    _enum("controller", "controller_status", "Controller status", _STATUS_OPTIONS),
    _enum("controller", "alarm_register_1", "Alarm 1", _ALARM_1_OPTIONS),
    _enum("controller", "alarm_register_2", "Alarm 2", _ALARM_2_OPTIONS),
    AirwellTFHSensorDescription(
        key="controller_eev_opening",
        name="EEV opening",
        component="controller",
        attribute="eev_opening",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AirwellTFHConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(AirwellTFHSensor(coordinator, d) for d in ENTITY_DESCRIPTIONS)


class AirwellTFHSensor(AirwellTFHEntity, SensorEntity):
    """A single value read from a component attribute."""

    entity_description: AirwellTFHSensorDescription

    def __init__(
        self,
        coordinator: AirwellTFHDataUpdateCoordinator,
        entity_description: AirwellTFHSensorDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, entity_description.key, entity_description.component)
        self.entity_description = entity_description

    @property
    def native_value(self) -> object:
        """Return the current value, mapping enums to their lowercase name."""
        value = getattr(self._subsystem, self.entity_description.attribute)
        if isinstance(value, IntEnum):
            return value.name.lower()
        return value
