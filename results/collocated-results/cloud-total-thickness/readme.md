Below are results for total cloud thickness model.

- All the channels of INSAT-3DR except Water Vapor channel were employed in the the model. However, it can be employed in the night time as well, since the XGBoost model is accomodative to NaN values. In addition, the infrared channels carry the bulk of the importance in the model, so it's safe to rely only on them in the night time.
- The model shows a value of 0.90 with a mean squared error of 0.99km on the test set.
- In this model, the TIR2 (11.5-12.5 μm) channel carries the highest importance in the model (63.60%).
- Here, we are not considering the optical depth of clouds, since it was not included in the 2B-CLDCLASS file. We suspect that this contributes the most to the error.

<p align= "center">
  <img src="thicknesscorrelationheatmap.png" alt="">
</p>
<p align="center" style="font-size: 50px;"><strong>Correlation (Pearson) map of cloud total thickness with Albedo, SWIR Radiance, MIR, TIR1 and TIR2 Brightness Temperatures</strong></p>


Some maps (for total cloud thickness) produced by our models have been included in this folder. Please note that the blank areas in the maps are those zones where our model is not working properly, i.e. it is predicting negative numbers as cloud thickness. Out of the three models developed by us, we have the least confidence on this model. 

******************************************************************************************************************************************************************************************

<p align="center"> <strong>01/January/2019</strong> </p>

<p align="center">
  <img src="01Jan2019_0315.png">
</p>

******************************************************************************************************************************************************************************************

<p align="center"> <strong>01/April/2019</strong> </p>

<p align="center">
  <img src="01Apr2019_0315.png">
</p>

******************************************************************************************************************************************************************************************

<p align="center"> <strong>01/August/2019</strong> </p>

<p align="center">
  <img src="01Aug2019_0315.png">
</p>

******************************************************************************************************************************************************************************************

<p align="center"> <strong>01/December/2019</strong> </p>

<p align="center">
  <img src="01Dec2019_0315.png">
</p>


