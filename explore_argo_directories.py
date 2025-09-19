"""
Directory exploration script for ARGO data sources
"""

import requests
from bs4 import BeautifulSoup
import re

def explore_directories():
    """Explore the actual directory structure of both data sources"""
    print("🔍 Exploring ARGO Data Source Directory Structures")
    print("=" * 60)
    
    # Test IFREMER base
    print("\n1️⃣ IFREMER Indian Ocean Base Structure:")
    try:
        url = "https://data-argo.ifremer.fr/geo/indian_ocean/"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            dirs = []
            for link in links:
                href = link.get('href', '')
                if href and href.endswith('/') and not href.startswith('..'):
                    dirs.append(href.rstrip('/'))
            
            print(f"   ✅ Found {len(dirs)} directories:")
            for d in sorted(dirs)[:10]:  # Show first 10
                print(f"      📁 {d}")
            if len(dirs) > 10:
                print(f"      ... and {len(dirs) - 10} more")
        else:
            print(f"   ❌ Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test NOAA NCEI base
    print("\n2️⃣ NOAA NCEI Base Structure:")
    try:
        url = "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data/"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            dirs = []
            for link in links:
                href = link.get('href', '')
                if href and href.endswith('/') and not href.startswith('..'):
                    dirs.append(href.rstrip('/'))
            
            print(f"   ✅ Found {len(dirs)} directories:")
            for d in sorted(dirs):
                print(f"      📁 {d}")
        else:
            print(f"   ❌ Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test NOAA Indian specific
    print("\n3️⃣ NOAA NCEI Indian Directory:")
    try:
        url = "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data/indian/"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            years = []
            for link in links:
                href = link.get('href', '')
                if href and href.endswith('/') and re.match(r'\d{4}/', href):
                    years.append(href.rstrip('/'))
            
            print(f"   ✅ Found {len(years)} year directories:")
            for year in sorted(years):
                print(f"      📅 {year}")
        else:
            print(f"   ❌ Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test a specific year from IFREMER
    print("\n4️⃣ IFREMER Recent Year Sample:")
    try:
        # Try 2023 which should have data
        url = "https://data-argo.ifremer.fr/geo/indian_ocean/2023/"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            netcdf_files = []
            for link in links:
                href = link.get('href', '')
                if href and href.endswith('.nc'):
                    netcdf_files.append(href)
            
            print(f"   ✅ 2023 directory contains {len(netcdf_files)} NetCDF files")
            if netcdf_files:
                print(f"   📄 Sample files:")
                for f in netcdf_files[:3]:
                    print(f"      • {f}")
        else:
            print(f"   ❌ 2023 directory status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing 2023: {e}")

if __name__ == "__main__":
    explore_directories()