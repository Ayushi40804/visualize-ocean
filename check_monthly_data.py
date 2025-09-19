"""
Check IFREMER monthly directory for actual files
"""

import requests
from bs4 import BeautifulSoup

def check_ifremer_monthly():
    """Check monthly subdirectories for NetCDF files"""
    print("🔍 Checking IFREMER Monthly Subdirectories")
    print("=" * 50)
    
    base_url = "https://data-argo.ifremer.fr/geo/indian_ocean/2020/"
    
    for month in ["01", "02", "03"]:  # Check first few months
        print(f"\n📅 Checking month {month}:")
        try:
            url = f"{base_url}{month}/"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a')
                
                netcdf_files = []
                for link in links:
                    href = link.get('href', '')
                    if href and href.endswith('.nc'):
                        netcdf_files.append(href)
                
                print(f"   📄 Found {len(netcdf_files)} NetCDF files")
                if netcdf_files:
                    for f in netcdf_files[:3]:
                        print(f"      🗂️ {f}")
                    if len(netcdf_files) > 3:
                        print(f"      ... and {len(netcdf_files) - 3} more")
                
            else:
                print(f"   ❌ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def check_noaa_older_years():
    """Check older NOAA years for data"""
    print("\n🔍 Checking NOAA Older Years")
    print("=" * 50)
    
    base_url = "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data/indian/"
    
    for year in ["2019", "2018"]:
        print(f"\n📅 Checking year {year}:")
        try:
            url = f"{base_url}{year}/"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a')
                
                netcdf_files = []
                for link in links:
                    href = link.get('href', '')
                    if href and href.endswith('.nc'):
                        netcdf_files.append(href)
                
                print(f"   📄 Found {len(netcdf_files)} NetCDF files")
                if netcdf_files:
                    for f in netcdf_files[:3]:
                        print(f"      🗂️ {f}")
                    if len(netcdf_files) > 3:
                        print(f"      ... and {len(netcdf_files) - 3} more")
                
            else:
                print(f"   ❌ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    check_ifremer_monthly()
    check_noaa_older_years()