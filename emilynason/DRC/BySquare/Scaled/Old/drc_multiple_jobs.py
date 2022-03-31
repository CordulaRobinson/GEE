# Imports
import numpy as np
import os
import sys

# create a large region of interest, of which we will create lots of jobs for
# upper right and lower left corners, orientated NS
upper_lon = 29.6 #30
upper_lat = 3.15 #10
lower_lon = 29.55 #28
lower_lat = 3.1 #8

# the above is a 0.05x0.1 degree box (previously 2x2)
# let us say we want to create jobs that work on 0.05x0.05 degree tiles (previously 1x1)
grid_space = 0.05 

# the small grid we want to work with
# 250m == 0.0025 degrees (about..), small_grid = 0.0025
# drc_mines.py code uses KM, instead of degrees
small_grid = 5 # 5 KM x 5 KM squares

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
        # filename is the highest res we will work with, plus the large square bounds, sent to bash_files folder
        bash_filename = 'bash_files/gee_dcr_'+str(small_grid)+'_'+str(lon_min)+'_'+str(lat_min)+'_'+str(lon_max)+'_'+str(lat_max)+'.sh'
        with open(bash_filename,'w') as f:
            # one node, one hour
            # name of job is DCR_i_j
            # 12 GB memory
            # load up conda with personal environment name (emily -> newEnv)
            # execute 'drc_mine.py'
            # the arguments passed are the bounding box (1x1 degree for now)
            # plus the high res sample size == 0.0025 degree
            # output files sent to output_files folder, with file names [job ID].out
            f.write('#!/bin/bash'+'\n')
            f.write('#SBATCH --nodes=1'+'\n')
            f.write('#SBATCH --time=01:00:00'+'\n')
            f.write('#SBATCH --job-name=DCR_'+str(i)+'_'+str(j)+'\n')
            f.write('#SBATCH --partition=short'+'\n')
            f.write('#SBATCH --mem=12GB'+'\n')
            f.write('#SBATCH --output=/scratch/nason.e/gee/output_files/%j.out'+'\n')
            f.write('module load anaconda3/2022.01'+'\n')
            f.write('source activate '+'\n')
            f.write('source activate newEnv'+'\n')
            f.write('conda activate newEnv'+'\n')
            f.write('conda init bash'+'\n')
            f.write('python3 drc_mines.py '+str(small_grid)+' '+str(lon_min)+' '+str(lat_min)+' '+str(lon_max)+' '+str(lat_max)+' \n')
        # now we will submit the job (the bash_filename) written above
        os.system("sbatch "+str(bash_filename))
