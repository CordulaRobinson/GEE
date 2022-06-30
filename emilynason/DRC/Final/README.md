"Images_and_Charts" folder contains all code used to create the various images and charts used in the paper.  
Not all in this folder are used currently in the paper as of 6/30/2022.

"Index_Value_Test"  folder contains GEE scripts that I used to take average values of SAR VH, GNDVI, and SWIR1/B over multiple types of samply areas to help determine what values were relevant to mining. 

"Other" folder contains code that I found helpful/efficient at different times throughout the last few months.  
Explanation of each file can be found in that folder's README.md

"GEE_Module.py" is our current mine detection routine as of 6/30/2022.  
This outputs 3 csv files (combined.csv - aka raw data results, combined_status.csv - has status calculated and appended per square, and combined_status_passing.csv - aka only squares that passed and their data),  
and optionally exports passing mines as a feature collection to GEE.

"run_GEE.sh" is the code that runs "GEE_Module.py". Variables in this file can be changed to adjust user, size of jobs, file names and locations, region tested, etc.

"Logistic_Fitting.ipynb" is the code developed by Eamon, which uses a logistic regressor to optimize our variables for mine detection. up to date as of 6/25/2022.

"polygon_mine_status.ipynb" is a code that can reformat a csv file (combined_status.csv) from our routine so that it works as an input to "Logistic_Fitting.ipynb".  
The code can resize the file such that only squares within a certain region are in the file, and changes the status from "Pass" and "Fail" to 1 and 0

"visualize_results" is a GEE script that I use to visualize my results.  
Links for assets used in this scripts:
IPIS mines:
https://code.earthengine.google.com/?asset=users/EmilyNason/cod_mines_curated_all_opendata_p_ipis  
Region Results for 25.25, -11, 25.95, -10:  
https://code.earthengine.google.com/?asset=users/EmilyNason/NativeRes_mainRegion
