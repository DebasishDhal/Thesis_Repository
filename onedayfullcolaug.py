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
import datetime
from pytz import timezone 


#13 files. 87 hours.

programstarttic = time.time()
programstarttimeind = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
print("Program starts at, {} IST".format(programstarttimeind))

csatfolder = r'/data/debasish/cloudsatdata/cldclasslidar/2017/2017aug/day06'
csatfiles = os.listdir(csatfolder)
csatfiles.sort()

insatfolderadress = r'/data/debasish/insatdata/l1b/2017/aug2017/day06'
insatfolder = insatfolderadress
insatfiles = os.listdir(insatfolder)
insatfiles.sort()


def insatcsatcollocation(insatfilepath, csatfilepath):


#Data reading from Cloudsat file block
    
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

    print("Cloudsat data read")
    print("INSAT-3DR data reading started")

#Data reading from INSAT file block

    #INSAT-3DR time preparation
    insatfile = h5py.File(insatfilepath, 'r')
    acq_start = str(insatfile.attrs['Acquisition_Start_Time'])[2:13]+"-"+ str(insatfile.attrs['Acquisition_Start_Time'])[14:-1] #To remove a T in the middle of string
    start_time_obj=datetime.datetime.strptime(acq_start, "%d-%b-%Y-%H:%M:%S")
    insatstarttime=start_time_obj.hour*3600+start_time_obj.minute*60+start_time_obj.second
    
    acq_end = str(insatfile.attrs['Acquisition_End_Time'])[2:13]+"-"+ str(insatfile.attrs['Acquisition_End_Time'])[14:-1]
    end_time_obj=datetime.datetime.strptime(acq_end, "%d-%b-%Y-%H:%M:%S")
    insatendtime = end_time_obj.hour*3600+end_time_obj.minute*60+end_time_obj.second

    #Latitude and longitude of INSAT-3DR (*works fine)
    vislatitude=np.ma.masked_equal(insatfile["Latitude_VIS"],327670)/1000
    vislongitude=np.ma.masked_equal(insatfile["Longitude_VIS"],327670)/1000
    tirlongitude=np.ma.masked_equal(insatfile["Longitude"],32767)/100
    tirlatitude=np.ma.masked_equal(insatfile["Latitude"],32767)/100
    solarelevationarray=np.ma.masked_equal(insatfile["Sun_Elevation"][0],32767)/100
    satelevationarray=np.ma.masked_equal(insatfile["Sat_Elevation"][0],32767)/100

    #BT and Albedo data preparation (works fine)
    channel_listtir= ['IMG_MIR','IMG_TIR1','IMG_TIR2']
    btlist=[]

    for i in channel_listtir:
        img_arr=insatfile[i][0,:,:] 
        img_arr_fill=insatfile[i].attrs['_FillValue'][0]
        nanmask=(img_arr==img_arr_fill)
        btlut=np.array(insatfile[i+str('_TEMP')])
        def count2bt(count):
            return btlut[count]
        bt_array=count2bt(img_arr)
        bt_array[nanmask]=np.nan
        btlist.append(bt_array)

    img_arr=insatfile['IMG_VIS'][0,:,:]
    img_arr_fill=insatfile['IMG_VIS'].attrs['_FillValue'][0]
    nanmask=(img_arr==img_arr_fill)
    albedolut=np.array(insatfile['IMG_VIS_ALBEDO'])
    def count2albedo(count):
        return albedolut[count]
    albedo_array=count2albedo(img_arr)/100
    albedo_array[nanmask]=np.nan

    print("Brightness temperature and albedo data read")
    print("All data read")

    print("Beginning collocation")

#Collocation block
    ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    print("Program starts - ",ind_time)

    tic = time.time()

    #Time collocation
    timeindex=[]
    for i in range(len(csatprofiletime)): 
        if csatprofiletime[i]>insatstarttime and csatprofiletime[i]<insatendtime:
            timeindex.append(i)
    print("Time collocation done")
    print("time collocated csat profile min = {}, max = {}".format(min(timeindex),max(timeindex)))

    #Space collocation
    print("Beginning space collocation")
    landseacolllist = [] #Done
    thicknesscolllist = [] #Done
    albedocolllist = [] #Done
    btmircolllist = [] #Done
    bttir1colllist = [] #Done
    bttir2colllist = [] #Done
    solarelevationcolllist = [] #Done
    satelevationcolllist = [] #Done
    tircoordinsat = [] #Done
    tircoordcsat = []   #Done
    viscoordinsat = [] #Done
    viscoordcsat = [] #Done 
    tiroffsetlist= [] #Done
    visoffsetlist= [] #Done
    elevationcolllist = [] #Done
    profilenolist = [] #Done
    orbitnolist = [] #Done


    collocatedpointcount = 0
    for i in timeindex:
        #print("profile no. = {}".format(i),end="\r")
        profile = i
        print("current profile = {}".format(profile),end='\r')
        clat=csatlatitude[i]
        clon=csatlongitude[i]

        if clat<-60 or clat>60:
            continue
        if clon<0 or clon>140:
            continue
        height=elevation[i]
        thick = thicknessarray[i]
        landsea = csatlandsea[i]

        if np.isnan(thick):
            continue
    #Main collocation starts here
        combineddifftir = np.abs(tirlatitude-clat)+np.abs(tirlongitude-clon)
        indextir = np.nanargmin(combineddifftir)
        indextir = np.unravel_index(indextir,combineddifftir.shape)
        closestlattir = tirlatitude[indextir]
        closestlontir = tirlongitude[indextir]
        satelevation = satelevationarray[indextir]
        solarelevation = solarelevationarray[indextir]
        tiroffset = geopy.distance.distance((clat,clon),(closestlattir,closestlontir)).km

        combineddiffvis = np.abs(vislatitude-clat)+np.abs(vislongitude-clon)
        indexvis = np.nanargmin(combineddiffvis)
        indexvis = np.unravel_index(indexvis,combineddiffvis.shape)
        closestlatvis = vislatitude[indexvis]
        closestlonvis = vislongitude[indexvis]
        visoffset = geopy.distance.distance((clat,clon),(closestlatvis,closestlonvis)).km

        if tiroffset>1.0:
            continue
        if visoffset>1.0:
            continue

        btmir=btlist[0][indextir]
        bttir1=btlist[1][indextir]
        bttir2=btlist[2][indextir]
        albedo=albedo_array[indexvis]

        if np.isnan(btmir) or np.isnan(bttir1) or np.isnan(bttir2) or np.isnan(albedo):
            continue
        #Print the collocated data with /r to overwrite the previous line
        collocatedpointcount = collocatedpointcount + 1
        print("current profile = {}, insat coords {}, offset {} km,   points={}".format(profile,((np.round(closestlattir,2),np.round(closestlontir,2))),np.round(tiroffset,2),collocatedpointcount),end='\r')


        landseacolllist.append(landsea)
        thicknesscolllist.append(thick)
        albedocolllist.append(albedo)
        btmircolllist.append(btmir)
        bttir1colllist.append(bttir1)
        bttir2colllist.append(bttir2)
        solarelevationcolllist.append(solarelevation)
        satelevationcolllist.append(satelevation)
        tircoordinsat.append((closestlattir,closestlontir))
        tircoordcsat.append((clat,clon))
        viscoordinsat.append((closestlatvis,closestlonvis))
        viscoordcsat.append((clat,clon))
        tiroffsetlist.append(tiroffset)
        visoffsetlist.append(visoffset)
        elevationcolllist.append(height)
        profilenolist.append(profile)
        orbitnolist.append(csatorbitnumber)
        
    toc = time.time()
    #Print time taken in hours, minutes and seconds using strptime
    print("Time taken for collocation = {}".format(time.strftime("%H:%M:%S",time.gmtime(toc-tic))))


    print("Space collocation done")

    #Make a dataframe of the collocated data
    collocateddata = pd.DataFrame({'btmir':btmircolllist,'bttir1':bttir1colllist,
                                   'bttir2':bttir2colllist,'albedo':albedocolllist,
                                   'thickness':thicknesscolllist,'insatcortir':tircoordinsat,
                                   'csatcortir':tircoordcsat,'tiroffset':tiroffsetlist,
                                   'insatcorvis':viscoordinsat,'csatcorvis':viscoordcsat,
                                   'visoffset':visoffsetlist,'solarelevation':solarelevationcolllist,
                                   'satelevation':satelevationcolllist,'elevation':elevationcolllist,
                                   'landsea':landseacolllist,'profile':profilenolist,
                                   'orbitnumber':orbitnolist})
    
    #Remove rows with any NaN values
    collocateddata = collocateddata.dropna()

    #Make a dataframe of the cloud type and base and top
    #Get a list of profile numbers from the collocated data and make c1type,c2type,c3type,c4type,c5type etc.
    #Then make a dataframe of the cloud type and base and top

    finalprofilelist = collocateddata['profile'].tolist()
    c1type = []
    c2type = []
    c3type = []
    c4type = []
    c5type = []
    c1base = []
    c2base = []
    c3base = []
    c4base = []
    c5base = []
    c1top = []
    c2top = []
    c3top = []
    c4top = []
    c5top = []

    for profile in finalprofilelist:
        c1type.append(cloudtypearray[profile][0])
        c2type.append(cloudtypearray[profile][1])
        c3type.append(cloudtypearray[profile][2])
        c4type.append(cloudtypearray[profile][3])
        c5type.append(cloudtypearray[profile][4])

        c1base.append(cloudbasearray[profile][0])
        c2base.append(cloudbasearray[profile][1])
        c3base.append(cloudbasearray[profile][2])
        c4base.append(cloudbasearray[profile][3])
        c5base.append(cloudbasearray[profile][4])

        c1top.append(cloudtoparray[profile][0])
        c2top.append(cloudtoparray[profile][1])
        c3top.append(cloudtoparray[profile][2])
        c4top.append(cloudtoparray[profile][3])
        c5top.append(cloudtoparray[profile][4])


    clouddataframe = pd.DataFrame({'c1type':c1type,'c1base':c1base, 'c1top':c1top,
                                    'c2type':c2type,'c2base':c2base, 'c2top':c2top,
                                    'c3type':c3type,'c3base':c3base, 'c3top':c3top,
                                    'c4type':c4type,'c4base':c4base, 'c4top':c4top,
                                    'c5type':c5type,'c5base':c5base, 'c5top':c5top})
    #Merge the two dataframes
    collocateddata = pd.concat([collocateddata,clouddataframe],axis=1)

    
    print("Collocated data made into a dataframe @ shape {}, filesize {} MB".format(collocateddata.shape,sys.getsizeof(collocateddata)/1e6))

    insatdatetime = ''.join(insatfilepath.split('/')[-1].split('_')[1:3])
    filename = 'col'+insatdatetime+'_'+str(csatorbitnumber)+'.csv'

    adress = r'/data/debasish/collocations/2017/2017aug/day06'

    #Check if path exists, if not, raise error
    if not os.path.exists(adress):
        raise ValueError("Path doesn't exist")



    #Save the dataframe as a csv file in the folder
    #If file size <1MB, don't save
    if len(collocateddata)==0:
        print("No collocated data, not saved")
        pass
    else:
        collocateddata.to_csv(os.path.join(adress,filename),index=False)
        print("Collocated data saved as {}".format(filename)) 
        ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        print("Program ends - ",ind_time)


#Deletion of truncated INSAT files

csatfiles.sort()
insatfiles.sort()

truncatedfilecount = 0 
for insatfileiterator in insatfiles:
    insatfilepath = os.path.join(insatfolder, insatfileiterator)
    try:
        insatfile = h5py.File(insatfilepath,'r')
    except OSError as e:
        print("File {} is truncated".format(insatfileiterator))
        os.remove(insatfilepath)
        truncatedfilecount += 1

print("Number of truncated files = {}".format(truncatedfilecount))

insatfolder = insatfolderadress

insatfiles = os.listdir(insatfolder)
insatfiles.sort()

for csatfileiterator in csatfiles:
    csatfilepath = os.path.join(csatfolder,csatfileiterator)
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

    clat,clon,cstarttime,cdiffprofiletime = oneddata(['Latitude','Longitude','UTC_start','Profile_time'])

    csatstarttime = cstarttime[0]
    profiletime = [csatstarttime + i for i in cdiffprofiletime]
    csatendtime = profiletime[-1]

    filename=csatfilepath.split('/')[-1]
    year=(filename[0:4])
    daynumber=(filename[4:7])
    daynumber = int(daynumber.lstrip('0'))
    hour=filename[7:9]
    minute=filename[9:11]
    second=filename[11:13]
    month = datetime.date.fromordinal(datetime.date(int(year), 1, 1).toordinal() + daynumber - 1).strftime('%b')
    day = datetime.date.fromordinal(datetime.date(int(year), 1, 1).toordinal() + daynumber - 1).strftime('%d')
    csat_starttime_obj = datetime.datetime.strptime(year+'-'+month+'-'+day+'-'+hour+':'+minute+':'+second, "%Y-%b-%d-%H:%M:%S")
    csat_endtime_obj = csat_starttime_obj + datetime.timedelta(seconds=cdiffprofiletime[-1])

    collocationno = 0
    nooffilescompared =0
    if clon[0] >0 and clon[0]< 180:
        print("Longitude is in the range 0-180")
        continue
        
    for insatfileiterator in insatfiles:
        insatfilepath = os.path.join(insatfolder, insatfileiterator)
        insatfile = h5py.File(insatfilepath,'r')
        
        acq_start = str(insatfile.attrs['Acquisition_Start_Time'])[2:-1].replace('T','-') #To remove a T in the middle of string
        start_time_obj=datetime.datetime.strptime(acq_start, "%d-%b-%Y-%H:%M:%S")
        acq_end=str(insatfile.attrs['Acquisition_End_Time'])[2:-1].replace('T','-')
        end_time_obj=datetime.datetime.strptime(acq_end, "%d-%b-%Y-%H:%M:%S")

        insat_start = start_time_obj.strftime("%H:%M:%S")
        insat_end = end_time_obj.strftime("%H:%M:%S")

        timeoverlap = False

        if (csat_endtime_obj>start_time_obj) and (csat_endtime_obj<end_time_obj) and (csat_starttime_obj<start_time_obj):
            timeoverlap = True
            print("Cloudsat orbit started before INSAT acq. start")

        if (csat_endtime_obj>end_time_obj) and (csat_starttime_obj<start_time_obj):
            timeoverlap = True
            print("Cloudsat orbit completely envelops INSAT acq. time")
        if (csat_starttime_obj>start_time_obj) and (csat_starttime_obj<end_time_obj) and (csat_endtime_obj>end_time_obj):
            timeoverlap = True
            print("Cloudsat orbit started after INSAT acq. start")
        #timeindex=[] 
        nooffilescompared +=1
        print("No of files compared: ",nooffilescompared)
        if timeoverlap == True:
            try:
                insatcsatcollocation(insatfilepath,csatfilepath)
                collocationno += 1
            except ValueError:
                print(insatfilepath)
                print(csatfilepath)
            except OSError:
                print(insatfilepath)
                print(csatfilepath)
            except Exception as e:
                print(f"An exception occurred: {e}")

programendtoc = time.time()
print("Program ends")

total_time_taken = programendtoc - programstarttic

seconds_per_hour = 3600
seconds_per_minute = 60


hours_taken = int(total_time_taken/seconds_per_hour)
minutes_taken = int((total_time_taken - hours_taken*seconds_per_hour)/seconds_per_minute)
seconds_taken = total_time_taken - hours_taken*seconds_per_hour - minutes_taken*seconds_per_minute

print("Program ends at, {} IST".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')))

print("Total time taken: {} hours, {} minutes, {} seconds".format(hours_taken, minutes_taken, seconds_taken))