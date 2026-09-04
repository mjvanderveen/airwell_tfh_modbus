"""Fixtures for the airwell_tfh integration tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.components.airwell_tfh.const import CONF_CONNECTION, CONF_UNIT_ID, DOMAIN


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """A config entry pointing at a fake modbus_connection entry and unit 1."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="TFH (300)",
        data={CONF_CONNECTION: "fake_connection_entry_id", CONF_UNIT_ID: 1},
        unique_id="fake_connection_entry_id_1",
    )


@pytest.fixture
def mock_airwell_device():
    """Patch AirwellTFH so tests never touch real Modbus I/O."""
    with patch("homeassistant.components.airwell_tfh.AirwellTFH") as mock_cls:
        device = mock_cls.return_value
        device.async_update = AsyncMock(return_value=None)
        device.info.async_update = AsyncMock(return_value=None)
        device.info.model = "TFH (300)"
        device.info.manufacturer = "Airwell"
        device.info.software_version = 12
        yield device
