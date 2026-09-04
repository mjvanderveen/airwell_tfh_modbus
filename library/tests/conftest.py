"""Shared fixtures for airwell_tfh_modbus tests."""

from __future__ import annotations

import pytest

from airwell_tfh_modbus import AirwellTFH


@pytest.fixture
def device(mock_modbus_unit) -> AirwellTFH:
    """An AirwellTFH bound to the in-memory Modbus mock."""
    return AirwellTFH(mock_modbus_unit)
