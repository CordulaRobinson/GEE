# Supervised Classification: Albany Metropolitan Area

These scripts use the Google Earth Engine API to perform supervised classifications on the Albany Metropolitan Area using remote sensing imagery and a Random Forest algorithm. 
Each image pixel is labeled as one of four discrete categories.
* Urban
* Bare
* Vegetation
* Water

Training data was manually labeled using geometry tools from Google Earth Engine's code editor. Classifications were performed using datasets from 
[Sentinel-2](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) and 
[Landsat](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) satellites.
