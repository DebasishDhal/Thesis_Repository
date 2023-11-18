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
from datetime import datetime

def insatplotter(insatfileorpath, figsize=9, axis=None, baseimage=False, time_label=False, time_label_color='r', 
time_label_fontsize=12, parameter='bt',channel='tir1',s=0.1, label=None, ax=None, stock=False, colorbar=False, coasttchikness=0.5,globalmap=True):
    
    if type(insatfileorpath)==str:
        insatfile=h5py.File(insatfileorpath,'r')
    else:
        insatfile=insatfileorpath

    acq_start = str(insatfile.attrs['Acquisition_Start_Time'])[2:-1].replace('T','-') #To remove a T in the middle of string
    start_time_obj=datetime.strptime(acq_start, "%d-%b-%Y-%H:%M:%S")
    acq_end=str(insatfile.attrs['Acquisition_End_Time'])[2:-1].replace('T','-')
    end_time_obj=datetime.strptime(acq_end, "%d-%b-%Y-%H:%M:%S")
    acq_time=start_time_obj+(end_time_obj-start_time_obj)/2 #Taking average of start and end time
    
    vislat=np.ma.masked_equal(np.array(insatfile['Latitude_VIS']),32767)/1000 #Note how the scale is different for different channels
    vislon=np.ma.masked_equal(np.array(insatfile['Longitude_VIS']),32767)/1000
    wvlat=np.ma.masked_equal(np.array(insatfile['Latitude_WV']),32767)/100
    wvlon=np.ma.masked_equal(np.array(insatfile['Longitude_WV']),32767)/100
    tirlat=np.ma.masked_equal(np.array(insatfile['Latitude']),32767)/100
    tirlon=np.ma.masked_equal(np.array(insatfile['Longitude']),32767)/100

    viscount=np.ma.masked_equal(np.array(insatfile['IMG_VIS'][0]),0)
    swircount=np.ma.masked_equal(np.array(insatfile['IMG_SWIR'][0]),0)
    mircount=np.ma.masked_equal(np.array(insatfile['IMG_MIR'][0]),1023)
    wvcount=np.ma.masked_equal(np.array(insatfile['IMG_WV'][0]),1023)
    tir1count=np.ma.masked_equal(np.array(insatfile['IMG_TIR1'][0]),1023)
    tir2count=np.ma.masked_equal(np.array(insatfile['IMG_TIR2'][0]),1023)

    visalbedolut=np.array(insatfile['IMG_VIS_ALBEDO'])
    visradlut=np.array(insatfile['IMG_VIS_RADIANCE'])
    swirradlut=np.array(insatfile['IMG_SWIR_RADIANCE'])
    mirradlut=np.array(insatfile['IMG_MIR_RADIANCE'])
    mirtemplut=np.array(insatfile['IMG_MIR_TEMP'])
    wvradlut=np.array(insatfile['IMG_WV_RADIANCE'])
    wvtemplut=np.array(insatfile['IMG_WV_TEMP'])
    tir1radlut=np.array(insatfile['IMG_TIR1_RADIANCE'])
    tir1templut=np.array(insatfile['IMG_TIR1_TEMP'])
    tir2radlut=np.array(insatfile['IMG_TIR2_RADIANCE'])
    tir2templut=np.array(insatfile['IMG_TIR2_TEMP'])

    def counttodata(count,lut): #This function converts the count to data, data can be radiance, albedo, temperature. 
        return lut[count]


    if parameter=='bt' or parameter=='temperature' or parameter=='temp':
        if channel=='vis':
            raise ValueError('VIS channel does not have BT')
        elif channel=='swir':
            raise ValueError('SWIR channel does not have BT')
        elif channel=='mir':
            plotarray=counttodata(mircount,mirtemplut)
#            plotarray=mirtemplut[mircount]
        elif channel=='tir1':
            plotarray=counttodata(tir1count,tir1templut)
#            plotarray=tir1templut[tir1count]
        elif channel=='tir2':
            plotarray=counttodata(tir2count,tir2templut)
#            plotarray=tir2templut[tir2count]
        elif channel=='wv':
            plotarray=counttodata(wvcount,wvtemplut)
#            plotarray=wvtemplut[wvcount]
        else:
            raise ValueError('Channel not found')

    if parameter=='rad' or parameter=='radiance':
        if channel=='vis':
            plotarray=counttodata(viscount,visradlut)
#            plotarray=visradlut[viscount]
        elif channel=='swir':
            plotarray=counttodata(swircount,swirradlut)
#            plotarray=swirradlut[swircount]
        elif channel=='mir':
            plotarray=counttodata(mircount,mirradlut)
#            plotarray=mirradlut[mircount]
        elif channel=='tir1':
            plotarray=counttodata(tir1count,tir1radlut)
#            plotarray=tir1radlut[tir1count]
        elif channel=='tir2':
            plotarray=counttodata(tir2count,tir2radlut)
#            plotarray=tir2radlut[tir2count]
        elif channel=='wv':
            plotarray=counttodata(wvcount,wvradlut)
#            plotarray=wvradlut[wvcount]
        else:
            raise ValueError('Channel not found')
    
    if  parameter=='albedo' or parameter=='alb':
        if channel=='vis':
            plotarray=counttodata(viscount,visalbedolut)
#            plotarray=visalbedolut[viscount]
        else:
            raise ValueError('Albedo is only for VIS channel')
    
    if parameter=='count':
        if channel=='vis':
            plotarray=viscount
        elif channel=='swir':
            plotarray=swircount
        elif channel=='mir':
            plotarray=mircount
        elif channel=='wv':
            plotarray=wvcount
        elif channel=='tir1':
            plotarray=tir1count
        elif channel== 'tir2':
            plotarray=tir2count
        else:
            raise ValueError("Channel not found")


    
    if channel=='vis' or channel=='swir':
        lat=vislat
        lon=vislon
    elif channel=='wv':
        lat=wvlat
        lon=wvlon
    elif channel=='mir' or channel=='tir1' or channel=='tir2':
        lat=tirlat
        lon=tirlon

    if channel=='vis':
        name='IMG_VIS'
    elif channel=='swir':
        name='IMG_SWIR'
    elif channel=='mir':
        name='IMG_MIR'
    elif channel=='wv':
        name='IMG_WV'
    elif channel=='tir1':
        name='IMG_TIR1'
    elif channel=='tir2':
        name='IMG_TIR2'
    
    wavelength=round(float(insatfile[name].attrs['central_wavelength']),2)
    band=round(float(insatfile[name].attrs['bandwidth']),2)
    interval=str(round(wavelength-band/2,2))+'-'+str(round(wavelength+band/2,2))+' µm'

    if axis==None:
        fig=plt.figure(figsize=(figsize,figsize))
        
        ax=plt.axes(projection=ccrs.PlateCarree())
        if globalmap:
            ax.set_global()
        ax.gridlines()
        ax.set_xticks(np.arange(-180, 180, 10), crs=ccrs.PlateCarree())
        ax.set_xticklabels(ax.get_xticks(), rotation=-90)
        ax.set_yticks(np.arange(-90, 90, 30), crs=ccrs.PlateCarree())
        ax.set_xlabel('Longitude',fontsize=15)
        ax.set_ylabel('Latitude',fontsize=15)
#        ax.scatter(lon,lat,c=plotarray,transform=ccrs.PlateCarree(),s=s,label=label)
        scatterplot=ax.scatter(lon,lat,c=plotarray,transform=ccrs.PlateCarree(),s=s,label=label, cmap='jet')
        #ax.coastlines(color='black',linewidth=coasttchikness,linestyle='solid')
        ax.add_feature(cfeature.NaturalEarthFeature(category='cultural',scale='10m',name='admin_0_countries',edgecolor='black',facecolor='none',linewidth=coasttchikness))
        if stock:
            ax.stock_img()
        ax.set_title(channel.upper()+'-'+str(parameter.upper())+' Acq. time - Date='+str(acq_time.strftime('%d-%b-%Y'))+str(' Time=')+str(acq_time.strftime('%H:%M:%S'))+'(UTC) \n Time interval- ' +str(start_time_obj.strftime('%H:%M:%S'))+'- '+str(end_time_obj.strftime('%H:%M:%S'))+'\n Cenral wavelength-'+str(wavelength)+'µm, Channel range-'+str(interval),color='r')
        cbar=plt.colorbar(scatterplot, ax=ax, pad=0.01, shrink=0.9, aspect=20)
        if parameter=='albedo' or parameter=='alb':
            text='Visible albedo (%)'
        elif parameter=='bt' or parameter=='temperature' or parameter=='temp':
            text='Brightness temp. (K)'
        elif parameter=='rad' or parameter=='radiance':
            text='Radiance (mW. $cm^{-2}.sr^{-1}.\mu^{-1} $)'
        cbar.set_label(text,fontsize=15, rotation=270, labelpad=14)
        plt.show()
        return 
    #Make channel string all caps

    if axis!=None:
        ax=axis
        ax.gridlines()
        ax.set_xticks(np.arange(-180, 180, 10), crs=ccrs.PlateCarree())
        ax.set_xticklabels(ax.get_xticks(), rotation=-90)
        ax.set_yticks(np.arange(-90, 90, 30), crs=ccrs.PlateCarree())
        ax.set_xlabel('Longitude',fontsize=15)
        ax.set_ylabel('Latitude',fontsize=15)

        scatterplot=ax.scatter(lon,lat,c=plotarray,transform=ccrs.PlateCarree(),s=s,label=label,cmap='jet')
        ax.add_feature(cfeature.NaturalEarthFeature(category='cultural',scale='10m',name='admin_0_countries',edgecolor='black',facecolor='none',linewidth=coasttchikness))
        ax.set_title(channel.upper()+'-'+str(parameter.upper())+' Acq. time - Date='+str(acq_time.strftime('%d-%b-%Y'))+str(' Time=')+str(acq_time.strftime('%H:%M:%S'))+'(UTC) \n Time interval- ' +str(start_time_obj.strftime('%H:%M:%S'))+' - '+str(end_time_obj.strftime('%H:%M:%S'))+'\n Central wavelength-'+str(wavelength)+'µm, Channel range-'+str(interval),color='r')
        cbar=plt.colorbar(scatterplot, ax=axis, pad=0.01, shrink=0.805, aspect=20)
        if parameter=='albedo' or parameter=='alb':
            text='Visible albedo (%)'
        elif parameter=='bt' or parameter=='temperature' or parameter=='temp':
            text='Brightness temp. (K)'
        elif parameter=='rad' or parameter=='radiance':
            text='Radiance (mW. $cm^{-2}.sr^{-1}.\mu^{-1} $)'
        cbar.set_label(text,fontsize=15, rotation=270, labelpad=14)
 
        return ax

#Plot for all the channels in a file
insatpath=r'/home/debasish/database/HD5collection/L1B data/INSAT-3DR/2019 Jan/3RIMG_01JAN2019_0515_L1B_STD_V01R00.h5' #We'll plot data if all the channels in this file.
#Output is here - https://github.com/DebasishDhal/Thesis_Repository/blob/main/miscellaneous/images/Allchannelsplot.png

fig=plt.figure(figsize=(15,22))
ax1=plt.subplot(3,2,1,projection=ccrs.PlateCarree())
ax2=plt.subplot(3,2,2,projection=ccrs.PlateCarree())
ax3=plt.subplot(3,2,3,projection=ccrs.PlateCarree())
ax4=plt.subplot(3,2,4,projection=ccrs.PlateCarree())
ax5=plt.subplot(3,2,5,projection=ccrs.PlateCarree())
ax6=plt.subplot(3,2,6,projection=ccrs.PlateCarree())

insatplotter(insatpath,channel='vis',parameter='albedo',stock=False,globalmap=False,axis=ax1,figsize=6)
insatplotter(insatpath,channel='swir',parameter='rad',stock=False,globalmap=False,axis=ax2,figsize=6)
insatplotter(insatpath,channel='mir',parameter='temp',stock=False,globalmap=False,axis=ax3,figsize=6)
insatplotter(insatpath,channel='wv',parameter='temp',stock=False,globalmap=False,axis=ax4,figsize=6)
insatplotter(insatpath,channel='tir1',parameter='temp',stock=False,globalmap=False,axis=ax5,figsize=6)
insatplotter(insatpath,channel='tir2',parameter='temp',stock=False,globalmap=False,axis=ax6,figsize=6)
plt.show()
