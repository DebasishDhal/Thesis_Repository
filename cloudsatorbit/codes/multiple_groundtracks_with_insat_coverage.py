#Input - Multiple cloudsat file paths, and one INSAT-3DR file path.
#Output - A beautiful map containing all the groundtracks and the INSAT-3DR coverage area. 
#Output - https://github.com/DebasishDhal/Thesis_Repository/blob/main/cloudsatorbit/Multi%20orbit%20groundtrack%20with%20INSAT3DR%20with%20start%20time.png
#For reference, check the beginning of this notebook - https://github.com/DebasishDhal/Thesis_Repository/blob/main/miscellaneous/Geo_colocation.ipynb

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
from time import gmtime, strftime
from datetime import datetime
import time
import geopy.distance


#Below is a collection of all cloudsat files for a single day
csfile1path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001005530_67526_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile2path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001023402_67527_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile3path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001041234_67528_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile4path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001055106_67529_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile5path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001072938_67530_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile6path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001090810_67531_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile7path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001104642_67532_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile8path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001122514_67533_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile9path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001140346_67534_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile10path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001154218_67535_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile11path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001172050_67536_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile12path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001185922_67537_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile13path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001203754_67538_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile14path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001221627_67539_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"
csfile15path=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\CLOUDSAT DATA\CLDCLASS-LIDAR\2019001235459_67540_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E08_F03.hdf"

csatfilepathcol=[csfile1path,csfile2path,csfile3path,csfile4path,csfile5path,csfile6path,csfile7path,csfile8path,csfile9path,csfile10path,csfile11path,csfile12path,csfile13path,csfile14path,csfile15path]

csatfilecol=[]

for i in csatfilepathcol:
    csatfilecol.append(SD(i, SDC.READ))



geofieldcol=[]
def oned_dataset_func(dataset_names,h):
    dataset_list = []
    for i in dataset_names:
        vs = h.vstart()
        xid = vs.find(i)
        dataid = vs.attach(xid)
        dataid.setfields(i)
        nrecs, _, _, _, _ = dataid.inquire()
        data = dataid.read(nRec=nrecs) #Each data point is singleton list, so we need to concatenate them
        data = list(np.concatenate(data)) 
        dataset_list.append(data)
        dataid.detach()
    return dataset_list

for i in csatfilepathcol:
    h=HDF.HDF(i)
    geofieldcol.append(oned_dataset_func(['Latitude','Longitude',"DEM_elevation","Profile_time","Navigation_land_sea_flag","UTC_start","Cloudlayer"],h))
print("geofieldcol is a list of len={}, each element is a list of len={}, corresponding to lat,lon,elevation, profile_time,Land/sea flag,UTC_start time and Cloudlayer file".format(len(geofieldcol),len(geofieldcol[0])))



#Reading the INSAT-3DR data
insatfilepath=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\L1B data\INSAT-3DR\3RIMG_01JAN2019_0615_L1B_STD_V01R00.h5"
insatfile=h5py.File(r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\L1B data\INSAT-3DR\3RIMG_01JAN2019_0615_L1B_STD_V01R00.h5",'r') #OK, this is file specific, works with other file Download it and retry
insatlat=insatfile["Latitude"]
insatlon=insatfile["Longitude"]
insatlat=np.ma.masked_equal(insatlat,32767)/100
insatlon=np.ma.masked_equal(insatlon,32767)/100
inleftlon=insatfile.attrs['left_longitude'][0]
inrightlon=insatfile.attrs['right_longitude'][0]
intoplat=insatfile.attrs['upper_latitude'][0]
inbottomlat=insatfile.attrs['lower_latitude'][0]




#Plot the lat,lon,elevation, profile_time and UTC_start time for all the files
#['Latitude','Longitude',"DEM_elevation","Profile_time","UTC_start"]

fig=plt.subplots(figsize=(20,10))
#Supress the ticklabels on the x axis
plt.tick_params(labelbottom=False)
plt.tick_params(labelleft=False)

ax=plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.coastlines()
ax.gridlines()
ax.stock_img()
ax.set_xticks(np.arange(-180,180,30), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-90,90,30), crs=ccrs.PlateCarree())
ax.set_xticklabels(np.arange(-180,180,30), fontsize=10);
ax.set_yticklabels(np.arange(-90,90,30), fontsize=10);
ax.set_xlabel("Longitude",fontsize=25)
ax.set_ylabel("Latitude",fontsize=25)

ax.plot([inleftlon,inrightlon,inrightlon,inleftlon,inleftlon],[intoplat,intoplat,inbottomlat,inbottomlat,intoplat],color='red',transform=ccrs.PlateCarree()) 
ax.scatter(insatlon,insatlat,s=0.0008,transform=ccrs.PlateCarree(),color="red")

for i in range(len(geofieldcol)):
    ax.scatter(geofieldcol[i][1],geofieldcol[i][0],s=0.1,transform=ccrs.PlateCarree())
    ax.text(geofieldcol[i][1][0]+1.0,geofieldcol[i][0][0]-8,"Orbit "+str(i+1),
    rotation=80,size=15,fontweight="bold",transform=ccrs.PlateCarree())
    ax.arrow(geofieldcol[i][1][2000],geofieldcol[i][0][2000],
    geofieldcol[i][1][2]-geofieldcol[i][1][0],
    geofieldcol[i][0][2]-geofieldcol[i][0][0],
    head_width=5, head_length=5,color="black")
    ax.text(geofieldcol[i][1][0]+6,geofieldcol[i][0][0]-9,time.strftime('%H:%M:%S', time.gmtime(geofieldcol[i][5][0])),
    rotation=80,size=15,fontweight="bold",transform=ccrs.PlateCarree())
#    transform=ccrs.PlateCarree())

ax.legend([Line2D([0], [0], color='red', linewidth=3, linestyle="dotted")],["INSAT-3DR\ncoverage"],loc="upper right",fontsize=20)
ax.set_title("All CloudSat orbits on 01 Jan 2019 with INSAT-3DR Coverage",fontsize=20); #The naming has not been automated
plt.show()
