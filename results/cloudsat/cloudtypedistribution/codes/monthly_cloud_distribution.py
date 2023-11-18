import numpy as np
import matplotlib.pyplot as plt
import h5py
from cartopy import crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.lines import Line2D
import seaborn as sns
import pandas as pd
import time
import datetime
from pyhdf.SD import SD, SDC
from pyhdf import HDF, VS, V
import os
from matplotlib.colors import Normalize, PowerNorm
from matplotlib.cm import get_cmap

#Input - One 2b-CLDCLASS file, Output - Dataframe containing stats of the cloud layers for that file

def csat_stats(path):
    def oneddata(path,searchdatasetlist):
        if type(path)==str:
            h=HDF.HDF(path)
        else:
            h=path
        datasetlist=[]
        for i in searchdatasetlist:
            vs=h.vstart()
            xid=vs.find(i)
            dataid=vs.attach(xid)
            dataid.setfields(i)
            nrecs,_,_,_,_=dataid.inquire()
            data=dataid.read(nRec=nrecs)
            data=list(np.concatenate(data))
            datasetlist.append(data)
            dataid.detach()
            vs.end()
        return datasetlist

    lat, lon, landseaflag = oneddata(path,['Latitude','Longitude', 'Navigation_land_sea_flag'])
    csatfile = SD(path, SDC.READ)
    toparray = np.array(csatfile.select('CloudLayerTop'))
    toparray[toparray==-99.0] = np.nan
    bottomarray = np.array(csatfile.select('CloudLayerBase'))
    bottomarray[bottomarray==-99.0] = np.nan
    typearray = np.array(csatfile.select('CloudLayerType'),dtype=np.float64)
    typearray[typearray==-9.0] = np.nan


    indices = np.where(~np.isnan(typearray)) #Returns a tuple of arrays, one for each dimension of a, containing the indices of the non-nan elements.
    typearray = typearray[indices] #Extracting the type of cloud for each non-nan value (i.e. a cloud or clear case)
    lat = np.take(lat,(indices[0])) #To access elements of list using a 1D array. 
    lon = np.take(lon,(indices[0]))
    landseaflag = np.take(landseaflag,(indices[0]))
    toparray = toparray[indices]
    bottomarray = bottomarray[indices]
    df = pd.DataFrame(columns=['type','lat','lon','top','bottom','landseaflag'])

    df['type'] = typearray
    df['lat'] = lat
    df['lon'] = lon
    df['top'] = toparray
    df['bottom'] = bottomarray
    df['landseaflag'] = landseaflag
    df['thickness'] = df['top'] - df['bottom']
    
    return df

import re
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013mar' #Applying this function on all that are available for a month (Take March for example)
dflist=[]
for subfolder in os.listdir(rootdir):
    if subfolder.endswith('.csv'):
        continue
    filecount=0
    subfolder_path = os.path.join(rootdir,subfolder)
    if os.path.isdir(subfolder_path):
        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path,file)
            df = csat_stats(file_path)
            #Add the day number to the dataframe
            df['day'] = int(subfolder)
            #Add the orbit number to the dataframe
            orbit = re.search(r'\d+_(CS)', file_path).group(0).rstrip("_CS")
            df['orbit'] = int(orbit)
            dflist.append(df)
            filecount=filecount+1
            #Print the length of each df without a new line
            print(len(df),end=' \r')
    print("Folder ",subfolder," done, files processed: ",filecount)
df = pd.concat(dflist, ignore_index=True)
df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')


name = '2013mar.csv'
folder = '/data/debasish/cloudsatdata/cldclasslidar/2013/2013mar'
df.to_csv(os.path.join(folder,name),index=False)

cloudtype_dict={1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'}
cloudlabel=np.arange(1,10)

#Plot the fractional abundance of each cloud type in the dataset
dfcopy = df.copy()
dfcopy['latbin']=np.floor(dfcopy['lat'])
#dfcopy['latbin'].value_counts().sort_index()

from matplotlib.colors import Normalize, PowerNorm
from matplotlib.cm import get_cmap

norm = PowerNorm(gamma=0.7) #Sharper colors with better contrast
cmap = get_cmap("tab10")
colors = cmap(norm(np.linspace(0, 1, 10)))

colors_subplot_1 = colors[0:4]
colors_subplot_2 = colors[5:9]

#Make a figure with 4 subplots 2x2. Plot the global fractional abundance in first two, and the fractional abundance in the area of interest in the last two
fig,ax=plt.subplots(2,2,figsize=(10,10))
plt.figtext(0.5,1.0050,'Global data',ha='center', va='center',fontsize=16)
#Plot the fractional abundance of each cloud type in the dataset
dfcopy = df.copy()
dfcopy['latbin']=np.floor(dfcopy['lat'])

for i, c in enumerate(colors_subplot_1):
    ax[0,0].plot(dfcopy[dfcopy['type']==i+1].groupby('latbin')['type'].count()/dfcopy.groupby('latbin')['type'].count(),label=cloudtype_dict[i+1], color=c)
    ax[0,0].set_xlabel('Latitude')
    ax[0,0].set_ylabel('Fractional Abundance of Cloud Types')
    ax[0,0].legend()

for i, c in enumerate(colors_subplot_2):
    ax[0,1].plot(dfcopy[dfcopy['type']==i+5].groupby('latbin')['type'].count()/dfcopy.groupby('latbin')['type'].count(),label=cloudtype_dict[i+5], color=c)
    ax[0,1].set_xlabel('Latitude')
    ax[0,1].set_ylabel('Fractional Abundance of Cloud Types')
    ax[0,1].legend()

#Plot the fractional abundance of each cloud type in the area of interest
#Add a short text over these two subplots to indicate that they are for the area of interest
plt.figtext(0.5,0.51,'Over Indian subcontinent region',ha='center', va='center',fontsize=16)
lon_left, lon_right, lat_bot, lat_top = 60, 100, 0, 40
dfcopy_aoi = dfcopy[(dfcopy['lon']>=lon_left) & (dfcopy['lon']<=lon_right) & (dfcopy['lat']>=lat_bot) & (dfcopy['lat']<=lat_top)]
for i, c in enumerate(colors_subplot_1):
    ax[1,0].plot(dfcopy_aoi[dfcopy_aoi['type']==i+1].groupby('latbin')['type'].count()/dfcopy_aoi.groupby('latbin')['type'].count(),label=cloudtype_dict[i+1], color=c)
    ax[1,0].set_xlabel('Latitude')
    ax[1,0].set_ylabel('Fractional Abundance of Cloud Types')
    ax[1,0].legend()

for i, c in enumerate(colors_subplot_2):
    ax[1,1].plot(dfcopy_aoi[dfcopy_aoi['type']==i+5].groupby('latbin')['type'].count()/dfcopy_aoi.groupby('latbin')['type'].count(),label=cloudtype_dict[i+5], color=c)
    ax[1,1].set_xlabel('Latitude')
    ax[1,1].set_ylabel('Fractional Abundance of Cloud Types')
    ax[1,1].legend()


#Add an axis axproj with platcarree projection to ax[1,1] to plot the area of interest on the map

projection = ccrs.PlateCarree()
axproj = fig.add_axes([0.5662, 0.380, 0.1, 0.1], projection=projection)
axproj.set_extent([lon_left, lon_right, lat_bot, lat_top], crs=projection)
axproj.stock_img()
axproj.coastlines()
axproj.add_feature(cfeature.BORDERS)

#Add a title to the figure
plt.figtext(0.5,1.051,'Fractional Abundance of Cloud Types as a Function of Latitude \n (Full month, March, 2013)',ha='center', va='center',fontsize=16,color='red')
plt.tight_layout()
