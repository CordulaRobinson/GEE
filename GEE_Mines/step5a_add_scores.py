import numpy as np
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt
import sys
import os
import ee
ee.Initialize()

file_name = sys.argv[1]

ex = np.genfromtxt("results/" + file_name + ".csv", delimiter=',', skip_header=0)

new_array = np.empty((0,17), float)
for row in ex:
    min_lon = row[0]
    min_lat = row[1]
    max_lon = row[2]
    max_lat = row[3]
    
    # Center Lon/Lat positions:
    center_lon = min_lon + (max_lon-min_lon)/2
    center_lat = min_lat + (max_lat-min_lat)/2
    
    new_row = np.append(row, [center_lon, center_lat], axis=None)
    new_array = np.append(new_array, np.array([new_row]), axis=0)
    
# Remove null values - not needed - null values were in the GEDI data
# new_array2 = np.delete(new_array, np.where(new_array[:,9]==-999), axis=0)

# Columns
lons = new_array[:,15]
lats = new_array[:,16]
nasa_dem = new_array[:,9]
b5_vals = new_array[:,13]
b6_vals = new_array[:,14]
# Interpolate all the center lon/lat positions with the elevation and band data metrics.
interp_elev = LinearNDInterpolator((lons, lats), nasa_dem)
interp_b5 = LinearNDInterpolator((lons, lats), b5_vals)
interp_b6 = LinearNDInterpolator((lons, lats), b6_vals)

new_array2 = np.empty((0,19), float)
for row in new_array:
    center_lon = row[15]
    center_lat = row[16]
    nasa = row[9]
    b5 = row[13]
    b6 = row[14]
    nd = ((b5 - b6)/(b5 + b6))
    score_elev = 0
    score_bands = 0
    
    # Replace null values - not needed - null values were in the GEDI data
    # if (nasa == -999):
    #     nasa = interp_elev.__call__(center_lon, center_lat)
    
    change = 250*0.00001
    
    # Left and right neighbors will have the same center lat
    left = [center_lon - change, center_lat]
    right = [center_lon + change, center_lat]
    # Up and down neighbors will have the same center lon
    up = [center_lon, center_lat + change]
    down = [center_lon, center_lat - change]
    # Corner neighbors
    ul = [center_lon - change, center_lat + change]
    ur = [center_lon + change, center_lat + change]
    dl = [center_lon - change, center_lat - change]
    dr = [center_lon + change, center_lat - change]
    
    neighbors = [left, right, up, down, ul, ur, dl, dr]
    for x in neighbors:
        x_nasa = interp_elev.__call__(x[0], x[1])
        x_b5 = interp_b5.__call__(x[0], x[1])
        x_b6 = interp_b6.__call__(x[0], x[1])
        x_nd = ((x_b5 - x_b6)/(x_b5 + x_b6))
        if (nasa < x_nasa):
            score_elev = score_elev+1
        if (abs(nd - x_nd) > 0.05):
            score_bands = score_bands+1

    new_row = np.append(row, [score_elev, score_bands], axis=None)
    new_array2 = np.append(new_array2, np.array([new_row]), axis=0)

# header_list = 'Mininum Longitude, Minimum Latitude, Maximum Longitude, Maximum Latitude, \
#             Percent Vegetation Loss, Percent Bare Initial, Percent Significant VH Values, \
#             Average NIR/G, Average SWIR1/B, NASA Elev, GEDI Elev, Elev Loss,GEDI Qual. Flag,\
#             B5 Value, B6 Value, Center Lat, Center Lon, Elevation Score, Band Variation Score'
# final = np.savetxt("results/compiled_scores.csv", new_array2, delimiter=",", header=header_list)
final = np.savetxt("results/" + file_name + "_scores.csv", new_array2, delimiter=",")

os.system("python3 step6_status_and_convert.py " + file_name)
