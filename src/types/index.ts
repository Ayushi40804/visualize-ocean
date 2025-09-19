export interface User {
  id: string;
  name: string;
  email: string;
  role: 'researcher' | 'weather_analyst' | 'marine_authority' | 'fleet_manager';
  avatar?: string;
}

export interface AgroBot {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  status: 'active' | 'maintenance' | 'offline';
  lastUpdate: string;
  data: {
    temperature: number;
    salinity: number;
    ph: number;
    oxygenLevel: number;
    pollutionIndex: number;
    currentSpeed: number;
    currentDirection: number;
  };
}

export interface Alert {
  id: string;
  type: 'cyclone' | 'anomaly' | 'pollution' | 'equipment';
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  location: {
    latitude: number;
    longitude: number;
  };
  timestamp: string;
  isRead: boolean;
}

export interface Route {
  id: string;
  name: string;
  startPoint: {
    latitude: number;
    longitude: number;
  };
  endPoint: {
    latitude: number;
    longitude: number;
  };
  optimizedPath: Array<{
    latitude: number;
    longitude: number;
  }>;
  estimatedTime: string;
  fuelSavings: number;
  weatherConditions: string;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: string;
}