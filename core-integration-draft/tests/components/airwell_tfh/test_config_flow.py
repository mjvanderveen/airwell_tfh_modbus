"""Test the airwell_tfh config flow."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.components.airwell_tfh.const import CONF_CONNECTION, CONF_UNIT_ID, DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_user_flow_success(hass: HomeAssistant, mock_airwell_device) -> None:
    """A reachable controller creates an entry titled with its model."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    with patch(
        "homeassistant.components.airwell_tfh.config_flow.async_get_unit",
        return_value="fake_unit",
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_CONNECTION: "fake_connection_entry_id", CONF_UNIT_ID: 1},
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "TFH (300)"
    assert result["data"] == {CONF_CONNECTION: "fake_connection_entry_id", CONF_UNIT_ID: 1}


async def test_user_flow_cannot_connect(hass: HomeAssistant) -> None:
    """An OSError while probing the model surfaces as cannot_connect."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "homeassistant.components.airwell_tfh.config_flow.async_get_unit",
        side_effect=OSError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_CONNECTION: "fake_connection_entry_id", CONF_UNIT_ID: 1},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}
