# Identifying Distinguishing Characteristics of Coltan Mining in the Democratic Republic of the Congo

## Overview

Exploratory analysis of distinguishing characteristics of Coltan mining. Focus on inspecting a wide variety of satelittes, band types, band ratios, and spectral indices. Searching for shared characteristics across a variety of mining areas for the purpose of creating an extensible detection model in the future.

## Objectives

1. region finding (clear and verifiable mining activity, 3 separate locations)
2. NDVI time series starting from before mine construction
3. view the following spectral indices and band ratios from 2014-2020:
	- NDVI (Normalized Difference Vegetation Index)
	+ VIGS (Vegetation Index considering Greenness and Shortwave infrared, outlined [here](https://www.sciencedirect.com/science/article/pii/S0034425715301577?via%3Dihub))
	+ NDMI (Normalized Difference Moisture Index)
	+ BSI (Bare Soil Index)
	+ Iron Concentration
	+ Clay Concentration
4. create time series of all, see what is significant and what is not
5. inspect cross sections of visual anomalies, look for significant band activity
6. inspect SAR data and look for any unique signatures

## Datasets

[USGS Landsat 8 Level 2, Collection 2, Tier 1](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2)

[Sentinel-2 MSI: MultiSpectral Instrument, Level-2A](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR#description)

[MOD13Q1.006 Terra Vegetation Indices 16-Day Global 250m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13Q1)

[Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD)

[FAO GAUL 500m: Global Administrative Unit Layers 2015, First-Level Administrative Units](https://developers.google.com/earth-engine/datasets/catalog/FAO_GAUL_2015_level1?hl=en)


[JRC Global Surface Water Mapping Layers, v1.3](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_3_GlobalSurfaceWater#description)

[Known active artisinal mining sites in the eastern DRC](http://geo.ipisresearch.be/geoserver/web/wicket/bookmarkable/org.geoserver.web.demo.MapPreviewPage?0)  created by [IPIS Research](https://ipisresearch.be/home/maps-data/open-data/)

## Methods

### 1. Region Finding

#### Description

Using the IPIS Research data, I identified a region in the northern DRC with active Coltan mining activity. Then, I chose 3 smaller locations within that region to focus my analysis on. Lastly, I attemped to verify the existence of mines in these 3 locations using Google Earth.

#### Routines

1. Downloaded the active mining dataset from IPIS Research and uploaded to the Google Earth Engine code editor as an asset
2. Imported the IPIS Research and FAO GAUL datasets
3. Extracted the geometry of the DRC by filtering the FAO GAUL dataset
4. Centered the map around the DRC
5. Added the locations of known active coltan mines as a layer to the map
6. Chose region of active Coltan mining in the northern DRC
7. Used the geometry tools in the Google Earth Engine Code Editor to map out 3 small sub-regions (2-3 mines) within that region to focus on
![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/rois.PNG)

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/rois2.PNG)

8. Verified existence of mining activity using Google Earth
	- Example for Region 1 (Kalimva):
		- 2005: 
		
		![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/roi1_2_05.PNG)
		
		- 2012: 
		
		![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/roi1_4_12.PNG)
		
		- 2020: 
		
		![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/roi1_8_21.PNG)

#### Results and Conclusions

I was able to find 3 small regions in the Northern DRC with active and verifiable mining activity. Region 1(Kalimva) stood out the most due to its rapid rate of development and degree of change in the landscape. I noticed a prominent body of water becoming depleted, which was likely used as a water source as the mines were developed.

<hr>

### 2. NDVI Time Series

#### Description

I used MODIS data to create an NDVI time series of the mines in Region 1, starting from before mining activity was observed (2004), and ending in 2020. I decided on MODIS data specifically because the data is consistently available over all needed years and there is a dervied MODIS NDVI dataset that conveniently exists in the Google Earth Engine Data Catalog. My intuition was that the onset of mining activity would cause a significant loss in NDVI as vegetation is cleared to build the mines, and I wanted to verify that hypothesis.

#### Routines

1. Imported the MODIS vegetation dataset as well as the geometry for Region 1 from the previous method
2. Created NDVI layers from 2014-2020 and added them to the map (1 layer for each year). Layers were created by taking the median NDVI value across the whole year
	-Example (2013)
	
![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/ndvi_2013.PNG)

3. Plotted a time series of median NDVI per year in the region using matplotlib

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/modis_ndvi.PNG)

#### Results and Conclusions

By manually inspecting the NDVI layers, I was able to see noticeable clearing of vegetation beginning in 2013. This observation was also reflected in the time series, where I witnessed a steep drop in NDVI from 2012-2013. In Region 1, I was able to conclude that the onset of mining activity caused a sharp loss in vegetation. If this same trend is witnessed generally across all mines, it could serve as 1 indicator of mining activity.

<hr>

### 3. Spectral Indices: Northern DRC

#### Description

I added the 6 spectral indices/band ratios outlines in the project objectives and inspected them over the 2014-2020 period, looking for changes and visual anomalies/distinct features. Also, I created multiple time series of various areas to highlight more concretely change over time.

#### Routines

1. Imported the Landsat 8 dataset as well as the geometry for Region 1 created in previous methods
2. Created median composite layers (worked with the 2014-2020 period)
3. Created NDVI layers
4. Created VIGS layers
5. Created NDMI layers
6. Created BSI layers
7. Created Iron Concentration layers
8. Created Clay Concentration layers
9. Added all indices and band ratios to the 2014-2020 median composite images as properties
10. Used matplotlib to create multiple time series of the entire region, of a tailing pond, and of a mining area close-up

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/region1_timeseries.PNG)

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/pond_timeseries.PNG)

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/mine_timeseries.PNG)

#### Results and Conclusions

- NDVI: Generally steady across the period, slight increase over entire region and slight decrease in tailing pond/mine close-up
- VIGS: Drop in 2017 followed by steady growth even while mines are expanding, some tailing ponds appear faintly
- NDMI: Moisture in mining areas very low/close to none. Some tailing ponds are highlighted while others are not
- BSI: General behavior is inverse of NDVI and VIGS. Slight increase in BSI as the mines are expanded
- Iron: Good at highlighting roads. In the specified tailing pond, iron spiked in 2017. Iron levels steadily increasing in the close-up mine area throughout the period
- Clay: Generally steady/slightly decreasing over the period with no noticeable or distinct features

<hr>

### 4. Cross Section Analysis of Visual Anomalies

#### Description

I created a cross section function that plots band values over a manually drawn cross section line on an image. My goal was to inspect band values and look for trends and outliers over features and visual anomalies such as tailing ponds and mining areas with bright signatures.

#### Routines

1. Imported the Landsat 8 dataset and geometry for Region 1 from previous methods
2. Created a median composite of Region 1 for the year 2020 and add it to the map as a layer
3. Wrote code that takes a drawn line and creates a specified number of equally spaced points along the line
4. Selected band values at every created point
5. Plotted selected band values on a chart

#### Results and Conclusions

#### Tailing Pond:

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/tailing_cross.PNG)

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/tailing_cross_chart.png)

Band grouping along the tailing pond

#### Mining Area (bright signature):

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/bright_cross.PNG)

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/congo/drc_bands/images/bright_chart.png)

<hr>

### 5. Inspecting SAR Data

#### Description

I took [Emily's SAR code](https://github.com/CordulaRobinson/GEE/blob/main/emilynason/DRC/CongoMinesSARv2.ipynb) and applied it to my own 3 regions to see what I could find and if our results matched. Routines outlined [here](https://github.com/CordulaRobinson/GEE/blob/main/emilynason/DRC/CongoMinesSAR_README.md)

#### Results and Conclusions

#### VV band:

#### VH band:

#### VV/VH ratio:

## Further Questions

-TRMM
-elevation
-we derived 1 new spectral index, can we find or create more?
-looking far out: VHR data (paid?)
