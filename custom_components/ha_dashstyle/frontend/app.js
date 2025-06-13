// HA Dashstyle JavaScript Application
class HADashstyle {
    constructor() {
        this.currentFloor = 'EG';
        this.adminMode = false;
        this.config = this.loadConfiguration();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadRooms();
        this.checkAdminAccess();
    }

    setupEventListeners() {
        // Floor tab navigation
        document.querySelectorAll('.floor-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchFloor(e.target.dataset.floor);
            });
        });

        // Admin tab navigation
        document.querySelectorAll('.admin-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchAdminTab(e.target.dataset.tab);
            });
        });

        // Theme color changes
        document.getElementById('primary-color')?.addEventListener('change', (e) => {
            this.updateThemeColor('--primary-color', e.target.value);
        });

        document.getElementById('accent-color')?.addEventListener('change', (e) => {
            this.updateThemeColor('--accent-color', e.target.value);
        });

        document.getElementById('background-color')?.addEventListener('change', (e) => {
            this.updateThemeColor('--background-color', e.target.value);
        });

        // Font family changes
        document.getElementById('font-family')?.addEventListener('change', (e) => {
            document.body.style.fontFamily = e.target.value;
        });
    }

    async checkAdminAccess() {
        try {
            const response = await fetch('/api/ha_dashstyle/admin_check', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.getAccessToken()}`,
                }
            });
            const data = await response.json();
            
            if (!data.is_admin) {
                document.getElementById('admin-btn').style.display = 'none';
            }
        } catch (error) {
            console.warn('Could not check admin access:', error);
        }
    }

    getAccessToken() {
        // Try to get the access token from various sources
        if (window.hassTokens) {
            return window.hassTokens.access_token;
        }
        // Fallback for different HA versions
        return localStorage.getItem('hassTokens') || '';
    }

    switchFloor(floor) {
        this.currentFloor = floor;
        
        // Update active floor tab
        document.querySelectorAll('.floor-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.floor === floor);
        });

        this.loadRooms();
    }

    switchAdminTab(tab) {
        // Update active admin tab
        document.querySelectorAll('.admin-tab').forEach(adminTab => {
            adminTab.classList.toggle('active', adminTab.dataset.tab === tab);
        });

        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tab}-tab`);
        });

        if (tab === 'rooms') {
            this.loadRoomConfig();
        } else if (tab === 'entities') {
            this.loadEntityConfig();
        }
    }

    async loadRooms() {
        const roomGrid = document.getElementById('room-grid');
        roomGrid.innerHTML = '<div class="loading">Loading rooms...</div>';

        try {
            const response = await fetch(`/api/ha_dashstyle/rooms/${this.currentFloor}`, {
                headers: {
                    'Authorization': `Bearer ${this.getAccessToken()}`,
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const rooms = await response.json();
            
            roomGrid.innerHTML = '';
            if (rooms.length === 0) {
                roomGrid.innerHTML = '<div class="no-rooms">No rooms found for this floor</div>';
                return;
            }
            
            rooms.forEach(room => {
                roomGrid.appendChild(this.createRoomCard(room));
            });
        } catch (error) {
            console.error('Failed to load rooms:', error);
            roomGrid.innerHTML = this.createMockRooms();
        }
    }

    createMockRooms() {
        const floors = {
            'EG': [
                { name: 'Wohnzimmer', icon: '🛋️', entities: ['Licht', 'TV', 'Heizung'], active: 3 },
                { name: 'Küche', icon: '🍳', entities: ['Licht', 'Herd', 'Kühlschrank'], active: 1 },
                { name: 'Büro', icon: '💻', entities: ['Licht', 'PC', 'Drucker'], active: 2 },
                { name: 'Eingangsflur', icon: '🚪', entities: ['Licht', 'Bewegungsmelder'], active: 0 }
            ],
            'OG': [
                { name: 'Schlafzimmer', icon: '🛏️', entities: ['Licht', 'Heizung', 'Rollladen'], active: 1 },
                { name: 'Kinderzimmer', icon: '🧸', entities: ['Licht', 'Heizung', 'Spielzeug'], active: 2 },
                { name: 'Badezimmer', icon: '🛁', entities: ['Licht', 'Heizung', 'Ventilator'], active: 1 },
                { name: 'Flur', icon: '🚶', entities: ['Licht', 'Bewegungsmelder'], active: 0 }
            ],
            'Keller': [
                { name: 'Partykeller', icon: '🎉', entities: ['Licht', 'Sound', 'Bar'], active: 0 },
                { name: 'Waschkeller', icon: '👕', entities: ['Waschmaschine', 'Trockner'], active: 1 },
                { name: 'Serverraum', icon: '🖥️', entities: ['Server', 'Netzwerk', 'Klima'], active: 3 },
                { name: 'Heizungskeller', icon: '🔥', entities: ['Heizung', 'Warmwasser'], active: 2 }
            ],
            'Außen': [
                { name: 'Garten', icon: '🌱', entities: ['Beleuchtung', 'Bewässerung'], active: 1 },
                { name: 'Terrasse', icon: '🪑', entities: ['Licht', 'Grill', 'Sonnenschirm'], active: 0 },
                { name: 'Garage', icon: '🚗', entities: ['Tor', 'Licht'], active: 0 }
            ]
        };

        const currentRooms = floors[this.currentFloor] || [];
        return currentRooms.map(room => this.createRoomCard(room)).join('');
    }

    createRoomCard(room) {
        const card = document.createElement('div');
        card.className = 'room-card';
        card.addEventListener('click', () => this.openRoomDetails(room));

        card.innerHTML = `
            <div class="room-header">
                <span class="room-name">${room.name}</span>
                <span class="room-icon">${room.icon}</span>
            </div>
            <div class="room-status">
                <span class="status-indicator ${room.active > 0 ? 'status-active' : 'status-inactive'}">
                    ${room.active} active
                </span>
            </div>
            <div class="room-entities">
                ${room.entities.map(entity => 
                    `<button class="entity-button">${entity}</button>`
                ).join('')}
            </div>
        `;

        return card;
    }

    openRoomDetails(room) {
        // Implement room details popup
        console.log('Opening room details for:', room.name);
        // This would open a detailed view of the room with controls
    }

    loadRoomConfig() {
        // Load room configuration for admin panel
        const roomConfig = document.querySelector('.room-config');
        roomConfig.innerHTML = `
            <div class="config-section">
                <h4>Add New Room</h4>
                <input type="text" placeholder="Room Name" id="new-room-name">
                <select id="new-room-floor">
                    <option value="EG">Erdgeschoss</option>
                    <option value="OG">Obergeschoss</option>
                    <option value="Keller">Keller</option>
                    <option value="Außen">Außenbereich</option>
                </select>
                <input type="text" placeholder="Room Icon" id="new-room-icon">
                <button onclick="dashstyle.addRoom()">Add Room</button>
            </div>
            <div class="existing-rooms">
                <h4>Existing Rooms</h4>
                <!-- Room list would be populated here -->
            </div>
        `;
    }

    loadEntityConfig() {
        // Load entity configuration for admin panel
        const entityConfig = document.querySelector('.entity-config');
        entityConfig.innerHTML = `
            <div class="config-section">
                <h4>Entity Types</h4>
                <div class="entity-types">
                    <div class="entity-type">
                        <label>Hoover/Vacuum</label>
                        <input type="text" placeholder="Entity ID" value="vacuum.">
                    </div>
                    <div class="entity-type">
                        <label>Temperature</label>
                        <input type="text" placeholder="Entity ID" value="sensor.temperature_">
                    </div>
                    <div class="entity-type">
                        <label>Lights</label>
                        <input type="text" placeholder="Entity ID" value="light.">
                    </div>
                    <!-- More entity types would be added here -->
                </div>
            </div>
        `;
    }

    addRoom() {
        const name = document.getElementById('new-room-name').value;
        const floor = document.getElementById('new-room-floor').value;
        const icon = document.getElementById('new-room-icon').value;

        if (!name) {
            alert('Please enter a room name');
            return;
        }

        // Add room logic here
        console.log('Adding room:', { name, floor, icon });
        
        // Clear form
        document.getElementById('new-room-name').value = '';
        document.getElementById('new-room-icon').value = '';
    }

    updateThemeColor(property, value) {
        document.documentElement.style.setProperty(property, value);
        this.config.theme = this.config.theme || {};
        this.config.theme[property] = value;
        this.saveConfiguration();
    }

    loadConfiguration() {
        const saved = localStorage.getItem('ha_dashstyle_config');
        return saved ? JSON.parse(saved) : {
            theme: {},
            rooms: {},
            entities: {}
        };
    }

    saveConfiguration() {
        localStorage.setItem('ha_dashstyle_config', JSON.stringify(this.config));
        console.log('Configuration saved');
    }

    resetConfiguration() {
        if (confirm('Are you sure you want to reset all configuration to default?')) {
            localStorage.removeItem('ha_dashstyle_config');
            location.reload();
        }
    }
}

// Global functions
function toggleAdminMode() {
    const adminPanel = document.getElementById('admin-panel');
    adminPanel.classList.toggle('hidden');
}

function toggleAllLights() {
    console.log('Toggling all lights');
    // Implement light toggle functionality
}

function activateSecurityMode() {
    console.log('Activating security mode');
    // Implement security mode functionality
}

function showMusicControl() {
    console.log('Showing music control');
    // Implement music control functionality
}

function showClimateControl() {
    console.log('Showing climate control');
    // Implement climate control functionality
}

function saveConfiguration() {
    dashstyle.saveConfiguration();
    alert('Configuration saved successfully!');
}

function resetConfiguration() {
    dashstyle.resetConfiguration();
}

// Initialize the application
let dashstyle;
document.addEventListener('DOMContentLoaded', () => {
    dashstyle = new HADashstyle();
});