import { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { Icon, LatLngExpression } from 'leaflet';
import { Activity, Thermometer, Droplets, Wind, Fish } from 'lucide-react';
import { AgroBot, Alert } from '../types';

// Fix for default Leaflet markers
import L from 'leaflet';
// eslint-disable-next-line @typescript-eslint/no-explicit-any
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface InteractiveMapProps {
  onBotSelect: (bot: AgroBot) => void;
  selectedBot: AgroBot | null;
}

// Custom icons for different bot statuses
const createBotIcon = (status: string, isSelected: boolean = false) => {
  const color = status === 'active' ? '#10B981' : status === 'maintenance' ? '#F59E0B' : '#EF4444';
  const size = isSelected ? 30 : 20;
  
  return new Icon({
    iconUrl: `data:image/svg+xml;base64,${btoa(`
      <svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" fill="${color}" stroke="white" stroke-width="2"/>
        <circle cx="12" cy="12" r="6" fill="white"/>
        <circle cx="12" cy="12" r="3" fill="${color}"/>
      </svg>
    `)}`,
    iconSize: [size, size],
    iconAnchor: [size/2, size/2],
    popupAnchor: [0, -size/2],
  });
};

const alertIcon = new Icon({
  iconUrl: `data:image/svg+xml;base64,${btoa(`
    <svg width="25" height="25" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="12" r="10" fill="#EF4444" stroke="white" stroke-width="2"/>
      <path d="M12 8v4M12 16h.01" stroke="white" stroke-width="2" stroke-linecap="round"/>
    </svg>
  `)}`,
  iconSize: [25, 25],
  iconAnchor: [12.5, 12.5],
  popupAnchor: [0, -12.5],
});

export function InteractiveMap({ onBotSelect, selectedBot }: InteractiveMapProps) {
  const [currentLayer, setCurrentLayer] = useState('temperature');

  // Indian Ocean center coordinates
  const center: LatLngExpression = [-20.0, 57.5];
  const zoom = 6;

  // Mock data for demonstration
  const mockAgrobots: AgroBot[] = [
    {
      id: 'bot-1',
      name: 'Agro-Bot Alpha',
      latitude: -20.0,
      longitude: 57.5,
      status: 'active',
      lastUpdate: '2024-01-15T10:30:00Z',
      data: {
        temperature: 24.5,
        salinity: 35.2,
        ph: 8.1,
        oxygenLevel: 7.2,
        pollutionIndex: 2.1,
        currentSpeed: 0.8,
        currentDirection: 120
      }
    },
    {
      id: 'bot-2',
      name: 'Agro-Bot Beta',
      latitude: -15.5,
      longitude: 60.2,
      status: 'active',
      lastUpdate: '2024-01-15T10:28:00Z',
      data: {
        temperature: 26.1,
        salinity: 34.8,
        ph: 7.9,
        oxygenLevel: 6.8,
        pollutionIndex: 3.2,
        currentSpeed: 1.2,
        currentDirection: 95
      }
    },
    {
      id: 'bot-3',
      name: 'Agro-Bot Gamma',
      latitude: -25.3,
      longitude: 55.8,
      status: 'maintenance',
      lastUpdate: '2024-01-15T09:45:00Z',
      data: {
        temperature: 23.8,
        salinity: 35.5,
        ph: 8.2,
        oxygenLevel: 7.5,
        pollutionIndex: 1.8,
        currentSpeed: 0.6,
        currentDirection: 140
      }
    },
    {
      id: 'bot-4',
      name: 'Agro-Bot Delta',
      latitude: -18.2,
      longitude: 63.1,
      status: 'active',
      lastUpdate: '2024-01-15T10:25:00Z',
      data: {
        temperature: 25.2,
        salinity: 34.9,
        ph: 8.0,
        oxygenLevel: 6.9,
        pollutionIndex: 2.5,
        currentSpeed: 1.0,
        currentDirection: 110
      }
    }
  ];

  const mockAlerts: Alert[] = [
    {
      id: 'alert-1',
      title: 'High Pollution Detected',
      description: 'Pollution index exceeding safe levels near shipping lanes',
      severity: 'high',
      location: { latitude: -15.5, longitude: 60.2 },
      timestamp: '2024-01-15T10:15:00Z',
      type: 'pollution',
      isRead: false
    },
    {
      id: 'alert-2',
      title: 'Temperature Anomaly',
      description: 'Unusually high water temperature detected',
      severity: 'medium',
      location: { latitude: -18.2, longitude: 63.1 },
      timestamp: '2024-01-15T09:30:00Z',
      type: 'anomaly',
      isRead: false
    }
  ];

  const bots = mockAgrobots;
  const alerts = mockAlerts;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Indian Ocean - Live Data</h2>
          <div className="flex space-x-2">
            <button
              onClick={() => setCurrentLayer('temperature')}
              className={`px-3 py-1 rounded-full text-sm ${
                currentLayer === 'temperature' 
                  ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300' 
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              Temperature
            </button>
            <button
              onClick={() => setCurrentLayer('currents')}
              className={`px-3 py-1 rounded-full text-sm ${
                currentLayer === 'currents' 
                  ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' 
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              Currents
            </button>
            <button
              onClick={() => setCurrentLayer('salinity')}
              className={`px-3 py-1 rounded-full text-sm ${
                currentLayer === 'salinity' 
                  ? 'bg-teal-100 dark:bg-teal-900/30 text-teal-700 dark:text-teal-300' 
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              Salinity
            </button>
          </div>
        </div>
      </div>

      <div className="relative bg-gray-100 dark:bg-gray-700" style={{ height: '500px', width: '100%' }}>
        <MapContainer
          center={center}
          zoom={zoom}
          style={{ height: '100%', width: '100%', zIndex: 1 }}
          className="leaflet-container"
          key="interactive-map"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            crossOrigin="anonymous"
          />

          {/* Temperature layer visualization */}
          {currentLayer === 'temperature' && bots.map((bot) => (
            <Circle
              key={`temp-${bot.id}`}
              center={[bot.latitude, bot.longitude]}
              radius={50000} // 50km radius
              fillColor={bot.data.temperature > 25 ? '#EF4444' : '#3B82F6'}
              fillOpacity={0.3}
              stroke={true}
              color={bot.data.temperature > 25 ? '#EF4444' : '#3B82F6'}
              weight={2}
            />
          ))}

          {/* Salinity layer visualization */}
          {currentLayer === 'salinity' && bots.map((bot) => (
            <Circle
              key={`salinity-${bot.id}`}
              center={[bot.latitude, bot.longitude]}
              radius={40000} // 40km radius
              fillColor={bot.data.salinity > 35 ? '#14B8A6' : '#06B6D4'}
              fillOpacity={0.3}
              stroke={true}
              color={bot.data.salinity > 35 ? '#14B8A6' : '#06B6D4'}
              weight={2}
            />
          ))}

          {/* Alert markers */}
          {alerts.map((alert) => (
            <Marker
              key={alert.id}
              position={[alert.location.latitude, alert.location.longitude]}
              icon={alertIcon}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-semibold text-red-600">{alert.title}</h3>
                  <p className="text-sm text-gray-600 mt-1">{alert.description}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    Severity: <span className="capitalize">{alert.severity}</span>
                  </p>
                </div>
              </Popup>
            </Marker>
          ))}

          {/* Agro-bot markers */}
          {bots.map((bot) => (
            <Marker
              key={bot.id}
              position={[bot.latitude, bot.longitude]}
              icon={createBotIcon(bot.status, selectedBot?.id === bot.id)}
              eventHandlers={{
                click: () => onBotSelect(bot),
              }}
            >
              <Popup>
                <div className="p-3 min-w-[250px]">
                  <h3 className="font-semibold text-gray-900 mb-2">{bot.name}</h3>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="flex items-center">
                      <Thermometer className="w-4 h-4 text-red-500 mr-2" />
                      <span>{bot.data.temperature}°C</span>
                    </div>
                    <div className="flex items-center">
                      <Droplets className="w-4 h-4 text-blue-500 mr-2" />
                      <span>{bot.data.salinity} PSU</span>
                    </div>
                    <div className="flex items-center">
                      <Fish className="w-4 h-4 text-teal-500 mr-2" />
                      <span>pH {bot.data.ph}</span>
                    </div>
                    <div className="flex items-center">
                      <Wind className="w-4 h-4 text-gray-500 mr-2" />
                      <span>{bot.data.currentSpeed} m/s</span>
                    </div>
                  </div>
                  <div className="mt-3 pt-2 border-t border-gray-200">
                    <div className="flex items-center justify-between">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        bot.status === 'active' ? 'bg-green-100 text-green-800' :
                        bot.status === 'maintenance' ? 'bg-yellow-100 text-yellow-800' : 
                        'bg-red-100 text-red-800'
                      }`}>
                        {bot.status}
                      </span>
                      <span className="text-xs text-gray-500">
                        {new Date(bot.lastUpdate).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>

        {/* Legend */}
        <div className="absolute top-4 left-4 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-lg p-3 shadow-lg z-[1000]">
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">Legend</h3>
          <div className="space-y-1 text-xs">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span className="text-gray-700 dark:text-gray-300">Active Agro-Bot</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
              <span className="text-gray-700 dark:text-gray-300">Maintenance</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-red-500 rounded-full mr-2 animate-pulse"></div>
              <span className="text-gray-700 dark:text-gray-300">Alert Zone</span>
            </div>
          </div>
        </div>
      </div>

      {/* Status Bar */}
      <div className="p-4 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-300">
          <div className="flex items-center space-x-4">
            <span>Active Bots: {bots.filter(b => b.status === 'active').length}</span>
            <span>Active Alerts: {alerts.length}</span>
            <span>Layer: {currentLayer.charAt(0).toUpperCase() + currentLayer.slice(1)}</span>
          </div>
          <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
            <Activity className="w-3 h-3 mr-1" />
            <span>Last updated: {new Date().toLocaleTimeString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}