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

#This function takes a single 2B-CLDCLASS file, produces a dataframe containing the statistics of clouds for that particular file.
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

#Applying the function on all the files for a particular month, let's say March
import re
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013mar'
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


cloudtype_dict={1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective'}
cloudlabel=np.arange(1,9)
dfcopy = df.copy()



#Make a figure with 2 subplots. Plot the global mean cloud thickness, top height and bottom height in first subplot, and the same for the area of interest in the second subplot
fig, ax = plt.subplots(1, 2,figsize=(10,6))

ax[0].set_title('Over Global region, {} points'.format(len(df)))
#plt.figtext(0.3,1.001,'Over Global region',ha='center', va='center',fontsize=12)
ax[0].plot(df.groupby('type')['thickness'].mean(),label='Cloud mean thickness',color='red')
ax[0].plot(df.groupby('type')['top'].mean(),label='Cloud mean top height',color='blue')
ax[0].plot(df.groupby('type')['bottom'].mean(),label='Cloud mean bottom height',color='green')
ax[0].set_xlabel('Cloud Type',fontsize=13)
ax[0].set_ylabel('(in km)',fontsize=15)
#ax[0].set_xticks(cloudlabel,cloudtype_dict.values(),rotation=60);
#Put xticks with labels at the bottom of the plot
ax[0].set_xticks(cloudlabel,cloudtype_dict.values(),rotation=50)
ax[0].legend();

lon_left, lon_right, lat_bot, lat_top = 60, 100, 0, 40
dfcopy_aoi = dfcopy[(dfcopy['lon']>=lon_left) & (dfcopy['lon']<=lon_right) & (dfcopy['lat']>=lat_bot) & (dfcopy['lat']<=lat_top)]

# Get a list of all the unique types
types = df['type'].unique()

# Create a dataframe with the missing types and the desired values
dummy_df = pd.DataFrame({'type': [i for i in types if i not in dfcopy_aoi['type'].values],
                        'thickness': 0,
                        'top': 0,
                        'bottom': 0})

# Concatenate the dummy dataframe with the original dataframe
dfcopy_aoi = pd.concat([dfcopy_aoi, dummy_df], ignore_index=True)


ax[1].set_title('Over Indian subcontinent region, {} points'.format(len(dfcopy_aoi)))
ax[1].plot(dfcopy_aoi.groupby('type')['thickness'].mean(),label='Cloud mean thickness',color='red')
ax[1].plot(dfcopy_aoi.groupby('type')['top'].mean(),label='Cloud mean top height',color='blue')
ax[1].plot(dfcopy_aoi.groupby('type')['bottom'].mean(),label='Cloud mean bottom height',color='green')
ax[1].set_xlabel('Cloud Type',fontsize=13)
ax[1].set_ylabel('(in km)',fontsize=15)
ax[1].set_xticks(cloudlabel,cloudtype_dict.values(),rotation=50);
ax[1].legend();

for i in cloudlabel:
    ax[0].text(i,df.groupby('type')['thickness'].mean()[i],str(np.round(df.groupby('type')['thickness'].mean()[i],2)),ha='center',va='top')
for i in cloudlabel:
    try:
        ax[1].text(i,dfcopy_aoi.groupby('type')['thickness'].mean()[i],str(np.round(dfcopy_aoi.groupby('type')['thickness'].mean()[i],2)),ha='center',va='top')
    except KeyError:
        continue


for i in cloudlabel:
    ax[0].text(i,df.groupby('type')['top'].mean()[i],str(np.round(df.groupby('type')['top'].mean()[i],2)),ha='center',va='top')
for i in cloudlabel:
    try:
        ax[1].text(i,dfcopy_aoi.groupby('type')['top'].mean()[i],str(np.round(dfcopy_aoi.groupby('type')['top'].mean()[i],2)),ha='center',va='top')
    except KeyError:
        continue
y_lim=[0,0]
y_lim = [min(ax[0].get_ylim()[0], ax[1].get_ylim()[0]), max(ax[0].get_ylim()[1], ax[1].get_ylim()[1])]
for i in range(2):
    ax[i].set_ylim(y_lim)
ax[0].legend(loc='upper center');
ax[1].legend(loc='upper center');

#Add a title to the figure
fig.suptitle('Global and regional mean cloud thickness, top and bottom height \n (Full month, March, 2013) (Stratus absent Indian region)',fontsize=16,color='red')
plt.tight_layout()