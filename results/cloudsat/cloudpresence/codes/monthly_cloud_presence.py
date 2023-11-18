#Input - Folders containing 2b-CLDCLASS of CloudSat satellite.
#Folder structure assumed - Single-year(2013 in our case) - Month(January,February etc.) - Day_Number (1,2,3....)
#Most of the time is spent on applying the csat_stats function on all the CloudSat files. IIRC, it was around 10 minutes per month.

#Output is bar plots of presence of clouds over land and ocean, as shown in https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudpresence/year2013%25landiscloudy.png
#and https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudpresence/year2013%25clearisonland.png


#Python 3.10.1. 
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
import re
from matplotlib.colors import Normalize, PowerNorm
from matplotlib.cm import get_cmap

#For a single csat file, make a function that takes in a file and returns stats of the cloud layers
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

#Now apply this function iteratively to every file for the year 2013. Merge them into one big dataframe. Ideally I should have done it using a for loop, but since I was on a notebook, I took the easy way.

dfmonthlycollection = [] #For each month, we process all CloudSat files of that month and add the resulting dataframe to this dfmonthlycollection.

#For month of January
import re
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013jan'

dflist=[]
print("Month - January")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#For month of February
import re
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013feb'

dflist=[]
print("Month - Febuary")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#For month of March
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013mar'

dflist=[]
print("Month - March")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#April
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013apr'

dflist=[]
print("Month - April")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#May
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013may'

dflist=[]
print("Month - May")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#June
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013jun'

dflist=[]
print("Month - June")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#July
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013jul'

dflist=[]
print("Month - July")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#August
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013aug'

dflist=[]
print("Month - August")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#sEPTEMBER
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013sep'

dflist=[]
print("Month - September")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#October
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013oct'

dflist=[]
print("Month - October")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#November
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013nov'

dflist=[]
print("Month - November")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))

#December
rootdir='/data/debasish/cloudsatdata/cldclasslidar/2013/2013dec'

dflist=[]
print("Month - December")
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
#df=df[df['type']!=0]
df['cloudname'] = df['type'].map({1:'Cirrus',2:'Altostratus',3:'Altocumulus',4:'Stratus',5:'Stratocumulus',6:'Cumulus',7:'Nimbostratus'
                ,8:'Deep convective',9:'Unknown'})
df['cloudname'] = df['cloudname'].astype('category')
print(len(df))
dfmonthlycollection.append(df)
print(len(dfmonthlycollection))


#Saving the output dataframes as a dictionary and then locally into the server
months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
dfmonthlycollectiondict = dict(zip(months, dfmonthlycollection))


import pickle
loadadress =r'/data/debasish/cloudsatdata/cldclasslidar/cloudyclearmonthlyfullyear2013collectiondict.pickle'
with open(loadadress, 'rb') as handle:
    dicttrial = pickle.load(handle)

print(type(dicttrial))


#Plotting the cloud presence map for a single month, let's say March

dfcopy = dicttrial['mar'].copy() #Stating the month here
dfcopy = dfcopy[dfcopy['type']!=9] 
print(len(dfcopy))
print(sorted(dfcopy['day'].unique()))

# Group the dataframe by 'lat', 'lon', and 'orbit' and find the index of the maximum value in 'type'
idx = dfcopy.groupby(['lat', 'lon', 'orbit'])['type'].idxmax()

# Select the rows with the maximum 'type' value based on the obtained index
result = dfcopy.loc[idx]

result = result[result['landseaflag']!=3] #Not considering the coastlines, inland water bodies etc. Just considering the ocean/sea and land, they're the overwhelming majority anyway.
result = result[result['landseaflag']!=4] #1- Land, 2- Ocean, 3- Coastlines, 4- Inland water,, 5- Mixed water-land, as per CloudSat conventions
result = result[result['landseaflag']!=5]
print(len(result))
print(sorted(result['day'].unique()))
result['cloudyorclear'] = result['thickness'].notnull().astype(int)
result['landseaflagchar'] = result['landseaflag'].map({1:'Land',2:'Ocean'})
result['cloudyornotchar'] = result['cloudyorclear'].map({0:'Clear',1:'Cloudy'})



#Plotting what percentage of land and ocean is occupied by clouds and what percentage is cloud-free.
clear_land_pixels = len(result[(result['landseaflagchar']=='Land') & (result['cloudyornotchar']=='Clear')]) #Clear pixels on land
cloudy_land_pixels = len(result[(result['landseaflagchar']=='Land') & (result['cloudyornotchar']=='Cloudy')]) #Cloudy pixels on land
clear_ocean_pixels = len(result[(result['landseaflagchar']=='Ocean') & (result['cloudyornotchar']=='Clear')]) #Clear pixels on ocean
cloudy_ocean_pixels = len(result[(result['landseaflagchar']=='Ocean') & (result['cloudyornotchar']=='Cloudy')]) #Cloudy pixels on ocean

total_land_pixels = len(result[result['landseaflagchar']=='Land'])
total_ocean_pixels = len(result[result['landseaflagchar']=='Ocean'])

# Calculate the percentage of clear and cloudy land and ocean pixels
clear_land_percentage = (clear_land_pixels / total_land_pixels) * 100
cloudy_land_percentage = (cloudy_land_pixels / total_land_pixels) * 100
clear_ocean_percentage = (clear_ocean_pixels / total_ocean_pixels) * 100
cloudy_ocean_percentage = (cloudy_ocean_pixels / total_ocean_pixels) * 100

# Create the data for the stacked bar plot
categories = ['Land', 'Ocean']
clear_percents = [clear_land_percentage, clear_ocean_percentage]
cloudy_percents = [cloudy_land_percentage, cloudy_ocean_percentage]
print(clear_percents)
print(cloudy_percents)

fig, ax = plt.subplots()
bar_width = 0.5
opacity = 0.8

# Plot the lower bars (clear percentages)
bar1 = ax.bar(categories, clear_percents, bar_width, alpha=opacity, color='r', label='Clear')

# Plot the upper bars (cloudy percentages)
bar2 = ax.bar(categories, cloudy_percents, bar_width, alpha=opacity, color='b', label='Cloudy', bottom=clear_percents)

# Set the y-axis limit to 100% to represent the maximum percentage
ax.set_ylim([0, 100])

# Add labels and title
ax.set_xlabel('Region', fontsize=16)
ax.set_ylabel('Percentage', fontsize=16)
ax.set_title('Percentage of Clear & Cloudy Pixels - Land vs Ocean \nMarch 2013, #Pixels: {}, #Orbits: {}'.format(len(result),len(result['orbit'].unique())), fontsize=15)
ax.legend()

# Add percentage labels to the bars within their regions
for category, bar1, bar2 in zip(categories, bar1, bar2):
    height1 = bar1.get_height()
    height2 = bar2.get_height()
    if category == 'Land':
        ax.annotate(f'{height1:.1f}%', xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',fontsize=14)
        ax.annotate(f'{clear_land_pixels} pixels', xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2*1.4),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',fontsize=14)
        


        ax.annotate(f'{height2:.1f}%', xy=(bar2.get_x() + bar2.get_width() / 2, height1 + height2 / 2),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',fontsize=14)
        ax.annotate(f'{cloudy_land_pixels} pixels', xy=(bar2.get_x() + bar2.get_width() / 2,( height1 + height2 / 2)*1.1),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',fontsize=14)
        
    elif category == 'Ocean':
        ax.annotate(f'{height1:.1f}%', xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2*1.5),
                    xytext=(0, -15), textcoords='offset points', ha='center', va='top',fontsize=14)
        ax.annotate(f'{clear_ocean_pixels} pixels', xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2*2.2),
                    xytext=(0, -15), textcoords='offset points', ha='center', va='top',fontsize=14)
        

        ax.annotate(f'{height2:.1f}%', xy=(bar2.get_x() + bar2.get_width() / 2, height1 + height2 / 2),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=14)
        ax.annotate(f'{cloudy_ocean_pixels} pixels', xy=(bar2.get_x() + bar2.get_width() / 2, (height1 + height2 / 2)*1.1),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=14)
        
ax.legend(fontsize=14)
plt.xticks(fontsize=14)
plt.tight_layout()
plt.show()


#Calculate the % of clear pixels that are over land and ocean, and cloudy pixels that are over land and ocean
perofclearthatareoverland = (clear_land_pixels / total_clear_pixels) * 100 #Percentage of clear pixels that are over the land
perofclearthatareoceanocean = (clear_ocean_pixels / total_clear_pixels) * 100 #Percentage of clear pixels that are over the ocean
perofcloudythatareoverland = (cloudy_land_pixels / total_cloudy_pixels) * 100 #Percentage of cloudy pixels that are over the land
perofcloudythatareoceanocean = (cloudy_ocean_pixels / total_cloudy_pixels) * 100 #Percentage of cloudy pixels that are over the ocean

fig, ax = plt.subplots()
bar_width = 0.5
opacity = 0.8

# Plot the lower bars (clear percentages)
bar1 = ax.bar(categories, [perofclearthatareoverland,perofcloudythatareoverland], bar_width, alpha=opacity, color='r', label='Land')

# Plot the upper bars (cloudy percentages)
bar2 = ax.bar(categories, [perofclearthatareoceanocean,perofcloudythatareoceanocean], bar_width, alpha=opacity, color='b', label='Ocean', bottom=[perofclearthatareoverland,perofcloudythatareoverland])

# Set the y-axis limit to 100% to represent the maximum percentage
ax.set_ylim([0, 100])

ax.set_xlabel('Cloud presence', fontsize=16)
ax.set_ylabel('Percentage', fontsize=16)
ax.set_title('Percentage of Clear & Cloudy Pixels - Land vs Ocean \nMarch 2013, #Pixels: {}, #Orbits: {}'.format(len(result),len(result['orbit'].unique())), fontsize=15)
ax.legend()

categories = ['Clear', 'Cloudy']

for category, bar1, bar2 in zip(categories, bar1, bar2):
    height1 = bar1.get_height()
    height2 = bar2.get_height()
    if category == 'Clear':
        ax.annotate(f'{height1:.1f}%', xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',fontsize=14)
        ax.annotate(f'{clear_land_pixels:.0f} pixels', xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2*1.3),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',fontsize=14)

        ax.annotate(f'{height2:.1f}%', xy=(bar2.get_x() + bar2.get_width() / 2, height1 + height2 / 2),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',fontsize=14)
        ax.annotate(f'{clear_ocean_pixels:.0f} pixels', xy=(bar2.get_x() + bar2.get_width() / 2, (height1 + height2 / 2)*1.1),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',fontsize=14)
    elif category == 'Cloudy':
        ax.annotate(f'{height1:.1f}%', xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2),
                    xytext=(0, -15), textcoords='offset points', ha='center', va='top',fontsize=14)
        ax.annotate(f'{cloudy_land_pixels} pixels', xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2*1.2),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='top',fontsize=14)


        ax.annotate(f'{height2:.1f}%', xy=(bar2.get_x() + bar2.get_width() / 2, height1 + height2 / 2),
                    xytext=(0, -15), textcoords='offset points', ha='center', va='bottom', fontsize=14)
        ax.annotate(f'{cloudy_ocean_pixels} pixels', xy=(bar1.get_x() + bar1.get_width() / 2, (height1 + height2) / 2*1.5),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='top',fontsize=14)
#In the middle of the bars, add the land/ocean pixel ratio and do this in latex format

ax.text(0.5, 0.6, r'$\frac{{Total\ land\ pixels}}{{Total\ ocean\ pixels}} = {:.2f}$'.format(total_land_pixels/total_ocean_pixels),
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes,
        fontsize=18,
        rotation=90)

ax.legend(fontsize=14)
plt.xticks(fontsize=14)
plt.tight_layout()
plt.show()
