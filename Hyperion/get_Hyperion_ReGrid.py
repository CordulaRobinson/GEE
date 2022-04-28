import ee
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.interpolate import LinearNDInterpolator
import netCDF4 as nc4
import datetime as dt
from sys import exit
    
def regrid(inlst):
    """
    This gets all the bands from the GEE list and re-grids them to a single data cube.
    GEE states that Bands 
    """
    m=len(inlst) # number of pixels
    bands = list(inlst[0]['properties'].keys())
    bnd_index = np.zeros(len(bands))
    N_bands = len(bands)
    data = np.zeros((m,N_bands))
    lon = np.zeros(m) ; lat = np.zeros(m)
    for i in range(m):
        lon[i] = inlst[i]['geometry']['coordinates'][0]
        lat[i] = inlst[i]['geometry']['coordinates'][1]   
        for j in range(N_bands):
            if(i==0):
                bnd_index[j] = int(bands[j].split('B')[1])
            data[i,j] = inlst[i]['properties'][bands[j]] 
            

    # define square grid and re-grid
    NN = len(lon)
    data_cube = np.zeros((NN,NN,N_bands),dtype=np.float32)
    idx=np.argsort(lon)
    lon_sort=lon[idx]
    idx=np.argsort(lat)
    lat_sort=lat[idx]
    xx,yy = np.meshgrid(lon_sort,lat_sort)
    for i in range(N_bands):
        interp = LinearNDInterpolator((lon,lat),data[:,i])
        data_cube[:,:,i] = interp((xx,yy))
    return xx,yy,data_cube,bnd_index


ee.Initialize()

"""
Define Region Bounds: Lower Left, Top Right of a bounding box
"""
# Mine 1.
lon_ll = 26.59 ; lon_tr = 26.63 ; lat_ll = -10.89 ; lat_tr= -10.88

# meter resolution per pixel, native = 30m
# caution, there are almost 200 bands. Arrays can be extremely large.
Resolution = 100

geom = ee.Geometry.Rectangle([lon_ll,lat_ll,lon_tr,lat_tr])

"""
Select Hyperion data measured from 2000-12-31 to 2018-01-02 i.e end of life-time
"""
hyper = ee.ImageCollection('EO1/HYPERION').filter(ee.Filter.date('2001-05-01', '2017-03-13'))\
    .select(['B.*']).filterBounds(geom)

"""
Number of measurements obtained, could be zero, could be many
"""
Nmeasurements = hyper.size().getInfo()

print(Nmeasurements)
#if(Nmeasurements != 0):
#    print(hyper.getInfo())


if(Nmeasurements != 0):
    print('Found ', Nmeasurements,' Hyperion measurements, retrieving and re-gridding them now.....')
    # convert the entire dataset to a list for GEE (server side)
    hyper_list = hyper.toList(hyper.size())
    for i in tqdm(range(Nmeasurements)):
        # create an image of the i'th measurement on the server
        hyper_i = ee.Image(hyper_list.get(i))#.clip(geom)
        sza = hyper_i.get('SENSOR_LOOK_ANGLE').getInfo()
        second = hyper_i.get('system:time_start').getInfo()
        date_acquisition = dt.datetime(year=1970,month=1,day=1) + dt.timedelta(seconds=second/1000)
        year = date_acquisition.year
        month = date_acquisition.month
        day = date_acquisition.day
        sc_sw = hyper_i.get('SCALING_FACTOR_SWIR').getInfo()
        sc_ir = hyper_i.get('SCALING_FACTOR_VNIR').getInfo()
        
        hyper_i = hyper_i.sample(geom,geometries=True,scale=Resolution)
        # download the measurement (i) locally
        lst = hyper_i.toList(hyper_i.size()).getInfo()
        lon,lat,data_array,bnd_indices = regrid(lst)
        
        """
        Term to multiple bands by to get radiance from DN
        Radiance = W/m^2 SRµm  = band_value[DN] * scale [W/m^2 SRµm DN^-1]
        """
        scale = np.ones(len(bnd_indices))
        for j in range(len(bnd_indices)):
            if(bnd_indices[j] >= 77 and bnd_indices[j] <=224):
                scale[j] = sc_sw
            elif(bnd_indices[j] >=8 and bnd_indices[j] <=57):
                scale[j] = sc_ir
        tm = str(year)+'-'+str(month)+'-'+str(day)
        fname = os.path.join(os.getcwd(),'Hyperion_'+str(lon_ll)+'_'+str(lat_ll)+'_'+str(lon_tr)+'_'+str(lat_tr)+'_'+tm+'.nc')
        with nc4.Dataset(fname,'w', format='NETCDF4') as f:
            f.createDimension('Pixel',lon.shape[0])
            f.createDimension('Bands',data_array.shape[2])
            f.createDimension('NMeasurement',1)
            
            data_nc = f.createVariable('DataCube','f4',('Pixel','Pixel','Bands'),zlib=True)
            lon_nc = f.createVariable('Longitude','f8',('Pixel','Pixel'),zlib=True)
            lat_nc = f.createVariable('Latitude','f8',('Pixel','Pixel'),zlib=True)
            time = f.createVariable('MeasurementTime','f8','NMeasurement',zlib=True)
            scale_nc = f.createVariable('ScalingFactor','i2','Bands',zlib=True)
            bands_nc = f.createVariable('BandLabels','i2','Bands',zlib=True)
            
            data_nc[:,:,:] = data_array
            data_nc.units = 'Digital Numbers [DN]'
            lon_nc[:,:] = lon
            lat_nc[:,:] = lat
            time[:] = second
            time.description = 'Seconds since 1970-1-1'
            scale_nc[:] = scale
            scale_nc.description = 'Converts DN to radiance: W/m^2 SRµm'
            bands_nc[:] = bnd_indices

else:
    print('No Hyperion within region specified')
