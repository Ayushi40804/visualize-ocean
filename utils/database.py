"""
Database utilities for ARGO oceanographic data
Handles both SQLite and TiDB Cloud database operations for the chatbot
Now supports both sample data and real NetCDF data ingestion
"""

import os
import sqlite3
from sqlalchemy import create_engine, text
from typing import Dict, List, Any, Optional
import logging
from utils.config import config

class ArgoDatabase:
    """Database manager for ARGO oceanographic data - TiDB Cloud only"""
    
    def __init__(self, use_real_data: bool = False):
        """Initialize TiDB Cloud database connection"""
        self.engine = None
        self.logger = logging.getLogger(__name__)
        self.use_real_data = use_real_data
        self.use_tidb = True
        self.db_config = config.get_database_config()
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize TiDB Cloud database connection"""
        try:
            self._initialize_tidb()
            
            # Check if database exists and has real data
            real_data_exists = self._check_real_data_exists()
            
            if real_data_exists:
                self.logger.info(f"Found existing real ARGO data in TiDB database")
                self.use_real_data = True
            else:
                # Create tables and insert sample data if no real data
                self._create_tables()
                if not self.use_real_data:
                    self._insert_sample_data()
                    self.logger.info(f"TiDB database initialized with sample data")
                else:
                    self.logger.info(f"TiDB database initialized for real data ingestion")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize TiDB database: {e}")
            raise
    
    def _initialize_tidb(self):
        """Initialize TiDB Cloud database connection"""
        try:
            tidb_host = self.db_config['tidb_host']
            tidb_port = self.db_config['tidb_port']
            tidb_user = self.db_config['tidb_user']
            tidb_password = self.db_config['tidb_password']
            tidb_database = self.db_config['tidb_database']
            
            # Create TiDB connection string
            connection_string = f"mysql+pymysql://{tidb_user}:{tidb_password}@{tidb_host}:{tidb_port}/{tidb_database}?ssl_ca=&ssl_cert=&ssl_key=&ssl_verify_cert=true&ssl_verify_identity=true"
            
            self.engine = create_engine(connection_string)
            self.use_tidb = True
            self.logger.info(f"Connected to TiDB Cloud: {tidb_host}:{tidb_port}/{tidb_database}")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to TiDB Cloud: {e}")
            raise
    
    def _check_real_data_exists(self) -> bool:
        """Check if the database already contains real ARGO data"""
        try:
            with self.engine.connect() as conn:
                # Check if tables exist and have data
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='argo_profiles'"))
                if result.fetchone():
                    count_result = conn.execute(text("SELECT COUNT(*) FROM argo_profiles"))
                    count = count_result.scalar()
                    if count > 50:  # Assume real data if more than 50 records
                        return True
                return False
        except Exception:
            return False
    
    def use_netcdf_data(self) -> bool:
        """
        Switch to using real NetCDF data from Indian Ocean ARGO sources
        Returns True if successful, False otherwise
        """
        try:
            from utils.indian_ocean_netcdf import IndianOceanArgoProcessor
            
            self.logger.info("Initiating Indian Ocean ARGO NetCDF data ingestion...")
            self.logger.info("Sources: NOAA NCEI & IFREMER Indian Ocean")
            processor = IndianOceanArgoProcessor(db_path=self.db_path)
            success = processor.run_full_ingestion()
            
            if success:
                self.use_real_data = True
                self.logger.info("Successfully switched to real Indian Ocean ARGO data!")
                return True
            else:
                self.logger.error("Failed to ingest Indian Ocean NetCDF data")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during Indian Ocean NetCDF data ingestion: {e}")
            return False
    
    def _create_tables(self):
        """Create database tables for TiDB Cloud"""
        with self.engine.connect() as conn:
            # ARGO profiles table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS argo_profiles (
                    profile_id INT AUTO_INCREMENT PRIMARY KEY,
                    float_id VARCHAR(50),
                    latitude DECIMAL(10, 6),
                    longitude DECIMAL(10, 6),
                    date_time DATETIME,
                    temperature DECIMAL(8, 4),
                    salinity DECIMAL(8, 4),
                    pressure DECIMAL(8, 4),
                    depth DECIMAL(8, 4),
                    dissolved_oxygen DECIMAL(8, 4),
                    ph DECIMAL(4, 2),
                    region VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_float_id (float_id),
                    INDEX idx_region (region),
                    INDEX idx_date_time (date_time)
                )
            """))
            
            # Ocean conditions table for additional monitoring data
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ocean_conditions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME,
                    latitude DECIMAL(10, 6),
                    longitude DECIMAL(10, 6),
                    temperature DECIMAL(8, 4),
                    salinity DECIMAL(8, 4),
                    current_speed DECIMAL(6, 4),
                    wave_height DECIMAL(6, 4),
                    wind_speed DECIMAL(6, 4),
                    pollution_index DECIMAL(6, 4),
                    alert_level VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Agro-bot monitoring table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS agro_bots (
                    bot_id VARCHAR(50) PRIMARY KEY,
                    bot_name VARCHAR(100),
                    status VARCHAR(20),
                    latitude DECIMAL(10, 6),
                    longitude DECIMAL(10, 6),
                    last_update DATETIME,
                    temperature DECIMAL(8, 4),
                    salinity DECIMAL(8, 4),
                    ph DECIMAL(4, 2),
                    battery_level DECIMAL(5, 2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            conn.commit()
    
    def _insert_sample_data(self):
        """Insert sample data for TiDB Cloud"""
        with self.engine.connect() as conn:
            # Check if data already exists
            result = conn.execute(text("SELECT COUNT(*) FROM argo_profiles"))
            count = result.scalar()
            
            if count == 0:
                # Insert ARGO profiles sample data
                conn.execute(text("""
                    INSERT INTO argo_profiles (float_id, latitude, longitude, date_time, temperature, salinity, pressure, depth, dissolved_oxygen, ph, region)
                    VALUES 
                    ('5904297', 20.5, 68.5, '2023-01-15 12:00:00', 25.2, 35.1, 10.5, 5.0, 220.5, 8.1, 'Arabian Sea'),
                    ('5904297', 20.5, 68.5, '2023-01-15 12:30:00', 24.8, 35.2, 50.2, 25.0, 218.3, 8.0, 'Arabian Sea'),
                    ('5904297', 20.5, 68.5, '2023-01-15 13:00:00', 22.1, 35.4, 150.8, 75.0, 195.2, 7.9, 'Arabian Sea'),
                    ('5904298', 21.0, 69.0, '2023-01-16 12:00:00', 26.1, 34.9, 15.3, 8.0, 225.1, 8.2, 'Arabian Sea'),
                    ('5904298', 21.0, 69.0, '2023-01-16 12:30:00', 24.5, 35.0, 75.6, 35.0, 210.8, 8.0, 'Arabian Sea'),
                    ('5904299', 19.8, 67.2, '2023-01-17 12:00:00', 23.5, 35.4, 80.1, 40.0, 200.5, 7.8, 'Arabian Sea'),
                    ('5904300', 15.2, 73.1, '2023-01-18 12:00:00', 27.8, 33.8, 12.1, 6.0, 230.2, 8.3, 'Indian Ocean'),
                    ('5904300', 15.2, 73.1, '2023-01-18 12:30:00', 25.9, 34.2, 55.3, 28.0, 215.7, 8.1, 'Indian Ocean'),
                    ('5904301', 12.5, 75.8, '2023-01-19 12:00:00', 28.2, 33.5, 8.9, 4.0, 235.1, 8.4, 'Indian Ocean'),
                    ('5904302', 8.1, 78.3, '2023-01-20 12:00:00', 29.1, 33.2, 18.7, 9.0, 240.8, 8.5, 'Bay of Bengal')
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
                self.logger.info("Sample data inserted successfully into TiDB Cloud")
    
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
        """Check TiDB database health and return status"""
        try:
            with self.engine.connect() as conn:
                # Test connection
                conn.execute(text("SELECT 1"))
                
                # Count records in main tables
                argo_count = conn.execute(text("SELECT COUNT(*) FROM argo_profiles")).scalar()
                conditions_count = conn.execute(text("SELECT COUNT(*) FROM ocean_conditions")).scalar()
                bots_count = conn.execute(text("SELECT COUNT(*) FROM agro_bots")).scalar()
                
                # Check data source type
                data_source = "Real NetCDF Data" if self.use_real_data or argo_count > 50 else "Sample Data"
                
                return {
                    "status": "healthy",
                    "database_type": "TiDB Cloud",
                    "database_path": f"{self.db_config['tidb_host']}:{self.db_config['tidb_port']}/{self.db_config['tidb_database']}",
                    "data_source": data_source,
                    "use_real_data": self.use_real_data,
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
                "database_type": "TiDB Cloud",
                "database_path": f"{self.db_config['tidb_host']}:{self.db_config['tidb_port']}/{self.db_config['tidb_database']}",
                "data_source": "Unknown"
            }
    
    def test_tidb_connection(self) -> Dict[str, Any]:
        """Test TiDB Cloud connection specifically"""
        try:
            tidb_host = self.db_config['tidb_host']
            tidb_port = self.db_config['tidb_port']
            tidb_user = self.db_config['tidb_user']
            tidb_password = self.db_config.get('tidb_password') or os.getenv('TIDB_PASSWORD')
            tidb_database = self.db_config['tidb_database']
            
            if not tidb_password:
                return {
                    "status": "error",
                    "error": "TiDB password not provided",
                    "suggestion": "Set TIDB_PASSWORD environment variable"
                }
            
            # Create test connection
            connection_string = f"mysql+pymysql://{tidb_user}:{tidb_password}@{tidb_host}:{tidb_port}/{tidb_database}?ssl_ca=&ssl_cert=&ssl_key=&ssl_verify_cert=true&ssl_verify_identity=true"
            test_engine = create_engine(connection_string)
            
            with test_engine.connect() as conn:
                result = conn.execute(text("SELECT VERSION() as version, DATABASE() as database"))
                row = result.fetchone()
                
                return {
                    "status": "success",
                    "host": tidb_host,
                    "port": tidb_port,
                    "user": tidb_user,
                    "database": tidb_database,
                    "server_version": row[0] if row else "Unknown",
                    "current_database": row[1] if row else "Unknown",
                    "message": "TiDB Cloud connection successful"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "host": self.db_config['tidb_host'],
                "port": self.db_config['tidb_port'],
                "suggestion": "Check credentials and network connectivity"
            }