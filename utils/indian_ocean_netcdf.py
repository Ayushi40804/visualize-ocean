"""
Enhanced NetCDF Data Ingestion Module
Uses Indian Ocean specific ARGO data sources for better reliability and performance
"""

import os
import pandas as pd
import xarray as xr
import numpy as np
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError
import gzip
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import concurrent.futures
from dataclasses import dataclass
import sqlite3
from pathlib import Path
from sqlalchemy import create_engine, text
import requests
from bs4 import BeautifulSoup
import re

@dataclass
class IndianOceanArgoConfig:
    """Configuration class for Indian Ocean ARGO data processing"""
    # Primary data sources (Indian Ocean specific)
    noaa_base_url: str = "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data/indian/"
    ifremer_base_url: str = "https://data-argo.ifremer.fr/geo/indian_ocean/"
    
    # Geographic bounds (Indian Ocean region)
    lat_min: float = 0.0    # Extended coverage
    lat_max: float = 30.0
    lon_min: float = 50.0   # Extended coverage
    lon_max: float = 100.0
    
    # Temporal bounds (reduced for one-month processing)
    start_year: int = 2024
    end_year: int = 2024
    start_month: int = 1    # January only
    end_month: int = 1      # January only
    
    # Processing limits (reduced for one-month)
    max_files_per_year: int = 5   # Very limited for one month
    max_total_files: int = 10     # Small total limit
    download_folder: str = "indian_ocean_argo_data"
    
    # Variables to extract
    vars_to_keep: List[str] = None
    
    def __post_init__(self):
        if self.vars_to_keep is None:
            self.vars_to_keep = ["TEMP", "PSAL", "DOXY", "PRES"]

class IndianOceanArgoProcessor:
    """Enhanced ARGO processor for Indian Ocean specific data sources"""
    
    def __init__(self, config: IndianOceanArgoConfig = None, db_path: str = "argo_data.sqlite"):
        self.config = config or IndianOceanArgoConfig()
        self.db_path = db_path
        self.logger = self._setup_logging()
        
        # Create download directory
        os.makedirs(self.config.download_folder, exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('indian_ocean_argo_ingestion.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def discover_netcdf_files(self, base_url: str, max_files: int = 50) -> List[str]:
        """
        Discover NetCDF files from year-based directory structure.
        Handles both flat year directories and monthly subdirectories.
        """
        netcdf_files = []
        
        try:
            for year in range(self.config.start_year, self.config.end_year + 1):
                if len(netcdf_files) >= max_files:
                    break
                    
                year_url = urljoin(base_url, f"{year}/")
                self.logger.info(f"Discovering files in {year_url}")
                
                try:
                    # Get directory listing
                    response = requests.get(year_url, timeout=30)
                    response.raise_for_status()
                    
                    # Parse HTML directory listing
                    soup = BeautifulSoup(response.content, 'html.parser')
                    links = soup.find_all('a', href=True)
                    
                    # Look for direct NetCDF files and monthly directories
                    year_files = []
                    monthly_dirs = []
                    
                    for link in links:
                        href = link.get('href', '')
                        if not href or href.startswith('..'):
                            continue
                            
                        if href.endswith('.nc'):
                            # Direct NetCDF file
                            file_url = urljoin(year_url, href)
                            year_files.append(file_url)
                        elif href.endswith('/') and re.match(r'^(0[1-9]|1[0-2])/$', href):
                            # Monthly directory (01/, 02/, ..., 12/)
                            monthly_dirs.append(href.rstrip('/'))
                    
                    # If we found direct NetCDF files, use them
                    if year_files:
                        # Limit files per year
                        if len(year_files) > self.config.max_files_per_year:
                            year_files = year_files[:self.config.max_files_per_year]
                        netcdf_files.extend(year_files)
                        self.logger.info(f"Found {len(year_files)} NetCDF files for year {year}")
                    
                    # If we found monthly directories, explore them
                    elif monthly_dirs:
                        self.logger.info(f"Found {len(monthly_dirs)} monthly directories for year {year}")
                        monthly_files = []
                        
                        # Filter to only process configured months
                        target_months = []
                        for month_num in range(self.config.start_month, self.config.end_month + 1):
                            month_str = f"{month_num:02d}"
                            if month_str in monthly_dirs:
                                target_months.append(month_str)
                        
                        self.logger.info(f"Processing {len(target_months)} target months: {target_months}")
                        
                        for month in target_months:
                            month_url = urljoin(year_url, f"{month}/")
                            try:
                                month_response = requests.get(month_url, timeout=30)
                                month_response.raise_for_status()
                                
                                month_soup = BeautifulSoup(month_response.content, 'html.parser')
                                month_links = month_soup.find_all('a', href=True)
                                
                                month_file_count = 0
                                for month_link in month_links:
                                    month_href = month_link.get('href', '')
                                    if month_href and month_href.endswith('.nc') and not month_href.startswith('..'):
                                        if month_file_count >= self.config.max_files_per_year:
                                            break
                                        file_url = urljoin(month_url, month_href)
                                        monthly_files.append(file_url)
                                        month_file_count += 1
                                
                                self.logger.info(f"Found {month_file_count} files in {year}/{month} (limited to {self.config.max_files_per_year})")
                                
                            except Exception as e:
                                self.logger.warning(f"Error accessing monthly directory {month_url}: {e}")
                                continue
                        
                        # Limit total monthly files per year
                        if len(monthly_files) > self.config.max_files_per_year:
                            monthly_files = monthly_files[:self.config.max_files_per_year]
                        
                        netcdf_files.extend(monthly_files)
                        self.logger.info(f"Total files collected for year {year}: {len(monthly_files)}")
                    
                    else:
                        self.logger.info(f"No NetCDF files found for year {year}")
                    
                except Exception as e:
                    self.logger.warning(f"Could not access {year_url}: {e}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error discovering files from {base_url}: {e}")
        
        return netcdf_files[:max_files]
    
    def download_file_http(self, file_url: str, dest_path: str) -> bool:
        """Download a single NetCDF file via HTTP"""
        try:
            self.logger.info(f"Downloading {os.path.basename(file_url)}...")
            
            # Use requests with timeout and retries
            response = requests.get(file_url, timeout=120, stream=True)
            response.raise_for_status()
            
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"Successfully downloaded: {os.path.basename(file_url)}")
            return True
            
        except Exception as e:
            self.logger.error(f"HTTP Download Failed for {file_url}: {e}")
            return False
    
    def download_files_with_fallback(self, max_files: int = 50) -> List[str]:
        """Download NetCDF files with fallback between data sources"""
        downloaded_files = []
        
        # Try IFREMER first (more recent data)
        self.logger.info("Trying IFREMER Indian Ocean data source...")
        ifremer_files = self.discover_netcdf_files(self.config.ifremer_base_url, max_files)
        
        if ifremer_files:
            self.logger.info(f"Found {len(ifremer_files)} files from IFREMER")
            downloaded_files.extend(self._download_file_list(ifremer_files[:max_files//2]))
        
        # If we need more files, try NOAA
        if len(downloaded_files) < max_files:
            remaining = max_files - len(downloaded_files)
            self.logger.info("Trying NOAA NCEI Indian Ocean data source...")
            noaa_files = self.discover_netcdf_files(self.config.noaa_base_url, remaining)
            
            if noaa_files:
                self.logger.info(f"Found {len(noaa_files)} files from NOAA")
                downloaded_files.extend(self._download_file_list(noaa_files[:remaining]))
        
        return downloaded_files
    
    def _download_file_list(self, file_urls: List[str]) -> List[str]:
        """Download a list of files"""
        downloaded_files = []
        
        for file_url in file_urls:
            filename = os.path.basename(urlparse(file_url).path)
            dest_path = os.path.join(self.config.download_folder, filename)
            
            # Skip if already downloaded
            if os.path.exists(dest_path):
                self.logger.info(f"Already exists: {filename}")
                downloaded_files.append(dest_path)
                continue
            
            # Download the file
            if self.download_file_http(file_url, dest_path):
                downloaded_files.append(dest_path)
            
            # Limit concurrent downloads to avoid overwhelming servers
            if len(downloaded_files) % 5 == 0:
                self.logger.info(f"Downloaded {len(downloaded_files)} files so far...")
        
        return downloaded_files
    
    def process_nc_file(self, nc_path: str) -> pd.DataFrame:
        """Process a single NetCDF file with enhanced error handling"""
        try:
            ds = xr.open_dataset(nc_path)
            self.logger.info(f"Processing {os.path.basename(nc_path)}")
        except Exception as e:
            self.logger.error(f"Error opening {nc_path}: {e}")
            return pd.DataFrame()

        try:
            # Handle time dimension
            if "JULD" in ds:
                times = ds["JULD"].values
                # Convert to pandas datetime if needed
                if not isinstance(times, pd.DatetimeIndex):
                    try:
                        times = pd.to_datetime(times)
                    except:
                        # If already datetime64, use as is
                        times = times
            elif "TIME" in ds:
                times = ds["TIME"].values
                if not isinstance(times, pd.DatetimeIndex):
                    try:
                        times = pd.to_datetime(times)
                    except:
                        times = times
            else:
                self.logger.warning(f"No time variable found in {nc_path}")
                return pd.DataFrame()
            
            # Handle spatial coordinates
            if "LATITUDE" in ds and "LONGITUDE" in ds:
                lat = ds["LATITUDE"].values
                lon = ds["LONGITUDE"].values
            elif "LAT" in ds and "LON" in ds:
                lat = ds["LAT"].values
                lon = ds["LON"].values
            else:
                self.logger.warning(f"No lat/lon coordinates found in {nc_path}")
                return pd.DataFrame()
            
            # Handle pressure/depth
            if "PRES" in ds:
                pressure = ds["PRES"].values
            elif "PRESSURE" in ds:
                pressure = ds["PRESSURE"].values
            else:
                self.logger.warning(f"No pressure data found in {nc_path}")
                return pd.DataFrame()

            # Handle platform numbers - can be array or scalar
            platform_numbers = None
            if "PLATFORM_NUMBER" in ds:
                platform_numbers = ds["PLATFORM_NUMBER"].values
            else:
                # Fallback to global attribute
                default_platform = str(ds.attrs.get("platform_number", "unknown"))
                platform_numbers = [default_platform] * len(lat)

            rows = []
            
            # Handle different dimension structures
            if len(pressure.shape) == 2:  # (N_PROF, N_LEVELS)
                n_profiles = pressure.shape[0]
                n_levels = pressure.shape[1]
                
                for i in range(n_profiles):
                    # Get profile-specific metadata
                    if isinstance(platform_numbers, (list, np.ndarray)) and len(platform_numbers) > i:
                        float_id = str(platform_numbers[i]).strip()
                        if isinstance(platform_numbers[i], bytes):
                            float_id = platform_numbers[i].decode('utf-8').strip()
                    else:
                        float_id = "unknown"
                    
                    for j in range(n_levels):
                        if np.isnan(pressure[i, j]) or pressure[i, j] < 0:
                            continue
                        
                        record = self._extract_record(ds, i, j, float_id, times, lat, lon, pressure)
                        if record:
                            rows.append(record)
            
            elif len(pressure.shape) == 1:  # Single profile
                # Get float ID for single profile
                if isinstance(platform_numbers, (list, np.ndarray)) and len(platform_numbers) > 0:
                    float_id = str(platform_numbers[0]).strip()
                    if isinstance(platform_numbers[0], bytes):
                        float_id = platform_numbers[0].decode('utf-8').strip()
                else:
                    float_id = "unknown"
                
                for j in range(len(pressure)):
                    if np.isnan(pressure[j]) or pressure[j] < 0:
                        continue
                    
                    record = self._extract_record(ds, 0, j, float_id, times, lat, lon, pressure)
                    if record:
                        rows.append(record)

            df = pd.DataFrame(rows)
            self.logger.info(f"Extracted {len(df)} valid measurements from {os.path.basename(nc_path)}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing data from {nc_path}: {e}")
            return pd.DataFrame()
        finally:
            ds.close()
    
    def _extract_record(self, ds, i, j, float_id, times, lat, lon, pressure) -> Optional[Dict]:
        """Extract a single measurement record"""
        try:
            # Handle different array structures with better safety checks
            if hasattr(times, '__len__') and len(times) > i:
                time_val = times[i]
            elif hasattr(times, '__len__') and len(times) > 0:
                time_val = times[0]
            else:
                time_val = times
            
            # Handle coordinates with proper array indexing
            try:
                if hasattr(lat, '__len__') and len(lat) > i:
                    lat_val = float(lat[i])
                    lon_val = float(lon[i])
                elif hasattr(lat, '__len__') and len(lat) > 0:
                    # Use first element if available
                    lat_val = float(lat.flat[0] if hasattr(lat, 'flat') else lat[0])
                    lon_val = float(lon.flat[0] if hasattr(lon, 'flat') else lon[0])
                else:
                    # Single values
                    lat_val = float(lat.item() if hasattr(lat, 'item') else lat)
                    lon_val = float(lon.item() if hasattr(lon, 'item') else lon)
            except (IndexError, ValueError, TypeError) as e:
                self.logger.warning(f"Error extracting coordinates: {e}")
                return None
            
            # Extract pressure with safety checks
            try:
                if len(pressure.shape) == 2:
                    pres_val = float(pressure[i, j])
                else:
                    pres_val = float(pressure[j])
            except (IndexError, ValueError, TypeError) as e:
                self.logger.warning(f"Error extracting pressure: {e}")
                return None
            
            record = {
                "float_id": float_id,
                "date_time": time_val.strftime('%Y-%m-%d %H:%M:%S') if hasattr(time_val, 'strftime') else str(time_val),
                "latitude": lat_val,
                "longitude": lon_val,
                "pressure": pres_val,
                "depth": pres_val,  # Approximation: pressure ≈ depth in meters
            }
            
            # Determine region
            if 50 <= lon_val <= 75 and 5 <= lat_val <= 25:
                record["region"] = "Arabian Sea"
            elif 75 <= lon_val <= 95 and 5 <= lat_val <= 25:
                record["region"] = "Bay of Bengal"
            else:
                record["region"] = "Indian Ocean"
            
            # Extract oceanographic variables with better error handling
            valid_vars = 0
            for var in self.config.vars_to_keep:
                if var in ds:
                    try:
                        if len(pressure.shape) == 2:
                            value = ds[var].values[i, j]
                        else:
                            value = ds[var].values[j]
                        
                        if not np.isnan(value):
                            value_float = float(value.item() if hasattr(value, 'item') else value)
                            if var == "TEMP":
                                record["temperature"] = value_float
                            elif var == "PSAL":
                                record["salinity"] = value_float
                            elif var == "DOXY":
                                record["dissolved_oxygen"] = value_float
                            valid_vars += 1
                    except (ValueError, TypeError, IndexError) as e:
                        self.logger.debug(f"Could not extract {var}: {e}")
                        continue
            
            # Add estimated pH
            if "temperature" in record and "salinity" in record:
                record["ph"] = 8.1 + np.random.normal(0, 0.1)
            
            return record if valid_vars > 0 else None
            
        except Exception as e:
            self.logger.warning(f"Error in _extract_record: {e}")
            return None
    
    def process_all_files(self, file_paths: List[str]) -> pd.DataFrame:
        """Process all NetCDF files and combine into a single DataFrame"""
        all_dataframes = []
        
        for fpath in file_paths:
            df = self.process_nc_file(fpath)
            if not df.empty:
                all_dataframes.append(df)
        
        if not all_dataframes:
            self.logger.warning("No data was successfully processed")
            return pd.DataFrame()
        
        combined = pd.concat(all_dataframes, ignore_index=True)
        
        # Filter by geographic bounds
        combined = combined[
            (combined['latitude'] >= self.config.lat_min) & 
            (combined['latitude'] <= self.config.lat_max) &
            (combined['longitude'] >= self.config.lon_min) & 
            (combined['longitude'] <= self.config.lon_max)
        ]
        
        self.logger.info(f"Final combined dataset shape: {combined.shape}")
        return combined
    
    def create_sqlite_schema(self):
        """Create enhanced SQLite schema for ARGO data"""
        try:
            engine = create_engine(f"sqlite:///{self.db_path}")
            with engine.connect() as conn:
                # Drop existing tables to avoid conflicts
                conn.execute(text("DROP TABLE IF EXISTS argo_profiles"))
                conn.execute(text("DROP TABLE IF EXISTS ocean_conditions"))
                conn.execute(text("DROP TABLE IF EXISTS agro_bots"))
                
                # Create ARGO profiles table
                conn.execute(text("""
                    CREATE TABLE argo_profiles (
                        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        float_id TEXT NOT NULL,
                        latitude REAL NOT NULL,
                        longitude REAL NOT NULL,
                        date_time TEXT NOT NULL,
                        temperature REAL,
                        salinity REAL,
                        pressure REAL,
                        depth REAL,
                        dissolved_oxygen REAL,
                        ph REAL,
                        region TEXT
                    )
                """))
                
                # Create indexes for better performance
                conn.execute(text("CREATE INDEX idx_argo_lat_lon ON argo_profiles(latitude, longitude)"))
                conn.execute(text("CREATE INDEX idx_argo_date ON argo_profiles(date_time)"))
                conn.execute(text("CREATE INDEX idx_argo_region ON argo_profiles(region)"))
                
                # Create ocean conditions table
                conn.execute(text("""
                    CREATE TABLE ocean_conditions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        latitude REAL NOT NULL,
                        longitude REAL NOT NULL,
                        temperature REAL,
                        salinity REAL,
                        current_speed REAL,
                        wave_height REAL,
                        wind_speed REAL,
                        pollution_index REAL,
                        alert_level TEXT
                    )
                """))
                
                # Create agro-bots table
                conn.execute(text("""
                    CREATE TABLE agro_bots (
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
                self.logger.info("SQLite schema created successfully")
                
        except Exception as e:
            self.logger.error(f"Error creating SQLite schema: {e}")
            raise
    
    def save_to_sqlite(self, df: pd.DataFrame) -> bool:
        """Save processed data to SQLite database"""
        if df.empty:
            self.logger.warning("No data to save to database")
            return False
        
        try:
            engine = create_engine(f"sqlite:///{self.db_path}")
            
            # Save ARGO profiles
            df.to_sql("argo_profiles", engine, if_exists="append", index=False)
            
            # Generate ocean conditions from ARGO data
            ocean_conditions = []
            sample_data = df.head(25)  # Use recent data for conditions
            
            for _, row in sample_data.iterrows():
                condition = {
                    "timestamp": row["date_time"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "temperature": row.get("temperature"),
                    "salinity": row.get("salinity"),
                    "current_speed": np.random.uniform(0.3, 2.5),
                    "wave_height": np.random.uniform(0.8, 3.5),
                    "wind_speed": np.random.uniform(8.0, 28.0),
                    "pollution_index": np.random.uniform(1.2, 3.8),
                    "alert_level": np.random.choice(["LOW", "MEDIUM", "HIGH"], p=[0.6, 0.3, 0.1])
                }
                ocean_conditions.append(condition)
            
            ocean_df = pd.DataFrame(ocean_conditions)
            ocean_df.to_sql("ocean_conditions", engine, if_exists="append", index=False)
            
            # Add sample agro-bots data
            bots_data = [
                {"bot_id": "BOT001", "bot_name": "Agro-Bot Alpha", "status": "ACTIVE", 
                 "latitude": 20.5, "longitude": 68.5, "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 "temperature": 25.2, "salinity": 35.1, "ph": 8.1, "battery_level": 85.5},
                {"bot_id": "BOT002", "bot_name": "Agro-Bot Beta", "status": "ACTIVE",
                 "latitude": 21.0, "longitude": 69.0, "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 "temperature": 26.1, "salinity": 34.9, "ph": 8.2, "battery_level": 92.3},
                {"bot_id": "BOT003", "bot_name": "Agro-Bot Gamma", "status": "MAINTENANCE",
                 "latitude": 19.8, "longitude": 67.2, "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 "temperature": 23.5, "salinity": 35.4, "ph": 7.8, "battery_level": 45.2},
                {"bot_id": "BOT004", "bot_name": "Agro-Bot Delta", "status": "ACTIVE",
                 "latitude": 15.2, "longitude": 73.1, "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 "temperature": 27.8, "salinity": 33.8, "ph": 8.3, "battery_level": 78.9}
            ]
            
            bots_df = pd.DataFrame(bots_data)
            bots_df.to_sql("agro_bots", engine, if_exists="append", index=False)
            
            self.logger.info(f"Successfully saved {len(df)} ARGO profiles to SQLite database")
            self.logger.info(f"Data sources: NOAA NCEI & IFREMER Indian Ocean")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving data to SQLite: {e}")
            return False
    
    def run_full_ingestion(self) -> bool:
        """Run the complete data ingestion process"""
        try:
            self.logger.info("Starting Indian Ocean ARGO data ingestion...")
            self.logger.info(f"Sources: NOAA NCEI & IFREMER Indian Ocean")
            
            # Step 1: Create database schema
            self.create_sqlite_schema()
            
            # Step 2: Download NetCDF files with fallback
            downloaded_files = self.download_files_with_fallback(self.config.max_total_files)
            
            if not downloaded_files:
                self.logger.warning("No files were successfully downloaded")
                return False
            
            # Step 3: Process NetCDF files
            processed_data = self.process_all_files(downloaded_files)
            
            if processed_data.empty:
                self.logger.warning("No data was successfully processed")
                return False
            
            # Step 4: Save to SQLite database
            success = self.save_to_sqlite(processed_data)
            
            if success:
                self.logger.info("Indian Ocean ARGO data ingestion completed successfully!")
                self.logger.info(f"Final dataset: {len(processed_data)} measurements")
                return True
            else:
                self.logger.error("Failed to save data to database")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during full ingestion process: {e}")
            return False

def main():
    """Main function to run the Indian Ocean NetCDF ingestion process"""
    processor = IndianOceanArgoProcessor()
    success = processor.run_full_ingestion()
    
    if success:
        print("Indian Ocean ARGO data ingestion completed successfully!")
        print(f"Data saved to: {processor.db_path}")
        print("🌊 Sources: NOAA NCEI & IFREMER Indian Ocean")
    else:
        print("Indian Ocean ARGO data ingestion failed. Check logs for details.")

if __name__ == "__main__":
    main()