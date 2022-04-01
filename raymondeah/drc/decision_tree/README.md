# Identifying Potential Mining Areas in the Democratic Republic of the Congo Using Vegetation Loss

## Overview

In the DRC, we observed that new mining infrastructure is often created by tearing down existing vegetation. Therefore, we decided that vegetation loss over time may be a good first metric for identifying mining areas. We implemented this idea by using classification methods to calculate areal change and percent loss of vegetation. This summary serves as an outline of our routines thus far.

## Objectives

1. Find high quality satellite data spanning over a large period of time
2. Train a classifier to identify vegetation and bare soil
3. Classify median composite images from past and present years
4. Calculate area and percent change in vegetation loss
5. Run process over areas of interest/entire DRC using methods above and square script

## Datasets

[USGS Landsat 5 Level 2, Collection 2, Tier 1](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2?hl=en)

[Sentinel-2 MSI: MultiSpectral Instrument, Level-2A](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR#description)

[FAO GAUL: Global Administrative Unit Layers 2015, Country Boundaries](https://developers.google.com/earth-engine/datasets/catalog/FAO_GAUL_2015_level0?hl=en)

[Known active artisinal mining sites in the eastern DRC](http://geo.ipisresearch.be/geoserver/web/wicket/bookmarkable/org.geoserver.web.demo.MapPreviewPage?0)  from [IPIS Research](https://ipisresearch.be/home/maps-data/open-data/)

## Methods

### 1. Data

#### Description

After a search through the Google Earth Engine Data Catalog, we found two potential options for available data:

+ MODIS
	+ Available from 2000-2020
	+ 500m spatial resolution
+ Landsat 5 and Sentinel-2
	+ Landsat 5 available from 1984-2012
		+ 30m spatial resolution
	+ Sentinel-2 available from 2015-Present
	 	+ 10-60m spatial resolution

After some initial work with MODIS, we decided to switch over to Landsat 5 and Sentinel-2 as we felt limited by the 500m resolution of MODIS in detecting smaller scale mines.

<hr>

### 2. Training Classifiers

#### Description

Since we were working with two separate datasets, we created two classifiers with two sets of training data. We decided specifically on a Random Forest Classifier because it is generally faster than other classification algorithms on larger datasets, and it has worked well in past applications.

#### Routines

#### Landsat 5:

1. Create a median composite image over an area of interest for the year 1985. We used 1985 because we wanted our time period to span over as many years as possible, and 1985 was the earliest available image.
2. Collect training data of bare earth and vegetation points using the geometry tools in the Google Earth Engine Code Editor
![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/drc/decision_tree/images/ls_training.PNG)
4. Train a Random Forest Classifier using the image and the training data

#### Sentinel-2

1. Create a median composite image over the same area of interest for the year 2021. We used 2021 because it was the most recent year available.
2. Collect Training data of bare earth and vegetation points using the geometry tools in the Google Earth Engine Code Editor
![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/drc/decision_tree/images/s2_training.PNG)
4. Train a Random Forest Classifier using the image and the training data

<hr>

### 3. Areal Change/Percent Loss

#### Description

We used our classifiers created above to classify past and present images and calculate areal change/percent loss of vegetation. These methods were compiled into a single function that can be used to map over FeatureCollections and compute percentage loss of vegetation.

#### Routines

1. Create a median composite using Landsat 5 from the years 1985-1990. Instead of using a single year, we expanded the range to ensure that data would be available across the entire DRC
2. Create a median composite using Sentinel-2 for the year 2021
3. Classify both images using the  respective classifier
4. Extract the classified vegetation pixels in the Landsat image, the classified bare pixels in the Sentinel image, and the intersection of both (vegetation in Landsat and bare in Sentinel)
5. Calculate the area of initial vegetation as well as the area of vegetation to bare pixels
6. Calculate the percentage loss of vegetation ((intial vegetation / vegetation to bare) * 100)

<hr>

### 4. Creating Squares

Our process and workflow involves splitting regions into smaller squares. We created a method to split a given rectangle geometry into squares of a given km size so that we could work together in standardized units instead of arbitrary lat/lon coordinates. Note that the formula to calculate lat/lon uses approximations and can result in small error depending on square size and distance from poles (for our use cases, percent error typically <1%).

#### Routines

Specific method details can be found in the "create_segments(geometry, size)" method here(LINK)..

<hr>

### 5. Workflow/Results

#### Description

Combining everything together, we tested the effectiveness of the vegetation loss metric at identifying mines for several different areas of interest in the DRC. Our current workflow is visualized below.

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/drc/decision_tree/images/w.png)

#### Area 1, 500m x 500m squares

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/drc/decision_tree/images/area1.png)

#### Area 2, 500m x 500m squares

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/drc/decision_tree/images/area2.png)

#### Area 3, 500m x 500m squares

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/drc/decision_tree/images/area3.png)

#### Area 4 (small-scale mining), 100m x 100m squares

![](https://github.com/CordulaRobinson/GEE/blob/main/raymondeah/drc/decision_tree/images/area4.png)

#### Conclusions

Judging from what we've seen so far, vegetation loss over time is an effective metric at narrowing down mining areas. However, it is not perfect, as it will also identify urban development and general deforestation unrelated to mining activity. Also, our current model sometimes struggles at identifying very small-scale mines. Possible solutions could include trying smaller squares (at the cost of performance) or attempting to run the model with data of higher spatial resolution.

<hr>

## Further Questions

- small scale mining/performance optimizations
- further layers for model (indices, etc)
- distinguishing between mines/urban/deforestation

