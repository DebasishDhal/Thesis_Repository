#Input - 2B-CLDCLASS file of CloudSat. 
#Output - A map showing the groundtrack of the CLoudsat orbit. It also has options for many features like timestamps, coastline, directional arrows, base image etc.
#Example output can be seen here - https://github.com/DebasishDhal/Thesis_Repository/blob/main/cloudsatorbit/cloudsat_groundtrack_with_timestamps.png

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

#Python 3.10.1

def groundtrackplotter(pathorfile,c='r', timestamp=True, passedaxis=None, baseimage=True, text=None, s=0.51,linewidths=0.51,arrow=True,arrow_color='black',arrow_width=0.0001,arrow_head_width=5,arrow_head_length=5
,time_label=True, time_label_color='black',time_label_fontsize=10,rotation=80, time_label_count=3):
    if type(pathorfile)==str:
        h=HDF.HDF(pathorfile)
    else:
        h=pathorfile

    def oneddata(searchdatasetlist): #This is to extract 1-D data from the cloudsat file, like latitude and longitude. 2D data like CloudLayerTop and CloudLayerBase have a height component to them. Their extraction is different.
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

    longitude,latitude=oneddata(['Longitude','Latitude'])
    fig=plt.figure(figsize=(10,10))
    if passedaxis==None:
        ax=plt.axes(projection=ccrs.PlateCarree())
    else:
        ax=passedaxis
    ax.coastlines()
    if baseimage==True:
        ax.stock_img()
    ax.gridlines()
    ax.set_xticks(np.arange(-180, 180, 10), crs=ccrs.PlateCarree())
    ax.set_xticklabels(ax.get_xticks(), rotation=-90)
    ax.set_yticks(np.arange(-90, 90, 30), crs=ccrs.PlateCarree())
    ax.set_xlabel('Longitude',fontsize=15)

    ax.scatter(longitude,latitude,transform=ccrs.PlateCarree(),c=c,s=s,linewidths=linewidths)

    if arrow==True:
    #Put arrow at 2000th profile, given there are 36000 profiles
        ax.arrow(longitude[2000],latitude[2000],longitude[2000+5]-longitude[2000],latitude[2000+5]-latitude[2000],
        transform=ccrs.PlateCarree(),color=arrow_color,width=arrow_width,head_width=arrow_head_width,head_length=arrow_head_length)
    
    if time_label==True:
        #Put a time label along the track at #time_label_count uniform intervals
        start_time,differential_time=oneddata(['UTC_start','Profile_time'])
        start_time=start_time[0]
        #print(start_time)
        if timestamp==True:

            profile_time=[start_time+i for i in differential_time]
            profile_time_utc=[time.strftime('%H:%M:%S', time.gmtime(i)) for i in profile_time]
            step=int(len(profile_time_utc)/(time_label_count))
            for i in range(0,int(len(profile_time_utc)-step),step):
                #Put a black dot at the time label

                ax.scatter(longitude[i],latitude[i],transform=ccrs.PlateCarree(),color=time_label_color,s=10)
                ax.text(longitude[i]-6,latitude[i]-5,profile_time_utc[i],transform=ccrs.PlateCarree(),color=time_label_color,fontsize=time_label_fontsize,
                rotation=np.rad2deg(np.arctan((latitude[i+5]-latitude[i])/(longitude[i+5]-longitude[i]))))

            ax.scatter(longitude[-1],latitude[-1],transform=ccrs.PlateCarree(),color=time_label_color,s=10)
            ax.text(longitude[-1],latitude[-1],profile_time_utc[-1],transform=ccrs.PlateCarree(),color=time_label_color,fontsize=time_label_fontsize,
            rotation=np.rad2deg(np.arctan((latitude[-1-5]-latitude[-1])/(longitude[-1-5]-longitude[-1]))))
    if text != None:
        ax.text(longitude[0]+2,latitude[0]-4,text,transform=ccrs.PlateCarree(),color='black',fontsize=10,rotation=80)

    if passedaxis==None:
        plt.show()
        return
    else:
        return ax
  
#Example given below
fig=plt.figure(figsize=(10,10))
ax=plt.axes(projection=ccrs.PlateCarree())
# ax.scatter(0,0,transform=ccrs.PlateCarree(),c='r',s=10.51,linewidths=0.51)
ax=groundtrackplotter(path2,passedaxis=ax,time_label_count=5, text="Orbit")
