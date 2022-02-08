TBD - Unfinished
# Identifying Possible Mining Regions With Modis Data

## Purpose

## Data Sources
[MODIS Terra Vegetation Indices 16-Day Global 250m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13Q1) \
[MODIS Nadir BRDF-Adjusted Reflectance Daily 500m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A4) \
[Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD) \
[Sentinel-2 MSI: MultiSpectral Instrument, Level-2A](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) \
[USGS Landsat 8 Level 2, Collection 2, Tier 1](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2)

## Specifications
Years: 2004-2020 \
Composite images created using median composites of an entire year \
Square Region Size: 0.05X0.05 (LatitudeXLongitude) \

## Routines Deployed
1. Select rectangular regions of interest that can be tested for mining areas.
2. Create a composite image for 2020 using the RED, GREEN, and BLUE bands from the Sentinel-2 data for the selected region.
3. Createa a composite image for 2020 using the VH and VV bands from the Sentinel-1 data for the selected region.
4. Compose a function that divides that given region of interest into smaller, evenly spaced square regions of 0.05X0.05 (LatitudeXLongitude). Note this currently requires the points to be hardcoded, and will have some uneven regions if the given rectangular area does not divide evenly into regions of 0.05X0.05.
5. Compose a function for each desired index/ratio that creates the given index for a region of interest for the starting year and ending year of the desired time-frame

## Illustrations

## Insights and Conclusions

## Future Work
1. Update the function that divides the regions so that it takes in a geometry
2. Update the function that divides the regions so that it takes an arbitrary geometry and divides it into equally spaced regions, regardless of size
3. test code on large scale region using HPC
4. test that the code works on other areas of the DRC and picks up various types of mines
5. refine code so that coltan mines specifically can be highlighted - will require more literature review on spectral signatures of coltan and how coltan mining process is different from other minerals (is the set up of the site distinct?)
6. add in even more indices?
7. make the regions smaller
