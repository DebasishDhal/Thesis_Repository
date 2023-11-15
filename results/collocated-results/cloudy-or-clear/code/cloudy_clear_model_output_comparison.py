#This function takes one INSAT-3DR L1B file, and its corresnponding cloud mask file produced by IMD. The output is a comparison of output of both the models.
#This is to compare the cloudy/clear map produced by our model with the cloudy/clear map provided by Indian Meteorological Department. Many such outputs have been shown the the cloudy-or-clear folder.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import h5py
import pickle
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
import datetime
from cartopy.feature.nightshade import Nightshade
import matplotlib.colors as mcolors
cmap = mcolors.ListedColormap(['gray', 'white'])

def model_mosdac_combined_plotter(insatfilepath,cmkfilepath, extent = -1): #extent is to check the number of points you want to plot. It has some 6M points in total, starting from Northern part of Russia.

    os.path.exists(insatfilepath), "INSAT-1B file does not exist"
    os.path.exists(cmkfilepath), "CMK file does not exist"

    #File reading
    insatfile = h5py.File(insatfilepath,'r')
    cmkfile = h5py.File(cmkfilepath,'r')
    
    longitudearray = np.array(insatfile['Longitude'])/100
    latitudearray = np.array(insatfile['Latitude'])/100
    fillvalue = insatfile['Longitude'].attrs['_FillValue'][0]/100
    latitudearray[latitudearray == fillvalue] = np.nan
    longitudearray[longitudearray == fillvalue] = np.nan

    insatdate = str(insatfile.attrs['Acquisition_Date'])[2:-1]
    insattime = str(insatfile.attrs['Acquisition_Time_in_GMT'])[2:-1]
    acqstart = str(insatfile.attrs['Acquisition_Start_Time'])[2:-1].split('T')[1]
    acqend = str(insatfile.attrs['Acquisition_End_Time'])[2:-1].split('T')[1]

    def count2bt(count,lut): #To convert counts to brightness temperature using look up table.
        bt = lut[count]
        return bt

    tir1count = np.array(insatfile['IMG_TIR1'])[0,:,:]
    fillvalue = insatfile['IMG_TIR1'].attrs['_FillValue'][0]
    tir1lut = np.array(insatfile['IMG_TIR1_TEMP'])
    tir1bt = count2bt(tir1count,tir1lut)
    tir1bt[tir1count == fillvalue] = np.nan

    tir2count = np.array(insatfile['IMG_TIR2'])[0,:,:]
    fillvalue = insatfile['IMG_TIR2'].attrs['_FillValue'][0]
    tir2lut = np.array(insatfile['IMG_TIR2_TEMP'])
    tir2bt = count2bt(tir2count,tir2lut)
    tir2bt[tir2count == fillvalue] = np.nan

    mircount = np.array(insatfile['IMG_MIR'])[0,:,:]
    fillvalue = insatfile['IMG_MIR'].attrs['_FillValue'][0]
    mirlut = np.array(insatfile['IMG_MIR_TEMP'])
    mirbt = count2bt(mircount,mirlut)
    mirbt[mircount == fillvalue] = np.nan

    swircount = np.array(insatfile['IMG_SWIR'])[0,:,:]
    fillvalue = insatfile['IMG_SWIR'].attrs['_FillValue'][0]
    swirlut = np.array(insatfile['IMG_SWIR_RADIANCE'])
    swirrad = count2bt(swircount,swirlut)
    swirrad[swircount == fillvalue] = np.nan

    viscount = np.array(insatfile['IMG_VIS'])[0,:,:]
    fillvalue = insatfile['IMG_VIS'].attrs['_FillValue'][0]
    vislut = np.array(insatfile['IMG_VIS_ALBEDO'])
    visalbedo = count2bt(viscount,vislut)
    visalbedo[viscount == fillvalue] = np.nan

    solarelevationarray = np.array(insatfile['Sun_Elevation'])[0,:,:]
    solarelevationarray = solarelevationarray/100
    fillvalue = insatfile['Sun_Elevation'].attrs['_FillValue'][0]/100
    solarelevationarray[solarelevationarray == fillvalue] = np.nan

    satelevationarray = np.array(insatfile['Sat_Elevation'])[0,:,:]
    satelevationarray = satelevationarray/100
    fillvalue = insatfile['Sat_Elevation'].attrs['_FillValue'][0]/100
    satelevationarray[satelevationarray == fillvalue] = np.nan
    print("File read successfully")

    swirraddown = swirrad[::4,::4] #Downscaling SWIR and VIS files by a fourth. These files (with resolution of 1 km) are exactly 4 × 4 of the size of TIR1, TIR2 and MIR files (res. = 4 km). 
    albedodown = visalbedo[::4,::4]

    print("Data being prepared for prediction")

    #Preparing the dataframe for prediction using our models.
    dffullfile = pd.DataFrame({'albedo':albedodown.flatten(),'swirrad':swirraddown.flatten(),
                           'btmir':mirbt.flatten(),'bttir1':tir1bt.flatten(),'bttir2':tir2bt.flatten(),
                           'solarelevation':solarelevationarray.flatten(),'satelevation':satelevationarray.flatten(),
                           'longitude':longitudearray.flatten(),'latitude':latitudearray.flatten()})

    dffullfile.dropna(inplace=True)
    dfday = dffullfile[dffullfile['solarelevation'] > 0] #This is because we've separate models for day and night time. Since, at night time, visible and swir channels don't work.
    dfnight = dffullfile[dffullfile['solarelevation'] <= 0]

    dfdayfinal = dfday[['albedo','swirrad','btmir','bttir1','bttir2','solarelevation']]
    dfnightfinal = dfnight[['btmir','bttir1','bttir2','satelevation']]

    print("Data prepared for prediction, predicting now")
  
    scaleradress = r'/data/debasish/cloudetectionmodels/cloudyornomodel/rfmodels/y79acc8d2msl5mss150est/trainscaler.pkl' #Loading our daytime cloudy/clear classification model and its scaler
    modeladress = r'/data/debasish/cloudetectionmodels/cloudyornomodel/rfmodels/y79acc8d2msl5mss150est/randomforestclassifier.pkl'
 
    import joblib
    import pickle

    scaler = joblib.load(scaleradress)
    model = joblib.load(modeladress)

    dfdayscaled = scaler.transform(dfdayfinal)
    dayprediction = model.predict(dfdayscaled)

    scaleradress = r'/data/debasish/cloudetectionmodels/cloudyornomodel/rfmodels/ironlywithsatelevation/trainscaler.pkl' #Loading our nighttime cloudy/clear classification model and its scaler
    modeladress = r'/data/debasish/cloudetectionmodels/cloudyornomodel/rfmodels/ironlywithsatelevation/randomforestclassifier.pkl'

    scaler = joblib.load(scaleradress)
    model = joblib.load(modeladress)

    dfnightscaled = scaler.transform(dfnightfinal)
    nightprediction = model.predict(dfnightscaled)

    print("Prediction done")


    dfday['prediction'] = list(dayprediction)
    dfnight['prediction'] = list(nightprediction)
    dfday['oldindex'] = dfday.index
    dfnight['oldindex'] = dfnight.index
    dfpredictioncombined = pd.concat([dfday,dfnight])
    dfpredictioncombined.sort_values(by=['oldindex'],inplace=True)
    print("Predicted dataframe shape is {}".format(dfpredictioncombined.shape))
    cmap = mcolors.ListedColormap(['gray', 'white'])

    #Below section is for datetime.

    year_insat  = int(insatdate[-4:])
    month_abbreviation_insat = insatdate[2:5]
    month_number_insat = datetime.datetime.strptime(month_abbreviation_insat, '%b').month
    day_insat   = int(insatdate[0:2])
    hour_insat  = int(insattime[:2])
    minute_insat = int(insattime[2:4])
    insatdate = str(day_insat)+'/'+month_abbreviation_insat+'/'+str(year_insat)
    acqstart = str(insatfile.attrs['Acquisition_Start_Time'])[2:-1].split('T')[1]
    acqend = str(insatfile.attrs['Acquisition_End_Time'])[2:-1].split('T')[1]
    date = datetime.datetime(year_insat,month_number_insat,day_insat,hour_insat,minute_insat,second=0)


    insatdate_cmk = cmkfile.attrs['Acquisition_Date'].decode('utf-8')
    insatstarttime_cmk = cmkfile.attrs['Acquisition_Start_Time'].decode('utf-8')
    insatendtime_cmk = cmkfile.attrs['Acquisition_End_Time'].decode('utf-8')
    acqstart_cmk = insatstarttime_cmk.split('T')[1]
    acqend_cmk = insatendtime_cmk.split('T')[1]
    year_cmk = int(insatdate_cmk[-4:])
    month_abbreviation_cmk = insatdate_cmk[2:5]
    month_number_cmk = datetime.datetime.strptime(month_abbreviation_cmk, "%b").month
    day_cmk = int(insatdate_cmk[:2])
    hour_cmk = int(acqstart_cmk[:2])
    minute_cmk = int(acqstart_cmk[3:5])
    second_cmk = int(acqstart_cmk[-2:])
    date_cmk = datetime.datetime(year_cmk,month_number_cmk,day_cmk,hour_cmk,minute_cmk,second_cmk)

    assert date_cmk.date() == date.date(), "CMK and INSAT-3DR data are not from the same date"
    assert abs(date_cmk-date) <= datetime.timedelta(minutes = 35), "CMK and INSAT-3DR data are not from the same time"

    print("Plotting")

    fig = plt.figure(figsize=(10,15),dpi=300)
    
    ax1 = plt.subplot(2,1,1,projection = ccrs.PlateCarree())
    ax2 = plt.subplot(2,1,2,projection = ccrs.PlateCarree())

    cmap = mcolors.ListedColormap(['gray', 'white'])
    #Plotting
    plot1 = ax1.scatter(
                    dfpredictioncombined['longitude'][0:extent].values ,
                    dfpredictioncombined['latitude'][0:extent].values ,
                    c = dfpredictioncombined['prediction'][0:extent] ,
                    cmap=cmap ,
                    #norm=matplotlib.colors.Normalize(vmin=0, vmax=1) ,
                    transform=ccrs.PlateCarree(),s=0.01
                    )

    ax1.set_global()
    gl = ax1.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.right_labels = False
    ax1.set_extent([-10,160,-85,85], crs=ccrs.PlateCarree())

    ax1.add_feature(Nightshade(date, alpha=0.5))

    cbar1 = plt.colorbar(plot1, orientation='vertical', pad=0.035, fraction=0.019, aspect=50,ticks=[0, 1],ax=ax1)
    cbar1.set_label('Clear=0                                                       Cloudy=1', fontsize=16)

    cloudytoclearratioinsat = len(dfpredictioncombined[dfpredictioncombined['prediction'] == 1])/len(dfpredictioncombined[dfpredictioncombined['prediction'] == 0])
    ax1.coastlines(color = 'red')
    ax1.set_title('Cloudy/Clear prediction from our {} model \n Date: {},Acquisition time: {}-{} (GMT) \n Cloudy pixels/Clear pixels ratio={:.3f}'.format(type(model).__name__,insatdate,acqstart,acqend,cloudytoclearratioinsat))


    cmk = np.array(cmkfile['CMK'],dtype=np.float32)[0,:,:]
    cmkfill = cmkfile['CMK'].attrs['_FillValue'][0]
    cmk[cmk == cmkfill] = np.nan
    cmk [cmk==2] = 0
    cmk [cmk==3] = 1
    cmklat = np.array(cmkfile['Latitude'])/100
    cmklon = np.array(cmkfile['Longitude'])/100
    cmklatfill = cmkfile['Latitude'].attrs['_FillValue'][0]/100
    cmklat [cmklat == cmklatfill] = np.nan
    cmklon [cmklon == cmklatfill] = np.nan

    
    plot2 = ax2.scatter(
                   cmklon.flatten()[0:extent], cmklat.flatten()[0:extent] ,
                   c=cmk.flatten()[0:extent], cmap=cmap,#, norm=norm ,
                   transform=ccrs.PlateCarree(), s=0.01
                    )

    ax2.set_global()
    gl = ax2.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.right_labels = False
    ax2.set_extent([-10,160,-85,85], crs=ccrs.PlateCarree())
    ax2.coastlines(color = 'red')
    cbar2 = plt.colorbar(plot2, orientation='vertical', pad=0.035, fraction=0.019, aspect=50,ticks=[0, 1],ax=ax2)
    cbar2.set_label('0-Clear/Likely Clear                   1 - Cloudy/Likely Cloudy', fontsize=16)    
    #Rotate the tick labels
    cloudytoclearratiocmk = len(cmk[cmk==1])/len(cmk[cmk==0])
    #Figure title
    ax2.set_title('IMD Cloud Mask using MIR, TIR1, TIR2 channels \n Date: {},Acquisition time: {}-{} (GMT) \n Cloudy pixels/Clear pixels ratio={:.3f}'.format(insatdate_cmk,
                                                                                                                                                                    acqstart_cmk,
                                                                                                                                                                    acqend_cmk,
                                                                                                                                                                    cloudytoclearratiocmk))


    fig.tight_layout()

    plt.show()
    return cloudytoclearratioinsat,cloudytoclearratiocmk

#An example has been given below. Notice that the datetime of both the files should excatly be the same, otherwise it's meaningless.
model_mosdac_combined_plotter(r'/data/debasish/insatdata/l1b/2019/dec2019_day1_std/3RIMG_01DEC2019_2345_L1B_STD_V01R00.h5',
                              r'/data/debasish/insatdata/2019_insat_cmk/dec2019_day1_cmk/3RIMG_01DEC2019_2345_L2B_CMK_V01R00.h5',
                              extent = -1);
