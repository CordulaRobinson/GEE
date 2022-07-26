from tqdm import tqdm
import os
import numpy as np
import pandas as pd
from multiprocessing import Pool
import multiprocessing
import time 
import glob

class reduce_class(object):

    def __init__(self):
        self.meter = 0.00001
        pass
    
    def inputs(self,nres):
        self.nres = nres
        pass
    
    
    def perfilecall(self,file,resolutions):
        
        col = ['Mininum Longitude','Minimum Latitude','Maximum Longitude','Maximum Latitude',\
        'Percent Vegetation Loss','Percent Bare Initial','Percent Significant VH Values','Average NIR/G','Average SWIR1/B','NASA Elev',\
        'Elev Loss','GEDI Qual. Flag','B5 Value','B6 Value','Elevation Score','Band Variation Score','NDMI',\
        'Center Lon','Center Lat','Status','GEDI Elev',\
                  'Elev Std','Elev %','B5 Std','B5 %','B6 Std','B6 %']
        pdf = pd.read_csv(file)

        x = reduce_class()
        
        for nres in resolutions:
            x.inputs(nres)
            lon_min,lat_min,lon_max,lat_max,mine_veg_loss,bare_initial,sar,nirg,swir1,nasa_elev,gedi_loss,\
            gedi_qual,b5,b6,elev_score,band_ratio,ndmi,clon,clat,calc_stat,gedi = x.reduce_region(pdf)

            d1,d2,d3,d4,d5,d6 = x.multi()

            d1=np.array(d1)
            d2=np.array(d2)
            d3=np.array(d3)
            d4=np.array(d4)
            d5=np.array(d5)
            d6=np.array(d6)

            npts = len(lon_min)

            data = np.array([lon_min[0:npts],lat_min[0:npts],lon_max[0:npts],lat_max[0:npts],mine_veg_loss[0:npts]\
                                 ,bare_initial[0:npts],sar[0:npts],\
                                 nirg[0:npts],swir1[0:npts],nasa_elev[0:npts],gedi_loss[0:npts],\
            gedi_qual[0:npts],b5[0:npts],b6[0:npts],elev_score[0:npts],band_ratio[0:npts],ndmi[0:npts],\
                                 clon[0:npts],clat[0:npts],calc_stat[0:npts],gedi[0:npts],\
                                d1[0:npts],d2[0:npts],d3[0:npts],d4[0:npts],d5[0:npts],d6[0:npts]])



            df = pd.DataFrame(data.T, columns=col)
            
            newname = os.path.basename(file)
            newname = newname.split('statusII')[1]
            newname = 'statusIII_'+str(nres)+'m_'+newname
            
            df.to_csv(newname,index=False)
        
    
    def multi(self):
    
        
        y = np.linspace(0,len(self.lon_min)-1,len(self.lon_min))
        y = np.array(y,dtype=int)
        y = list(y)
        pool = Pool(processes=multiprocessing.cpu_count())                        
        d1,d2,d3,d4,d5,d6 = zip(*pool.map(self.looper, y))

        
        pool.close() 
        pool.join()

        
        return d1,d2,d3,d4,d5,d6

    def reduce_region(self,df):
        """
        args:
        df: dataframe
        mine_pos: indices of variables we wish to return. It is a vector.
        return:
        lon_min,lat_min,lon_max,lat_max,mine_veg_loss,bare_initial,sar,nirg,swir1,nasa_elev,
        gedi_loss,gedi_qual,b5,b6,elev_score,band_ratio
        at the indices
        """
        self.lon_min = df['Mininum Longitude'][:].values
        self.lat_min = df['Minimum Latitude'][:].values
        self.lon_max = df['Maximum Longitude'][:].values
        self.lat_max = df['Maximum Latitude'][:].values
        mine_veg_loss = df['Percent Vegetation Loss'][:].values
        bare_initial = df['Percent Bare Initial'][:].values
        sar = df['Percent Significant VH Values'][:].values
        nirg = df['Average NIR/G'][:].values
        swir1 = df['Average SWIR1/B'][:].values
        self.nasa_elev = df['NASA Elev'][:].values
        gedi_loss = df['Elev Loss'][:].values
        gedi_qual = df['GEDI Qual. Flag'][:].values
        self.b5 = df['B5 Value'][:].values
        self.b6 = df['B6 Value'][:].values
        ndmi = df['NDMI'][:].values
        clon = df['Center Lon'][:].values
        clat = df['Center Lat'][:].values
        elev_score = df['Elevation Score'][:].values
        band_ratio = df['Band Variation Score'][:].values
        calc_status = df['Status'][:].values
        gedi = df['GEDI Elev'][:].values


        return(self.lon_min,self.lat_min,self.lon_max,self.lat_max,mine_veg_loss,bare_initial,sar,nirg,swir1,\
                   self.nasa_elev,gedi_loss,gedi_qual,\
               self.b5,self.b6,elev_score,band_ratio,ndmi,clon,clat,calc_status,gedi)

    def looper(self,i):
        # get b-box for this i'th pixel
        ll_lon = self.lon_min[i] - self.nres * self.meter
        ll_lat = self.lat_min[i] - self.nres * self.meter
        ur_lon = self.lon_max[i] + self.nres * self.meter
        ur_lat = self.lat_max[i] + self.nres * self.meter    

        idx = np.logical_and(self.lon_min>=ll_lon,self.lon_max<ur_lon)
        idy = np.logical_and(self.lat_min>=ll_lat,self.lat_max<ur_lat)

        idf = np.logical_and(idx==True,idy==True)

        npix = len(idf)
        
        
        elev_pp = self.nasa_elev[idf]
        b5_pp = self.b5[idf]
        b6_pp = self.b6[idf]
        
        #ELEV STATS
        std_elev = np.nanstd(elev_pp-self.nasa_elev[i])
        idp = len(np.where(elev_pp > self.nasa_elev[i])[0])
        idn = len(np.where(elev_pp < self.nasa_elev[i])[0])
        elev_pcnt = 100*(idp - idn)/npix
        
        
        #B5 STATS
        std_b5 = np.nanstd(b5_pp-self.b5[i])
        idp = len(np.where(b5_pp > self.b5[i])[0])
        idn = len(np.where(b5_pp < self.b5[i])[0])
        b5_score = 100*(idp - idn)/npix   
        
        #B6 STATS
        std_b6 = np.nanstd(b6_pp-self.b6[i])
        idp = len(np.where(b6_pp > self.b6[i])[0])
        idn = len(np.where(b6_pp < self.b6[i])[0])
        b6_score = 100*(idp - idn)/npix          

        return std_elev,elev_pcnt,std_b5,b5_score,std_b6,b6_score


if __name__ == '__main__':
    
    
    tz = time.time()
    
    resolutions = [100,200,500]

    cwd = os.getcwd()
    
    files = glob.glob(cwd+'/statusII*')

    for file in files:
        file = os.path.join(cwd,file)

        x = reduce_class()
        
        x.perfilecall(file,resolutions)
        
        

