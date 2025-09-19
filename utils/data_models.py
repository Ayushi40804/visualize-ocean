from datetime import datetime, timedelta
import random
import pandas as pd
from typing import List, Dict, Any
from utils.database import ArgoDatabase

# Global database instance
_db_instance = None

def get_database():
    """Get or create database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = ArgoDatabase()
    return _db_instance

def get_real_argo_data(limit: int = 100) -> pd.DataFrame:
    """Get real ARGO data from TiDB Cloud database"""
    try:
        db = get_database()
        query = """
        SELECT float_id, latitude, longitude, temperature, salinity, 
               pressure, depth, ph, date_time, region
        FROM argo_profiles 
        WHERE temperature IS NOT NULL AND salinity IS NOT NULL
        ORDER BY date_time DESC
        LIMIT %s
        """
        
        with db.engine.connect() as conn:
            df = pd.read_sql_query(query, conn, params=(limit,))
        return df
    except Exception as e:
        print(f"Error getting real ARGO data: {e}")
        return pd.DataFrame()

def get_argo_summary_stats() -> Dict[str, Any]:
    """Get summary statistics from ARGO data in TiDB Cloud"""
    try:
        db = get_database()
        
        with db.engine.connect() as conn:
            # Get basic stats
            stats_query = """
            SELECT 
                COUNT(*) as total_measurements,
                COUNT(DISTINCT float_id) as unique_floats,
                AVG(temperature) as avg_temperature,
                AVG(salinity) as avg_salinity,
                AVG(ph) as avg_ph,
                MIN(date_time) as earliest_date,
                MAX(date_time) as latest_date
            FROM argo_profiles 
            WHERE temperature IS NOT NULL AND salinity IS NOT NULL
            """
            
            result = pd.read_sql_query(stats_query, conn)
            
            if not result.empty:
                row = result.iloc[0]
                stats = {
                    'total_measurements': int(row['total_measurements']),
                    'unique_floats': int(row['unique_floats']),
                    'avg_temperature': round(float(row['avg_temperature']), 2) if pd.notna(row['avg_temperature']) else 0,
                    'avg_salinity': round(float(row['avg_salinity']), 2) if pd.notna(row['avg_salinity']) else 0,
                    'avg_ph': round(float(row['avg_ph']), 2) if pd.notna(row['avg_ph']) else 0,
                    'earliest_date': str(row['earliest_date']) if pd.notna(row['earliest_date']) else None,
                    'latest_date': str(row['latest_date']) if pd.notna(row['latest_date']) else None
                }
            else:
                stats = {
                    'total_measurements': 0,
                    'unique_floats': 0,
                    'avg_temperature': 0,
                    'avg_salinity': 0,
                    'avg_ph': 0,
                    'earliest_date': None,
                    'latest_date': None
                }
            
            # Get regional breakdown
            regional_query = """
            SELECT region, COUNT(*) as count, 
                   AVG(temperature) as avg_temp, 
                   AVG(salinity) as avg_sal
            FROM argo_profiles 
            WHERE temperature IS NOT NULL AND salinity IS NOT NULL
            GROUP BY region
            """
            regional_df = pd.read_sql_query(regional_query, conn)
            
            stats['regional_breakdown'] = [
                {
                    'region': row['region'],
                    'count': int(row['count']),
                    'avg_temperature': round(float(row['avg_temp']), 2) if pd.notna(row['avg_temp']) else 0,
                    'avg_salinity': round(float(row['avg_sal']), 2) if pd.notna(row['avg_sal']) else 0
                }
                for _, row in regional_df.iterrows()
            ]
            
            return stats
        
    except Exception as e:
        print(f"Error getting ARGO summary stats: {e}")
        return {
            'total_measurements': 0,
            'unique_floats': 0,
            'avg_temperature': 0,
            'avg_salinity': 0,
            'avg_ph': 0,
            'earliest_date': None,
            'latest_date': None,
            'regional_breakdown': []
        }

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