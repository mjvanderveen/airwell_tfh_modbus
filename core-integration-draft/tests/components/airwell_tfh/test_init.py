"""Test setup and teardown of the airwell_tfh integration."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant


async def test_setup_and_unload_entry(
    hass: HomeAssistant, mock_config_entry, mock_airwell_device
) -> None:
    """The entry loads, forwards platforms, and unloads cleanly."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "homeassistant.components.airwell_tfh.async_get_unit",
        return_value="fake_unit",
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
