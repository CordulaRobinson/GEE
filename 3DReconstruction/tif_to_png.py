import matplotlib.pyplot as plt
import rasterio
import os
import numpy as np
from PIL import Image
import glob
from scipy import interpolate
from scipy.interpolate import griddata
from tqdm import tqdm

direct = '/scratch/e.conway/3DReconstruction/SpaceNet_Buildings2/Images/Satellite-Images/Jacksonville/WV3/MSI/'
files=glob.glob(direct+'/*.tif')

count=0
nfiles=len(files)
for i in tqdm(range(len(files))):
    file = files[i]
    df = rasterio.open(file)
    x = df.read()
    lon_min=df.bounds[0] ; lon_max=df.bounds[2] ; lat_min=df.bounds[1] ; lat_max=df.bounds[3]
    lon=np.zeros((x.shape[1],x.shape[2])) ; lat=np.zeros((x.shape[1],x.shape[2]))
    lon = np.linspace(lon_min,lon_max,x.shape[1])
    lat = np.linspace(lat_min,lat_max,x.shape[2])
    
    arr = np.zeros((x.shape[1],x.shape[2],3))
    arr[:,:,0] = x[4,:,:]/np.nanmax(x[4,:,:])
    arr[:,:,1] = x[2,:,:]/np.nanmax(x[2,:,:])
    arr[:,:,2] = x[1,:,:]/np.nanmax(x[1,:,:])
    arr=arr*255
    arr=np.array(arr,dtype=np.uint8)
    
    small_lon = np.linspace(-81.66,-81.6,3000)
    small_lat = np.linspace(30.28,30.35,3000)
    print('3')
    lon,lat=np.meshgrid(lon,lat)
    print('4')
    ll = np.stack((lon.flatten(),lat.flatten())).T
    print('5')
    x_new_0 = griddata(ll,arr[:,:,0].flatten(),(small_lon,small_lat))
    print('6')
    x_new_1 = griddata(ll,arr[:,:,1].flatten(),(small_lon,small_lat))
    print('7')
    x_new_2 = griddata(ll,arr[:,:,2].flatten(),(small_lon,small_lat))
    print('8')
    arr = np.zeros((ll.shape[0],ll.shape[2],3))
    arr[:,:,0] = x_new_0
    arr[:,:,1] = x_new_1
    arr[:,:,2] = x_new_2
    img = Image.fromarray(arr)
    #img.show()
    name = file.split('.tif')[0]+'_sub.png'
    img.save(name)
