"""Constants for airwell_tfh."""

from __future__ import annotations

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "airwell_tfh"

CONF_UNIT_ID = "unit_id"

DEFAULT_PORT = 502
DEFAULT_UNIT_ID = 1

ATTRIBUTION = "Data provided by a locally connected Airwell TFH heat pump water heater"
