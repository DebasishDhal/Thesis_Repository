#This program takes in a L1B file adress, channel, parameter as inputs and gives us a plot on the globe of the parameter as output.
#Example output - https://github.com/DebasishDhal/Thesis_Repository/blob/main/miscellaneous/images/Fani%20BT%20plot.png

import h5py
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade
from datetime import datetime
from matplotlib import colors
from matplotlib.widgets import Cursor

file=r'C:\Users\HP\OneDrive\Desktop\HD5 Collection\3DIMG_03MAY2019_0230_L1B_STD.h5' #Change here

with h5py.File(file) as f:
    
#Image data retrieval
    image="IMG_TIR1"  #IMG_TIR1, IMG_TIR2, IMG_VIS, IMG_SWIR, IMG_MIR, IMG_WV are different options #Change here
    parameter = 'temp' #temp or radiance or count are the options #Change here
  
    if parameter in ['temp','Temp','bt,'BT','Brightness_Temperature']:
      parameter = 'temp'
    if parameter in ['radiance','rad','Radiance']:
      parameter = 'radiance'
    
    img_arr=f[image][0,:,:]
    img_arr_fill=f[image].attrs['_FillValue'][0]#[0] #Getting fill value, #0 as it's the fill value is a numpy array

    #print(type(img_arr_fill)) #with [0] it's numpy.ndarray, with [0] it's numpy.uint16
    img_arr_m=np.ma.masked_equal(img_arr,img_arr_fill, copy=True)

    central_wavelength=str(f[image].attrs['central_wavelength'][0])
    l=float(central_wavelength)*10**(-6)
    central_wavelength="{}{}".format(central_wavelength,str("μm"))
    print(central_wavelength)

    bandwidth=f[image].attrs['bandwidth']

    acquisition_date=str(f.attrs['Acquisition_Date'])[2:-1]
    start_time=str(f.attrs['Acquisition_Start_Time'])[2:-1].split('T')[1]
    end_time=str(f.attrs['Acquisition_End_Time'])[2:-1].split('T')[1]
    
    time="{} - {} GMT".format(start_time,end_time)
    

#Plot extent retrieval

    left_lon=f.attrs['left_longitude'][0]
    right_lon=f.attrs['right_longitude'][0]

    upper_lat=f.attrs['upper_latitude'][0]
    lower_lat=f.attrs['lower_latitude'][0]

    sat_lon=f.attrs['Nominal_Central_Point_Coordinates(degrees)_Latitude_Longitude'][1] #Lat_Lon = np.array(([0,82.0]))
    sat_alt=f.attrs['Observed_Altitude(km)'][0]*1000 #For alt. in m.
    #print(sat_pos)
    #print(sat_alt)

#Count to radiance conversion

    sensor_name=f.attrs['Sensor_Name'].decode()
    #print(sensor_name) #Without decoding, it'd show b'IMAGER' as it's encoded in UTF-8
    
    #Radiance from count
    def counttodata(count,lut): #This function converts the count to data, data can be radiance, albedo, temperature. 
        return lut[count]

    if parameter == 'radiance':
      lut=np.array(f[image+'_RADIANCE'])
      radiance_masked = counttodata(img_arr_m, lut)
    if parameter == 'temp':
      lut=np.array(f[image+'_TEMP'])
      radiance_masked = counttodata(img_arr_m, lut) #This is actually the brightness temp lut, i.e. btlut. But I'm not changing the name again (This code is already 1.5 years old)
    if parameter == 'count':
      radiance_masked = img_arr_m
  
    
    
    


img_extent_deg = (left_lon, right_lon, lower_lat, upper_lat)
map_proj = ccrs.Geostationary(central_longitude=sat_lon)



fig=plt.figure(figsize=(12,12))
ax1 = plt.axes(projection=map_proj)
ax1.coastlines(color='white')
ax1.add_feature(cfeature.NaturalEarthFeature(category='cultural',scale='10m',name='admin_0_countries',edgecolor='black',facecolor='none'))
ax1.gridlines(color='black', alpha=0.5, linestyle='--', linewidth=1.75, draw_labels=True)


map_extend_geos = ax1.get_extent(crs=map_proj)

divnorm=colors.TwoSlopeNorm(vmin=0.05, vcenter=0.35,vmax=0.8)
plot1=plt.imshow(radiance_masked, extent=map_extend_geos,norm=divnorm,cmap='jet')#,cmap='gray' #'jet' map has more intense variations, thus better contrast
#plt.imshow(radiance_masked, extent=map_extend_geos)
cbar=plt.colorbar(plot1,ax=ax1,fraction=0.046,pad=0.04)
cbar.set_label(('Intensity (mW. $cm^{-2}.sr^{-1}.\mu^{-1} $)'),rotation=270,fontsize=20,labelpad=25)
map_proj_text=str(type(map_proj)).split(".")[-1][:-2]
if parameter == 'radiance':
  unit = 'Radiance unit: mW. $cm^{-2}.sr^{-1}.\mu^{-1} $\n'
if parameter = 'bt':
  unit = 'Temperature Unit : K\n'
if parameter == 'count':
  unit = 'Count is unitless\n'
plt.title(f'Projection: {map_proj_text}\n' + f' Raster Data: {image}_{parameter} (masked), $\lambda$={central_wavelength}\n' + 
unit+f'{acquisition_date}, Acquisition time = {time}') #f -> literal string, r -> raw string. Turns 

# plt.savefig(r"C:\Users\HP\OneDrive\Desktop\Thesis work\Results".format("Fani BT plot"))
plt.show()
