"""Energy platform: per-site Solcast forecast for the Energy dashboard."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_SITE
from .forecast import async_site_wh_hours

_LOGGER = logging.getLogger(__name__)


async def async_get_solar_forecast(hass: HomeAssistant, config_entry_id: str) -> dict[str, Any] | None:
    """Return the forecast of the site behind this config entry."""
    entry = hass.config_entries.async_get_entry(config_entry_id)
    if entry is None:
        return None
    site = entry.data[CONF_SITE]
    try:
        return {"wh_hours": await async_site_wh_hours(hass, site)}
    except HomeAssistantError as err:
        _LOGGER.warning("Solcast forecast for site %s unavailable: %s", site, err)
        return None
