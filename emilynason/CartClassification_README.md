The CartClassification scripts utilize Landsat 8 data to classify land cover in Boston, MA. 
The image classified is the composite of the median pixel values for the year 2019.
The data for the classes of Urban, Bare, Water, and Vegetation were selected using the true-color RGB composite. 
In order to perform an accuracy assessment, the data was randomly split into two groups: one for training and the other for validation.
A CART classifier was used, and the overall accuracy came to about 90%.

This is available in python (CartClassificationLandsat.ipynb) and javascript in the GEE API (CartClassificationLandsatGEE).

CartClassificationLandsat_WithIndices is another version of this script i javascript, that is updated to include common indices. 
These include NDVI, NDBI, and MNDWI. This script had about the same accuracy as the scripts without indices. 
