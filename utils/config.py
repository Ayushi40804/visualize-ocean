"""
Environment configuration for the ARGO Ocean Monitoring System
Handles API keys and configuration settings
"""

import os
import streamlit as st
from typing import Optional
import logging

class EnvironmentConfig:
    """Manages environment configuration and API keys"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_google_api_key(self) -> Optional[str]:
        """Get Google API key from multiple sources"""
        api_key = None
        
        try:
            # First, try Streamlit secrets
            api_key = st.secrets["api_keys"]["google_api_key"]
            self.logger.info("Google API key loaded from Streamlit secrets")
        except (KeyError, FileNotFoundError):
            try:
                # Fallback to environment variable
                api_key = os.getenv("GOOGLE_API_KEY")
                if api_key:
                    self.logger.info("Google API key loaded from environment variable")
                else:
                    # Last resort - use the known key for this demo
                    api_key = "AIzaSyCYe3H3jZynoektAjJ9g-e7-r5iGkYEIzE"
                    self.logger.info("Using fallback Google API key")
            except Exception as e:
                self.logger.error(f"Failed to load Google API key: {e}")
        
        return api_key
    
    def get_database_config(self) -> dict:
        """Get database configuration - TiDB Cloud only"""
        return {
            "tidb_host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            "tidb_port": 4000,
            "tidb_user": "2skvbktzy1zRC6L.root",
            "tidb_password": "802twyBx0xPzBBOX",
            "tidb_database": "test",
            "use_tidb": True
        }
    
    def get_api_config(self) -> dict:
        """Get API configuration"""
        return {
            "api_host": os.getenv("API_HOST", "127.0.0.1"),
            "api_port": int(os.getenv("API_PORT", "8000")),
            "streamlit_port": int(os.getenv("STREAMLIT_PORT", "8501"))
        }
    
    def get_system_config(self) -> dict:
        """Get system configuration"""
        return {
            "max_query_length": int(os.getenv("MAX_QUERY_LENGTH", "500")),
            "rate_limit_per_minute": int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "log_file": os.getenv("LOG_FILE", "argo_system.log")
        }
    
    def validate_config(self) -> dict:
        """Validate configuration and return status"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check Google API key
        api_key = self.get_google_api_key()
        if not api_key:
            validation_result["valid"] = False
            validation_result["errors"].append("Google API key not found")
        elif len(api_key) < 20:  # Basic validation
            validation_result["warnings"].append("Google API key seems too short")
        
        # Check other configurations
        try:
            db_config = self.get_database_config()
            api_config = self.get_api_config()
            system_config = self.get_system_config()
            
            self.logger.info("Configuration validation completed")
            
        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Configuration error: {e}")
        
        return validation_result

# Global configuration instance
config = EnvironmentConfig()