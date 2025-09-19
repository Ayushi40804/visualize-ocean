"""
Database utilities for ARGO oceanographic data
Handles SQLite database operations for the chatbot
"""

import os
import sqlite3
from sqlalchemy import create_engine, text
from typing import Dict, List, Any, Optional
import logging

class ArgoDatabase:
    """Database manager for ARGO oceanographic data"""
    
    def __init__(self, db_path: str = "argo_data.sqlite"):
        """Initialize database connection"""
        self.db_path = db_path
        self.engine = None
        self.logger = logging.getLogger(__name__)
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize SQLite database with sample data"""
        try:
            # Create SQLite database connection
            self.engine = create_engine(f"sqlite:///{self.db_path}")
            
            # Create tables and insert sample data
            self._create_tables()
            self._insert_sample_data()
            
            self.logger.info(f"Database initialized successfully at {self.db_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _create_tables(self):
        """Create database tables"""
        with self.engine.connect() as conn:
            # ARGO profiles table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS argo_profiles (
                    profile_id INTEGER PRIMARY KEY,
                    float_id TEXT,
                    latitude REAL,
                    longitude REAL,
                    date_time TEXT,
                    temperature REAL,
                    salinity REAL,
                    pressure REAL,
                    depth REAL,
                    dissolved_oxygen REAL,
                    ph REAL,
                    region TEXT
                )
            """))
            
            # Ocean conditions table for additional monitoring data
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ocean_conditions (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    latitude REAL,
                    longitude REAL,
                    temperature REAL,
                    salinity REAL,
                    current_speed REAL,
                    wave_height REAL,
                    wind_speed REAL,
                    pollution_index REAL,
                    alert_level TEXT
                )
            """))
            
            # Agro-bot monitoring table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS agro_bots (
                    bot_id TEXT PRIMARY KEY,
                    bot_name TEXT,
                    status TEXT,
                    latitude REAL,
                    longitude REAL,
                    last_update TEXT,
                    temperature REAL,
                    salinity REAL,
                    ph REAL,
                    battery_level REAL
                )
            """))
            
            conn.commit()
    
    def _insert_sample_data(self):
        """Insert sample data if tables are empty"""
        with self.engine.connect() as conn:
            # Check if data already exists
            result = conn.execute(text("SELECT COUNT(*) FROM argo_profiles"))
            count = result.scalar()
            
            if count == 0:
                # Insert ARGO profiles sample data
                conn.execute(text("""
                    INSERT INTO argo_profiles (float_id, latitude, longitude, date_time, temperature, salinity, pressure, depth, dissolved_oxygen, ph, region)
                    VALUES 
                    ('5904297', 20.5, 68.5, '2023-01-15', 25.2, 35.1, 10.5, 5.0, 220.5, 8.1, 'Arabian Sea'),
                    ('5904297', 20.5, 68.5, '2023-01-15', 24.8, 35.2, 50.2, 25.0, 218.3, 8.0, 'Arabian Sea'),
                    ('5904297', 20.5, 68.5, '2023-01-15', 22.1, 35.4, 150.8, 75.0, 195.2, 7.9, 'Arabian Sea'),
                    ('5904298', 21.0, 69.0, '2023-01-16', 26.1, 34.9, 15.3, 8.0, 225.1, 8.2, 'Arabian Sea'),
                    ('5904298', 21.0, 69.0, '2023-01-16', 24.5, 35.0, 75.6, 35.0, 210.8, 8.0, 'Arabian Sea'),
                    ('5904299', 19.8, 67.2, '2023-01-17', 23.5, 35.4, 80.1, 40.0, 200.5, 7.8, 'Arabian Sea'),
                    ('5904300', 15.2, 73.1, '2023-01-18', 27.8, 33.8, 12.1, 6.0, 230.2, 8.3, 'Indian Ocean'),
                    ('5904300', 15.2, 73.1, '2023-01-18', 25.9, 34.2, 55.3, 28.0, 215.7, 8.1, 'Indian Ocean'),
                    ('5904301', 12.5, 75.8, '2023-01-19', 28.2, 33.5, 8.9, 4.0, 235.1, 8.4, 'Indian Ocean'),
                    ('5904302', 8.1, 78.3, '2023-01-20', 29.1, 33.2, 18.7, 9.0, 240.8, 8.5, 'Bay of Bengal')
                """))
                
                # Insert ocean conditions data
                conn.execute(text("""
                    INSERT INTO ocean_conditions (timestamp, latitude, longitude, temperature, salinity, current_speed, wave_height, wind_speed, pollution_index, alert_level)
                    VALUES 
                    ('2023-01-15 12:00:00', 20.5, 68.5, 25.2, 35.1, 0.8, 1.5, 15.2, 2.1, 'LOW'),
                    ('2023-01-16 12:00:00', 21.0, 69.0, 26.1, 34.9, 1.2, 2.1, 18.5, 3.2, 'HIGH'),
                    ('2023-01-17 12:00:00', 19.8, 67.2, 23.5, 35.4, 0.6, 1.8, 12.3, 2.8, 'MEDIUM'),
                    ('2023-01-18 12:00:00', 15.2, 73.1, 27.8, 33.8, 0.9, 1.2, 20.1, 1.9, 'LOW'),
                    ('2023-01-19 12:00:00', 12.5, 75.8, 28.2, 33.5, 1.1, 2.5, 25.8, 2.5, 'MEDIUM')
                """))
                
                # Insert agro-bot data
                conn.execute(text("""
                    INSERT INTO agro_bots (bot_id, bot_name, status, latitude, longitude, last_update, temperature, salinity, ph, battery_level)
                    VALUES 
                    ('BOT001', 'Agro-Bot Alpha', 'ACTIVE', 20.5, 68.5, '2023-01-20 14:30:00', 25.2, 35.1, 8.1, 85.5),
                    ('BOT002', 'Agro-Bot Beta', 'ACTIVE', 21.0, 69.0, '2023-01-20 14:25:00', 26.1, 34.9, 8.2, 92.3),
                    ('BOT003', 'Agro-Bot Gamma', 'MAINTENANCE', 19.8, 67.2, '2023-01-19 16:45:00', 23.5, 35.4, 7.8, 45.2),
                    ('BOT004', 'Agro-Bot Delta', 'ACTIVE', 15.2, 73.1, '2023-01-20 14:35:00', 27.8, 33.8, 8.3, 78.9)
                """))
                
                conn.commit()
                self.logger.info("Sample data inserted successfully")
    
    def get_connection(self):
        """Get database connection for external use"""
        return self.engine
    
    def execute_query(self, query: str, parameters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Execute a custom query and return results"""
        try:
            with self.engine.connect() as conn:
                if parameters:
                    result = conn.execute(text(query), parameters)
                else:
                    result = conn.execute(text(query))
                
                # Convert result to list of dictionaries
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            raise
    
    def get_table_info(self) -> Dict[str, List[str]]:
        """Get information about available tables and columns"""
        table_info = {}
        
        try:
            with self.engine.connect() as conn:
                # Get table names
                tables_result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in tables_result.fetchall()]
                
                # Get column info for each table
                for table in tables:
                    columns_result = conn.execute(text(f"PRAGMA table_info({table})"))
                    columns = [row[1] for row in columns_result.fetchall()]
                    table_info[table] = columns
                    
        except Exception as e:
            self.logger.error(f"Failed to get table info: {e}")
            
        return table_info
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample data from a specific table"""
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)
    
    def health_check(self) -> Dict[str, Any]:
        """Check database health and return status"""
        try:
            with self.engine.connect() as conn:
                # Test connection
                conn.execute(text("SELECT 1"))
                
                # Count records in main tables
                argo_count = conn.execute(text("SELECT COUNT(*) FROM argo_profiles")).scalar()
                conditions_count = conn.execute(text("SELECT COUNT(*) FROM ocean_conditions")).scalar()
                bots_count = conn.execute(text("SELECT COUNT(*) FROM agro_bots")).scalar()
                
                return {
                    "status": "healthy",
                    "database_path": self.db_path,
                    "records": {
                        "argo_profiles": argo_count,
                        "ocean_conditions": conditions_count,
                        "agro_bots": bots_count
                    }
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "database_path": self.db_path
            }