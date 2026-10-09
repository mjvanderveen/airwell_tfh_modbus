"""Adds config flow for airwell_tfh."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import selector
from modbus_connection import ModbusError, ModbusTcpParams
from modbus_connection.tmodbus import ModbusConnection

from .airwell_tfh_modbus import AirwellTFH
from .const import CONF_UNIT_ID, DEFAULT_PORT, DEFAULT_UNIT_ID, DOMAIN, LOGGER


class AirwellTFHFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for airwell_tfh."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors: dict[str, str] = {}
        if user_input is not None:
            # NumberSelector returns floats; modbus-connection requires an int port.
            user_input = {
                **user_input,
                CONF_PORT: int(user_input[CONF_PORT]),
                CONF_UNIT_ID: int(user_input[CONF_UNIT_ID]),
            }
            try:
                model = await self._test_connection(
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                    unit_id=user_input[CONF_UNIT_ID],
                )
            except (ModbusError, OSError, TimeoutError) as exception:
                LOGGER.warning(exception)
                _errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(
                    f"{user_input[CONF_HOST]}_{user_input[CONF_PORT]}_{user_input[CONF_UNIT_ID]}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=model, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST, vol.UNDEFINED),
                    ): selector.TextSelector(),
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT, DEFAULT_PORT),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1, max=65535, step=1, mode=selector.NumberSelectorMode.BOX
                        ),
                    ),
                    vol.Required(
                        CONF_UNIT_ID,
                        default=(user_input or {}).get(CONF_UNIT_ID, DEFAULT_UNIT_ID),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1, max=255, step=1, mode=selector.NumberSelectorMode.BOX
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_connection(self, host: str, port: int, unit_id: int) -> str:
        """Open a short-lived connection, read the model, then close it."""
        connection = ModbusConnection(ModbusTcpParams(host=host, port=port, framer="rtu"))
        try:
            unit = connection.for_unit(int(unit_id))
            device = AirwellTFH(unit)
            await device.info.async_update()
        finally:
            await connection.close()
        return device.info.model
