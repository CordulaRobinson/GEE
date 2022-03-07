The CongoMinesSAR.ipynb file contains a script for Google Earth Engine through the Python API. 
This script focuses on a selected area in southern DRC, near a concentrated area of known mines. 
This calculates images for a year-long period for 2019, 2020, and 2021.
Sentinel-2 data is used to calculate true color composite images for each year, along with the NDVI, NDMI, and NIR/G indices. 
Sentinel-1 Radar data is used to show the VH, VV, VH/VV, and VV/VH values for each year. 
Calculations for each of the above bands are combined with the index values from Sentinel-2, to create water and mining estimates for each year.
A false color composite of the VH and VV bands is also created.
