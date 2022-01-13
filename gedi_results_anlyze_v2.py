# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:28:40 2022

@author: e.conway
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:32:28 2022

@author: e.conway@kri.neu.edu

Code to analyze the data of the GEDI LIDAR L1B NetCDF4 files for waveform maxima/minima feature extraction
produced by the fit_gedi_v3.py code

Inputs are a .nc file

Output is a .kml for google earth plotting plus some figures for now

Requirements: 
The EGM2008 dataset interpreter interp_2p5min.f is located from:/scratch/e.conway/GEDI/
Once compiled, it reads the EGM2008 parameters Und_min2.5x2.5_egm2008_isw=82_WGS84_TideFree_SE located at /scratch/e.conway/GEDI/
It wil compile in your cwd. 
This code, below, creates the inputs.dat and the fortran code outputs the GEOID elevation above the wgs84 ellipsoid in outputs.dat
We pass the fortran code the location of inputs.dat and outputs.dat respectively

These allow us to get height above MSL.

"""

import netCDF4 as nc4
import numpy as np
from sys import exit
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata
from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import NearestNDInterpolator
import make_kmz_v2
import os
from osgeo import osr
import glob

parameters = {'axes.labelsize': 40,
          'axes.titlesize': 40,
          'xtick.labelsize': 30,
          'ytick.labelsize': 30,
          'legend.fontsize': 30}
plt.rcParams.update(parameters)

nmin = 17700#16000
nmax = 17800#18000
n = nmax-nmin

myresults = '/scratch/e.conway/GEDI/Testing/'
outdir = '/scratch/e.conway/GEDI/Testing/'

files = glob.glob(myresults+'*.nc')
file=files[0]

beams = ['BEAM0001','BEAM0000','BEAM0010','BEAM0011']#,'BEAM0101','BEAM0110','BEAM1000','BEAM1011']

geoid = []
maxi = []
maxi_lat = []
maxi_lon = []
dem = []

for beam in beams:
    maxi_zero = []
    geoid_zero = []
    maxi_lat_zero = []
    maxi_lon_zero = []
    dem_zero = []
    with nc4.Dataset(file,'r') as f:


        time = f.groups[beam].variables['Time'][:]#[nmin:nmax]     
        max_elev = f.groups[beam].variables['MaximaElevation'][:]
        min_elev = f.groups[beam].variables['MinimaElevation'][:]
        max_wf = f.groups[beam].variables['WaveformSignalMax'][:]
        min_wf = f.groups[beam].variables['WaveformSignalMin'][:]
        int_sig = f.groups[beam].variables['IntegratedSignal'][:]
        max_count = f.groups[beam].variables['MaximaCounter'][:]
        min_count = f.groups[beam].variables['MinimaCounter'][:]
        #lon_maxima = f.groups[beam].variables['LonMaxima'][:]
        #lat_maxima = f.groups[beam].variables['LatMaxima'][:]
        #lon_minima = f.groups[beam].variables['LonMinima'][:]
        #lat_minima = f.groups[beam].variables['LatMinima'][:]
        lon = f.groups[beam].variables['Lon'][:]#[nmin:nmax]
        lat = f.groups[beam].variables['Lat'][:]#[nmin:nmax]
        dem_srtm = f.groups[beam].variables['DEM_Srtm'][:]#[nmin:nmax]
        dem_x90=f.groups[beam].variables['DEM_x90'][:]#[nmin:nmax]
        geoid_raw=f.groups[beam].variables['GEOID'][:]#[nmin:nmax]

  
    max_counter = 0
    npts = len(time)
    

    dem_choice = dem_x90
    
    # routine for pulling the maximum 'max elevation' point from our previous waveform analysis.
    # we want the lon/lat too.
    # elevation is w.r.t WGS84 Ellipsoid
    for i in range(int(nmax)):
        if(i < nmin):
            nmaxpnt = max_count[i]
            max_counter = max_counter + nmaxpnt
        else:
            iter = i - nmin
            if(int_sig[i] != -1 and max_count[i] != 0):
                nmaxpnt = max_count[i]
                maxi_zero.append( np.nanmax(max_elev[int(max_counter):int(max_counter+nmaxpnt)]))
                geoid_zero.append(geoid_raw[iter])
                # position of maximum feature in the vector
                pointer = np.argmax(max_elev[int(max_counter):int(max_counter+nmaxpnt)])
                # get the lon + lat's
                maxi_lat_zero.append(lat[iter])
                maxi_lon_zero.append(lon[iter])
                dem_zero.append(dem_choice[iter])
                max_counter = max_counter + nmaxpnt
            else:
                maxi_zero.append(np.nan)
                maxi_lat_zero.append(np.nan)
                maxi_lon_zero.append(np.nan)
                dem_zero.append(np.nan)
                geoid_zero.append(np.nan)
    maxi.append(maxi_zero)
    maxi_lat.append(maxi_lat_zero)
    maxi_lon.append(maxi_lon_zero)
    dem.append(dem_zero)    
    geoid.append(geoid_zero)    


maxi_full=np.zeros((len(dem),len(dem[0])))
maxi_lon_full=np.zeros((len(dem),len(dem[0])))
maxi_lat_full=np.zeros((len(dem),len(dem[0])))
dem_full=np.zeros((len(dem),len(dem[0])))
geoid_full=np.zeros((len(dem),len(dem[0])))

for i in range(len(dem)):
    maxi_full[i,:] = maxi[i][:] 
    maxi_lat_full[i,:] = maxi_lat[i][:] 
    maxi_lon_full[i,:] = maxi_lon[i][:] 
    dem_full[i,:] = dem[i][:] 
    geoid_full[i,:] = geoid[i][:] 



maxi = maxi_full
maxi_lat=maxi_lat_full
maxi_lon=maxi_lon_full
dem = dem_full
geoid = geoid_full



#print(np.nanmax(maxi_lat))
#print(np.nanmax(maxi_lon))
#print(np.nanmin(maxi_lat))
#print(np.nanmin(maxi_lon))



"""
idx = np.isfinite(maxi)


x = np.linspace(0,len(dem[0,:])-1,len(dem[0,:]))


axes = plt.subplot()

plt.ylabel(r'Latitude [$degree$]')
plt.xlabel(r'Longitude [$\degree$]')
plt.title('Max Elevated Feature '+str(file))

im = axes.scatter(x[idx[0,:]],x[idx[0,:]],c=maxi[0,idx[0,:]])

axes.set_xticks(list(maxi_lon[0,idx[0,:]]))
axes.set_yticks(list(maxi_lat[0,idx[0,:]]))


divider = make_axes_locatable(axes)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
plt.savefig('GEDI_Elev.png',dpi=1000)
plt.close()


exit()
"""

    

"""
fig, ax1 = plt.subplots(sharex=True)
ax1.plot(maxi_lat[0,:],maxi[0,])
#ax1.plot(maxi_lon[idx],dsm[idx])
plt.show()
exit()
"""

msl = maxi - geoid

if(np.nanmean(maxi) == np.nan):
    print('Change the bounds, maxi is full on nan vals')
    exit()


vmax = np.nanmax(maxi)
vmin = np.nanmin(maxi)

#print(vmax,vmin)


color = 255*maxi.flatten() / vmax

idx = np.isfinite(maxi.flatten())

fname = os.path.basename(file).split('nc')[0]
fname=fname+'kml'
fname = os.path.join(outdir,fname)

msl = msl.flatten()[idx]
maxi = maxi.flatten()[idx]
maxi_lat = maxi_lat.flatten()[idx]
maxi_lon=maxi_lon.flatten()[idx]
color = color[idx]

make_kmz_v2.make_kml(maxi_lon,maxi_lat,msl,color,fname)


