While collocating CloudSat data against INSAT-3DR data, I considered 4 channels only, i.e. VIS, MIR, TIR1 & TIR2. The WV channel wasn't considered since it has a 
resolution of 8km (too high). Howver, INSAT-3DR Imager has 6 channels, the other one being SWIR channel (Short Wave Infrared), with a resolution of 1km. This could have 
been collocated but I forgot about while running my collocation code. So, to append the collocated data from MIR to the collocated dataset, I ran this short script.

To run this script for the full year, I didn't take more than a week. The core of this script is not doing max and min of an array (which was the case during collocation),
but to using array indices to find some number stored in it, which is significantly faster. 

Since this collocation is considerably fast, I mae 31 notebooks, each for one day. So notebook no. 2 will contain the SWIR retrieval for all the files, for the 2nd day of all the months.
Such a notebook is here - https://github.com/DebasishDhal/Thesis_Repository/blob/main/collocations/SWIR-retrieval-code/swir_retrieval_output_day2_all_months.ipynb


