# Opioid function file 

import geopandas as gpd
import matplotlib.pyplot as plt 
import requests 
import pandas as pd 

def get_api_dataframe(url):
    
    table = requests.get(url)
    
    df = pd.DataFrame(table.json())
    
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    return df

def merge_shapefile_data(shapefile_path, dataframe, merge_column, data_column):
    """
    Plots a choropleth map using a census shapefile and a dataframe with a 'rate' column.

    Parameters:
    - shapefile_path: Path to the census shapefile.
    - dataframe: DataFrame containing the 'rate' column and a key column to merge on.
    - key_column: The column to merge the dataframe with the shapefile.
    - cmap: Color map for the choropleth.
    - title: Title of the map.
    """
    try:
        # Load the shapefile into a GeoDataFrame
        gdf = gpd.read_file(shapefile_path)

        # Merge the GeoDataFrame with the DataFrame on the key column
        if merge_column not in gdf.columns or merge_column not in dataframe.columns:
            raise ValueError(f"Key column '{key_column}' must exist in both the shapefile and the dataframe.")

        return gdf.merge(dataframe[[merge_column, data_column]], on=merge_column)
        
    except Exception as e:
        print(f"Error: {e}")

def plot_choropleth_map(shapefile,data_column,cmap='Blues'):
    
    # Plot the choropleth map
    fig, ax = plt.subplots(figsize=(10, 6))
    shapefile.plot(column=data_column, cmap=cmap, legend=True, ax=ax, 
                   edgecolor='k',vmin=0,vmax=10)

    ax.set_xlim([-130, -60])
    ax.set_ylim([20, 50])
    ax.set_title(data_column)
    ax.axis('off')
    plt.tight_layout()
    plt.show()