#Goal - Produce two maps, excatly 6 months apart, to demonstrate that solar elevation indeed depends on the season.
#Output can be seen here - https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/INSAT-3DR%20only/variation%20in%20solar%20elevation%20with%20season.png

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
from pyhdf.SD import SD, SDC
from pyhdf import HDF, VS, V
import os
from cartopy.feature.nightshade import Nightshade

#Any two files that are exactly 6 months apart should work. This combination below produced the best aesthetics.
insatpath1 = r'/data/debasish/insatdata/l1b/2019/2019jan/day01/3RIMG_01JAN2019_0345_L1B_STD_V01R00.h5'
insatpath2 = r'/data/debasish/insatdata/l1b/2019/jul2019_day1_std/3RIMG_01JUL2019_0345_L1B_STD_V01R00.h5'

insatfile1 = h5py.File(insatpath1, 'r')
insatfile2 = h5py.File(insatpath2, 'r')

lat1 = np.array(insatfile1['Latitude'],dtype=float)
lat_fill1 = insatfile1['Latitude'].attrs['_FillValue'][0]
lat1[lat1==lat_fill1] = np.nan
lat1 = lat1/100

lon1 = np.array(insatfile1['Longitude'],dtype=float)
lon_fill1 = insatfile1['Longitude'].attrs['_FillValue'][0]
lon1[lon1==lon_fill1] = np.nan
lon1 = lon1/100

lat2 = np.array(insatfile2['Latitude'],dtype=float)
lat_fill2 = insatfile2['Latitude'].attrs['_FillValue'][0]
lat2[lat2==lat_fill2] = np.nan
lat2 = lat2/100

lon2 = np.array(insatfile2['Longitude'],dtype=float)
lon_fill2 = insatfile2['Longitude'].attrs['_FillValue'][0]
lon2[lon2==lon_fill2] = np.nan
lon2 = lon2/100


solarelevation1 = np.array(insatfile1['Sun_Elevation'],dtype=float)
solarelevation_fill1 = insatfile1['Sun_Elevation'].attrs['_FillValue'][0]
solarelevation1[solarelevation1==solarelevation_fill1] = np.nan
solarelevation1 = solarelevation1/100

solarelevation2 = np.array(insatfile2['Sun_Elevation'],dtype=float)
solarelevation_fill2 = insatfile2['Sun_Elevation'].attrs['_FillValue'][0]
solarelevation2[solarelevation2==solarelevation_fill2] = np.nan
solarelevation2 = solarelevation2/100

date1 = insatfile1.attrs['Acquisition_Date'].decode('utf-8')
acq_start1 = insatfile1.attrs['Acquisition_Start_Time'].decode('utf-8')[-8:]
acq_end1 = insatfile1.attrs['Acquisition_End_Time'].decode('utf-8')[-8:]

date2 = insatfile2.attrs['Acquisition_Date'].decode('utf-8')
acq_start2 = insatfile2.attrs['Acquisition_Start_Time'].decode('utf-8')[-8:]
acq_end2 = insatfile2.attrs['Acquisition_End_Time'].decode('utf-8')[-8:]

year1 = int(date1[-4:])
month_abb1 = date1[2:5]
month_no1 = datetime.datetime.strptime(month_abb1, "%b").month
day1 = int(date1[:2])
hour1 = int(acq_start1.split(":")[0])
minute1 = int(acq_start1.split(":")[1])
second1  = int(acq_start1.split(":")[2])

year2 = int(date2[-4:])
month_abb2 = date2[2:5]
month_no2 = datetime.datetime.strptime(month_abb2, "%b").month
day2 = int(date2[:2])
hour2  = int(acq_start2.split(":")[0])
minute2 = int(acq_start2.split(":")[1])
second2 = int(acq_start2.split(":")[2])
#print(date1, acq_start1, acq_end1, date2, acq_start2, acq_end2)

fig = plt.figure(figsize=(10,11),dpi=300)

ax1 = plt.subplot(2,1,1, projection = ccrs.PlateCarree())
ax2 = plt.subplot(2,1,2, projection = ccrs.PlateCarree())

extent = -1

plot1 = ax1.scatter(lon1.flatten()[0:extent], lat1.flatten()[0:extent], 
        c = solarelevation1.flatten()[0:extent], cmap = 'jet', s = 0.1, 
        transform = ccrs.PlateCarree())
ax1.set_global()
gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, 
                    linewidth=1, color='black', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
date1_datetime  = datetime.datetime(year1, month_no1, day1, hour1, minute1, second1)
ax1.add_feature(Nightshade(date1_datetime, alpha=0.5))
ax1.coastlines()
cbar1 = plt.colorbar(plot1, 
                     orientation = 'vertical',
                     pad=0.035, 
                     #fraction=0.019, 
                     aspect=50,
                     shrink = 0.815,
                     ax=ax1)
cbar1.set_label('Solar elevation angle (deg.)', fontsize=16)
ax1.set_title('Date : {},Time interval : {}-{} GMT'.format(date1, acq_start1, acq_end1), fontsize=16)


plot2 = ax2.scatter(lon2.flatten()[0:extent], lat2.flatten()[0:extent], 
        c = solarelevation2.flatten()[0:extent], cmap = 'jet', s = 0.1, 
        transform = ccrs.PlateCarree())
ax2.set_global()
gl = ax2.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, 
                    linewidth=1, color='black', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
date2_datetime  = datetime.datetime(year2, month_no2, day2, hour2, minute2, second2)
ax2.add_feature(Nightshade(date2_datetime, alpha=0.5))
ax2.coastlines()
cbar2 = plt.colorbar(plot2, orientation = 'vertical',
                     #pad=0.035, 
                     #fraction=0.019, 
                     aspect=50,
                     shrink = 0.815,
                     ax=ax2)
cbar2.set_label('Solar elevation angle (deg.)', fontsize=16)
ax2.set_title('Date : {},Time interval : {}-{} GMT'.format(date2, acq_start2, acq_end2), fontsize=16)

fig.suptitle('Seasonal variation in solar elevation angle', fontsize=20, fontweight = 'bold',
             y=0.94, x=0.45)
plt.tight_layout()
plt.show()
