"""Query per-site forecasts from the solcast_solar integration."""

from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import FORECAST_FIELD_ENTITY, FUTURE_DAYS, HISTORY_DAYS, SOLCAST_DOMAIN


async def async_query_site(hass: HomeAssistant, site: str, start, end) -> list[dict[str, Any]]:
    """Return Solcast's cached half-hour forecasts for one site (no API call)."""
    response = await hass.services.async_call(
        SOLCAST_DOMAIN,
        "query_forecast_data",
        {
            "start_date_time": start,
            "end_date_time": end,
            "site": site,
        },
        blocking=True,
        return_response=True,
    )
    return list((response or {}).get("data", []))


def forecast_field(hass: HomeAssistant) -> str:
    """Follow Solcast's own 'use forecast field' choice (estimate/estimate10/estimate90)."""
    state = hass.states.get(FORECAST_FIELD_ENTITY)
    if state is not None and state.state in ("estimate", "estimate10", "estimate90"):
        return f"pv_{state.state}"
    return "pv_estimate"


async def async_site_wh_hours(hass: HomeAssistant, site: str) -> dict[str, float]:
    """Energy dashboard series for one site: half-hour start -> Wh."""
    now = dt_util.utcnow()
    rows = await async_query_site(
        hass, site, now - timedelta(days=HISTORY_DAYS), now + timedelta(days=FUTURE_DAYS)
    )
    field = forecast_field(hass)
    # pv_estimate is the mean kW over a 30-minute period: kW * 0.5 h * 1000 = Wh.
    return {
        dt_util.as_utc(row["period_start"]).isoformat(): round(float(row.get(field) or 0) * 500, 0)
        for row in rows
    }
