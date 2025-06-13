"""Constants for the HA Dashstyle integration."""

DOMAIN = "ha_dashstyle"

# Default configuration
DEFAULT_NAME = "HA Dashstyle"

# Configuration keys
CONF_ROOMS = "rooms"
CONF_ENTITIES = "entities"
CONF_THEMES = "themes"

# Room floors
FLOORS = {
    "EG": {
        "name": "Erdgeschoss",
        "icon": "mdi:home",
        "rooms": [
            "wohnzimmer",
            "buero", 
            "kueche",
            "eingangsflur",
            "gaesteklo",
            "treppe_erdgeschoss"
        ]
    },
    "OG": {
        "name": "Obergeschoss", 
        "icon": "mdi:home-floor-1",
        "rooms": [
            "kids",
            "kinderbad",
            "flur",
            "aupair", 
            "schlafzimmer"
        ]
    },
    "Keller": {
        "name": "Keller",
        "icon": "mdi:stairs-down",
        "rooms": [
            "partykeller",
            "heizungskeller",
            "kellerflur",
            "waschkeller",
            "serverraum",
            "buero_keller",
            "sauna"
        ]
    },
    "Außen": {
        "name": "Außenbereich",
        "icon": "mdi:tree",
        "rooms": [
            "aussen"
        ]
    }
}

# Entity types for sensors
SENSOR_TYPES = {
    "hoover": {
        "name": "Staubsauger",
        "icon": "mdi:robot-vacuum"
    },
    "temperature": {
        "name": "Temperatur",
        "icon": "mdi:thermometer"
    },
    "humidity": {
        "name": "Luftfeuchtigkeit", 
        "icon": "mdi:water-percent"
    },
    "motion": {
        "name": "Bewegung",
        "icon": "mdi:motion-sensor"
    },
    "door": {
        "name": "Tür",
        "icon": "mdi:door"
    },
    "window": {
        "name": "Fenster",
        "icon": "mdi:window-open"
    },
    "light": {
        "name": "Licht",
        "icon": "mdi:lightbulb"
    },
    "switch": {
        "name": "Schalter",
        "icon": "mdi:toggle-switch"
    },
    "cover": {
        "name": "Rollladen",
        "icon": "mdi:window-shutter"
    },
    "climate": {
        "name": "Heizung",
        "icon": "mdi:thermostat"
    },
    "media": {
        "name": "Medien",
        "icon": "mdi:play"
    },
    "security": {
        "name": "Sicherheit",
        "icon": "mdi:shield-home"
    }
}

# Default theme colors
DEFAULT_THEME = {
    "primary_color": "#1976d2",
    "accent_color": "#ff9800",
    "background_color": "#fafafa",
    "card_background_color": "#ffffff",
    "text_primary_color": "#212121",
    "text_secondary_color": "#727272",
    "active_color": "#4caf50",
    "inactive_color": "#9e9e9e"
}