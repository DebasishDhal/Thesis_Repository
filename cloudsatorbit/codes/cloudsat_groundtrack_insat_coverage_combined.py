#Input - One cloudsat file, and one insat-3dr file. Everything else like timestamps and datetimes are automated.
#Output - Combined maps of cloudsat groundtrack and insat-3dr coverage area.
#Example output - https://github.com/DebasishDhal/Thesis_Repository/blob/main/cloudsatorbit/Actual%20photo%20used%20in%20collocation%20INSAT%20cloudsat%20combined.png

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
import datetime
import time
import geopy.distance
import os
import sys
import geopy

print("All imports successful")

insatfilepath = r'/data/debasish/insatdata/l1b/2017/mar2017/day01/3RIMG_01MAR2017_0445_L1B_STD_V01R00.h5' #Example
csatfilepath= r'/data/debasish/cloudsatdata/cldclasslidar/2017/2017mar/day01/2017060041204_57670_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E06_F01.hdf' #Example

def groundtrackplotter(pathorfile,c='r', timestamp=True, passedaxis=None, baseimage=True, text=None, s=0.51,linewidths=0.51,arrow=True,arrow_color='black',arrow_width=0.0001,arrow_head_width=5,arrow_head_length=5
,time_label=True, time_label_color='black',time_label_fontsize=10,rotation=80, time_label_count=3):
    if type(pathorfile)==str:
        h=HDF.HDF(pathorfile)
    else:
        h=pathorfile

    def oneddata(searchdatasetlist):
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

    if passedaxis==None:
        ax=plt.axes(projection=ccrs.PlateCarree())
    else:
        ax=passedaxis
    ax.coastlines()
    if baseimage==True:
        ax.stock_img()
        
    #Make gridlines color black
    ax.gridlines(color='black', alpha=0.5, linestyle='--')
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
            profile_time_utc=[time.strftime('%H:%M', time.gmtime(i)) for i in profile_time]
            step=int(len(profile_time_utc)/(time_label_count))
            for i in range(0,int(len(profile_time_utc)-step),step):
                #Put a black dot at the time label

                ax.scatter(longitude[i],latitude[i],transform=ccrs.PlateCarree(),color=time_label_color,s=10)
                ax.text(longitude[i]-6,latitude[i]-1,profile_time_utc[i],transform=ccrs.PlateCarree(),color=time_label_color,fontsize=time_label_fontsize,
                rotation=np.rad2deg(np.arctan((latitude[i+5]-latitude[i])/(longitude[i+5]-longitude[i]))))

            #ax.scatter(longitude[-1],latitude[-1],transform=ccrs.PlateCarree(),color=time_label_color,s=10)
            ax.text(longitude[-1],latitude[-1],profile_time_utc[-1],transform=ccrs.PlateCarree(),color=time_label_color,fontsize=time_label_fontsize,
            rotation=np.rad2deg(np.arctan((latitude[-1-5]-latitude[-1])/(longitude[-1-5]-longitude[-1]))))
    #Get the data about date and time of the file from the filename

    filename=csatfilepath.split('/')[-1]
    year=(filename[0:4])
    daynumber=(filename[4:7])
    daynumber = int(daynumber.lstrip('0'))
    hour=filename[7:9]
    minute=filename[9:11]
    second=filename[11:13]
    #Get month and day from daynumber and year from existing library

    month = datetime.date.fromordinal(datetime.date(int(year), 1, 1).toordinal() + daynumber - 1).strftime('%b')
    day = datetime.date.fromordinal(datetime.date(int(year), 1, 1).toordinal() + daynumber - 1).strftime('%d')
    if text == None:
        text = ''

    #Put the text at upper left corner
    ax.text(-153,86,text+str(day)+"/"+month+"/"+str(year) +"\n Orbit Start Time:\n "+hour+":"+minute+":"+second,transform=ccrs.PlateCarree(),color='red',fontsize=8,horizontalalignment='center',verticalalignment='top',backgroundcolor='white',bbox=dict(facecolor='white', edgecolor='blue', pad=5.0))

    if passedaxis==None:
        plt.show()
        return
    else:
        return ax

#Make a blank axis, scatter INSAT data, then plot CSat data on top of it

fig=plt.figure(figsize=(10,10)) #The logic is, we create a fig and axis first. Plot the INSAT-3DR coverage in it first, then pass it to the cloudsat groundtrackplotter function.
ax=plt.axes(projection=ccrs.PlateCarree())

#Just plotting the latitude and longitude of INSAT data. If required, some parameter like brightness temperature can be plotted for INSAT-3DR with 2-3 more lines of code.
insatfile=h5py.File(insatfilepath,'r')
latitudewv=np.ma.masked_equal(np.array(insatfile['Latitude_WV']),32767)/100
longitudewv=np.ma.masked_equal(np.array(insatfile['Longitude_WV']),32767)/100

ax.scatter(longitudewv,latitudewv,transform=ccrs.PlateCarree(),c='b',s=0.1,label='INSAT-3DR')
acq_start = str(insatfile.attrs['Acquisition_Start_Time'])[2:-1].replace('T','-') #To remove a T in the middle of string
start_time_obj=datetime.datetime.strptime(acq_start, "%d-%b-%Y-%H:%M:%S")
acq_end=str(insatfile.attrs['Acquisition_End_Time'])[2:-1].replace('T','-')
end_time_obj=datetime.datetime.strptime(acq_end, "%d-%b-%Y-%H:%M:%S")

#Get only date from the datetime object in the format of day/month/year
acq_date=start_time_obj.strftime("%d/%b/%Y")

#Put a title on the plot
plt.title('INSAT-3DR acquisition - '+acq_date+'\n Acquisition time (GMT)->'+start_time_obj.strftime("%H:%M:%S")+'-'+end_time_obj.strftime("%H:%M:%S"),fontsize=15,c='b')

ax=groundtrackplotter(csatfilepath,passedaxis=ax,time_label_count=8,time_label_color='black', time_label_fontsize=15,text="Cloudsat \n groundtrack \n ") 

plt.show()
