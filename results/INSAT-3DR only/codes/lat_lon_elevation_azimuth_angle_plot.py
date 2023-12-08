# This is a template code to plot simple parameters like latitude, longitude, solar elevation angle, solar azimuth angle, satellite elevation angle, satellite azimuth angle etc.
#The logic is that longitude is x, latitude is y, and the intensity of the color is the parameter we want to plot (elevation angle, longitude etc)

import numpy as np
import matplotlib.pyplot as plt
import h5py
from cartopy import crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.lines import Line2D
import pandas as pd
import time
import datetime

inastfilepath = r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\L1B data\INSAT-3DR\3RIMG_01APR2022_0015_L1B_STD_V01R00.h5" #Replace this
insatfile = h5py.File(inastfilepath,'r')
print(insatfile.keys())

#Reading latitude and longitude arrays
latitudearray = np.array(insatfile['Latitude'],dtype=float)
lat_fill = insatfile['Latitude'].attrs['_FillValue'][0]
latitudearray[latitudearray==lat_fill] = np.nan
latitudearray = latitudearray/100

longitudearray = np.array(insatfile['Longitude'],dtype=float)
lon_fill = insatfile['Longitude'].attrs['_FillValue'][0]
longitudearray[longitudearray==lon_fill] = np.nan
longitudearray = longitudearray/100

#Reading solar elevation and azimuth arrays
solarelevation = np.array(insatfile['Sun_Elevation'],dtype=float)
solarelevation_fill = insatfile['Sun_Elevation'].attrs['_FillValue'][0]
solarelevation[solarelevation==solarelevation_fill] = np.nan
solarelevation = solarelevation/100
solarazimuth = np.array(insatfile['Sun_Azimuth'],dtype=float)
solarazimuth_fill = insatfile['Sun_Azimuth'].attrs['_FillValue'][0]
solarazimuth[solarazimuth==solarazimuth_fill] = np.nan
solarazimuth = solarazimuth/100

#Reading satellite elevation and azimuth arrays
satelevation = np.array(insatfile['Sat_Elevation'],dtype=float)
satelevation_fill = insatfile['Sat_Elevation'].attrs['_FillValue'][0]
satelevation[satelevation==satelevation_fill] = np.nan
satelevation = satelevation/100
satazimuth = np.array(insatfile['Sat_Azimuth'],dtype=float)
satazimuth_fill = insatfile['Sat_Azimuth'].attrs['_FillValue'][0]
satazimuth[satazimuth==satazimuth_fill] = np.nan
satazimuth = satazimuth/100

#Reading datetime information

date = insatfile.attrs['Acquisition_Date'].decode('utf-8')
acq_start = insatfile.attrs['Acquisition_Start_Time'].decode('utf-8')[-8:]
acq_end = insatfile.attrs['Acquisition_End_Time'].decode('utf-8')[-8:]

year = int(date1[-4:])
month_abb = date1[2:5]
month_no = datetime.datetime.strptime(month_abb, "%b").month
day = int(date[:2])
hour = int(acq_start.split(":")[0])
minute = int(acq_start.split(":")[1])
second  = int(acq_start.split(":")[2])

#Plotting

extent = -1 #Around 6M points to plot, extent can be used to fine-tune the image before going for the full plot which might take time.
fig = plt.figure(figsize=(8,6))
ax = plt.axes(projection=ccrs.PlateCarree())

plot = plt.scatter(
                   longitudearray.flatten()[0:extent],latitudearray.flatten()[0:extent],
                   c =longitudearray.flatten()[0:extent], 
                   # c =latitudearray.flatten()[0:extent], #You can uncomment/add more parameters to plot them instead 
                   # c =solarelevation.flatten()[0:extent]
                   # c =satelevation.flatten()[0:extent]
                   # c = 'r' #This will put uniform red color over the entire coverage area of INSAT-3DR, but you have to comment the cmap while using it
                   cmap='jet',
                   transform=ccrs.PlateCarree(),
                   s=0.1
                  )

# ax.stock_img() #Optional stock image
ax.set_global()
ax.coastlines()
ax.gridlines()
cbar = plt.colorbar(plot, orientation='horizontal', pad=0.005, fraction=0.05, aspect=50)
cbar.set_label('Longitude (In degrees)') #Change it accordingly to what parameter you are plotting
plt.title('Longitude \n Date: {} \n File acquisition time: {}-{} (GMT)'.format(insatdate,acqstart,acqend)) #Change the parameter here too.
plt.show()
