"""The HA Dashstyle integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN
from .api import setup_api_views

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = []


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA Dashstyle from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    # Register static files for the frontend
    hass.http.register_static_path(
        "/ha_dashstyle_frontend",
        hass.config.path("custom_components/ha_dashstyle/frontend"),
        cache_headers=False,
    )

    # Register the custom panel
    hass.components.frontend.async_register_built_in_panel(
        "iframe",
        "Dashstyle",
        "mdi:view-dashboard",
        frontend_url_path="ha-dashstyle",
        config={"url": "/ha_dashstyle_frontend/index.html"},
    )

    # Set up API views
    setup_api_views(hass)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok