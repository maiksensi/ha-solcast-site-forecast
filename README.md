# Solcast Site Forecast

Shows one Energy dashboard forecast per Solcast rooftop site.

The [Solcast PV Forecast](https://github.com/BJReplay/ha-solcast-solar) integration gives the Energy dashboard one combined forecast for all sites. Home Assistant asks for a forecast once per config entry, and Solcast allows only one entry. This integration adds one config entry per site, so each solar source on the Energy dashboard gets its own forecast line.

It reads the forecasts that Solcast PV Forecast already holds in Home Assistant, through the `solcast_solar.query_forecast_data` action. It makes no Solcast API calls and does not use your API quota.

## Requirements

- Home Assistant 2026.10 or later.
- Solcast PV Forecast, set up with your rooftop sites.

## Installation

1. In HACS, open **Custom repositories**.
2. Add `https://github.com/maiksensi/ha-solcast-site-forecast` with the type **Integration**.
3. Download **Solcast Site Forecast** and restart Home Assistant.

## Configuration

1. Go to **Settings > Devices & services > Add integration** and select **Solcast Site Forecast**.
2. Enter a name and the Solcast site resource ID (for example `1234-5678-9012-3456`). The resource ID is on your Solcast rooftop site page.
3. Repeat for each site.
4. Go to **Settings > Dashboards > Energy**. Edit each solar production source and select the matching site as its forecast.

Do not also select the Solcast PV Forecast entry on a source. It holds the total of all sites, so the forecast would count twice.

## Behaviour

- The forecast follows Solcast's **Use forecast field** setting (estimate, estimate10 or estimate90) and its dampening.
- The series covers up to 730 days back and 30 days ahead, as far as Solcast has data.
