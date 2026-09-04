"""Controller identity (holding registers 1000-1001)."""

from __future__ import annotations

from modbus_connection.model import Component, integer


class DeviceInformation(Component):
    """Identity registers. Read once at setup, never polled again."""

    model_code = integer(1000, signed=False)
    """Raw model code reported by the controller."""

    software_version = integer(1001, signed=False)
    """Raw firmware version code reported by the controller."""

    @property
    def manufacturer(self) -> str:
        """Controller manufacturer."""
        return "Airwell"

    @property
    def model(self) -> str:
        """Model name. The controller only reports a numeric code."""
        code = self.model_code
        return f"TFH ({code})" if code is not None else "TFH series"
