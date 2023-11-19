import os
import pandas as pd
import numpy as np
import h5py
import time 
import pytz
import datetime
from pytz import timezone 
#SWIR retrieval for one whole day.
#Done

filesavingadress = r'/data/debasish/transferfiles/2017swirincluded/2017feb/day02'
def swiraddersinglefile(collocationfileadress, insatfolderadress):
    starttic = time.time()
    assert os.path.exists(collocationfileadress), "Collocation file does not exist"
    assert os.path.exists(insatfolderadress), "Insat folder does not exist"

    #Get full name of the col file from the adress
    colfilenamewithextension = collocationfileadress.split('/')[-1]

    insatfolderadress = insatfolderadress
    os.listdir(insatfolderadress)
    #Sort the files in ascending order
    insatfilescollection = sorted(os.listdir(insatfolderadress))

    #Extract which INSAT file is needed for the task

    colfilenoswiradress = collocationfileadress
    dateandtime = colfilenoswiradress.split('/')[-1].split('_')[0]
    #Delete col from dateandtime string
    dateandtime = dateandtime[3:] #To get 02JAN20170415
    dateandtime = dateandtime[0:9]+'_'+dateandtime[9:] #To get 02JAN2017_0445
    currentfiledateandtime = dateandtime
    print(" Collocated file date-time: ",currentfiledateandtime)
    matchedinsatadress = None #Assume that you won't find the file
    for i in range(len(insatfilescollection)):
        if currentfiledateandtime in insatfilescollection[i]:
            
            print(' INSAT file which was used: ',insatfilescollection[i])
            matchedinsatadress = insatfolderadress+'/'+insatfilescollection[i]
            break
    try:
        insatfile = h5py.File(matchedinsatadress,'r')
    except:
        matchedinsatadress = None
        print(' The INSAT file for col_file {} is not present in the list, check the date of INSAT folder'.format(currentfiledateandtime))
        return None
    
    #Prepare the INAST file for the task
    vislatitude = np.ma.masked_equal(insatfile["Latitude_VIS"],327670)/1000
    vislongitude = np.ma.masked_equal(insatfile["Longitude_VIS"],327670)/1000
    swir_img_arr = np.array(insatfile["IMG_SWIR"][0,:,:])
    swir_img_arr_fill = insatfile["IMG_SWIR"].attrs["_FillValue"][0]
    nan_mask = (swir_img_arr == swir_img_arr_fill)
    swir_rad_lut = np.array(insatfile["IMG_SWIR_RADIANCE"])
    
    def count2rad(count):
        return swir_rad_lut[count]
    swir_rad_arr = count2rad(swir_img_arr)
    swir_rad_arr[nan_mask] = np.nan

    #Extract SWIR radiance values for the collocation points
    swirradlist = []
    df = pd.read_csv(colfilenoswiradress)
    print(" Intial Length of collocation file = ",len(df))
    #Separate the latitude and longitude from the insatcorvis column and put it in two new columns
    df['insatcorvislat'] = df['insatcorvis'].apply(lambda x: x.split(',')[0])
    df['insatcorvislat'] = df['insatcorvislat'].apply(lambda x: x.split('(')[1]).astype(float)

    df['insatcorvislon'] = df['insatcorvis'].apply(lambda x: x.split(',')[1])
    df['insatcorvislon'] = df['insatcorvislon'].apply(lambda x: x.split(')')[0]).astype(float)

    for i in range(len(df)):
        lat = df['insatcorvislat'][i]
        lon = df['insatcorvislon'][i]
        #Find the index of the lat and lon in the insat file
        indices = np.argwhere((vislatitude == lat) & (vislongitude == lon))
        x_index = indices[0][0]
        y_index = indices[0][1]
        swirradlist.append(swir_rad_arr[x_index][y_index])
        print(i, end='\r')
    
    #Add the swir radiance values to the collocation file
    df['swirrad'] = swirradlist
    df['cloudyornot'] = df['thickness'].apply(lambda x: 1 if x>0 else 0)
    df['date'] = currentfiledateandtime.split('_')[0]
    df['time'] = currentfiledateandtime.split('_')[1]
    df.dropna(subset=['bttir1', 'bttir2', 'albedo', 'swirrad', 'thickness', 'cloudyornot', 'solarelevation'])

    #Save the collocation file with the swir radiance values
    colfilenamewithextension = colfilenamewithextension.replace('col','swr')
    df.to_csv(filesavingadress+'/'+colfilenamewithextension)
    print(' The collocation file with the swir radiance values is saved at: ',filesavingadress+'/'+colfilenamewithextension)
    print(' Final Length of the collocation file is: ',len(df))
    endtoc = time.time()
    print(' The time taken for this file is: ',endtoc-starttic)
    print()

#collocationfileadress = r'/data/debasish/collocations/2017/2017jan/day01/col01JAN20170345_56810.csv'

rootstart = time.time()
print("Program start (IST) = ",datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%d-%b-%Y %H:%M:%S.%f'))
#swiraddersinglefile(collocationfileadress, insatfolderadress)

insatfolderadress = r'/data/debasish/insatdata/l1b/2017/feb2017/day02'
onedaycollocationfolder = r'/data/debasish/collocations/2017/2017feb/day02'
#Sort all the collocation files in the folder
onedaycollocationfoldercollection = sorted(os.listdir(onedaycollocationfolder))

#Apply the function to all the collocation files in the folder
for i in range(len(onedaycollocationfoldercollection)):
    collocationfileadress = onedaycollocationfolder+'/'+onedaycollocationfoldercollection[i]
    swiraddersinglefile(collocationfileadress, insatfolderadress)

rootend = time.time()
hours_taken = int((rootend-rootstart)/3600)
minutes_taken = int(((rootend-rootstart)-hours_taken*3600)/60)
seconds_taken = (rootend-rootstart)-hours_taken*3600-minutes_taken*60

print("Program end (IST) = ",datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%d-%b-%Y %H:%M:%S.%f'))
print('The total time taken for the task is: ',hours_taken,' h',minutes_taken,' min ',seconds_taken,' sec')