"""
Test script for the integrated ARGO chatbot functionality
Run this to verify that all components work together properly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import ArgoDatabase
from utils.config import config
import logging

def test_database():
    """Test database initialization and operations"""
    print("🧪 Testing Database...")
    try:
        db = ArgoDatabase()
        
        # Test health check
        health = db.health_check()
        print(f"   Database status: {health['status']}")
        
        if health['status'] == 'healthy':
            records = health['records']
            print(f"   ARGO profiles: {records['argo_profiles']}")
            print(f"   Ocean conditions: {records['ocean_conditions']}")
            print(f"   Agro-bots: {records['agro_bots']}")
            
            # Test sample query
            sample_data = db.get_sample_data("argo_profiles", 3)
            print(f"   Sample data retrieved: {len(sample_data)} records")
            
            print("   ✅ Database test passed")
            return True
        else:
            print(f"   ❌ Database error: {health.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("🧪 Testing Configuration...")
    try:
        # Test API key loading
        api_key = config.get_google_api_key()
        if api_key:
            print(f"   Google API key: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
        else:
            print("   ❌ No Google API key found")
            return False
        
        # Test configuration validation
        validation = config.validate_config()
        print(f"   Configuration valid: {validation['valid']}")
        
        if validation['errors']:
            print(f"   Errors: {validation['errors']}")
        
        if validation['warnings']:
            print(f"   Warnings: {validation['warnings']}")
        
        print("   ✅ Configuration test passed")
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
        return False

def test_langchain_imports():
    """Test that LangChain imports work"""
    print("🧪 Testing LangChain Imports...")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_community.utilities import SQLDatabase
        from langchain_community.agent_toolkits import SQLDatabaseToolkit
        from langchain_community.agent_toolkits.sql.base import create_sql_agent
        
        print("   ✅ All LangChain imports successful")
        return True
        
    except ImportError as e:
        print(f"   ❌ LangChain import failed: {e}")
        print("   💡 Try installing missing dependencies with: pip install -r requirements.txt")
        return False

def test_llm_initialization():
    """Test LLM initialization"""
    print("🧪 Testing LLM Initialization...")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        api_key = config.get_google_api_key()
        if not api_key:
            print("   ❌ No API key available for LLM test")
            return False
        
        # Initialize LLM with minimal settings
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.1
        )
        
        print("   ✅ LLM initialization successful")
        return True
        
    except Exception as e:
        print(f"   ❌ LLM initialization failed: {e}")
        return False

def test_sql_agent():
    """Test SQL agent creation"""
    print("🧪 Testing SQL Agent...")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_community.utilities import SQLDatabase
        from langchain_community.agent_toolkits import SQLDatabaseToolkit
        from langchain_community.agent_toolkits.sql.base import create_sql_agent
        
        # Initialize components
        db_manager = ArgoDatabase()
        engine = db_manager.get_connection()
        db = SQLDatabase(engine)
        
        api_key = config.get_google_api_key()
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.1
        )
        
        # Create SQL agent
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=False,
            handle_parsing_errors=True
        )
        
        print("   ✅ SQL Agent creation successful")
        return True
        
    except Exception as e:
        print(f"   ❌ SQL Agent creation failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 Starting Integration Tests for ARGO Chatbot\n")
    
    tests = [
        ("Configuration", test_config),
        ("LangChain Imports", test_langchain_imports),
        ("Database", test_database),
        ("LLM Initialization", test_llm_initialization),
        ("SQL Agent", test_sql_agent)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("📋 Test Summary:")
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The chatbot integration is ready to use.")
        print("💡 You can now run the Streamlit app: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("💡 Make sure to:")
        print("   - Install all requirements: pip install -r requirements.txt")
        print("   - Check your Google API key in .env file")
        print("   - Verify network connectivity")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise
    
    run_all_tests()