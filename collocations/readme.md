This folder contains the codes for collocation. For the most part, collocation here is defined as collecting radiometric data from INSAT-3DR and cloud-properties data from CloudSat, with a certain tolerable
temporal and spatial offset. The temporal offset is 30 minutes and the spatial offset is 1 km in this case. In fact, the maximum spatial offset is reduced to 0.55 km through filtering, while using
the data. 

The same logic has also been used to collocate Cloud-Mask produced by Indian Meteorological Department with the cloud-properties data from CloudSat. This particular step is for validation of Cloud-Mask from IMD.

# Contents

- Collocation code for single file and single day. The single file code takes one CloudSat file and one INSAT-3DR file, produces a map with all the necessary information and asks the user the permission to collocate. Such an image is provided below. In the image below, both the CloudSat and INSAT-3DR files are from the same date. Notice that there is a temporal and spatial overlap between both the coverage area of both the files from 0815 hours till 0841 hours, in between the area from Antarctica till western India. Thus, we can go ahead for the collocation with this particular combination of files. 

<p align= "center">
  <img src="../cloudsatorbit/Actual photo used in collocation INSAT cloudsat combined.png" alt="">
</p>

  
Analyzing all these maps is laborious. Hence, this process of choosing the correct combination of CloufSat and INSAT-3DR file has been automated in the single day code. It takes all CloudSat and INSAT-3DR files for one day and does the collocation for all the combinations that match the collocation criteria, i.e. there must be a temporal and spatial overlap between both the files.

- CMK collocation. CMK is short for Cloud Mask, or a geo-referenced file that shows which pixel is cloudy and which is clear. We have CMK files from IMD (Indian Meteorological Department). In order to compare our model's performance with IMD, we need to compare the CMK produced by IMD with CloudSat readings. The CloudSat readings are taken as the truth value since it physically detects clouds through active scanning.
For this, collocating CMK files against CloudSat readings is required.

- SWIR retrival is an error-correction folder. During our main collocation process, I had forgotten to include the SWIR channel in the collocation. Hence, the resulting dataset did not contain any SWIR data. To rectify this, a short script was prepared which will append the SWIR channel data to the dataset. This is more of an array operation as compared to collocation.
