"""Config flow for Water Pattern Classifier."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    TextSelector,
)

from .const import (
    CONF_FLOW_SENSOR,
    CONF_SESSION_DURATION_SENSOR,
    CONF_SESSION_FLOW_SENSOR,
    CONF_SESSION_VOLUME_SENSOR,
    DOMAIN,
)


class WaterClassifierConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Water Pattern Classifier."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """User step: choose source sensors."""
        errors: dict[str, str] = {}

        if user_input is not None:
            title = user_input.get("title", "Water Classifier")
            return self.async_create_entry(title=title, data=user_input)

        schema = vol.Schema(
            {
                vol.Required("title", default="Water Classifier"): TextSelector(),
                vol.Required(CONF_FLOW_SENSOR): EntitySelector(
                    EntitySelectorConfig(domain="sensor"),
                ),
                vol.Required(CONF_SESSION_VOLUME_SENSOR): EntitySelector(
                    EntitySelectorConfig(domain="sensor"),
                ),
                vol.Required(CONF_SESSION_DURATION_SENSOR): EntitySelector(
                    EntitySelectorConfig(domain="sensor"),
                ),
                vol.Required(CONF_SESSION_FLOW_SENSOR): EntitySelector(
                    EntitySelectorConfig(domain="sensor"),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
