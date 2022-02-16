TBD - Unfinished
# Identifying Possible Mining Regions With Sentinel Data
#### Started: 2/10/2022
## Purpose
Determine which smaller regions within an area may be potential mining spots based on index and band values in a given year.

## Data Sources
[Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD) \
[Sentinel-2 MSI: MultiSpectral Instrument, Level-2A](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) \

## Specifications
Composite images created using median composites of an entire year \
Sentinel-2 images selected based on "CLOUDY_PIXEL_PERCENTAGE" less than 20% \
Sentinel-1 images selected based on the following properties:
- "instrumentMode" = IW (Interferometric Wide)
- "orbitProperties_pass" = Descending
- "resolution_meters" = 10 

Square Region Size: 0.005X0.005 (LatitudeXLongitude) \
Selected Indices (Using Sentinel-2 data):
- Normalized Difference Vegetation Index (NDVI)
  - (B8 - B4) / (B8 + B4)
- Normalized Difference Moisture Index (NDMI)
  - (B8 - B11) / (B8 + B11)
- NIR/SWIR2
  - (B8 - B12) / (B8 + B12)
- NIR/G
  - (B8 - B3) / (B8 + B3)
- IRON
  - (B4 - B2) / (B4 + B2)

Band Names:
- B2 = BLUE
- B3 = GREEN
- B4 = RED
- B8 = NIR (Near Infrared)
- B11 = SWIR1 (Shortwave Infrared 1)
- B12 = SWIR2 (Shortwave Infrared 2)

## Routines Deployed
1. Select rectangular regions of interest that can be tested for mining areas.
2. Input desired region under "area" variable, and desired year under "year" variable. Possible years range from 2018-2021. 
3. Create a composite image for the given year using the RED, GREEN, and BLUE bands from the Sentinel-2 data for the selected region.
4. Createa a composite image for the given year using the VH and VV bands from the Sentinel-1 data for the selected region.
5. Compose a function that divides that given region of interest into smaller, evenly spaced square regions of 0.005X0.005 (LatitudeXLongitude). Note this may cause some uneven regions if the given rectangular area does not divide evenly into regions of 0.005X0.005.
6. Compose a function that extracts the mean value for NDVI for a given region and year.
7. Compose a function to determine which square regions have an average NDVI lower than 0.4, and adds the passing regions into a list. \
   a) Take that list and create a multipolygon. Add this to the map as a layer named "Pass", along with the composite image for the entire original region. \
   b) Within the "Pass" layer, use the NDVI index to map possible mines in purple. \
   c) Within the "Pass" layer, use the NDMI and NIR/G indices, along with the "VV" band from Sentinel-1, to map possible water/tailing ponds in blue. \
   d) Within the "Pass" layer, use the IRON index to map possible infrastructure in gray. 

## Breakdown of Files 
SquaresPerYear.ipynb: Squares created are .01x.01 \
SquaresPerYear_0.005.ipynb: Squares created are .005x.005

## Illustrations

## Insights and Conclusions

## Future Work
2. Update the function that divides the regions so that it takes an arbitrary geometry and divides it into equally spaced regions, regardless of size
5. Refine code so that coltan mines specifically can be highlighted - will require more literature review on spectral signatures of coltan and how coltan mining process is different from other minerals (is the set up of the site distinct?)
6. Add in additional indices
