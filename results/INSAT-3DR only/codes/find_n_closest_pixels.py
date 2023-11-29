#Takes in a L1B file, a latitude (lat_user) and longitude (lon_user) of user's choice.
#Output = n nearest pixels to that (lat_user,lon_user) coordinate. The pixels can be of any channel array of user's choice (VIS, WV, or TIR)

import geopy.distance
import h5py

#Logic - We find the closest pixel to a given coordinate, let the offset be x. Now we set that offset x to be infinity. 
#Now we get the second closest pixel, the offset is again set to infinity. This continues till n closest points are obtained

def findclosest(insatfileorpath ,lat, lon, n=5, channel='tir1', output = 'coordinates'):

    if type(insatfileorpath)==str:
        insatfile=h5py.File(insatfileorpath,'r')
    else:
        insatfile=insatfileorpath

    if channel in ['tir1','tir2','mir']:
      lat_arr=np.ma.masked_equal(np.array(insatfile['Latitude']),32767)/100
      lon_arr=np.ma.masked_equal(np.array(insatfile['Longitude']),32767)/100

    if channel in ['vis','swir']:
      lat_arr=np.ma.masked_equal(np.array(insatfile['Latitude_VIS']),32767)/1000 #Note how the scale is different for different channels
      lon_arr=np.ma.masked_equal(np.array(insatfile['Longitude_VIS']),32767)/1000

    if channel in ['wv']:
      lat_arr=np.ma.masked_equal(np.array(insatfile['Latitude_WV']),32767)/100
      lon_arr=np.ma.masked_equal(np.array(insatfile['Longitude_WV']),32767)/100
        
    combined_difference_copy=np.abs(lat_arr-lat)+np.abs(lon_arr-lon) 
    combined_minimum_index=np.unravel_index(combined_difference_copy.argmin(),combined_difference_copy.shape)
    combined_minimum=combined_difference_copy[combined_minimum_index] #Closest pixel in (lat,lon)

    indices = []
    for _ in range(n-1):
      index=np.unravel_index(combined_difference_copy.argmin(),combined_difference_copy.shape)
      indices.append(index)
      combined_difference_copy[index]=np.inf #Setting the nearest pixel's distance from the (lat_arr,lon_arr) to infinity
      
    indices.sort(key=lambda x:geopy.distance.distance((lat,lon),(lat_arr[x[0]][x[1]],lon_arr[x[0]][x[1]])).km)

    if output == 'indices':
      return indices
    else:
      list_of_nearest_coordinates = [(lat_arr[i[0]][i[1]],lon_arr[i[0]][i[1]]) for i in indices]
      return list_of_nearest_coordinates


if __name__ == '__main__' 
    file=r"C:\Users\HP\OneDrive\Desktop\HD5 Collection\L1B data\INSAT-3DR\3RIMG_01APR2022_0015_L1B_STD_V01R00.h5"
    
    point = [30,77]
    coords = findclosest(file,point[0],point[1],10,'vis','coordinates')
    
    
    for i in range(len(coords)):
        print("Pixel coords = {}, Offset = {} ".format(coords[i],geopy.distance.distance(coords[i], point).km))


#Output : - (A commented output has been given below, the descending order of offset is proof that this function is working as intended)

# Pixel coords = (29.999, 77.0), Offset = 0.11085243406840489 
# Pixel coords = (29.999, 77.01), Offset = 0.9712146121809441 
# Pixel coords = (29.999, 76.989), Offset = 1.0671276542774186 
# Pixel coords = (30.01, 77.0), Offset = 1.1085252676742565 
# Pixel coords = (29.987, 76.999), Offset = 1.4443072140731923 
# Pixel coords = (30.01, 76.989), Offset = 1.5346586569364198 
# Pixel coords = (30.01, 77.011), Offset = 1.5346586569364198 
# Pixel coords = (29.999, 77.021), Offset = 2.029252082977216 
# Pixel coords = (30.021, 77.0), Offset = 2.3279050090692475 
