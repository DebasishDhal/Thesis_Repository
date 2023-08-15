# Thesis_Repository
This repository consists of codes I wrote for my MSc thesis work

collocations folder contains collocation code for INSAT-3DR 1B-IMAGER and CloudSat 2B-CLDCLASS data. The goal is to collocate pixels close by spatially and temporally, 
and collect radiometric information about the pixel from INSAT-3DR file and cloud related data from CloudSat file. I've included codes to collocate one file at a time
and files of entire day at a time (fully automated). In the examples, there's an example notebook, 3 cells are present there, each containing code for single file collocation.
In the first 2 cells, the permission to collocate was denied, while it was granted in the 3rd cell. This process has been fully automated in the fulldaycollocation code. For an entire day it takes around 40-120 hours. 

The goal of the collocation process is to generate a dataset which has radiometric data and the correponding cloud-related data. The cloud-related data includes (No. of separate cloud layers, their top and base height, type). Thus it gives us relation between radiometric data and cloud-related data.

Our goal is to use the radiometric data to predict the cloud-parameters, i.e. Cloudy/Clear (Whether a pixel has clouds or not), Cloud top height and Total Cloud thickness over a pixel of area 4km * 4km.

## Cloud/Clear Model

- Day-time model to predict cloudy/clear classification has an overall accuracy of 79.84%, which predicts 71.06% of all clear pixels and 84.95% of the cloudy pixels correctly.
- Night-time model to predict cloudy/clear classification has an overall accuracy of 78.90%, which predicts 73.48% of all clear pixels and 82.18% of the cloudy pixels correctly.

- 
