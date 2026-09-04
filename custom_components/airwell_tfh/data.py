"""Custom types for airwell_tfh."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration
    from modbus_connection import ModbusConnection

    from .coordinator import AirwellTFHDataUpdateCoordinator


type AirwellTFHConfigEntry = ConfigEntry[AirwellTFHData]


@dataclass
class AirwellTFHData:
    """Runtime data for the airwell_tfh integration."""

    connection: ModbusConnection
    coordinator: AirwellTFHDataUpdateCoordinator
    integration: Integration
