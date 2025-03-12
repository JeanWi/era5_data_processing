from src import *

# Download from era5
# area = [60.5, 10, 59, 11.5]
# years = [1995, 2008, 2009]
# for year in years:
#     filename = 'D:/00_Data/00_ClimateData/ERA5/norway'+str(year)+'.nc'
#     print(filename)
#     download_era5_climate_data(area, year, filename)

# Read from nc file
year = 2009
lon = 3.936
lat = 53.178
nc_filepath = "D:/00_Data/00_ClimateData/ERA5/northwesteurope"+ str(year) + ".nc"
output_filepath = "C:/Users/6574114/PycharmProjects/PyHubProductive/DAC_Offshore_RawData/ClimateData/OffshoreNode.csv"
data = convert_era5_data(nc_filepath, lon, lat)
data['dataframe'].to_csv(output_filepath)

year = 2009
lon = 4.244
lat = 51.761
nc_filepath = "D:/00_Data/00_ClimateData/ERA5/northwesteurope"+ str(year) + ".nc"
output_filepath = "C:/Users/6574114/PycharmProjects/PyHubProductive/DAC_Offshore_RawData/ClimateData/OnshoreNode.csv"
data = convert_era5_data(nc_filepath, lon, lat)
data['dataframe'].to_csv(output_filepath)
