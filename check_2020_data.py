"""
Check IFREMER 2020 directory structure
"""

import requests
from bs4 import BeautifulSoup

def check_ifremer_2020():
    """Check what's in IFREMER 2020 directory"""
    print("🔍 Checking IFREMER 2020 Directory Structure")
    print("=" * 50)
    
    try:
        url = "https://data-argo.ifremer.fr/geo/indian_ocean/2020/"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            
            dirs = []
            files = []
            
            for link in links:
                href = link.get('href', '')
                if href and not href.startswith('..'):
                    if href.endswith('/'):
                        dirs.append(href.rstrip('/'))
                    elif href.endswith('.nc'):
                        files.append(href)
            
            print(f"📁 Directories found: {len(dirs)}")
            for d in dirs[:10]:
                print(f"   📂 {d}")
            
            print(f"\n📄 NetCDF files found: {len(files)}")
            for f in files[:5]:
                print(f"   🗂️ {f}")
                
            # If there are directories, check the first one
            if dirs:
                subdir_url = url + dirs[0] + "/"
                print(f"\n🔍 Checking subdirectory: {dirs[0]}")
                sub_response = requests.get(subdir_url, timeout=15)
                if sub_response.status_code == 200:
                    sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
                    sub_links = sub_soup.find_all('a')
                    sub_files = [l.get('href', '') for l in sub_links if l.get('href', '').endswith('.nc')]
                    print(f"   📄 NetCDF files in {dirs[0]}: {len(sub_files)}")
                    for sf in sub_files[:3]:
                        print(f"      🗂️ {sf}")
                
        else:
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_noaa_2020():
    """Check what's in NOAA 2020 directory"""
    print("\n🔍 Checking NOAA NCEI 2020 Directory Structure")
    print("=" * 50)
    
    try:
        url = "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data/indian/2020/"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            
            netcdf_files = []
            for link in links:
                href = link.get('href', '')
                if href and href.endswith('.nc'):
                    netcdf_files.append(href)
            
            print(f"📄 NetCDF files found: {len(netcdf_files)}")
            for f in netcdf_files[:5]:
                print(f"   🗂️ {f}")
                
        else:
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_ifremer_2020()
    check_noaa_2020()