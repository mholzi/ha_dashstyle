# HA Dashstyle

A custom Home Assistant integration providing a fully configurable dashboard.

![hassfest](https://github.com/mholzi/ha_dashstyle/workflows/Validate/badge.svg)
![hacs](https://github.com/mholzi/ha_dashstyle/workflows/HACS/badge.svg)

## Features

- Floor-based room organization
- Native implementation (no HACS card dependencies)
- Admin configuration panel
- Theme customization
- Entity classification system
- Responsive design

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Install "HA Dashstyle" from HACS
3. Restart Home Assistant
4. Add the integration through the UI

### Manual

1. Download and copy `custom_components/ha_dashstyle` to your Home Assistant
2. Restart Home Assistant
3. Add the integration through the UI

## Configuration

The integration provides a configuration flow in the Home Assistant UI. After installation:

1. Go to Configuration > Integrations
2. Click "Add Integration"
3. Search for "HA Dashstyle"
4. Complete the setup wizard

## Usage

After configuration, access the dashboard through the sidebar. Admin users can configure rooms, entities, and themes through the admin panel.

For detailed documentation, see the full [README](README.md).