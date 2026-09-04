"""Binary sensor platform — relay and alarm-contact states."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AirwellTFHConfigEntry, AirwellTFHCoordinator
from .entity import AirwellTFHEntity


@dataclass(frozen=True, kw_only=True)
class AirwellTFHBinaryDescription(BinarySensorEntityDescription):
    """Describes a binary sensor reading one coil or discrete input of one component."""

    component: str
    attribute: str


def _binary(
    component: str,
    attribute: str,
    name: str,
    device_class: BinarySensorDeviceClass | None = None,
    *,
    diagnostic: bool = True,
) -> AirwellTFHBinaryDescription:
    return AirwellTFHBinaryDescription(
        key=f"{component}_{attribute}",
        name=name,
        component=component,
        attribute=attribute,
        device_class=device_class,
        entity_category=EntityCategory.DIAGNOSTIC if diagnostic else None,
    )


_BINARY_SENSORS: tuple[AirwellTFHBinaryDescription, ...] = (
    _binary(
        "relays", "compressor", "Compressor", BinarySensorDeviceClass.RUNNING, diagnostic=False
    ),
    _binary(
        "relays",
        "electric_heater",
        "Electric heater",
        BinarySensorDeviceClass.RUNNING,
        diagnostic=False,
    ),
    _binary("relays", "four_way_valve", "Four-way valve", BinarySensorDeviceClass.RUNNING),
    _binary("relays", "fan", "Fan", BinarySensorDeviceClass.RUNNING),
    _binary("alarms", "high_pressure", "High pressure alarm", BinarySensorDeviceClass.PROBLEM),
    _binary("alarms", "low_pressure", "Low pressure alarm", BinarySensorDeviceClass.PROBLEM),
    _binary("alarms", "condensation", "Condensation alarm", BinarySensorDeviceClass.PROBLEM),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AirwellTFHConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Airwell TFH binary sensors."""
    coordinator = entry.runtime_data
    async_add_entities(AirwellTFHBinarySensor(coordinator, d) for d in _BINARY_SENSORS)


class AirwellTFHBinarySensor(AirwellTFHEntity, BinarySensorEntity):
    """A single coil or discrete input read from a component attribute."""

    entity_description: AirwellTFHBinaryDescription

    def __init__(
        self, coordinator: AirwellTFHCoordinator, description: AirwellTFHBinaryDescription
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, description.key, description.component)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return true if the coil/discrete input is set."""
        return getattr(self._subsystem, self.entity_description.attribute)
