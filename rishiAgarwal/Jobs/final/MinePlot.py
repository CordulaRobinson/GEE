import os
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from simplekml import (Kml,Color)
import numpy as np
import matplotlib.pyplot as plt
from sys import exit
from tqdm import tqdm

"""
Routine will open an Excel file, extract positive mine detections and make a .kml/.kml file. 
Open with google earth.
"""


def make_kml(lon,lat,alt,colorrange,outname):
    kml = Kml()
    npnts = len(lon)
    for i in tqdm(range(npnts)):
        pnt = kml.newpoint(coords=[(lon[i],lat[i],alt[i])],altitudemode='clampToGround')#'relativeToSeaFloor') 
        #pnt.style.labelstyle.color = Color.rgb(int(colorrange[i]),0,0,255)
        pnt.style.iconstyle.color = Color.rgb(int(colorrange[i]),0,0,255)#int(colorrange[i]))
        pnt.style.iconstyle.icon.href = 'http://earth.google.com/images/kml-icons/track-directional/track-none.png'
    kml.savekmz(outname)


file = 'compiled_26.25_-11_27.25_-10.xlsx'
df = pd.read_excel(file)

clon = df['Center Lon']
clat = df['Center Lat']
stat = df['Status']


mine_pos = np.where(stat=='Pass')[0]
mine_neg = np.where(stat=='Fail')[0]

#mine_pos = np.concatenate((mine_neg[0:3000],mine_pos[0:3000]))
#print(mine_pos.shape)


# take positive detection stats
mine_pos_lon = np.array(clon[mine_pos])
mine_pos_lat = np.array(clat[mine_pos])

mine_veg_loss = np.array(df['Percent Vegetation Loss'][mine_pos])
bare_initial = np.array(df['Percent Bare Initial'][mine_pos])
sar = np.array(df['Percent Significant VH Values'][mine_pos])
nirg = np.array(df['Average NIR/G'][mine_pos])
swir1 = np.array(df['Average SWIR1/B'][mine_pos])
nasa_elev = np.array(df['NASA Elev'][mine_pos])
gedi_loss = np.array(df['Elev Loss'][mine_pos])
gedi_qual = np.array(df['GEDI Qual. Flag'][mine_pos])
b5 = np.array(df['B5 Value'][mine_pos])
b6 = np.array(df['B6 Value'][mine_pos])
elev_score = np.array(df['Elevation Score'][mine_pos])
band_ratio = np.array(df['Band Variation Score'][mine_pos])
module_pass = np.array(df['Status'][mine_pos])

idx = np.where(module_pass=='Pass')
module_pass[idx] = 1
idx = np.where(module_pass=='Fail')
module_pass[idx] = 0


# make a kml
alt=np.ones(len(mine_pos_lon))
color=255*np.ones(len(mine_pos_lon))
make_kml(mine_pos_lon,mine_pos_lat,alt,color,'mine_positive.kmz')
