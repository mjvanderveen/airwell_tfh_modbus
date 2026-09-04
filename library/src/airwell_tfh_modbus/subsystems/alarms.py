"""Hardware alarm contacts (discrete inputs, FC02).

Distinct from the alarm *code* registers on :class:`~airwell_tfh_modbus.subsystems.controller.Controller`
— these are the raw physical switches, independent of the controller's own
diagnosis.
"""

from __future__ import annotations

from modbus_connection.model import Component, discrete_input


class Alarms(Component):
    """Read-only fault contacts."""

    high_pressure = discrete_input(5)
    """Refrigerant high-pressure switch tripped."""

    low_pressure = discrete_input(6)
    """Refrigerant low-pressure switch tripped."""

    condensation = discrete_input(7)
    """Condensation / water-leak sensor tripped."""
