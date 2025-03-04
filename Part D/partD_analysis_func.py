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

def extract_sex_data(data):

    variables = ['GEOID','DP05_0002PE','DP05_0003PE']
    
    labels = ['GEOID','Male','Female']
    
    extracted_data = data[variables].copy()
    extracted_data.columns = labels
    
    extracted_data.iloc[:, 1:] = extracted_data.iloc[:, 1:].astype(float)
    
    return extracted_data

def extract_housing_data(data):
    
    variables = ['GEOID','DP02_0002PE','DP02_0003PE','DP02_0004PE',
                 'DP02_0005PE','DP02_0006PE','DP02_0007PE','DP02_0008PE',
                 'DP02_0009PE','DP02_0010PE','DP02_0011PE','DP02_0012PE',
                 'DP02_0013PE']
    
    labels = ['GEOID','Married_total','Married_kids','Cohabit_total',
              'Cohabit_kids','Male_total','Male_kids','Male_alone_total',
              'Male_alone_over65','Female_total','Female_kids',
              'Female_alone_total','Female_alone_over65']
    
    extracted_data = data[variables].copy()
    extracted_data.columns = labels 
    
    extracted_data.iloc[:, 1:] = extracted_data.iloc[:, 1:].astype(float)
    
    # derived quantities 
    extracted_data['Married_no_kids'] = extracted_data['Married_total'] - extracted_data['Married_kids']
    extracted_data['Cohabit_no_kids'] = extracted_data['Cohabit_total'] - extracted_data['Cohabit_kids']
    extracted_data['Male_alone_under65'] = extracted_data['Male_alone_total'] - extracted_data['Male_alone_over65']
    extracted_data['Male_adults'] = extracted_data['Male_total'] - extracted_data['Male_kids'] - extracted_data['Male_alone_total']
    extracted_data['Female_alone_under65'] = extracted_data['Female_alone_total'] - extracted_data['Female_alone_over65']
    extracted_data['Female_adults'] = extracted_data['Female_total'] - extracted_data['Female_kids'] - extracted_data['Female_alone_total']
    
    return extracted_data
    
def extract_marriage_data(data):
    
    variables = ['GEOID','DP02_0026PE','DP02_0027PE','DP02_0028PE',
                 'DP02_0029PE','DP02_0030PE','DP02_0032PE','DP02_0033PE',
                 'DP02_0034PE','DP02_0035PE','DP02_0036PE']
    
    labels = ['GEOID','male_never_married','male_married','male_separated',
              'male_widowed','male_divorced','female_never_married',
              'female_married','female_separated','female_widowed',
              'female_divorced']
    
    extracted_data = data[variables].copy()
    extracted_data.columns = labels 
    
    extracted_data.iloc[:, 1:] = extracted_data.iloc[:, 1:].astype(float)
    
    return extracted_data

def extract_school_enrollment_data(data):
    
    variables = ['GEOID','DP02_0054PE','DP02_0055PE','DP02_0056PE',
                 'DP02_0057PE','DP02_0058PE']
    
    labels = ['GEOID','preschool','kindergarten','elementary_school',
              'high_school','college']
    
    extracted_data = data[variables].copy()
    extracted_data.columns = labels 
    
    extracted_data.iloc[:, 1:] = extracted_data.iloc[:, 1:].astype(float)
    
    return extracted_data

def extract_education_data(data):
    
    variables = ['GEOID','DP02_0060PE','DP02_0061PE','DP02_0062PE',
                 'DP02_0063PE','DP02_0064PE','DP02_0065PE','DP02_0066PE']
                 
    labels = ['GEOID','less_than_ninth','ninth_to_twelfth','hs_graduate',
              'some_college','associates','bachelors','graduate_degree']
    
    extracted_data = data[variables].copy()
    extracted_data.columns = labels 
    
    extracted_data.iloc[:, 1:] = extracted_data.iloc[:, 1:].astype(float)
    
    return extracted_data

def extract_household_income_data(data):
    
    variables = ['GEOID','DP03_0052PE','DP03_0053PE','DP03_0054PE',
                 'DP03_0055PE','DP03_0056PE','DP03_0057PE','DP03_0058PE',
                 'DP03_0059PE','DP03_0060PE','DP03_0061PE']
                 
    labels = ['GEOID','less_10k','10k_to_15k','15k_to_25k','25k_to35k',
              '35k_to_50k','50k_to_75k','75k_to_100k','100k_to_150k',
              '150k_to_200k','200k_more']
    
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