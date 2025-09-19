from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

def get_mock_agrobots() -> List[Dict[str, Any]]:
    """Get mock Agro-Bot data"""
    return [
        {
            'id': 'bot-1',
            'name': 'Agro-Bot Alpha',
            'latitude': -20.0,
            'longitude': 57.5,
            'status': 'active',
            'lastUpdate': (datetime.now() - timedelta(minutes=2)).isoformat(),
            'data': {
                'temperature': 24.5,
                'salinity': 35.2,
                'ph': 8.1,
                'oxygenLevel': 7.2,
                'pollutionIndex': 2.1,
                'currentSpeed': 0.8,
                'currentDirection': 120
            }
        },
        {
            'id': 'bot-2',
            'name': 'Agro-Bot Beta',
            'latitude': -15.5,
            'longitude': 60.2,
            'status': 'active',
            'lastUpdate': (datetime.now() - timedelta(minutes=4)).isoformat(),
            'data': {
                'temperature': 26.1,
                'salinity': 34.8,
                'ph': 7.9,
                'oxygenLevel': 6.8,
                'pollutionIndex': 3.2,
                'currentSpeed': 1.2,
                'currentDirection': 95
            }
        },
        {
            'id': 'bot-3',
            'name': 'Agro-Bot Gamma',
            'latitude': -25.3,
            'longitude': 55.8,
            'status': 'maintenance',
            'lastUpdate': (datetime.now() - timedelta(minutes=45)).isoformat(),
            'data': {
                'temperature': 23.8,
                'salinity': 35.5,
                'ph': 8.2,
                'oxygenLevel': 7.5,
                'pollutionIndex': 1.8,
                'currentSpeed': 0.6,
                'currentDirection': 140
            }
        },
        {
            'id': 'bot-4',
            'name': 'Agro-Bot Delta',
            'latitude': -18.2,
            'longitude': 63.1,
            'status': 'active',
            'lastUpdate': (datetime.now() - timedelta(minutes=7)).isoformat(),
            'data': {
                'temperature': 25.2,
                'salinity': 34.9,
                'ph': 8.0,
                'oxygenLevel': 6.9,
                'pollutionIndex': 2.5,
                'currentSpeed': 1.0,
                'currentDirection': 110
            }
        }
    ]

def get_mock_alerts() -> List[Dict[str, Any]]:
    """Get mock alert data"""
    return [
        {
            'id': 'alert-1',
            'title': 'High Pollution Detected',
            'description': 'Pollution index exceeding safe levels near shipping lanes',
            'severity': 'high',
            'location': {'latitude': -15.5, 'longitude': 60.2},
            'timestamp': (datetime.now() - timedelta(minutes=15)).isoformat(),
            'type': 'pollution',
            'isRead': False
        },
        {
            'id': 'alert-2',
            'title': 'Temperature Anomaly',
            'description': 'Unusually high water temperature detected',
            'severity': 'medium',
            'location': {'latitude': -18.2, 'longitude': 63.1},
            'timestamp': (datetime.now() - timedelta(minutes=30)).isoformat(),
            'type': 'anomaly',
            'isRead': False
        },
        {
            'id': 'alert-3',
            'title': 'Bot Maintenance Required',
            'description': 'Agro-Bot Gamma requires scheduled maintenance',
            'severity': 'low',
            'location': {'latitude': -25.3, 'longitude': 55.8},
            'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
            'type': 'equipment',
            'isRead': True
        }
    ]

def get_recent_data() -> List[Dict[str, Any]]:
    """Get recent time-series data for charts"""
    times = []
    current_time = datetime.now()
    
    for i in range(30, 0, -5):  # Last 30 minutes, every 5 minutes
        times.append((current_time - timedelta(minutes=i)).strftime('%H:%M'))
    
    data = []
    base_temp = 24.0
    base_salinity = 35.0
    base_ph = 8.0
    
    for time_str in times:
        data.append({
            'time': time_str,
            'temperature': base_temp + random.uniform(-0.5, 0.5),
            'salinity': base_salinity + random.uniform(-0.3, 0.3),
            'ph': base_ph + random.uniform(-0.2, 0.2)
        })
        # Add slight trending
        base_temp += random.uniform(-0.1, 0.1)
        base_salinity += random.uniform(-0.05, 0.05)
        base_ph += random.uniform(-0.02, 0.02)
    
    return data

def get_mock_routes() -> List[Dict[str, Any]]:
    """Get mock route optimization data"""
    return [
        {
            'id': 'route-1',
            'name': 'Mumbai to Port Louis',
            'startPoint': {'latitude': 19.0760, 'longitude': 72.8777},
            'endPoint': {'latitude': -20.1619, 'longitude': 57.5012},
            'optimizedPath': [
                {'latitude': 19.0760, 'longitude': 72.8777},
                {'latitude': 15.0, 'longitude': 70.0},
                {'latitude': 10.0, 'longitude': 65.0},
                {'latitude': 0.0, 'longitude': 60.0},
                {'latitude': -10.0, 'longitude': 58.0},
                {'latitude': -20.1619, 'longitude': 57.5012}
            ],
            'estimatedTime': '14 days 6 hours',
            'fuelSavings': 15.2,
            'weatherConditions': 'Favorable'
        },
        {
            'id': 'route-2',
            'name': 'Chennai to Colombo',
            'startPoint': {'latitude': 13.0827, 'longitude': 80.2707},
            'endPoint': {'latitude': 6.9271, 'longitude': 79.8612},
            'optimizedPath': [
                {'latitude': 13.0827, 'longitude': 80.2707},
                {'latitude': 10.0, 'longitude': 80.0},
                {'latitude': 6.9271, 'longitude': 79.8612}
            ],
            'estimatedTime': '2 days 8 hours',
            'fuelSavings': 8.7,
            'weatherConditions': 'Moderate seas'
        }
    ]

def get_chat_messages() -> List[Dict[str, Any]]:
    """Get mock chat messages"""
    return [
        {
            'id': '1',
            'type': 'assistant',
            'content': 'Hello! I\'m your Agro-Ocean AI assistant. How can I help you today? I can provide information about ocean conditions, bot status, and help optimize your operations.',
            'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat()
        }
    ]