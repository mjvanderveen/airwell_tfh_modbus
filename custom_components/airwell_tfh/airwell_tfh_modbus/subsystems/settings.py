"""User- and installer-configurable holding registers (10-33)."""

from __future__ import annotations

from modbus_connection.model import Component, boolean, integer


class Settings(Component):
    """Writable setpoints and tuning parameters."""

    target_temperature = integer(10, writable=True, unit="°C")
    """Domestic hot water setpoint."""

    temperature_difference = integer(11, writable=True, unit="°C")
    """Hysteresis between compressor start/stop."""

    stop_ambient_temperature = integer(12, writable=True, unit="°C")
    """Ambient temperature below which the heat pump stops and the backup heater takes over."""

    max_heatpump_temperature = integer(13, writable=True, unit="°C")
    """Highest water temperature the compressor alone is allowed to reach."""

    electric_heater_mode = integer(14, signed=False, writable=True)
    """Backup-heater mode. Encoding not publicly documented; exposed as raw."""

    electric_heater_start_temperature = integer(15, writable=True, unit="°C")
    """Water temperature below which the backup heater is allowed to assist."""

    sterilization_heater_enable = boolean(16, writable=True)
    """Whether periodic anti-legionella sterilization is enabled."""

    sterilization_cycle_hours = integer(17, signed=False, writable=True, unit="h")
    """Interval between automatic sterilization cycles."""

    temperature_correction = integer(18, writable=True, unit="°C")
    """Offset applied to the water tank sensor reading."""

    compressor_start_delay = integer(20, signed=False, writable=True, unit="min")
    """Minimum time between successive compressor starts."""

    econ_mode_heater_enable = boolean(27, writable=True)
    """Whether the backup heater may assist while in Eco mode."""

    heatpump_enable = boolean(28, writable=True)
    """Master enable for the compressor circuit."""

    defrost_start_temperature = integer(30, writable=True, unit="°C")
    """Defrost-sensor temperature that triggers a defrost cycle."""

    defrost_finish_temperature = integer(31, writable=True, unit="°C")
    """Defrost-sensor temperature that ends a defrost cycle."""

    defrost_start_time = integer(32, signed=False, writable=True, unit="min")
    """Minimum compressor runtime before a defrost cycle is allowed to trigger."""

    defrost_max_time = integer(33, signed=False, writable=True, unit="min")
    """Maximum duration of a single defrost cycle."""
