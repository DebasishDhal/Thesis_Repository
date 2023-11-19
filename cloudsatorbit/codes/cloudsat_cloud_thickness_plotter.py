#Input - A 2B-CLDCLASS file.
#Output - Map showing the total cloud thickness along its orbit
#Example output - https://github.com/DebasishDhal/Thesis_Repository/blob/main/cloudsatorbit/Total%20cloud%20thickness%20sample%20result.jpg
#For reference, check this ending part of this notebook- https://github.com/DebasishDhal/Thesis_Repository/blob/main/miscellaneous/cloudsat%20basic%20data%20reading.ipynb

csatpath=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001041234_67528_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"

import numpy as np
import matplotlib.pyplot as plt
import h5py
from cartopy import crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.lines import Line2D
import pandas as pd
from pyhdf.SD import SD, SDC
from pyhdf import HDF, VS, V

def thickness_extractor(adress):
  csatfile = SD(adress, SDC.READ)
  
  cloudlayerbase=csatfile.select('CloudLayerBase')[:,:]
  cloudlayerbase=np.ma.masked_equal(cloudlayerbase,-99)
  cloudlayertop=csatfile.select('CloudLayerTop')[:,:]
  cloudlayertop=np.ma.masked_equal(cloudlayertop,-99)
  cloudlayerheight=cloudlayertop-cloudlayerbase
  
  #Add the cloudlayerheight along rows to get the total height of the cloud layer
  cloudlayerheight=(np.sum(cloudlayerheight,axis=1))
  
  cloudlayerheight=np.ma.filled(cloudlayerheight,0)
  return cloudlayerheight
  
cloudlayerheight = thickness_extractor(csatpath)

#Retrieving latitude and longitude profiles from the HDF file

h = HDF.HDF(r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001041234_67528_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf")

def oned_dataset_func(dataset_names):
    dataset_list = []
    for i in dataset_names:
        vs = h.vstart()
        xid = vs.find(i)
        dataid = vs.attach(xid)
        dataid.setfields(i)
        nrecs, _, _, _, _ = dataid.inquire()
        data = dataid.read(nRec=nrecs)
        data=list(np.concatenate(data))
        dataset_list.append(data)
        dataid.detach()
    return dataset_list

csatlat,csatlon=oned_dataset_func(['Latitude','Longitude'])

fig=plt.figure()
ax=plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.set_global()
ax.gridlines()
ax.set_xticks(np.arange(-180, 180, 30), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-90, 90, 30), crs=ccrs.PlateCarree())
ax.set_xlabel('Longitude',fontsize=15)

#First do the groundtrack, then the cloud layer height

divnorm=colors.TwoSlopeNorm(vmin=0.00,vcenter=0.2,vmax=16)
ax.scatter(
          csatlon,csatlat,
          edgecolors='black',
          s=5,
          alpha=0.002,
          facecolors='none',
          transform=ccrs.PlateCarree()
          );

#Apply legend after plotting the ground track, otherwise the legend will appear near colorbar and not near the plot

lines=Line2D([0],[0],color='black',lw=3,linestyle='solid')

legend=plt.legend(
                  [lines],['Clear sky'],
                  fontsize=10,
                  handlelength=1,
                  loc=(0.01,0.455)
                 )

#Plotting the cloudlayerheight

plot=ax.scatter(
                csatlon,csatlat,c=cloudlayerheight,
                s=5,
                norm=divnorm, 
                cmap='jet',
                transform=ccrs.PlateCarree()
               )

plt.title('Total cloud thickness over a place with \n satellite ground track, 01Jan2019,0412UTC') #The datetime has not been automated.

#Add colorbar
cax =  fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
cbar=plt.colorbar(plot,cax=cax)
cbar.set_label('Cloud thickness (km)',rotation=270,fontsize=15,labelpad=10) #labelpad is used to move the label away from the colorbar

plt.show()
