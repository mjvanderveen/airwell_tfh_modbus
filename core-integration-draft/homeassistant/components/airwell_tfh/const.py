"""Constants for the Airwell TFH integration."""

from __future__ import annotations

from datetime import timedelta
from typing import Final

DOMAIN: Final = "airwell_tfh"

CONF_CONNECTION: Final = "connection_entry_id"
CONF_UNIT_ID: Final = "unit_id"

DEFAULT_UNIT_ID: Final = 1  # matches the reference installation's Modbus slave id

# A domestic hot water heat pump changes slowly, but we poll aggressively and fixed.
SCAN_INTERVAL: Final = timedelta(seconds=30)
