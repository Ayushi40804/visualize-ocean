"""
Data Refresh Utility
Provides scheduled updates and maintenance for ARGO NetCDF data
"""

import schedule
import time
from datetime import datetime, timedelta
import logging
from pathlib import Path
import json
import os

from utils.netcdf_ingestion import ArgoNetCDFProcessor, ArgoConfig
from utils.database import ArgoDatabase

class ArgoDataRefreshManager:
    """Manages periodic refresh of ARGO NetCDF data"""
    
    def __init__(self, refresh_interval_hours: int = 24):
        self.refresh_interval_hours = refresh_interval_hours
        self.logger = self._setup_logging()
        self.status_file = "data_refresh_status.json"
        self.config = ArgoConfig()
        
    def _setup_logging(self):
        """Setup logging for refresh manager"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('argo_data_refresh.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def get_refresh_status(self) -> dict:
        """Get the current refresh status"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r') as f:
                    return json.load(f)
            else:
                return {
                    "last_refresh": None,
                    "last_success": None,
                    "refresh_count": 0,
                    "error_count": 0,
                    "status": "never_run"
                }
        except Exception as e:
            self.logger.error(f"Error reading status file: {e}")
            return {"status": "error", "error": str(e)}
    
    def update_refresh_status(self, success: bool, error_msg: str = None):
        """Update the refresh status file"""
        try:
            status = self.get_refresh_status()
            current_time = datetime.now().isoformat()
            
            status["last_refresh"] = current_time
            status["refresh_count"] = status.get("refresh_count", 0) + 1
            
            if success:
                status["last_success"] = current_time
                status["status"] = "success"
                status["error"] = None
            else:
                status["error_count"] = status.get("error_count", 0) + 1
                status["status"] = "error"
                status["error"] = error_msg
            
            with open(self.status_file, 'w') as f:
                json.dump(status, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error updating status file: {e}")
    
    def should_refresh(self) -> bool:
        """Check if data should be refreshed based on time interval"""
        status = self.get_refresh_status()
        
        if status.get("last_success") is None:
            return True  # Never successfully refreshed
        
        try:
            last_success = datetime.fromisoformat(status["last_success"])
            time_since_refresh = datetime.now() - last_success
            
            return time_since_refresh.total_seconds() > (self.refresh_interval_hours * 3600)
        except Exception:
            return True  # If we can't parse the date, refresh anyway
    
    def refresh_data(self, force: bool = False) -> bool:
        """Refresh ARGO data if needed"""
        if not force and not self.should_refresh():
            self.logger.info("Data refresh not needed yet")
            return True
        
        self.logger.info("Starting ARGO data refresh...")
        
        try:
            # Update config for fresher data
            current_date = datetime.now()
            self.config.start_date = (current_date - timedelta(days=60)).strftime("%Y-%m-%d")
            self.config.end_date = current_date.strftime("%Y-%m-%d")
            
            # Run NetCDF ingestion
            processor = ArgoNetCDFProcessor(config=self.config)
            success = processor.run_full_ingestion()
            
            if success:
                self.logger.info("Data refresh completed successfully")
                self.update_refresh_status(True)
                return True
            else:
                error_msg = "NetCDF ingestion failed"
                self.logger.error(error_msg)
                self.update_refresh_status(False, error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Error during data refresh: {str(e)}"
            self.logger.error(error_msg)
            self.update_refresh_status(False, error_msg)
            return False
    
    def cleanup_old_files(self, days_to_keep: int = 7):
        """Clean up old downloaded NetCDF files"""
        try:
            download_folder = Path(self.config.download_folder)
            if not download_folder.exists():
                return
            
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            files_removed = 0
            
            for file_path in download_folder.glob("*.nc"):
                if file_path.stat().st_mtime < cutoff_date.timestamp():
                    file_path.unlink()
                    files_removed += 1
            
            self.logger.info(f"Cleaned up {files_removed} old NetCDF files")
            
        except Exception as e:
            self.logger.error(f"Error during file cleanup: {e}")
    
    def run_scheduled_refresh(self):
        """Run the scheduled refresh job"""
        self.logger.info("Running scheduled data refresh check...")
        
        # Refresh data if needed
        success = self.refresh_data()
        
        # Clean up old files
        self.cleanup_old_files()
        
        return success
    
    def start_scheduler(self):
        """Start the scheduled refresh process"""
        self.logger.info(f"Starting ARGO data refresh scheduler (every {self.refresh_interval_hours} hours)")
        
        # Schedule the refresh
        schedule.every(self.refresh_interval_hours).hours.do(self.run_scheduled_refresh)
        
        # Run initial check
        self.run_scheduled_refresh()
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def manual_refresh(force: bool = False):
    """Manually trigger a data refresh"""
    print("🔄 Manual ARGO Data Refresh")
    print("=" * 30)
    
    manager = ArgoDataRefreshManager()
    
    # Show current status
    status = manager.get_refresh_status()
    print(f"📊 Current Status:")
    print(f"   Last Refresh: {status.get('last_refresh', 'Never')}")
    print(f"   Last Success: {status.get('last_success', 'Never')}")
    print(f"   Refresh Count: {status.get('refresh_count', 0)}")
    print(f"   Error Count: {status.get('error_count', 0)}")
    
    if not force and not manager.should_refresh():
        print("\n⏰ Data is still fresh - no refresh needed")
        print("   Use --force to refresh anyway")
        return True
    
    print(f"\n🚀 Starting data refresh...")
    success = manager.refresh_data(force=force)
    
    if success:
        print("✅ Data refresh completed successfully!")
    else:
        print("❌ Data refresh failed. Check logs for details.")
    
    return success

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ARGO data refresh utility")
    parser.add_argument("--manual", action="store_true", help="Run manual refresh")
    parser.add_argument("--force", action="store_true", help="Force refresh even if recent")
    parser.add_argument("--schedule", action="store_true", help="Start scheduled refresh daemon")
    parser.add_argument("--status", action="store_true", help="Show refresh status")
    parser.add_argument("--interval", type=int, default=24, help="Refresh interval in hours")
    
    args = parser.parse_args()
    
    if args.status:
        manager = ArgoDataRefreshManager()
        status = manager.get_refresh_status()
        print("📊 ARGO Data Refresh Status:")
        print(json.dumps(status, indent=2))
    
    elif args.manual:
        manual_refresh(force=args.force)
    
    elif args.schedule:
        manager = ArgoDataRefreshManager(refresh_interval_hours=args.interval)
        manager.start_scheduler()
    
    else:
        print("Use --manual, --schedule, or --status")
        parser.print_help()