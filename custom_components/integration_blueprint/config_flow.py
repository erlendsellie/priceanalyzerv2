"""Adds config flow for Blueprint."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    IntegrationBlueprintApiClient,
    IntegrationBlueprintApiClientAuthenticationError,
    IntegrationBlueprintApiClientCommunicationError,
    IntegrationBlueprintApiClientError,
)
from .const import DOMAIN, LOGGER

from homeassistant.const import CONF_ENTITY_ID
from homeassistant.helpers import selector


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_entity(user_input[CONF_ENTITY_ID])
            except IntegrationBlueprintApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_ENTITY_ID],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ENTITY_ID): selector.EntitySelector(
                        selector.EntitySelectorConfig()
                        # selector.EntitySelectorConfig(domain="nordpool")
                    )
                },
            ),
            errors=_errors,
        )

    async def _test_entity(self, entity_id: str) -> None:
        """Validate the entity selection."""
        # If needed, implement any checks for the entity here, or remove this if it's not required.
        client = IntegrationBlueprintApiClient(
            entity_id=entity_id,
            session=async_create_clientsession(self.hass),
            hass=self.hass,
        )
        await client.async_get_data()
