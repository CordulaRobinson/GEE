The CongoMinesSAR.ipynb file contains a script for Google Earth Engine through the Python API. 
This script focuses on a selected area in southern DRC, near a concentrated area of known mines. 
This calculates images for a 6 month period in both 2019 and 2021
Sentinel-2 data is used to calculate true color composite images for both years, along with the NDVI index. 
Sentinel-1 Radar data is used to show the VH values for both years. 
The script calculates areas with the lowest VH values and marks them as water.
Areas with VH values that are low but not as low as the 'water' values are marked as possible mines.
Finally, the possible mine values are combined with low NDVI values to create a mine estimate for both years. 
