"""API endpoints for HA Dashstyle."""
from __future__ import annotations

import json
import logging
from typing import Any

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.auth.models import User

from .const import DOMAIN, FLOORS, SENSOR_TYPES, DEFAULT_THEME

_LOGGER = logging.getLogger(__name__)


class DashstyleAdminCheckView(HomeAssistantView):
    """View to check if user is admin."""

    url = "/api/ha_dashstyle/admin_check"
    name = "api:ha_dashstyle:admin_check"

    async def get(self, request: web.Request) -> web.Response:
        """Check if current user is admin."""
        user: User = request.get("hass_user")
        if not user:
            return self.json({"is_admin": False})
        
        return self.json({"is_admin": user.is_admin})


class DashstyleRoomsView(HomeAssistantView):
    """View to get rooms for a floor."""

    url = "/api/ha_dashstyle/rooms/{floor}"
    name = "api:ha_dashstyle:rooms"

    async def get(self, request: web.Request) -> web.Response:
        """Get rooms for a specific floor."""
        floor = request.match_info["floor"]
        hass: HomeAssistant = request.app["hass"]
        
        if floor not in FLOORS:
            return self.json_message("Floor not found", 404)
        
        # Get floor configuration
        floor_config = FLOORS[floor]
        rooms = []
        
        for room_name in floor_config["rooms"]:
            room_data = await self._get_room_data(hass, room_name)
            rooms.append(room_data)
        
        return self.json(rooms)
    
    async def _get_room_data(self, hass: HomeAssistant, room_name: str) -> dict[str, Any]:
        """Get data for a specific room."""
        # Get entities for this room
        entities = self._get_room_entities(hass, room_name)
        active_count = sum(1 for entity in entities if self._is_entity_active(hass, entity))
        
        # Get room icon based on room type
        room_icon = self._get_room_icon(room_name)
        
        return {
            "name": room_name.replace("_", " ").title(),
            "id": room_name,
            "icon": room_icon,
            "entities": [entity.split(".")[-1].replace("_", " ").title() for entity in entities],
            "entity_ids": entities,
            "active": active_count,
            "total": len(entities)
        }
    
    def _get_room_entities(self, hass: HomeAssistant, room_name: str) -> list[str]:
        """Get entities for a room."""
        entities = []
        
        # Look for entities with the room name in their entity_id
        for entity_id in hass.states.all():
            if room_name in entity_id.entity_id:
                entities.append(entity_id.entity_id)
        
        # Also check for combined sensor
        combined_sensor = f"binary_sensor.combined_sensor_{room_name}"
        if hass.states.get(combined_sensor):
            entities.append(combined_sensor)
        
        return entities[:10]  # Limit to first 10 entities
    
    def _is_entity_active(self, hass: HomeAssistant, entity_id: str) -> bool:
        """Check if an entity is active."""
        state = hass.states.get(entity_id)
        if not state:
            return False
        
        # Define active states for different entity types
        active_states = ["on", "open", "active", "playing", "home", "heat", "cool"]
        return state.state.lower() in active_states
    
    def _get_room_icon(self, room_name: str) -> str:
        """Get icon for room based on name."""
        room_icons = {
            "wohnzimmer": "🛋️",
            "kueche": "🍳",
            "buero": "💻",
            "eingangsflur": "🚪",
            "gaesteklo": "🚽",
            "treppe_erdgeschoss": "🪜",
            "kids": "🧸",
            "kinderbad": "🛁",
            "flur": "🚶",
            "aupair": "🛏️",
            "schlafzimmer": "🛌",
            "partykeller": "🎉",
            "heizungskeller": "🔥",
            "kellerflur": "🚶",
            "waschkeller": "👕",
            "serverraum": "🖥️",
            "buero_keller": "💻",
            "sauna": "🧖",
            "aussen": "🌳"
        }
        return room_icons.get(room_name, "🏠")


class DashstyleConfigView(HomeAssistantView):
    """View to manage dashboard configuration."""

    url = "/api/ha_dashstyle/config"
    name = "api:ha_dashstyle:config"

    async def get(self, request: web.Request) -> web.Response:
        """Get current configuration."""
        hass: HomeAssistant = request.app["hass"]
        
        # Get stored configuration
        config = await self._get_stored_config(hass)
        
        return self.json(config)
    
    async def post(self, request: web.Request) -> web.Response:
        """Save configuration."""
        user: User = request.get("hass_user")
        if not user or not user.is_admin:
            return self.json_message("Admin access required", 403)
        
        try:
            data = await request.json()
            hass: HomeAssistant = request.app["hass"]
            
            # Save configuration
            await self._save_config(hass, data)
            
            return self.json({"success": True})
        except Exception as err:
            _LOGGER.error("Error saving configuration: %s", err)
            return self.json_message("Error saving configuration", 500)
    
    async def _get_stored_config(self, hass: HomeAssistant) -> dict[str, Any]:
        """Get stored configuration."""
        # For now, return default configuration
        # In a real implementation, this would read from storage
        return {
            "floors": FLOORS,
            "sensor_types": SENSOR_TYPES,
            "theme": DEFAULT_THEME,
            "rooms": {},
            "entities": {}
        }
    
    async def _save_config(self, hass: HomeAssistant, config: dict[str, Any]) -> None:
        """Save configuration."""
        # In a real implementation, this would save to storage
        _LOGGER.info("Saving configuration: %s", config)


class DashstyleEntityControlView(HomeAssistantView):
    """View to control entities."""

    url = "/api/ha_dashstyle/control/{entity_id}"
    name = "api:ha_dashstyle:control"

    async def post(self, request: web.Request) -> web.Response:
        """Control an entity."""
        entity_id = request.match_info["entity_id"]
        hass: HomeAssistant = request.app["hass"]
        
        try:
            data = await request.json()
            action = data.get("action", "toggle")
            
            # Determine service call based on entity type
            domain = entity_id.split(".")[0]
            
            if domain == "light":
                service = "turn_on" if action == "on" else "turn_off"
                await hass.services.async_call("light", service, {"entity_id": entity_id})
            elif domain == "switch":
                service = "turn_on" if action == "on" else "turn_off"
                await hass.services.async_call("switch", service, {"entity_id": entity_id})
            elif domain == "cover":
                service_map = {"open": "open_cover", "close": "close_cover", "stop": "stop_cover"}
                service = service_map.get(action, "toggle")
                await hass.services.async_call("cover", service, {"entity_id": entity_id})
            else:
                # Generic toggle
                await hass.services.async_call("homeassistant", "toggle", {"entity_id": entity_id})
            
            return self.json({"success": True})
        except Exception as err:
            _LOGGER.error("Error controlling entity %s: %s", entity_id, err)
            return self.json_message("Error controlling entity", 500)


def setup_api_views(hass: HomeAssistant) -> None:
    """Set up API views."""
    hass.http.register_view(DashstyleAdminCheckView)
    hass.http.register_view(DashstyleRoomsView)
    hass.http.register_view(DashstyleConfigView)
    hass.http.register_view(DashstyleEntityControlView)