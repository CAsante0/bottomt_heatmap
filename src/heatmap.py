import os
import glob
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

def generate_average_heatmap(input_dir: str, output_dir: str, variable_name: str):
    """
    Reads all NetCDF files in a directory, averages the specified variable over time, 
    and saves a heatmap image.
    """

    # Look for standard NetCDF files
    search_pattern = os.path.join(input_dir, '*.nc')
    files = glob.glob(search_pattern)
    
    if not files:
        raise ValueError(f"No .nc files found in directory: {input_dir}")
    
    print(f"Found {len(files)} files. Processing...")

    # Open multiple files as a single dataset using Dask for out-of-core computation
    ds = xr.open_mfdataset(files, combine='by_coords')
    min_time = ds['time'].min().values
    max_time = ds['time'].max().values

    # 2. Format the dates into clean strings (e.g., "YYYYMMDD")
    start_date = pd.to_datetime(min_time).strftime('%Y%m%d')
    end_date = pd.to_datetime(max_time).strftime('%Y%m%d')

    # 3. Create the dynamic filename
    filename = f"{variable_name}_average_{start_date}_to_{end_date}.png"

    # 4. Concatenate the filename to the output folder path
    # (Assuming 'output_dir' is passed to the function instead of a raw file path)
    final_output_path = os.path.join(output_dir, filename)

    print(f"Constructed output path: {final_output_path}")
    if variable_name not in ds.variables:
        raise KeyError(f"Variable '{variable_name}' not found in the datasets. Available variables: {list(ds.variables.keys())}")
    
    # Calculate the mean along the time dimension
    print(f"Calculating temporal average for '{variable_name}'...")
    avg_data = ds[variable_name].mean(dim='time')
    
    # Plotting the heatmap
    print("Generating heatmap...")
    plt.figure(figsize=(12, 8))

    # Xarray's built-in plotting wrapper handles coordinates automatically
    avg_data.plot(
        cmap='viridis',
        cbar_kwargs={'label': ds[variable_name].attrs.get('units', 'Units')}
    )
    
    # Extract long name for the title if available in the CF conventions
    long_name = ds[variable_name].attrs.get('long_name', variable_name)
    plt.title(f'Time-Averaged {long_name}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.tight_layout()
    
    plt.savefig(final_output_path, dpi=300)
    plt.close()
    print(f"Success: Heatmap saved to {final_output_path}")