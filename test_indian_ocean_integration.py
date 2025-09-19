"""
Test script for Indian Ocean ARGO NetCDF data integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.indian_ocean_netcdf import IndianOceanArgoProcessor, IndianOceanArgoConfig
from utils.database import ArgoDatabase

def test_indian_ocean_integration():
    """Test the Indian Ocean ARGO NetCDF integration"""
    print("🧪 Testing Indian Ocean ARGO NetCDF Data Integration")
    print("=" * 60)
    
    # Test 1: Configuration
    print("\n1️⃣ Testing Configuration...")
    config = IndianOceanArgoConfig()
    print(f"   ✅ NOAA NCEI URL: {config.noaa_base_url}")
    print(f"   ✅ IFREMER URL: {config.ifremer_base_url}")
    print(f"   ✅ Region: {config.lat_min}-{config.lat_max}°N, {config.lon_min}-{config.lon_max}°E")
    print(f"   ✅ Years: {config.start_year}-{config.end_year}")
    print(f"   ✅ Max files: {config.max_total_files}")
    
    # Test 2: Processor initialization
    print("\n2️⃣ Testing Processor...")
    try:
        processor = IndianOceanArgoProcessor(config=config)
        print("   ✅ Indian Ocean processor initialized")
        print(f"   ✅ Download folder: {processor.config.download_folder}")
    except Exception as e:
        print(f"   ❌ Processor error: {e}")
        return False
    
    # Test 3: Data source discovery
    print("\n3️⃣ Testing Data Source Discovery...")
    try:
        print("   🔄 Testing IFREMER Indian Ocean source...")
        ifremer_files = processor.discover_netcdf_files(config.ifremer_base_url, max_files=5)
        print(f"   ✅ Found {len(ifremer_files)} files from IFREMER")
        
        if ifremer_files:
            print(f"   📄 Sample file: {os.path.basename(ifremer_files[0])}")
        
        print("   🔄 Testing NOAA NCEI Indian Ocean source...")
        noaa_files = processor.discover_netcdf_files(config.noaa_base_url, max_files=5)
        print(f"   ✅ Found {len(noaa_files)} files from NOAA")
        
        if noaa_files:
            print(f"   📄 Sample file: {os.path.basename(noaa_files[0])}")
        
        total_discovered = len(ifremer_files) + len(noaa_files)
        print(f"   📊 Total files discovered: {total_discovered}")
        
        if total_discovered == 0:
            print("   ⚠️  No NetCDF files found. Check network connectivity.")
            return False
        
    except Exception as e:
        print(f"   ❌ Data discovery error: {e}")
        return False
    
    # Test 4: Database integration
    print("\n4️⃣ Testing Database Integration...")
    try:
        db = ArgoDatabase(use_real_data=True)
        health = db.health_check()
        print(f"   ✅ Database status: {health['status']}")
        print(f"   ✅ Data source: {health.get('data_source', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False
    
    print("\n✅ All tests passed! Ready for Indian Ocean ARGO data ingestion.")
    print("\n💡 To run full data ingestion:")
    print("   from utils.indian_ocean_netcdf import IndianOceanArgoProcessor")
    print("   processor = IndianOceanArgoProcessor()")
    print("   success = processor.run_full_ingestion()")
    
    return True

def run_quick_ingestion():
    """Run a quick data ingestion with limited files"""
    print("\n🚀 Running Quick Indian Ocean ARGO Data Ingestion...")
    print("=" * 60)
    
    # Configure for quick test
    config = IndianOceanArgoConfig(
        max_files_per_year=3,   # Very limited for testing
        max_total_files=10,     # Total limit
        start_year=2024,        # Recent data only
        end_year=2024
    )
    
    processor = IndianOceanArgoProcessor(config=config)
    success = processor.run_full_ingestion()
    
    if success:
        print("\n✅ Quick ingestion completed successfully!")
        
        # Test database
        db = ArgoDatabase()
        health = db.health_check()
        print(f"📊 Database now contains:")
        print(f"   - ARGO Profiles: {health['records']['argo_profiles']}")
        print(f"   - Ocean Conditions: {health['records']['ocean_conditions']}")
        print(f"   - Data Source: {health.get('data_source', 'Unknown')}")
        
        # Show sample data
        sample_data = db.get_sample_data("argo_profiles", 3)
        if sample_data:
            print(f"\n📄 Sample measurements:")
            for i, record in enumerate(sample_data, 1):
                print(f"   {i}. Float {record['float_id']} - {record['region']}")
                print(f"      📍 {record['latitude']:.2f}°N, {record['longitude']:.2f}°E")
                print(f"      🌡️ {record.get('temperature', 'N/A')}°C, 🧂 {record.get('salinity', 'N/A')} PSU")
        
    else:
        print("\n❌ Quick ingestion failed. Check logs for details.")
    
    return success

def test_data_sources():
    """Test connectivity to both data sources"""
    print("\n🔗 Testing Data Source Connectivity...")
    print("=" * 50)
    
    import requests
    
    sources = [
        ("NOAA NCEI", "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data/indian/2024/"),
        ("IFREMER", "https://data-argo.ifremer.fr/geo/indian_ocean/2024/")
    ]
    
    for name, url in sources:
        try:
            print(f"\n🔄 Testing {name}...")
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {name}: Accessible")
            else:
                print(f"   ⚠️  {name}: Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Indian Ocean ARGO NetCDF data integration")
    parser.add_argument("--quick", action="store_true", help="Run quick data ingestion")
    parser.add_argument("--test-only", action="store_true", help="Run tests only (no data download)")
    parser.add_argument("--connectivity", action="store_true", help="Test data source connectivity")
    
    args = parser.parse_args()
    
    if args.connectivity:
        test_data_sources()
    elif args.test_only:
        test_indian_ocean_integration()
    elif args.quick:
        if test_indian_ocean_integration():
            run_quick_ingestion()
    else:
        test_indian_ocean_integration()