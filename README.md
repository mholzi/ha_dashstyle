# HA Dashstyle

A custom Home Assistant integration providing a fully configurable dashboard designed for larger setups with multiple rooms and various entities. The dashboard offers a native implementation without requiring additional HACS cards.

## Features

### Main Dashboard
- **Floor-based Navigation**: Organize your home by floors (Erdgeschoss, Obergeschoss, Keller, Außenbereich)
- **Room Cards**: Visual representation of each room with active entity counts
- **Quick Actions**: Instant access to common functions (lights, security, music, climate)
- **Real-time Status**: Live updates of entity states and room activity
- **Native Implementation**: No dependency on custom HACS cards

### Admin Configuration
- **Room Management**: Add, edit, and organize rooms across different floors
- **Entity Classification**: Classify entities by type (hoover, temperature, lights, etc.)
- **Theme Customization**: Configure colors, fonts, and visual appearance
- **Admin-only Access**: Configuration panel only visible to Home Assistant administrators

### Supported Entity Types
- **Vacuum/Hoover**: Robot vacuum cleaners and cleaning devices
- **Temperature**: Temperature sensors and thermostats
- **Humidity**: Humidity sensors
- **Motion**: Motion and presence sensors
- **Doors/Windows**: Contact sensors and opening detectors
- **Lights**: All types of lighting controls
- **Switches**: Toggle switches and smart plugs
- **Covers**: Blinds, shutters, and garage doors
- **Climate**: Heating and cooling systems
- **Media**: Music players and entertainment systems
- **Security**: Alarm systems and security devices

## Installation

### Via HACS (Recommended)
1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the "+" button to add a repository
4. Enter the repository URL: `https://github.com/mholzi/ha_dashstyle`
5. Select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation
1. Copy the `custom_components/ha_dashstyle` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Configuration > Integrations
4. Click "Add Integration" and search for "HA Dashstyle"

## Configuration

### Initial Setup
1. After installation, go to Configuration > Integrations
2. Click "Add Integration" and search for "HA Dashstyle"
3. Follow the configuration flow:
   - Enter a name for your dashboard (default: "HA Dashstyle")
   - Choose whether to include the admin panel (recommended: Yes)
4. Click "Submit" to complete the setup

### Access the Dashboard
Once configured, the dashboard will be available in your Home Assistant sidebar as "Dashstyle" with a dashboard icon.

### Admin Configuration
1. Click the "Admin" button in the top right corner of the dashboard (only visible to administrators)
2. Configure your setup using the three tabs:

#### Rooms Tab
- Add new rooms to any floor
- Specify room names, icons, and floor assignment
- Manage existing room configurations

#### Entities Tab
- Classify entities by type (hoover, temperature, lights, etc.)
- Set up entity patterns for automatic room assignment
- Configure entity-specific settings

#### Themes Tab
- Customize color scheme (primary, accent, background colors)
- Select font family for the dashboard
- Apply visual styling preferences

## Floor Structure

The dashboard organizes your home into four main areas:

### Erdgeschoss (EG) - Ground Floor
- Living Room (Wohnzimmer)
- Office (Büro)
- Kitchen (Küche)
- Entrance Hall (Eingangsflur)
- Guest Toilet (Gäste-WC)
- Ground Floor Stairs (Treppe Erdgeschoss)

### Obergeschoss (OG) - Upper Floor
- Kids Room (Kinderzimmer)
- Children's Bathroom (Kinderbad)
- Hallway (Flur)
- Au Pair Room (Aupair)
- Master Bedroom (Schlafzimmer)

### Keller - Basement
- Party Basement (Partykeller)
- Heating Room (Heizungskeller)
- Basement Hallway (Kellerflur)
- Laundry Room (Waschkeller)
- Server Room (Serverraum)
- Basement Office (Büro Keller)
- Sauna

### Außenbereich - Outdoor Area
- Garden/Outdoor (Außen)

## Entity Detection

The integration automatically detects entities based on naming patterns:
- Entities containing room names in their entity IDs
- Combined sensors (e.g., `binary_sensor.combined_sensor_wohnzimmer`)
- Standard Home Assistant entity domains (light, switch, sensor, etc.)

## Theme Customization

### Default Color Scheme
- **Primary Color**: #1976d2 (Blue)
- **Accent Color**: #ff9800 (Orange)
- **Background**: #fafafa (Light Gray)
- **Card Background**: #ffffff (White)
- **Text Primary**: #212121 (Dark Gray)
- **Active Color**: #4caf50 (Green)

### CSS Custom Properties
The dashboard uses CSS custom properties for theming, allowing for easy customization:
```css
:root {
    --primary-color: #1976d2;
    --accent-color: #ff9800;
    --background-color: #fafafa;
    --card-background-color: #ffffff;
    --text-primary-color: #212121;
    --active-color: #4caf50;
}
```

## API Endpoints

The integration provides several API endpoints for configuration and control:

- `GET /api/ha_dashstyle/admin_check` - Check admin access
- `GET /api/ha_dashstyle/rooms/{floor}` - Get rooms for a specific floor
- `GET /api/ha_dashstyle/config` - Get current configuration
- `POST /api/ha_dashstyle/config` - Save configuration (admin only)
- `POST /api/ha_dashstyle/control/{entity_id}` - Control entities

## Troubleshooting

### Dashboard Not Loading
1. Check that the integration is properly installed and enabled
2. Verify that Home Assistant has restarted after installation
3. Check the Home Assistant logs for any error messages
4. Ensure your browser supports modern JavaScript features

### Admin Panel Not Visible
1. Verify that you're logged in as a Home Assistant administrator
2. Check that "include_admin" was enabled during setup
3. Try refreshing the browser page

### Entities Not Appearing
1. Ensure entities follow the expected naming patterns
2. Check that entities are available in Home Assistant's Developer Tools
3. Verify that entities are not hidden or disabled

### Performance Issues
1. The dashboard is optimized for setups with up to 100 entities per room
2. Consider organizing entities into more specific rooms if experiencing slowdowns
3. Check browser console for JavaScript errors

## Development

### Structure
```
custom_components/ha_dashstyle/
├── __init__.py          # Integration setup
├── manifest.json        # Integration manifest
├── const.py            # Constants and configuration
├── config_flow.py      # Configuration flow
├── api.py              # API endpoints
└── frontend/           # Frontend assets
    ├── index.html      # Main dashboard HTML
    ├── style.css       # Dashboard styling
    └── app.js          # Dashboard JavaScript
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, feature requests, or questions:
- Create an issue on [GitHub](https://github.com/mholzi/ha_dashstyle/issues)
- Check the [Home Assistant Community Forum](https://community.home-assistant.io/)

## Changelog

### Version 1.0.0
- Initial release
- Floor-based room organization
- Admin configuration panel
- Theme customization
- Native implementation without HACS dependencies
- Support for all major entity types
- Responsive design for mobile and desktop
