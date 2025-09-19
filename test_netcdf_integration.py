"""
Test script for NetCDF ARGO data integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.netcdf_ingestion import ArgoNetCDFProcessor, ArgoConfig
from utils.database import ArgoDatabase

def test_netcdf_integration():
    """Test the complete NetCDF integration workflow"""
    print("🧪 Testing NetCDF ARGO Data Integration")
    print("=" * 50)
    
    # Test 1: Configuration
    print("\n1️⃣ Testing Configuration...")
    config = ArgoConfig()
    print(f"   ✅ Config loaded - Region: {config.lat_min}-{config.lat_max}°N, {config.lon_min}-{config.lon_max}°E")
    print(f"   ✅ Time range: {config.start_date} to {config.end_date}")
    print(f"   ✅ Max profiles: {config.max_profiles}")
    
    # Test 2: Database initialization
    print("\n2️⃣ Testing Database...")
    try:
        db = ArgoDatabase(use_real_data=True)
        health = db.health_check()
        print(f"   ✅ Database status: {health['status']}")
        print(f"   ✅ Data source: {health.get('data_source', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False
    
    # Test 3: NetCDF Processor initialization
    print("\n3️⃣ Testing NetCDF Processor...")
    try:
        processor = ArgoNetCDFProcessor(config=config)
        print("   ✅ NetCDF processor initialized")
        print(f"   ✅ Download folder: {processor.config.download_folder}")
        print(f"   ✅ FTP URL: {processor.config.ftp_base_url}")
    except Exception as e:
        print(f"   ❌ NetCDF processor error: {e}")
        return False
    
    # Test 4: FTP connectivity (just test index fetch)
    print("\n4️⃣ Testing FTP Connectivity...")
    try:
        print("   🔄 Attempting to fetch ARGO index...")
        df_index = processor.fetch_global_index()
        print(f"   ✅ Successfully fetched {len(df_index)} profiles from global index")
        
        # Test filtering
        filtered = processor.filter_profiles(df_index)
        print(f"   ✅ Filtered to {len(filtered)} profiles matching criteria")
        
        if len(filtered) == 0:
            print("   ⚠️  No profiles match the filtering criteria")
            print("   💡 Try adjusting the geographic or temporal bounds")
        
    except Exception as e:
        print(f"   ❌ FTP connectivity error: {e}")
        print("   💡 This might be due to network issues or FTP server availability")
        return False
    
    print("\n✅ All tests passed! Ready for NetCDF data ingestion.")
    print("\n💡 To run full data ingestion:")
    print("   from utils.netcdf_ingestion import ArgoNetCDFProcessor")
    print("   processor = ArgoNetCDFProcessor()")
    print("   success = processor.run_full_ingestion()")
    
    return True

def run_quick_ingestion():
    """Run a quick data ingestion with limited data"""
    print("\n🚀 Running Quick NetCDF Data Ingestion...")
    print("=" * 50)
    
    # Configure for quick test
    config = ArgoConfig(
        max_profiles=10,  # Very limited for testing
        batch_size=2,
        max_workers=1
    )
    
    processor = ArgoNetCDFProcessor(config=config)
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
        
    else:
        print("\n❌ Quick ingestion failed. Check logs for details.")
    
    return success

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test NetCDF ARGO data integration")
    parser.add_argument("--quick", action="store_true", help="Run quick data ingestion")
    parser.add_argument("--test-only", action="store_true", help="Run tests only (no data download)")
    
    args = parser.parse_args()
    
    if args.test_only:
        test_netcdf_integration()
    elif args.quick:
        if test_netcdf_integration():
            run_quick_ingestion()
    else:
        test_netcdf_integration()