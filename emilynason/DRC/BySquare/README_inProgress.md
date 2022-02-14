TBD - Unfinished - Illustrations, Conclusions not completed
# Identifying Possible Mining Regions With MODIS Data
#### Started: 2/03/2022
## Purpose
Determine which smaller regions within an area may be potential mining spots based on initial index values and changes over time.

## Data Sources
[MODIS Terra Vegetation Indices 16-Day Global 250m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13Q1) \
[MODIS Nadir BRDF-Adjusted Reflectance Daily 500m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A4) \
[Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD) \
[Sentinel-2 MSI: MultiSpectral Instrument, Level-2A](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) \

## Specifications
Years: 2004-2020 \
Composite images created using median composites of an entire year \
Sentinel-2 images selected based on "CLOUDY_PIXEL_PERCENTAGE" less than 20% \
Sentinel-1 images selected based on the following properties:
- "instrumentMode" = IW (Interferometric Wide)
- "orbitProperties_pass" = Descending
- "resolution_meters" = 10 

Square Region Size: 0.05X0.05 (LatitudeXLongitude) \
Selected Indices (Using MODIS data):
- Normalized Difference Vegetation Index (NDVI)
  - MODIS Vegetation NDVI band used, with values ranging from -2,000 to 10,000
- Normalized Difference Moisture Index (NDMI)
  - (Band2 - Band6) / (Band2 + Band6)
  - Band2 = NIR, Band6 = SWIR1
- NIR/SWIR2
  - (Band2 - Band7) / (Band2 + Band7)
  - Band2 = NIR, Band7 = SWIR2

Additional Indices (Using Sentinel-2 data):
- NDMI
  - (B8 - B11) / (B8 + B11)
  - B8 = NIR, B11 = SWIR1
- NIR/G
  - (B8 - B3) / (B8 + B3)
  - B8 = NIR, B3 = GREEN
- IRON
  - (B4 - B2) / (B4 + B2)
  - B4 = RED, B2 = BLUE

## Routines Deployed
1. Select rectangular regions of interest that can be tested for mining areas.
2. Create a composite image for 2020 using the RED, GREEN, and BLUE bands from the Sentinel-2 data for the selected region.
3. Createa a composite image for 2020 using the VH and VV bands from the Sentinel-1 data for the selected region.
4. Compose a function that divides that given region of interest into smaller, evenly spaced square regions of 0.05X0.05 (LatitudeXLongitude). Note this currently requires the points to be hardcoded, and will have some uneven regions if the given rectangular area does not divide evenly into regions of 0.05X0.05.
5. Compose a function for each desired index/ratio that creates the given index for a region of interest for the starting year and ending year of the desired time-frame.
6. Compose a function for each index that extracts the mean value for that index for a given region for the start and end year.
7. Compose a function for each index that sets the desired requirements for a region to be considered a mining area. These include a baseline level for the start year OR a specified level of change between the start and end year.
8. Compose a function that incorporates all of steps 5-7 for each index. This function will test each region with each index. If a region passes the requirements for all indices, it will be added to the map as a composite image from the Sentinel-2 data for the end year, created in step 2. Additionally, for passing regions, this function will incorporate the NDMI and NIR/G ratios, along with the VV band from Sentinel-1, to map out potential water storage/sources for a mining area. Lastly, for passing regions, this function will use the IRON index to map out potential infrastructure for a mining area. These indices were calculated using the Sentinel-2 data for 2020. 

## Breakdown of Files 
ModisMineSquares_OnlyNDVI.ipynb
- Only the NDVI index is incorporated in this file. 
ModisMineSquares_Separate.ipynb
- This file has all indices, however they are separated. Each index has a result map of regions that pass that index specifically
ModisMineSquares.ipynb
- This has all indices, and compiles them into one function. There is one resulting map, that only has the regions that passed all index requirements

## Illustrations

## Insights and Conclusions

## Future Work
1. Update the function that divides the regions so that it takes in a geometry
2. Update the function that divides the regions so that it takes an arbitrary geometry and divides it into equally spaced regions, regardless of size
3. Test code on large scale region using HPC
4. Test that the code works on other areas of the DRC and picks up various types of mines
5. Refine code so that coltan mines specifically can be highlighted - will require more literature review on spectral signatures of coltan and how coltan mining process is different from other minerals (is the set up of the site distinct?)
6. Add in additional indices
7. Make the regions smaller
