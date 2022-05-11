# Supervised Classification: Albany Metropolitan Area

These scripts use the Google Earth Engine API to perform supervised classifications on the Albany Metropolitan Area using remote sensing imagery and a Random Forest algorithm.   

Training data was manually labeled using geometry tools from Google Earth Engine's code editor. Classifications were performed using datasets from 
[Sentinel-2](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) and 
[Landsat](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) satellites.

Each image pixel is labeled as one of four discrete categories:
| Color | Label      |
| ----- | -----      |
| gray  | urban      |
| red   | bare       |
| green | vegetation |
| blue  | water      |

### USGS Landsat 8 Level 2, Collection 2, Tier 1
![](https://github.com/CordulaRobinson/GEE/blob/raymondeah/tutorials/supervised_classification_albany/images/landsat_albany_classified.PNG)

### Sentinel-2 MSI: MultiSpectral Instrument, Level-2A
![](https://github.com/CordulaRobinson/GEE/blob/raymondeah/tutorials/supervised_classification_albany/images/s2_albany_classified.PNG)
