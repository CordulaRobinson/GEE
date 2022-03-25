import numpy as np
import os
import sys

# create a large region of interest, of which we will create lots of jobs for
# upper right and lower left corners, orientated NS
upper_lon = 29.65 #30
upper_lat = 3.15 #10
lower_lon = 29.55 #28
lower_lat = 3.1 #8

# the above is a 5x5 degree box
# let us say we want to create jobs that work on 1x1 degree tiles 
grid_space = 0.05 # degrees

# the small grid we want to work with
# 250m == 0.0025 degrees (about..)
# small_grid = 0.0025
# takes km in code, not degrees
small_grid = 1

#  get the numnber of x,y tiles we will loop over
n_lon = int(np.ceil((upper_lon - lower_lon)/grid_space ))
n_lat = int(np.ceil((upper_lat - lower_lat)/grid_space ))

# let's start from the bottom left 
for i in range(n_lon):
    lon_min = i*grid_space + lower_lon
    lon_max = (i+1)*grid_space + lower_lon
    for j in range(n_lat):
        lat_min = j*grid_space + lower_lat
        lat_max = (j+1)*grid_space + lower_lat
        # filename is the highest res we will work with, plus the large square bounds
        bash_filename = 'gee_dcr_'+str(small_grid)+'_'+str(lon_min)+'_'+str(lat_min)+'_'+str(lon_max)+'_'+str(lat_max)+'.sh'
        with open(bash_filename,'w') as f:
            # one node, one hour
            # name of job is DCR_i_j
            # 12 GB memory
            # load up conda #changes MyEnv to NewEnv
            # execute 'gee_dcr.py' (your jupyter codes turned to .py) # drc_mine.py
            # the arguments passed are the bounding box (1x1 degree for now)
            # plus the high res smaple size == 0.0025 degree
            f.write('#!/bin/bash'+'\n')
            f.write('#SBATCH --nodes=1'+'\n')
            f.write('#SBATCH --time=01:00:00'+'\n')
            f.write('#SBATCH --job-name=DCR_'+str(i)+'_'+str(j)+'\n')
            f.write('#SBATCH --partition=short'+'\n')
            f.write('#SBATCH --mem=12GB'+'\n')
            f.write('module load anaconda3/2022.01'+'\n')
            f.write('source activate '+'\n')
            f.write('source activate newEnv'+'\n')
            f.write('conda activate newEnv'+'\n')
            f.write('conda init bash'+'\n')
            f.write('python3 drc_mines.py '+str(small_grid)+' '+str(lon_min)+' '+str(lat_min)+' '+str(lon_max)+' '+str(lat_max)+' \n')
        # now we will submit the job (the bash_filename) written above
        os.system("sbatch "+str(bash_filename))
        # output = os.path.join('/scratch/nason.e/gee/drc/outputs/')