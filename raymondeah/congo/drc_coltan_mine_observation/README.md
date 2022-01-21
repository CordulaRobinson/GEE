# Observation of Coltan Mines in the Democratic Republic of the Congo

## Overview

The Democratic Republic of the Congo is a leading producer of coltan, an ore from which the rare earth element Tantalum (Ta) can be extracted. Tantalum is in very high demand due to its use in creating electronic capacitors that are used in a wide variety of modern technologies. These methods serve as an introduction to a project in which we will attempt to identify and map Coltan mining sites across the Democratic Republic of the Congo using remote sensing.

## Objectives

+ Find existing datasets of known or possible mining sites in the DRC and overlay their locations onto the map using Google Earth Engine
+ Inspect active mining locations to find a small region with significant observable mining activity and change over time
+ Calculate the change in area over time of vegetation using classification methods
	+ Loss of vegetation may serve as a good indication of increased mining activity
	
## Datasets

[Sentinel-2 MSI: MultiSpectral Instrument, Level-2A](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR#description)


[FAO GAUL 500m: Global Administrative Unit Layers 2015, First-Level Administrative Units](https://developers.google.com/earth-engine/datasets/catalog/FAO_GAUL_2015_level1?hl=en)


[Known active artisinal mining sites in the eastern DRC](http://geo.ipisresearch.be/geoserver/web/wicket/bookmarkable/org.geoserver.web.demo.MapPreviewPage?0)  created by [IPIS Research](https://ipisresearch.be/home/maps-data/open-data/)


[Issued mining permits in the DRC](https://data.globalforestwatch.org/datasets/gfw::democratic-republic-of-the-congo-mining-permits/about) from Global Forest Watch

## Methods/Results

### Locations of known/possible mines using existing datasets:

#### Description

We found datasets of issued mining permits and active Coltan mines in the DRC and added their locations to the map. Locations of issued mining permits can represent possible locations of mines and/or areas where mines will be built in the future.

#### Routines:
                
1. Download the mining pemits and active mines datasets from Global Forest Watch and IPIS Reserach and upload to the Google Earth Engine code editor as assets
2. Import the datasets into the project file
3. Import the FAO GAUL dataset
4. Extract the geometry of the DRC by filtering the FAO GAUL dataset
5. Center the map around the DRC
6. Add the locations of issued mining permits as a layer to the map
![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_coltan_mine_observation/images/issued_mining_permits.PNG)
7. Filter the 'resource' property in the issued mining permits dataset to 'Ta' to extract locations of Tantalum mines
8. Add the locations of issued mining permits for Tantalum to the map
![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_coltan_mine_observation/images/issued_mining_permits_ta.png)
9. Add the locations of known active coltan mines as a layer to the map
![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_coltan_mine_observation/images/active_mines.png)
                

### Calculating Loss of Vegetation Using Classification:

#### Description

Using the IPIS Research data, I identified a small area of active mining in the South Kivu area. I focused in on this area for analysis and calculated the percentage loss in vegetation between 2019 and 2021 using classification methods.

#### Routines
                
1. Import the Sentinel-2 and active Coltan mines datasets into a project file in the Google Earth Engine Code Editor
2. Add the locations of active coltan mines a layer to the map
3. Use the drawing tools in the code editor to create a rectangle around the region of interest (South Kivu area)
4. Center the map around the region of interest
5. Filter the Sentinel-2 data to a cloud percentage of less than 20%, apply a cloud masking function, and filter to the bounds of the region of interest
6. Create a 'before' image by filtering the data in step 5 to the year 2019 and taking median values
7. Create an 'after' image by filtering the data in step 5 to the year 2021 and taking median values
8. Add the before and after images to the map as layers
9. Mark training data for water, vegetation, and bare ground as FeatureCollections using the point tool in the code editor. Assign a 'landcover' property with a unique value for each class
10. Classify both images using a Random Forest classifier and add as layers to the map
11. Add a layer to the map that shows all pixels that changed from vegetation to another class
12. Calculate the area of vegetation in both classifications
13. Determine the percentage change of vegetation between 2019 and 2021 ((2019 area - 2021 area) / (2019 area) ) * 100
                

#### Results
