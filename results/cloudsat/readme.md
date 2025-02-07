# Cloudsat only results
This folder consists of analysis based on data from CloudSat satellite alone. It's divided into 3 sections. The 2B-CLDCLASS CloudSat data (for daytime only) from the entire year 2013 was analyzed.
## Cloud cover over land and ocean ([Code1](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudpresence/codes/monthly_cloud_presence.py),[Code2](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudpresence/codes/monthly_cloud_presence.py))
On an average what fraction of the total land area is covered by clouds? What is the case with oceanic areas? Is there a difference between cloud covers of both regions?

- Oceans are more likely to be cloudy as compared to land. Over the year, around 78% of oceanic pixels and 62.9% of land pixels were found to be cloudy. This
inequality in cloud cover was found to be consistent throughout the year.
- Similarly, 21.4% of all oceanic pixels and 37.1% of all land pixels were found to be clear. So, on an average, sky over land is twice as more likely to be clear as compared to sky over sea/ocean.
-  This probability of ”cloudiness” over both land and ocean is at its maximum during May-June-July-August.

<p align= "center">
  <img src="cloudpresence/year2013whatpercentagelandiscloudy.png" alt="Cloud distribution over land and sea">
</p>

## Cloud height distribution ([Code1](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudheight/codes/full_year_cloud_height.py),[Code2](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudheight/codes/monthly_cloud_height.py),[Code3](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudheight/codes/monthly_cloud_height_change.py))
- Please check the photos done of the cloud mean top-height, mean base-height and mean thickness in the folder above.
- The analysis has been done on different cloud types separetly. We're considering 8 distinct cloud types here.
- In addition, a time-series graph has also been provided to track the change in cloud height over the months.

Below are some of the findings of the analysis:

- Cirrus is the only type of cloud with a high base and high top height. As a result, it has a low thickness.
- Nimbostratus and deep convective clouds have their base at low heights but top at very high altitudes. Hence, they have a large thickness
-  Stratus, stratocumulus, and cumulus clouds have low base and top heights. Their thickness is comparable to that of cirrus clouds as a result.

<p align= "center">
  <img src= "cloudheight/images/fullyearcloudheight.png" alt = "Top height, Base height and Mean thickness of different cloud types">
  <img src= "cloudheight/images/cloudheoghttimeserieslogscale.png" alt = "Top height, Base height and Mean thickness of different cloud types">
</p>

## Cloud type distribution ([Code1](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudtypedistribution/codes/full_year_cloud_type_distribution.py),[Code2](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudtypedistribution/codes/monthly_cloud_distribution.py))

Here as well, 8 distinct cloud types have been considered. Cloud types are distributed unevenly as a function of latitude. Some findings of the analysis are as: 
- Cirrus clouds are the most dominant clouds in tropical regions. The frequency of occurrence of cirrus clouds (or fractional abundance) decreases from 33% in tropical regions to 7% in polar regions.
- Cirrus and stratocumulus clouds form the bulk of clouds all over the globe, and their presence is almost inverse of each other.
- Deep convective clouds comparatively have very low occurrences and are primarily concentrated in tropical regions.

<p align= "center">
   <img src= "cloudtypedistribution/images/fullyearcloudtypemap.png" alt = "Distribution of different cloud types as a function of Latitude">
</p>




