"""AirwellTFHEntity class.

The controller is a single physical device — every entity attaches to it
directly; there are no sub-devices.
"""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import AirwellTFHDataUpdateCoordinator


class AirwellTFHEntity(CoordinatorEntity[AirwellTFHDataUpdateCoordinator]):
    """Common identity and device-info for every airwell_tfh entity."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(
        self, coordinator: AirwellTFHDataUpdateCoordinator, key: str, component: str
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._component = component
        entry = coordinator.config_entry
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        info = coordinator.device.info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer=info.manufacturer,
            model=info.model,
            name=info.model,
            sw_version=(str(info.software_version) if info.software_version is not None else None),
        )

    @property
    def _subsystem(self) -> object:
        """The library sub-system object this entity reads from."""
        return getattr(self.coordinator.device, self._component)
