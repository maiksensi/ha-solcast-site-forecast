"""Solcast Site Forecast: one Energy dashboard forecast per Solcast rooftop site.

Reads per-site forecasts that the solcast_solar integration already holds in
memory (action solcast_solar.query_forecast_data). It never calls the Solcast API.
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a site entry. The energy platform does the work on demand."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a site entry."""
    return True
