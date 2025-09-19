# NetCDF ARGO Data Integration Guide

## 🌊 Overview

Your RAG data now comes from **real ARGO oceanographic data** instead of sample data! This integration connects your chatbot to the global ARGO float network via NetCDF files from the IFREMER FTP server.

## 📊 Data Source: `ftp://ftp.ifremer.fr/ifremer/argo/`

### What is ARGO?
- **Global ocean observing system** with ~4,000 autonomous floats
- **Real-time data collection** of temperature, salinity, pressure, dissolved oxygen
- **Worldwide coverage** with data updated regularly
- **NetCDF format** - self-describing scientific data format

### Data Flow Architecture

```
ARGO Floats (Global Ocean) 
    ↓
IFREMER FTP Server (ftp://ftp.ifremer.fr/ifremer/argo/)
    ↓
NetCDF Files Download & Processing
    ↓
SQLite Database (argo_data.sqlite)
    ↓
LangChain SQL Agent + Google Gemini
    ↓
Natural Language Responses
```

## 🚀 New Components Added

### 1. NetCDF Data Ingestion (`utils/netcdf_ingestion.py`)
- **ArgoNetCDFProcessor**: Downloads and processes real ARGO NetCDF files
- **Quality Control**: Filters data based on QC flags
- **Geographic Filtering**: Focuses on Indian Ocean region (Arabian Sea, Bay of Bengal)
- **Batch Processing**: Handles multiple files efficiently

### 2. Enhanced Database (`utils/database.py`)
- **Dual Mode**: Supports both sample data and real NetCDF data
- **Auto-Detection**: Recognizes when real data is present
- **Real Data Schema**: Optimized for ARGO profile structure

### 3. Data Refresh System (`utils/data_refresh.py`)
- **Scheduled Updates**: Automatic data refresh every 24 hours
- **Manual Control**: Force refresh when needed
- **File Cleanup**: Removes old NetCDF files
- **Status Tracking**: Monitors refresh success/failures

### 4. Updated UI (`pages/ai_chat.py`)
- **Data Source Indicator**: Shows whether using real or sample data
- **Load Real Data Button**: One-click NetCDF data loading
- **Progress Monitoring**: Real-time status during download

## 🛠️ Usage Instructions

### Method 1: Via Streamlit UI
1. Run your app: `streamlit run app.py`
2. Go to AI Chat page
3. In sidebar, click **"📥 Load Real NetCDF Data"**
4. Wait for download and processing (2-5 minutes)
5. ✅ Chatbot now uses real ARGO data!

### Method 2: Via Command Line
```bash
# Test the integration
python test_netcdf_integration.py --test-only

# Quick data load (10 profiles)
python test_netcdf_integration.py --quick

# Manual data refresh
python -m utils.data_refresh --manual

# Check refresh status
python -m utils.data_refresh --status

# Start scheduled refresh daemon
python -m utils.data_refresh --schedule
```

### Method 3: Programmatic
```python
from utils.database import ArgoDatabase

# Initialize database with NetCDF data
db = ArgoDatabase(use_real_data=True)
success = db.use_netcdf_data()

if success:
    print("✅ Now using real ARGO data!")
```

## 📋 Configuration Options

### Geographic Coverage
```python
# Default: Indian Ocean region
lat_min: 10.0    # 10°N 
lat_max: 25.0    # 25°N
lon_min: 65.0    # 65°E
lon_max: 85.0    # 85°E
```

### Temporal Coverage
```python
# Default: Last year of data
start_date: "2024-01-01"
end_date: "2024-12-31"
```

### Processing Limits
```python
max_profiles: 50      # Limit for testing
batch_size: 5         # FTP download batch size
max_workers: 2        # Concurrent downloads
```

## 🔄 Data Processing Pipeline

### Step 1: Index Fetching
- Downloads global ARGO index (`ar_index_global_prof.txt.gz`)
- Contains metadata for all ~2M+ profiles worldwide

### Step 2: Geographic/Temporal Filtering
- Filters profiles by location and date
- Focuses on Indian Ocean region
- Selects recent data (last 1-2 years)

### Step 3: NetCDF Download
- Downloads actual profile files (`.nc` format)
- Concurrent FTP downloads for efficiency
- Handles network errors gracefully

### Step 4: Data Extraction
- Parses NetCDF files using xarray
- Extracts: temperature, salinity, pressure, dissolved oxygen, pH
- Applies quality control flags
- Converts to standard database format

### Step 5: Database Storage
- Stores in SQLite database
- Replaces sample data with real measurements
- Maintains compatibility with existing chatbot

## 🎯 What Your Chatbot Can Now Answer

### Real Oceanographic Queries
- "What's the average temperature at 100 meters depth in the Arabian Sea?"
- "Show me salinity measurements from ARGO float 5904297"
- "Find the deepest temperature readings"
- "Compare dissolved oxygen between Arabian Sea and Bay of Bengal"

### Temporal Analysis
- "How has temperature changed over the last year?"
- "Show the most recent ARGO measurements"
- "Find seasonal temperature variations"

### Geographic Analysis
- "Show me all data from coordinates 20°N, 68°E"
- "Compare measurements between different regions"
- "Find the northernmost ARGO profiles"

## 📊 Data Quality & Coverage

### Quality Control
- Only uses QC flags '1' (good) and '2' (probably good)
- Filters out invalid/missing values
- Handles instrument errors gracefully

### Typical Coverage
- **Profiles**: 50-200 individual float profiles
- **Measurements**: 1,000-10,000 individual readings
- **Depth Range**: Surface to 2000+ meters
- **Update Frequency**: Every 24 hours (configurable)

### Data Freshness
- **Real-time**: Data typically 1-30 days old
- **Auto-refresh**: Updates every 24 hours
- **Manual refresh**: Force update anytime

## 🔧 Troubleshooting

### Common Issues

**1. FTP Download Fails**
```bash
# Check connectivity
python test_netcdf_integration.py --test-only
```

**2. No Data Found**
- Check geographic bounds in configuration
- Verify date ranges (ARGO data may be sparse in some regions)
- Try wider temporal window

**3. Database Issues**
```bash
# Reset to sample data
rm argo_data.sqlite
python app.py  # Will recreate with sample data
```

**4. Processing Errors**
- Check NetCDF file integrity
- Verify xarray and netCDF4 packages installed
- Check logs: `argo_netcdf_ingestion.log`

### Performance Optimization

**For Faster Loading:**
```python
config = ArgoConfig(
    max_profiles=20,     # Reduce profile count
    batch_size=3,        # Smaller batches
    max_workers=1        # Single thread for stability
)
```

**For More Data:**
```python
config = ArgoConfig(
    max_profiles=200,    # More profiles
    lat_min=5, lat_max=30,  # Wider area
    start_date="2023-01-01"  # Longer time range
)
```

## 🌟 Benefits of Real Data

### Enhanced Chatbot Capabilities
- **Authentic Responses**: Real oceanographic measurements
- **Scientific Accuracy**: Actual ARGO float data
- **Current Conditions**: Up-to-date ocean state
- **Research Quality**: Publication-ready data

### Educational Value
- **Real Science**: Students interact with actual research data
- **Global Perspective**: Worldwide ocean monitoring
- **Data Literacy**: Understanding scientific data formats
- **Climate Awareness**: Real ocean climate data

## 🔮 Future Enhancements

### Planned Features
1. **Real-time Alerts**: Notifications for anomalous conditions
2. **Data Visualization**: Interactive maps and time series
3. **Predictive Models**: ML-based ocean forecasting
4. **Multi-source Integration**: Satellite + float data
5. **Export Capabilities**: Download processed data

### Advanced Integrations
- **Global Coverage**: Expand beyond Indian Ocean
- **Multi-format Support**: Add other oceanographic formats
- **Real-time Streaming**: Live data feeds
- **Quality Metrics**: Data confidence scores

## 📞 Support

### Log Files
- `argo_netcdf_ingestion.log` - NetCDF processing
- `argo_data_refresh.log` - Scheduled updates
- `argo_system.log` - General system logs

### Configuration Files
- `.env` - Environment variables
- `data_refresh_status.json` - Refresh status
- `argo_data.sqlite` - Main database

### Getting Help
1. Check log files for specific errors
2. Run test script: `python test_netcdf_integration.py --test-only`
3. Verify network connectivity to IFREMER FTP
4. Check disk space for NetCDF downloads

---

🎉 **Congratulations!** Your chatbot now uses real oceanographic data from the global ARGO network instead of sample data. The RAG system pulls from live scientific measurements from autonomous floats across the world's oceans!