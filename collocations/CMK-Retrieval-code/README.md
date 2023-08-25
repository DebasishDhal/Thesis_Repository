To benchmark our model's accuracy, we also need to check how well the cloudy/clear mask provided by the Indian Meteorological Department performs. The IMD cloudy/clear mask is collocated against
real-time observation from CLOUDSAT to check its accuracy.

This is the code required to do the collocation. 

Note that we do not need to do this for cloud height or cloud thickness as IMD doesn't provide its own maps for these two parameters.
