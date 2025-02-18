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

def extract_age_data(data):
    
    variables = ['GEOID','DP05_0005PE','DP05_0006PE','DP05_0007PE','DP05_0008PE',
                 'DP05_0009PE','DP05_0010PE','DP05_0011PE','DP05_0012PE',
                 'DP05_0013PE','DP05_0014PE','DP05_0015PE','DP05_0016PE',
                 'DP05_0017PE']
    labels = ['GEOID','under 5','5-9','10-14','15-19','20-24','25-34','35-44','45-54',
              '55-59','60-64','65-74','75-84','85+']

    age_data = data[variables].copy()
    age_data.columns = labels
    
    age_data.iloc[:, 1:] = age_data.iloc[:, 1:].astype(float)
    
    
    return age_data

def extract_race_data(data):
    
    variables = ['GEOID','DP05_0037PE','DP05_0038PE','DP05_0039PE','DP05_0045PE',
                 'DP05_0046PE','DP05_0047PE','DP05_0048PE','DP05_0049PE',
                 'DP05_0050PE','DP05_0051PE','DP05_0053PE','DP05_0054PE',
                 'DP05_0055PE','DP05_0056PE','DP05_0057PE','DP05_0059PE',
                 'DP05_0060PE','DP05_0061PE','DP05_0062PE']
    
    labels = ['GEOID','White','Black','American Indian','Asian Indian','Chinese',
              'Filipino','Japenese','Korean','Vietnamese','Other Asian',
              'Native Hawaiian','Guamanian or Chamorro','Samoan',
              'Other Pacific Islander','Some other race',
              'White and Black or African American',
              'White and American Indian and Alaska Native','White and Asian',
              'Black or African American and American Indian and Alaska Native']

    extracted_data = data[variables].copy()
    extracted_data.columns = labels
    
    extracted_data.iloc[:, 1:] = extracted_data.iloc[:, 1:].astype(float)
    
    return extracted_data
    

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