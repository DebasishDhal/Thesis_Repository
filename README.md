# Retrieval of Earth's Atmospheric Properties using INSAT-3DR satellite data
This repository consists of codes I wrote for my MSc thesis work

## AIM
### 1) To predict cloud properties using the readings from INSAT-3DR geostationary satellite. <br>
### 2) To study clouds based on the data of CloudSat.

## Motivation
INSAT-3DR produces full-disk image of the Indian side of hte globe, every half an hour with a resolution of 1km, 4km and 8km. If we are succesful, we can have new new full-disk maps of cloud properties every half an hour.

## Challenge
INSAT-3DR, like all satellites that employ passive scanning, do not measure any meteorological parameter directly, they just measure the radiometric data that is incident on them. It is our job ot retrieve useful meteorological properties from the reading.

## Solution 
CloudSat satellite (a polar satellite), a NASA-operated satellite dedicated for observations of clouds, measures all the cloud-properties that we want to retrieve from INSAT-3DR. The cloud related data was colloacted against the radiometric readings from INSAT-3DR, the resulting data was fed into ML algorightms (XGBoost and Random Forest)

## Collocation process
Collocations folder contains collocation code for INSAT-3DR 1B-IMAGER and CloudSat 2B-CLDCLASS data. The goal is to collocate pixels close by spatially and temporally, 
and collect radiometric information about the pixel from INSAT-3DR file and cloud related data from CloudSat file. I've included codes to collocate one file at a time
and files of entire day at a time (fully automated). In the examples, there's an example notebook, 3 cells are present there, each containing code for single file collocation.
In the first 2 cells, the permission to collocate was denied, while it was granted in the 3rd cell. This process has been fully automated in the fulldaycollocation code. For an entire day it takes around 40-120 hours. 

The goal of the collocation process is to generate a dataset which has radiometric data and the correponding cloud-related data. The cloud-related data includes (No. of separate cloud layers, their top and base height, type). Thus it gives us relation between radiometric data and cloud-related data.

Our goal is to use the radiometric data to predict the cloud-parameters, i.e. Cloudy/Clear (Whether a pixel has clouds or not), Cloud top height and Total Cloud thickness over a pixel of area 4km × 4km.

## Cloud/Clear Classification Model

- Day-time model to predict cloudy/clear classification has an overall accuracy of 79.84%, which predicts 71.06% of all clear pixels and 84.95% of the cloudy pixels correctly.
- Night-time model to predict cloudy/clear classification has an overall accuracy of 78.90%, which predicts 73.48% of all clear pixels and 82.18% of the cloudy pixels correctly.
- Our models are compared with the classification produced by IMD. We cross-checked the classifications of IMD against the observed readings from CloudSat.
- It was found that IMD cloudy/clear classificaion has an overall accuracy of 77.18%, with an accuracy of 74% with clear pixels and 79% with cloudy pixels.

## Cloud top height Regression Model

- Only the Infrared channels of INSAT-3DR (dependent only on the Earth's thermal radiation) were used in this model, so that it can be used both during day and night.
- The model shows a $r^2$ value of 0.95 with a mean squared error of 1.10km in the test set.
- Using this model, it was found that the average global cloud top height is in the range 2-3 km throughout the year
- The TIR1 channel (10.3-11.3 μm) of INSAT-3DR has the highest importance in the model (69.05).

## Cloud total thickness Regression Model

- All the channels of INSAT-3DR except Water Vapor channel were employed in the the model. However, it can be employed in the night time as well, since the XGBoost model is accomodative to NaN values. In addition, the infrared channels carry the bulk of the importance in the model, so it's safe to rely only on them in the night time.
- The model shows a $r^2$ value of 0.90 with a mean squared error of 0.99km on the test set.
- In this model, the TIR2 (11.5-12.5 μm) channel carries the highest importance in the model (63.60%).
- Here, we are not considering the optical depth of clouds, since it was not included in the 2B-CLDCLASS file. We suspect that this contributes the most to the error.

## CloudSat only results 
We took all the 2B-CLDCLASS data from CloudSat for the year 2013 and analyzed it. Below are the findings : -

- Oceans are more likely to be cloudy as compared to land. Over the year, around 78% of oceanic pixels and 62.9% of land pixels were found to be cloudy. This inequality in cloud cover was found to be consistent throughout the year.
- The cloud top height (averaged over the globe) is in the order Cirrus ≈ Deep
Convective > Altostratus > Cumulus > Altocumulus > Stratocumulus ≈ Cumulus ≈ Stratus cloud. Deep convective clouds are the thickest, and Stratus clouds are the thinnest of all cloud types.
- For most practical purposes, there are at most five distinct cloud layers in any given atmospheric layer. More than five distinct cloud layers are extremely rare in nature.
- The distribution of different cloud types is a function of latitude. Cirrus is the most dominating type of cloud over the tropics and the Indian region, while Altostratus and Stratocumulus dominate in the polar regions. On the other hand, Stratus clouds are almost absent over the Indian region.

(Note that the CloudSat orbit scans only a very tiny section of the atmosphere at a time. We have assumed that taking a large number (a full year) of observed data points will get us an image that is resembles the true nature of earth's atmosphere).


