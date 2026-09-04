"""Physical temperature sensors (input registers, FC04)."""

from __future__ import annotations

from modbus_connection.model import Component, gauge


class Sensors(Component):
    """Read-only temperature measurements."""

    register_space = "input"

    water_tank_temperature = gauge(0, 0.1, unit="°C")
    """Domestic hot water storage tank temperature."""

    defrost_temperature = gauge(1, 0.1, unit="°C")
    """Evaporator / defrost sensor temperature."""

    ambient_temperature = gauge(2, 0.1, unit="°C")
    """Outdoor ambient air temperature."""

    exhaust_temperature = gauge(3, 0.1, unit="°C")
    """Compressor discharge (exhaust) gas temperature."""

    return_gas_temperature = gauge(4, 0.1, unit="°C")
    """Compressor suction (return) gas temperature."""
