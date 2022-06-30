"DRC_map_known_mines" contains a GEE script to create the image for the paper of the entire DRC,  
overlaid with known coltan mines from the IPIS database,  
and mining permits and tantalum permits from Global Forest Watch  

Links to assets used in this file:  
IPIS:  
https://code.earthengine.google.com/?asset=users/EmilyNason/cod_mines_curated_all_opendata_p_ipis  
Global Forest Watch:  
https://code.earthengine.google.com/?asset=users/EmilyNason/Democratic_Republic_of_the_Congo_mining_permits

"all_charts_final" contains a GEE script used to create the charts for SAR, Elevation, and Indices (GNDVI and SWIR1/B).  
It was also used to create composite SAR images and composite images of the three main mining regions (Kibali, Kanunka, Musonoi)

"timeseries_bands_ls5_s2.ipynb" creates a time series chart using LS5 and S2 for NDMI, GNDVI, and SWIR1/B for a sample mine.  
This chart is not used in the paper as of 6/30/2022.

"veg_loss_image_and_calc.ipynb" classifies a region into vegetation and bare earth using LS5 for 1985 and S2 for 2021.  
Then calculates the percent vegetation loss for the region.  
Provides composite RGB images for 1985 and 2021, and a map of vegetation loss. 
