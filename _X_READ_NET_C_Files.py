import pandas as pd
import numpy as np
# import h5py

from netCDF4 import Dataset
#######################################################################################################################

''' Introduction and practice to read HDF files
    author: Ivan Dario Pabon Fernandez
    date: 20.04.2020
 '''
#######################################################################################################################


file_root_1 = r"C:\Users\500509\Desktop\File_A.nc4"
file_root_2 = r"C:\Users\500509\Desktop\AIRS.2019.10.31.240.L2.SUBS2RET.v6.0.31.1.G19305123450 (1).h5"
file_root_3 = r'C:\Users\500509\Desktop\test_hdf.hdf'
filename = "File_A.nc4"

data = Dataset(r'C:\Users\500095\Downloads\netCDFSample.nc4', 'r')
# # with pd.read_hdf(file_root_2) as hdf:
# with h5py.File(file_root_3) as hdf:
#     print(hdf.keys())

# print(data)
print("-----------------------------------------------------------------------------------------------")
print("READING VARIABLES: ")
print(data.keys())
longitude = data.variables['Longitude']
latitude = data.variables['Latitude']
temperature_asc = data.variables['Temperature_A']
rel_humidity_asc = data.variables['RelHum_A']
surf_air_temperature_asc = data.variables['SurfAirTemp_A']
surf_Rel_humidity_asc = data.variables['RelHumSurf_A']
print("-----------------------------------------------------------------------------------------------")
print("PRINTING VARIABLES: ")
print(longitude)
print(latitude)
print(temperature_asc)
print(rel_humidity_asc)
print(surf_air_temperature_asc)
print(surf_Rel_humidity_asc)
print("-----------------------------------------------------------------------------------------------")
print("++++  VARIABLE DIMENSIONS: ++++")
print(data.dimensions.keys())
for item in data.dimensions.items():
    print(item)

print("AIR TEMPERATURE DIMENSIONS:   ", end='')
print(temperature_asc.dimensions)
print("REL HUMIDITY DIMENSIONS:   ", end='')
print(rel_humidity_asc)
print("SURF AIR TEMPERATURE DIMENSIONS:   ", end='')
print(surf_air_temperature_asc.dimensions)
print("SURF RELATIVE HUMIDITY DIMENSIONS:   ", end='')
print(surf_Rel_humidity_asc.dimensions)
print("LATITUDE DIMENSIONS:   ", end='')
print(latitude.dimensions)
print("LONGITUDE DIMENSIONS:  ", end='')
print(longitude.dimensions)
print("-----------------------------------------------------------------------------------------------")
print("ACCESSING TO THE DATA OF A VARIABLE: ")
long = longitude[:]
lat = latitude[:]
print(long)
print(lat)
print("-----------------------------------------------------------------------------------------------")
print("CREATING INFORMATION FOR DATA FRAME ")
list_latitudes = list()
list_longitudes = list()
list_temperature_K = list()
list_temperature_C = list()
list_rel_humidity = list()
for value_lat in lat:
    for value_long in long:
        list_latitudes.append(value_lat)
        list_longitudes.append(value_long)
        value_temperature_k = surf_air_temperature_asc[value_lat, value_long]
        list_temperature_K.append(value_temperature_k)
        list_temperature_C.append(value_temperature_k-273.15)
        list_rel_humidity.append(surf_Rel_humidity_asc[value_lat, value_long])

dict_data = {'Latitude': list_latitudes,
             'Longitude': list_longitudes,
             'Temperature K': list_temperature_K,
             'temperature C': list_temperature_C,
             'Rel_Humidity': list_rel_humidity}
info_df = pd.DataFrame(dict_data)
print(info_df)

csv_result_root = r'D:\NASA_AIRS_DATA\NASA_AIRS_CSV_incl_Enthalpy\netCDF_DataExtract.csv'
info_df.to_csv(r"C:\Users\500509\Desktop\Nasa_Data_1.csv", sep=';', index=None, header=True)






#######################################################################################################################
# with h5py.File(filename, "r") as f:
#     # List all groups
#     print("Keys: %s" % f.keys())
#     a_group_key = list(f.keys())[0]
#
#     # Get the data
#     data = list(f[a_group_key])