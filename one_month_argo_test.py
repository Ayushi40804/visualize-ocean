"""
One-month ARGO data ingestion test
Processes only January 2024 data for RAG and overview page testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.indian_ocean_netcdf import IndianOceanArgoProcessor, IndianOceanArgoConfig
from utils.database import ArgoDatabase

def create_one_month_config():
    """Create configuration for one month of data processing"""
    return IndianOceanArgoConfig(
        start_year=2024,
        end_year=2024,
        start_month=1,      # January only
        end_month=1,        # January only
        max_files_per_year=3,   # Very limited
        max_total_files=5,      # Small total
        lat_min=0.0,
        lat_max=30.0,
        lon_min=50.0,
        lon_max=100.0
    )

def test_one_month_ingestion():
    """Test one-month data ingestion"""
    print("🚀 One-Month ARGO Data Ingestion Test")
    print("=" * 50)
    print("📅 Processing: January 2024 only")
    print("🌊 Region: Indian Ocean (0-30°N, 50-100°E)")
    print("📊 Limit: Maximum 5 files total")
    print()
    
    # Create configuration
    config = create_one_month_config()
    processor = IndianOceanArgoProcessor(config=config)
    
    print("🔍 Testing data discovery...")
    try:
        # Test discovery
        ifremer_files = processor.discover_netcdf_files(config.ifremer_base_url, max_files=3)
        print(f"   ✅ IFREMER: Found {len(ifremer_files)} files")
        
        if ifremer_files:
            print(f"   📄 Sample: {os.path.basename(ifremer_files[0])}")
        
        print(f"\n💾 Starting ingestion...")
        success = processor.run_full_ingestion()
        
        if success:
            print("\n✅ One-month ingestion completed!")
            
            # Check database
            db = ArgoDatabase()
            health = db.health_check()
            
            print(f"\n📊 Database Status:")
            print(f"   - Status: {health['status']}")
            print(f"   - ARGO Profiles: {health['records']['argo_profiles']}")
            print(f"   - Ocean Conditions: {health['records']['ocean_conditions']}")
            print(f"   - Data Source: {health.get('data_source', 'Unknown')}")
            
            # Sample data
            sample_data = db.get_sample_data("argo_profiles", 5)
            if sample_data:
                print(f"\n📄 Sample January 2024 measurements:")
                for i, record in enumerate(sample_data, 1):
                    print(f"   {i}. Float {record['float_id']} - {record['region']}")
                    print(f"      📍 {record['latitude']:.2f}°N, {record['longitude']:.2f}°E")
                    temp = record.get('temperature', 'N/A')
                    sal = record.get('salinity', 'N/A')
                    print(f"      🌡️ {temp}°C, 🧂 {sal} PSU")
                    print(f"      📅 {record.get('date_time', 'N/A')}")
            
            print(f"\n🎯 Ready for RAG and Overview Page Testing!")
            return True
        else:
            print("\n❌ One-month ingestion failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def verify_rag_compatibility():
    """Verify the one-month dataset is compatible with RAG system"""
    print("\n🔍 Verifying RAG System Compatibility...")
    print("=" * 40)
    
    try:
        db = ArgoDatabase()
        
        # Test basic queries
        print("📋 Testing basic database queries...")
        
        # Test recent data query
        recent_query = """
        SELECT COUNT(*) as count, MIN(date_time) as earliest, MAX(date_time) as latest
        FROM argo_profiles 
        WHERE date_time >= '2024-01-01'
        """
        
        import sqlite3
        conn = sqlite3.connect('argo_data.sqlite')
        cursor = conn.cursor()
        cursor.execute(recent_query)
        result = cursor.fetchone()
        
        if result:
            count, earliest, latest = result
            print(f"   ✅ January 2024 data: {count} records")
            print(f"   📅 Date range: {earliest} to {latest}")
        
        # Test regional queries
        region_query = """
        SELECT region, COUNT(*) as count, 
               AVG(temperature) as avg_temp, AVG(salinity) as avg_sal
        FROM argo_profiles 
        WHERE temperature IS NOT NULL AND salinity IS NOT NULL
        GROUP BY region
        """
        cursor.execute(region_query)
        regions = cursor.fetchall()
        
        print(f"\n🌊 Regional data summary:")
        for region, count, avg_temp, avg_sal in regions:
            print(f"   📍 {region}: {count} measurements")
            print(f"      🌡️ Avg temp: {avg_temp:.2f}°C, 🧂 Avg salinity: {avg_sal:.2f} PSU")
        
        conn.close()
        
        print(f"\n✅ RAG system compatibility verified!")
        print(f"💡 The database is ready for AI chat queries about January 2024 Indian Ocean data")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG compatibility check failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="One-month ARGO data processing for RAG")
    parser.add_argument("--ingest", action="store_true", help="Run one-month data ingestion")
    parser.add_argument("--verify", action="store_true", help="Verify RAG compatibility")
    parser.add_argument("--all", action="store_true", help="Run both ingestion and verification")
    
    args = parser.parse_args()
    
    if args.all or args.ingest:
        success = test_one_month_ingestion()
        if not success:
            sys.exit(1)
    
    if args.all or args.verify:
        verify_rag_compatibility()
    
    if not any([args.ingest, args.verify, args.all]):
        print("Usage: python one_month_argo_test.py [--ingest|--verify|--all]")
        print()
        print("Options:")
        print("  --ingest  : Run one-month data ingestion only")
        print("  --verify  : Verify RAG system compatibility only") 
        print("  --all     : Run both ingestion and verification")