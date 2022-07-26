import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import glob

from sys import exit

from sklearn.tree import DecisionTreeClassifier

import pickle
from joblib import dump, load


# Load Model
clf2 = pickle.load(open('../Training/class_noB56StDev_withNDiffB56Native.pkl', 'rb'))

# List of Datasets/csv's
#files1 = glob.glob(os.path.join(os.getcwd(),'25.25_27.35_-11_-10/status_20m_*.csv*'))
files1=glob.glob(os.path.join(os.getcwd(),'25.25_27.35_-11_-10/compiled_26.65_-10.3_27.35_*'))
#files2 = glob.glob(os.path.join(os.getcwd(),'25.25_27.35_-11_-10/compiled_*.csv*'))

files = files1 #+ files2

count = 0
nfiles = len(files)
for file in files:
    count=count+1
    print("File ",int(count),' of ',int(nfiles),' ......')
    
    df = pd.read_csv(file)

    veg = df['Percent Vegetation Loss'].values
    bare = df['Percent Bare Initial'].values
    sar = df['Percent Significant VH Values'].values
    swir = df['Average SWIR1/B'].values
    nirg = df['Average NIR/G'].values
    
    try:
        clon = df['Center Lon'].values
        clat = df['Center Lat'].values
    except Exception as e:
        clon =  (df['Mininum Longitude'].values + df['Maximum Longitude'].values) / 2
        clat =  (df['Minimum Latitude'].values + df['Maximum Latitude'].values) / 2
        
    try:
        b5 = df['B5 Value'].values
        b6 = df['B6 Value'].values
    except Exception as e:
        b5 = df['B5'].values
        b6 = df['B6'].values

    b56_2 = (b5 - b6)/(b5+b6)

    data2 = np.array([veg,bare,sar,nirg,swir,b56_2])
    
    result2 = clf2.predict(data2.T)


    
    outfile2 = file.split('/')[-1]
    outfile2 = os.path.join('/scratch/e.conway/GEDI/GEE_Gedi/DCR_HighRes_Region3/Analysis/Results_no_B56SdDev_WithNdiffofB56Native',outfile2)
    
    x2 = np.stack([clon[result2==1],clat[result2==1]])
    
    np.savetxt(outfile2,x2.T,delimiter=',',fmt=['%.6f','%.6f'])



