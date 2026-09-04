"""Actuator relay states (coils, FC01)."""

from __future__ import annotations

from modbus_connection.model import Component, coil


class Relays(Component):
    """Read-only relay / contactor states driven by the controller."""

    compressor = coil(0)
    """Compressor contactor."""

    electric_heater = coil(1)
    """Backup electric heating element."""

    four_way_valve = coil(2)
    """Refrigerant four-way reversing valve."""

    fan = coil(3)
    """Outdoor unit fan."""
