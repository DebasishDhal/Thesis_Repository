# Thesis_Repository
This repository consists of codes I wrote/used for my MSc thesis work

collocations folder contains collocation code for INSAT-3DR 1B-IMAGER and CloudSat 2B-CLDCLASS data. The goal is to collocate pixels close by spatially and temporally, 
and collect radiometric information about the pixel from INSAT-3DR file and cloud related data from CloudSat file. I've included codes to collocate one file at a time
and files of entire day at a time (fully automated). In the examples, there's an example notebook, 3 cells are present there, each containing code for single file collocation.
In the first 2 cells, the permission to collocate was denied, while it was granted in the 3rd cell. This process has automated in the fulldaycollocation code.
