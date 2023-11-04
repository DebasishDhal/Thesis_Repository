#Input -  Adress of L1B file of INSAT-3DR. Output is cloud top height map produced by our model. In addition, it also returns a dataframe consisting of latitude, longitude, estimated cloud top height.

def insatcloudheightprediction(insatfilepath, cmap='jet_r',extent=-1, nightshade='Yes'):
    assert os.path.isfile(insatfilepath)

    insatfile = h5py.File(insatfilepath,'r')

    def count2bt(count,lut):
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

    longitudearray = np.array(insatfile['Longitude'])/100
    latitudearray = np.array(insatfile['Latitude'])/100
    fillvalue = insatfile['Longitude'].attrs['_FillValue'][0]/100
    latitudearray[latitudearray == fillvalue] = np.nan
    longitudearray[longitudearray == fillvalue] = np.nan

    dfirdata = pd.DataFrame(
                {'btmir': mirbt.flatten(),
                'bttir1': tir1bt.flatten(),
                'bttir2': tir2bt.flatten(),
                'insatcorvislat': latitudearray.flatten(),
                'insatcorvislon': longitudearray.flatten()
                }
            )
    dfirdata.dropna(inplace=True)

    scalaradress =r"/data/debasish/cloudetectionmodels/cloudtopheightmodel/untunedxgboost/trainscaler.pkl"
    modeladress = r"/data/debasish/cloudetectionmodels/cloudtopheightmodel/untunedxgboost/xgboostcloudtopheightuntunedironly.pkl"

    with open(scalaradress, 'rb') as file:
        scaler = pickle.load(file)

    with open(modeladress, 'rb') as file:
        model = pickle.load(file)

    dfirdatascaled = scaler.transform(dfirdata[['btmir','bttir1','bttir2','insatcorvislat']])
    print(dfirdatascaled.shape)

    heighprediction = model.predict(dfirdatascaled)
    dfirdata['heightprediction'] = heighprediction
    
    extent = extent

    fig = plt.figure(figsize=(10,8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    dfirdata[dfirdata['heightprediction']<0] = np.nan

    plot = plt.scatter(
                        dfirdata['insatcorvislon'][0:extent],
                        dfirdata['insatcorvislat'][0:extent],
                        c=dfirdata['heightprediction'][0:extent],
                        cmap=cmap,
                        transform=ccrs.PlateCarree(),
                        s=0.05
                        )
    
    ax.set_global()
    ax.coastlines()
    ax.gridlines()

    #Make longitude and latitude tick labels
    ax.set_xticks(np.arange(-180,180,20),crs=ccrs.PlateCarree())
    #Rotate xtixk labels using single line
    #plt.xticks(rotation = 90)
    ax.set_extent([-10,160,-85,85], crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(-90,90,10),crs=ccrs.PlateCarree())
    plt.grid(True)


    insatdate = str(insatfile.attrs['Acquisition_Date'])[2:-1]
    insattime = str(insatfile.attrs['Acquisition_Time_in_GMT'])[2:-1]
    acqstart = str(insatfile.attrs['Acquisition_Start_Time'])[2:-1].split('T')[1]
    acqend = str(insatfile.attrs['Acquisition_End_Time'])[2:-1].split('T')[1]   
    year  = int(insatdate[-4:])
    month_abbreviation = insatdate[2:5]
    month_number = datetime.datetime.strptime(month_abbreviation, '%b').month
    day   = int(insatdate[0:2])
    hour  = int(insattime[:2])
    minute = int(insattime[2:4])
    date = datetime.datetime(year,month_number,day,hour,minute,second=0)
    
    if nightshade == 'Yes':
        ax.add_feature(Nightshade(date, alpha=0.5))
    cbar = plt.colorbar(plot,orientation='horizontal',pad=0.039, fraction=0.019, aspect=50)
    cbar.set_label('Cloud Top Height (km)')
    plt.title('Uppermost cloud layers top height prediction by {} model \n Date: {}, Acquisition time: {}-{} (GMT) \n Mean={:.2f}km,25%={:.2f}km,50%={:.2f}km,75%={:.2f}km,Max={:.2f}km'.format(type(model).__name__,insatdate,acqstart,acqend,
                                                                                                                                                                                                                                                                                                                                                                                                                    dfirdata['heightprediction'].mean(),
                                                                                                                                                                                                    dfirdata['heightprediction'].quantile(0.25),
                                                                                                                                                                                                    dfirdata['heightprediction'].quantile(0.5),
                                                                                                                                                                                                    dfirdata['heightprediction'].quantile(0.75),
                                                                                                                                                                                                    dfirdata['heightprediction'].max())
             )
    
    plt.show()

    return dfirdata

#Example given below

insatcloudheightprediction(insatfilepath=r'/data/debasish/insatdata/l1b/2019/2019jan/day01/3RIMG_01JAN2019_0315_L1B_STD_V01R00.h5');

