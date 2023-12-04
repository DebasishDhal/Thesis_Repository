# Variation in Solar elevation angle, exactly six months apart ([Code](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/INSAT-3DR%20only/codes/solar_elevation_angle.py))

- The two pictures are taken at an interval of exactly six months, at the same GMT. One is in the Summer Solstice, another in the Winter Solstice.
-  It can be observed that the solar elevation angles in the two images are complementary to each other, and so are the day-night divider lines.

<p align= "center">
  <img src="variation in solar elevation with season.png" alt="Variation in solar elevation angle within a span of six months">
</p>

# Dependency of VIS (Visible) and SWIR (Short-Wave Infrared) channels on sunlight ([Code](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/INSAT-3DR%20only/codes/insat_channel_plot.py))

- Below is a plot for all 6 channels of INSAT-3DR IMAGER.
- It's 0515 hours (GMT), and the month is January (Winter solstice), so the sun would be more inclined towards teh Souther Hemisphere, which is the case here.
- For the first two plots, it's night in the darker part of the globe and day in the brighter parts.
- Such a sharp contrast is not observed in the rest of the four plots.
- It's because the first two channels are Visible and Short-wave Infrared Channel, whose most of the contributions come from sunlight reflected from earth. The rest of the four channels are thermal channels, whose most of the contributions come from the thermal waves emitted from the Earth.

  <p align= "center">
   <img src= "../../miscellaneous/images/Allchannelsplot.png" alt = "Distribution of different cloud types as a function of Latitude">
</p>

# Cooler brightness temperature for higher clouds ([Code](https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/INSAT-3DR%20only/codes/insat_channel_plot_globe.py))
A cyclone has clouds with high altitude, high especially compared to its neighborhood. This plot is for Fani cyclone, just before its landfall. Now, there are clouds in the cyclone for sure, and those have less brightness temperature, as compared to its sorroundings. This is a proof that the higher we go, the lesser the brightness temperature becomes, as a general trend.

<p align="center">
  <img src="../../miscellaneous/images/Fani BT plot.png" width="45%" alt="Image 2">
  <img src="../../miscellaneous/images/Fani radiance plot.png" width="45%" alt="Image 1">
</p>
