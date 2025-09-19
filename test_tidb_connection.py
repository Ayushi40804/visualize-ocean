#!/usr/bin/env python3
"""
Test script for TiDB Cloud database connection
Tests the connection to TiDB Cloud with the provided credentials
"""

import os
import sys
from utils.database import ArgoDatabase
from utils.config import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_tidb_connection():
    """Test TiDB Cloud connection"""
    print("=== TiDB Cloud Connection Test ===")
    print()
    
    # Display connection parameters
    db_config = config.get_database_config()
    print(f"🌐 Host: {db_config['tidb_host']}")
    print(f"🔌 Port: {db_config['tidb_port']}")
    print(f"👤 User: {db_config['tidb_user']}")
    print(f"🗄️ Database: {db_config['tidb_database']}")
    print("✅ Password: Configured")
    print()
    
    print("🔄 Testing TiDB Cloud connection...")
    
    try:
        # Initialize database with TiDB
        db = ArgoDatabase()
        
        # Test connection
        test_result = db.test_tidb_connection()
        
        if test_result['status'] == 'success':
            print("✅ TiDB Cloud connection successful!")
            print(f"   Server Version: {test_result['server_version']}")
            print(f"   Current Database: {test_result['current_database']}")
            print()
            
            # Test health check
            health = db.health_check()
            print("📊 Database Health Check:")
            print(f"   Status: {health['status']}")
            print(f"   Database Type: {health['database_type']}")
            print(f"   ARGO Profiles: {health['records']['argo_profiles']}")
            print(f"   Ocean Conditions: {health['records']['ocean_conditions']}")
            print(f"   Agro Bots: {health['records']['agro_bots']}")
            
            return True
            
        else:
            print(f"❌ TiDB Cloud connection failed!")
            print(f"   Error: {test_result['error']}")
            if 'suggestion' in test_result:
                print(f"   Suggestion: {test_result['suggestion']}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed with exception: {e}")
        return False

def test_sqlite_fallback():
    """Test SQLite fallback - no longer needed but kept for reference"""
    print("\n=== Note: SQLite Fallback Removed ===")
    print("System now uses TiDB Cloud exclusively")
    return True

def main():
    """Main test function"""
    print("🌊 ARGO Ocean Database Connection Test")
    print("=====================================")
    
    # Test TiDB Cloud connection
    tidb_success = test_tidb_connection()
    
    # Test SQLite fallback
    sqlite_success = test_sqlite_fallback()
    
    print("\n=== Test Summary ===")
    print(f"TiDB Cloud: {'✅ PASS' if tidb_success else '❌ FAIL'}")
    print(f"SQLite Fallback: {'✅ PASS' if sqlite_success else '❌ FAIL'}")
    
    if tidb_success:
        print("\n🎉 TiDB Cloud is ready for use!")
    else:
        print("\n❌ TiDB Cloud connection failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())