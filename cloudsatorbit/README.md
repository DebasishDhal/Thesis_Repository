This directory contains various output images of CloudSat orbit(s) and photos about how CloudSat scans the Earth's atmosphere. This is the first step of my work related to CloudSat, which includes plotting groundtracks along with proper time stamps, color coding as per different parameters. 

Let's say we want to see the cloud top height as measured by CloudSat during one orbit. We can easily plot it by making the color of the groundtrack, a function of the parameter (here, cloud top height).

- Groundtrack is the path traced on Earth, by a satellite, as it moves along its orbit.

- The instantaneous scanning area of CloudSat is 1.3 km × 1.7 km. A smaller instantaneous scanning area (or pixel size) it makes our task a lot simpler, as compared to satellites who do sideways scan. 

- CloudSat completes 14-15 orbits per day. It traces the exact same groundtrack after an interval of 16 days. 

Below is a short description of how the CloudSat orbits around the Earth and how it scans the atmosphere.

# Orbit
- Visualization of a single orbit of CloudSat, on a given random day.
  
<p align= "center">
  <img src="CloudsatGroundtrack26Apr2019.jpg" alt="Cloudsat single orbit">
</p>

- Visualization of the total cloud thickness, as measured by CloudSat, in a single orbit.
  
<p align= "center">
  <img src="Total cloud thickness sample result.jpg" alt="Total cloud thickness plot">
</p>

- 3D visualization of all CloudSat orbit of a given single day. 
<p align= "center">
  <img src="Groundtrack cloudsat.jpg" alt="Cloudsat orbit 3D">
</p>

- All orbits of CloudSat for one day, in a 2D projection.
<p align= "center">
  <img src="Multi orbit groundtrack.png" alt="Many cloudsat orbits at once">
</p>

- All orbits of CloudSat for one day, along with start time and INSAT-3DR satellite's coverage area.
<p align= "center">
  <img src="Multi orbit groundtrack with INSAT3DR with start time.png" alt="Cloudsat orbit with insat coverage and start time">
</p>
    
# Scanning

- Visulization of how CloudSat scans the Earth's atmosphere. In one orbit, it scans the atmosphere 37,088 time. Each scan is of an area 1.1 km (along the orbit) × 1.7 km (across the orbit).
  Vertically, each scan spans an area from the Earth's surface till 30 km of altitude. Each scan is divided into 125 bins, with each bin being 240 m thick. (Photo taken from ccplot manual)
<p align= "center">
  <img src="Cloudsat scan.jpg" alt="How cloudsat scans">
</p>


Codes can be found here 

https://github.com/DebasishDhal/Thesis_Repository/blob/main/miscellaneous/csatdatareading.pdf 

It's in pdf form as in notebook form, it's more than 25MB. 
