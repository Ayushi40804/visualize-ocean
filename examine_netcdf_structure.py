"""
Diagnostic script to examine NetCDF file structure
"""

import xarray as xr
import numpy as np
import os

def examine_netcdf_file(filepath):
    """Examine the structure of a NetCDF file"""
    print(f"🔍 Examining: {os.path.basename(filepath)}")
    print("=" * 60)
    
    try:
        ds = xr.open_dataset(filepath)
        
        print("📊 File Information:")
        print(f"   Dimensions: {dict(ds.dims)}")
        print(f"   Variables: {list(ds.data_vars.keys())}")
        print(f"   Coordinates: {list(ds.coords.keys())}")
        print(f"   Attributes: {list(ds.attrs.keys())}")
        
        print("\n🗃️ Key Variables:")
        
        # Check coordinates
        for coord in ['LATITUDE', 'LONGITUDE', 'LAT', 'LON']:
            if coord in ds:
                var = ds[coord]
                print(f"   {coord}: shape={var.shape}, dtype={var.dtype}")
                print(f"      values={var.values if var.size <= 5 else f'[array of {var.size} elements]'}")
                break
        
        # Check time
        for time_var in ['JULD', 'TIME']:
            if time_var in ds:
                var = ds[time_var]
                print(f"   {time_var}: shape={var.shape}, dtype={var.dtype}")
                print(f"      values={var.values if var.size <= 5 else f'[array of {var.size} elements]'}")
                break
        
        # Check pressure
        for pres_var in ['PRES', 'PRESSURE']:
            if pres_var in ds:
                var = ds[pres_var]
                print(f"   {pres_var}: shape={var.shape}, dtype={var.dtype}")
                print(f"      sample values: {var.values.flat[:5] if var.size > 0 else 'empty'}")
                break
        
        # Check other variables
        for var_name in ['TEMP', 'PSAL', 'DOXY']:
            if var_name in ds:
                var = ds[var_name]
                print(f"   {var_name}: shape={var.shape}, dtype={var.dtype}")
                sample_vals = var.values.flat[:5] if var.size > 0 else []
                print(f"      sample values: {sample_vals}")
        
        # Check platform number
        if 'PLATFORM_NUMBER' in ds:
            pn = ds['PLATFORM_NUMBER']
            print(f"   PLATFORM_NUMBER: shape={pn.shape}, dtype={pn.dtype}")
            print(f"      values={pn.values}")
        
        print(f"\n🔗 Dataset attributes:")
        for key, value in list(ds.attrs.items())[:5]:
            print(f"   {key}: {value}")
        
        ds.close()
        
    except Exception as e:
        print(f"❌ Error examining file: {e}")

def main():
    """Examine downloaded NetCDF files"""
    data_dir = "indian_ocean_argo_data"
    
    if not os.path.exists(data_dir):
        print(f"❌ Data directory {data_dir} not found")
        return
    
    nc_files = [f for f in os.listdir(data_dir) if f.endswith('.nc')]
    
    if not nc_files:
        print(f"❌ No NetCDF files found in {data_dir}")
        return
    
    print(f"🔍 Found {len(nc_files)} NetCDF files")
    
    # Examine first file in detail
    for i, nc_file in enumerate(nc_files[:2]):  # Check first 2 files
        filepath = os.path.join(data_dir, nc_file)
        examine_netcdf_file(filepath)
        if i < len(nc_files) - 1:
            print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()