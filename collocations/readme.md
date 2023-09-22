This folder contains the codes for collocation. For the most part, collocation here is defined as collecting radiometric data from INSAT-3DR and cloud-properties data from CloudSat, with a certain tolerable
temporal and spatial offset. The temporal offset is 30 minutes and the spatial offset is 1 km in this case. In fact, the maximum spatial offset is reduced to 0.55 km through filtering, while using
the data. 

The same logic has also been used to collocate Cloud-Mask produced by Indian Meteorological Department with the cloud-properties data from CloudSat. This particular step is for validation of Cloud-Mask from IMD.

# Contents

- Collocation code for single file and single day. The single file takes one CloudSat file and one INSAT-3DR file, produces a map with all the necessary information and asks the user the permission to collocate. Such an image is provided below.

<p align= "center">
  <img src="../cloudsatorbit/Actual photo used in collocation INSAT cloudsat combined.png" alt="">
</p>

  
This is laborious, hence, it has been automated in the single day file. It takes all CloudSat and INSAT-3DR files for one day and does the collocation for all the combinations that match the collocation criteria.

- CMK collocation. CMK is short for Cloud Mask. We have CMK files from IMD (Indian Meteorological Department). In order to compare our model's performance with IMD, we need to compare the CMK produced by IMD with CloudSat readings.
For this, collocating CMK files against CloudSat readings is required.

- SWIR retrival is an error-correction folder. During our main collocation process, I had forgotten to include the SWIR channel in the collocation. Hence, the resulting dataset did not contain
  any SWIR data. To rectify this, a short script was prepared which will append the SWIR channel data to the dataset. This is more of an array operation as compared to collocation.
