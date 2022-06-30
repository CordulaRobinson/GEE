"DegradeResolution.ipynb" this file takes a csv with 20m resolution data and tries to take averages to degrade the resolution to a desired value (currently 200m).  
This does not work on a large scale currently.

"MinePlot.py" is a code from Eamon that takes an excel file and creates a kml file. Uses files from our routine but they must be changed from csv to xslx first.

"check_region_ran_and_bounds.ipynb" this code takes a csv file from our routine and plots the coordinates of the squares.  
Use it to check that you have data from the entire region desired, and that there are no gaps from jobs timing out.  
This file also contains code to give you the min and max latitudes and longitudes from a csv file.

"closest_mine.py" nearest neighbor function to used with our results and IPIS data on known mining location to see how our results compare. 

"redo_status_and_convert.py" takes in our csv files, calculates status column, can convert results to asset in GEE for visualization
