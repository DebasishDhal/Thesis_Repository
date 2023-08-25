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
from time import gmtime, strftime
import datetime
import time
import geopy.distance
import sys
from pytz import timezone 
import time

#Done

csatdayfolder = r"/data/debasish/cloudsatdata/cldclasslidar/2017/2017jan/001"
insatdayfolderpath = r"/data/debasish/insatdata/2017_insat_cmk/01_jan2017_cmk/jan01"
saving_folder = r"/data/debasish/cmkcollocationfiles/2017_01_jan"

assert os.path.exists(saving_folder), "Saving_folder doesn't exist lol"

def insatcmkcsatcollocation(insatfilepath, csatfilepath):
    singlefilestart = time.time()
    csatfile=SD(csatfilepath, SDC.READ)
    h=HDF.HDF(csatfilepath)
    csatorbitnumber = int(csatfilepath.split('/')[-1].split('_')[1])

    #Reading cloudlayer, geogrphical parameters
    geofieldsearch=['Latitude','Longitude','DEM_elevation','Profile_time','Navigation_land_sea_flag','UTC_start']
    oneddatasearch=['Cloudlayer']

    geodatasetlist=[]
    oneddatasetlist=[]
    for i in geofieldsearch:
        vs=h.vstart()
        xid=vs.find(i)
        dataid=vs.attach(xid)
        dataid.setfields(i)
        nrecs,_,_,_,_=dataid.inquire()
        data=dataid.read(nRec=nrecs)
        data=list(np.concatenate(data))
        geodatasetlist.append(data)
    for i in oneddatasearch:
        vs=h.vstart()
        xid=vs.find(i)
        dataid=vs.attach(xid)
        dataid.setfields(i)
        nrecs,_,_,_,_=dataid.inquire()
        data=dataid.read(nRec=nrecs)
        data=list(np.concatenate(data))
        oneddatasetlist.append(data)
    
    csatlatitude=geodatasetlist[0] #Works fine, all the geo fields work fine
    csatlongitude=geodatasetlist[1]
    elevation=geodatasetlist[2] 
    diffprofiletime=geodatasetlist[3] #Difference between profile time and UTC start

    #Reading topography data, land sea flag
    csatlandsea=geodatasetlist[4] #1 = Land, 2 = Sea, 3 = Coast
    csatlandsea=np.array(csatlandsea,dtype=float)
    csatlandsea[csatlandsea==3]=1+0.5
    csatlandsea[csatlandsea==4]=2.0
    csatlandsea[csatlandsea==5]=1+0.5 #Just eliminating 4,5 and putting coast as 1.5

    #Time preparation for cloudsat data
    csatstart=geodatasetlist[5][0] #UTC start time of the orbit
    cloudlayer=oneddatasetlist[0] #No.of cloud layers
    csatprofiletime = [(i+csatstart) for i in diffprofiletime] #Profile time in seconds (UTC)
    csatendtime = csatprofiletime[-1] #UTC end time of the orbit
    csatfilename=csatfilepath.split('/')[-1]
    csatyear=(csatfilename[0:4])
    csatdaynumber=(csatfilename[4:7])
    csatdaynumber = int(csatdaynumber.lstrip('0'))
    csathour=csatfilename[7:9]
    csatminute=csatfilename[9:11]
    csatsecond=csatfilename[11:13]
    csatmonth = datetime.date.fromordinal(datetime.date(int(csatyear), 1, 1).toordinal() + csatdaynumber - 1).strftime('%b')
    csatmonthnum = datetime.date.fromordinal(datetime.date(int(csatyear), 1, 1).toordinal() + csatdaynumber - 1).strftime('%m')
    csatday = datetime.date.fromordinal(datetime.date(int(csatyear), 1, 1).toordinal() + csatdaynumber - 1).strftime('%d')
    csat_starttime_obj = datetime.datetime.strptime(csatyear+'-'+csatmonth+'-'+csatday+'-'+csathour+':'+csatminute+':'+csatsecond, "%Y-%b-%d-%H:%M:%S")
    csat_endtime_obj = csat_starttime_obj + datetime.timedelta(seconds=diffprofiletime[-1])

    #Reading cloud top and base data, and cloud type

    cloudtypearray = csatfile.select('CloudLayerType')[:,:]
    cloudtypearray = np.array(cloudtypearray,dtype=np.float32)
    cloudtypearray[cloudtypearray==-9]=np.nan
    
    cloudbasearray=csatfile.select('CloudLayerBase')[:,:]
    cloudbasearray[cloudbasearray==-99]=np.nan #-99.0 means undetermined

    cloudtoparray=csatfile.select('CloudLayerTop')[:,:]
    cloudtoparray[cloudtoparray==-99]=np.nan

    #Subtracting cloud base from cloud top to get cloud thickness
    cloudthicknessarray=cloudtoparray-cloudbasearray
    thicknessarray=np.nansum(cloudthicknessarray,axis=1)
    #nansum would give sum of 2 NaNs as 0, so we do corrections for that
    thicknessarray[np.array(cloudlayer)==-9.0]=np.nan #Otherwise, undetermined and clear pixels produce the same thickness i.e. 0

    csatorbitnumber = int(csatfilepath.split('/')[-1].split('_')[1])
    cloudyornotlist = []
    for i in range(len(cloudlayer)): #Cloud layer, 1D list that says how many cloud layers are there in each profile.
        if cloudlayer[i] > 0: #More than 0 cloud layers, so pixel cloudy
            cloudyornotlist.append(1)
        elif cloudlayer[i] == 0: #0 cloud layers, so pixel clear
            cloudyornotlist.append(0)
        else: #Undetermined
            cloudyornotlist.append(np.nan)

    #print("Cloudsat data read")
    #print("INSAT-3DR data reading started")
    

    #Reading INSAT-3DR data

    cmkfile = h5py.File(insatfilepath,'r')
    insatlongitude=np.array(cmkfile["Longitude"])/100
    insatlatitude=np.array(cmkfile["Latitude"])/100
    insatlonfill = cmkfile['Longitude'].attrs['_FillValue'][0]/100
    insatlatfill = cmkfile['Latitude'].attrs['_FillValue'][0]/100
    insatlongitude[insatlongitude==insatlonfill]=np.nan
    insatlatitude[insatlatitude==insatlatfill]=np.nan

    cmkarray = np.array(cmkfile['CMK'],dtype=float)[0]
    cmkarrayfill = cmkfile['CMK'].attrs['_FillValue'][0]
    cmkarray[cmkarray==cmkarrayfill]=np.nan

    acq_start=str(cmkfile.attrs['Acquisition_Start_Time'])[2:13]+"-"+ str(cmkfile.attrs['Acquisition_Start_Time'])[14:-1] #To remove a T in the middle of string
    start_time_obj=datetime.datetime.strptime(acq_start, "%d-%b-%Y-%H:%M:%S")
    insatstarttime=start_time_obj.hour*3600+start_time_obj.minute*60+start_time_obj.second

    acq_end = str(cmkfile.attrs['Acquisition_End_Time'])[2:13]+"-"+ str(cmkfile.attrs['Acquisition_End_Time'])[14:-1]
    end_time_obj=datetime.datetime.strptime(acq_end, "%d-%b-%Y-%H:%M:%S")
    insatendtime = end_time_obj.hour*3600+end_time_obj.minute*60+end_time_obj.second

    try:
        assert start_time_obj.date() == csat_starttime_obj.date()
    except AssertionError:
        print("INSAT-3DR and Cloudsat files are not from the same date")
        return 0



    timeindex = []

    for i in range(len(csatprofiletime)):
        if csatprofiletime[i]>insatstarttime and csatprofiletime[i]<insatendtime:
            timeindex.append(i)

    print("Time collocated profile extent = {}-{}, len = {}".format(timeindex[0],timeindex[-1],len(timeindex)))

    #Collocating the INSAT-3DR data with Cloudsat data

    insatcmklist = []
    csatcmklist = []
    offsetlist = []
    csatlonlist = []
    csatlatlist = []
    insatlonlist = []
    insatlatlist = []
    thicknesslist = []
    collocatedprofilelist = []
    orbitnumberlist = []
    datelist = []
    landsealist = []

    #print("First few time-collocated profile numbers of csat file are - ",timeindex[0:5])
    print("Collocation starts at, {} IST".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')))
    for profileno in timeindex:
        #print(profileno)
        csatlat = csatlatitude[profileno]
        csatlon = csatlongitude[profileno]
        
        if csatlat <-60  or csatlat > 60:
            continue
        #print(1)
        if csatlon < 0 or csatlon > 140:
            continue
        #print(1)
        if cloudlayer[profileno]==-9.0:
            continue
        #print(1)
        combineddiff = np.abs(insatlatitude-csatlat)+np.abs(insatlongitude-csatlon)
        minabsdistance = np.nanargmin(combineddiff)
        
        insatindex = np.unravel_index(minabsdistance,insatlongitude.shape)
        closestinsatlat = insatlatitude[insatindex]
        closestinsatlon = insatlongitude[insatindex]
        closestdistance = geopy.distance.distance((csatlat,csatlon),(closestinsatlat,closestinsatlon)).km
        #print(closestdistance)
        if closestdistance>1.0:
            continue

        insatcmk = cmkarray[insatindex]
        csatcmk = cloudyornotlist[profileno]
        thickness = thicknessarray[profileno]

        insatcmklist.append(insatcmk)
        csatcmklist.append(csatcmk)
        thicknesslist.append(thickness)
        offsetlist.append(closestdistance)
        csatlonlist.append(csatlon)
        csatlatlist.append(csatlat)
        insatlonlist.append(closestinsatlon)
        insatlatlist.append(closestinsatlat)
        collocatedprofilelist.append(profileno)
        orbitnumberlist.append(csatorbitnumber)
        datelist.append(csat_starttime_obj.date())
        landsealist.append(csatlandsea[profileno])

        print("Profile no. = {}, InsatLat = {:.2f}, InsatLon = {:.2f}, offset = {:.2f} km, InsatCMK = {}, CsatCMK= {}".format(profileno, closestinsatlat, closestinsatlon, closestdistance,insatcmk, csatcmk), end="\r")

    #Print a blank line to move the cursor to next line
    print()

    dfcollocated = pd.DataFrame(
                                { 'csatcmk':csatcmklist,
                                 'insatcmk':insatcmklist,
                                 'thickness':thicknesslist,
                                 'offset':offsetlist,
                                 'csatlat':csatlatlist,
                                 'csatlon':csatlonlist,
                                 'insatlat':insatlatlist,
                                 'insatlon':insatlonlist,
                                 'profile':collocatedprofilelist,
                                 'orbitnumber':orbitnumberlist,
                                 'date':datelist,
                                 'landorsea': landsealist
                                 } 
                                 )
    if len(dfcollocated)==0:
#        print("No collocated profiles found")
        return 0
    print()
    print("Initial length of collocated dataframe = {}".format(len(dfcollocated)))
    dfcollocated.dropna(inplace=True)
    dfcollocated = dfcollocated[dfcollocated['insatcmk']!=9.0]
    print("Length after removing NaNs = {}".format(len(dfcollocated)))
    dfcollocated = dfcollocated.sort_values(by=['offset'])
    dfcollocated = dfcollocated.drop_duplicates(subset=['insatlat','insatlon'],keep='first')
    print("Length after removing duplicates = {}".format(len(dfcollocated)))
    dfcollocated = dfcollocated.sort_values(by='profile')

    singlefileend = time.time()
    timetaken = singlefileend-singlefilestart
    #print(len(dfcollocated))
    #Print it in HH:MM:SS format
    print("Time taken to collocate a single file = {}".format(datetime.timedelta(seconds=timetaken)))

    return dfcollocated
    
#csatdayfolder = r"/data/debasish/cloudsatdata/cldclasslidar/2017/2017jan/001"
#insatdayfolderpath = r"/data/debasish/insatdata/2017_insat_cmk/01_jan2017_cmk/jan01"

print("Program starts at, {} IST".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')))

csatsinglefilelist = sorted(os.listdir(csatdayfolder))
#print(csatsinglefilelist[0:5])

insatsinglefilelist = sorted(os.listdir(insatdayfolderpath))
#print(insatsinglefilelist[0:5])
#Let's access all folder

programstart = time.time()
dfonedaycollocatedlist = []

totalcorruptedfiles = 0
for insatfileiterator in insatsinglefilelist:
    insatfilepath = os.path.join(insatdayfolderpath,insatfileiterator)
    try:
        insatfile = h5py.File(insatfilepath,'r')
    except:
        os.remove(insatfilepath)
        totalcorruptedfiles += 1
        print("Corrupted file removed")

insatsinglefilelist = sorted(os.listdir(insatdayfolderpath))

for csatfileiterator in csatsinglefilelist:
    csatfilepath = os.path.join(csatdayfolder,csatfileiterator)
    csatfile = HDF.HDF(csatfilepath)

    def oneddata(searchdatasetlist):
        datasetlist=[]
        for i in searchdatasetlist:
            vs=csatfile.vstart()
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
    
    clat, clon, cstarttime, cdiffprofiletime = oneddata(['Latitude','Longitude','UTC_start','Profile_time'])
    csatstarttime = cstarttime[0]
    profiletime = [csatstarttime+i for i in cdiffprofiletime]
    csatendtime = profiletime[-1]

    filename = csatfilepath.split('/')[-1]
    year = filename[0:4]
    daynumber = filename[4:7]
    daynumber = int(daynumber.lstrip('0'))
    hour = filename[7:9]
    minute = filename[9:11]
    second = filename[11:13]

    month = datetime.date.fromordinal(datetime.date(int(year),1,1).toordinal()+daynumber-1).strftime('%b')
    day = datetime.date.fromordinal(datetime.date(int(year),1,1).toordinal()+daynumber-1).strftime('%d')
    csat_starttime_obj = datetime.datetime.strptime(year+'-'+month+'-'+day+'-'+hour+':'+minute+':'+second,'%Y-%b-%d-%H:%M:%S')
    csat_endtime_obj = csat_starttime_obj + datetime.timedelta(seconds=cdiffprofiletime[-1])

    collocationno = 0
    nooffilescompared = 0
    if clat[0] >0 and clon[0] < 180:
        print("Longitude is in the range 0-180")
        continue

    for insatfileiterator in insatsinglefilelist:
        insatfilepath = os.path.join(insatdayfolderpath,insatfileiterator)
        insatfile = h5py.File(insatfilepath,'r')

        acq_start = str(insatfile.attrs['Acquisition_Start_Time'])[2:-1][0:11]+'-'+str(insatfile.attrs['Acquisition_Start_Time'])[2:-1][12:] #To remove a T in the middle of string
        start_time_obj=datetime.datetime.strptime(acq_start, "%d-%b-%Y-%H:%M:%S")
        acq_end=str(insatfile.attrs['Acquisition_End_Time'])[2:-1][0:11]+'-'+str(insatfile.attrs['Acquisition_End_Time'])[2:-1][12:]
        end_time_obj=datetime.datetime.strptime(acq_end, "%d-%b-%Y-%H:%M:%S")
        
        insat_start = start_time_obj.strftime("%H:%M:%S")
        insat_end = end_time_obj.strftime("%H:%M:%S")

        if csat_starttime_obj.date() != start_time_obj.date():
            continue

        timeoverlap = False

        if (csat_endtime_obj>start_time_obj) and (csat_endtime_obj<end_time_obj) and (csat_starttime_obj<start_time_obj):
            timeoverlap = True
            print("Cloudsat orbit started before INSAT acq. start", end="\r")

        if (csat_endtime_obj>end_time_obj) and (csat_starttime_obj<start_time_obj):
            timeoverlap = True
            print("Cloudsat orbit completely envelops INSAT acq. time", end="\r")
        if (csat_starttime_obj>start_time_obj) and (csat_starttime_obj<end_time_obj) and (csat_endtime_obj>end_time_obj):
            timeoverlap = True
            print("Cloudsat orbit started after INSAT acq. start", end="\r")
        
        nooffilescompared +=1

        print("No. of files compared: {}".format(nooffilescompared),end="\r")

        if timeoverlap == True:
            print()
            try:
                df = insatcmkcsatcollocation(insatfilepath,csatfilepath)
                if type(df) == pd.core.frame.DataFrame:

                    dfonedaycollocatedlist.append(df)
                    collocationno += 1
                    print("Length of dfonedaycollocatedlist: {}".format(len(dfonedaycollocatedlist)))
                    time.sleep(5)
                    print()
            except:
                pass


# Concatenate all the elements of dfonedaycollocatedlist



programend = time.time()

print("Program ends at, {} IST".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')))

print("Total time taken: {}".format(datetime.timedelta(seconds=programend-programstart)))

dfoneday = pd.concat(dfonedaycollocatedlist)

print("Shape of full data datarame is {}".format(dfoneday.shape))



collocatefilename = insatdayfolderpath.split("/")[-1]+".csv"
print("Date - ", dfoneday['date'].unique())
dfoneday.to_csv(saving_folder+"/"+collocatefilename)

print("Execution over")