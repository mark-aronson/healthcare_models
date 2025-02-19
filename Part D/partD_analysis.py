# Medicare Part D Utilization 

import pandas as pd
import requests
import partD_analysis_func as fun

# from https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-opioid-prescribing-rates/medicare-part-d-opioid-prescribing-rates-by-geography

opioid_data = pd.read_csv('Medicare_Part_D_Opioid_Prescribing_Rates_by_Geography_2022.csv')

# Add leading zeros to ensure all entries have five characters
opioid_data['GEOID'] = opioid_data['Prscrbr_Geo_Cd'].apply(lambda x: str(x).zfill(5))

#%% plot choropleth of opioid perscription rate 

# shapefile_path_counties_2022 = 'tl_2022_us_county/tl_2022_us_county.shp'

# shapefile = fun.merge_shapefile_data(shapefile_path_counties_2022,opioid_data,'GEOID','Opioid_Prscrbng_Rate')
# fun.plot_choropleth_map(shapefile,'Opioid_Prscrbng_Rate')


#%% Get DP05 datatable from the Census website 

url_dp05 = 'https://api.census.gov/data/2022/acs/acs5/profile?get=group(DP05)&ucgid=pseudo(0100000US$0500000)'

acs_demographic_housing_data = fun.get_api_dataframe(url_dp05)
acs_demographic_housing_data['GEOID'] = acs_demographic_housing_data['GEO_ID'].str[-5:]

#%% Extract demographic groups 

age_data = fun.extract_age_data(acs_demographic_housing_data)
race_data = fun.extract_race_data(acs_demographic_housing_data)
sex_data = fun.extract_sex_data(acs_demographic_housing_data) 

# codebook: https://api.census.gov/data/2018/acs/acs5/profile/groups/DP05.html

#%% Get DP02 Datatable 

url_dp02 = 'https://api.census.gov/data/2022/acs/acs5/profile?get=group(DP02)&ucgid=pseudo(0100000US$0500000)'

dp02 = fun.get_api_dataframe(url_dp02)
dp02['GEOID'] = dp02['GEO_ID'].str[-5:]

#%% Extract Social Characteristics 

# codebook: https://api.census.gov/data/2022/acs/acs5/profile/groups/DP02.html
# variable view: https://data.census.gov/table?q=DP02:%20Selected%20Social%20Characteristics%20in%20the%20United%20States

housing_data = fun.extract_housing_data(dp02)
marriage_data = fun.extract_marriage_data(dp02)

#%% start building dataset 

data = opioid_data[['GEOID','Opioid_Prscrbng_Rate']]

data = pd.merge(data,age_data,on='GEOID',how='left')
data = pd.merge(data,race_data,on='GEOID',how='left')
data = pd.merge(data,sex_data,on='GEOID',how='left')
data = pd.merge(data,housing_data,on='GEOID',how='left')
data = pd.merge(data,marriage_data,on='GEOID',how='left')


