"""Config flow: one entry per Solcast rooftop site."""

from datetime import timedelta
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.exceptions import HomeAssistantError, ServiceNotFound
from homeassistant.util import dt as dt_util

from .const import CONF_SITE, DOMAIN
from .forecast import async_query_site


class SolcastSiteForecastConfigFlow(ConfigFlow, domain=DOMAIN):
    """Add one Solcast site as its own forecast entry."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Ask for the Solcast site resource ID and a display name."""
        errors: dict[str, str] = {}
        if user_input is not None:
            site = user_input[CONF_SITE].strip().replace("_", "-")
            await self.async_set_unique_id(site)
            self._abort_if_unique_id_configured()
            now = dt_util.utcnow()
            try:
                await async_query_site(self.hass, site, now - timedelta(hours=1), now + timedelta(hours=1))
            except ServiceNotFound:
                errors["base"] = "solcast_missing"
            except HomeAssistantError:
                errors[CONF_SITE] = "unknown_site"
            else:
                return self.async_create_entry(title=user_input["name"], data={CONF_SITE: site})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("name"): str, vol.Required(CONF_SITE): str}),
            errors=errors,
        )
