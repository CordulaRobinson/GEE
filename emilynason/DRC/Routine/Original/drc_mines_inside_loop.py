# Imports
import numpy as np
import os
import sys
import csv
from decimal import *

# create a large region of interest, of which we will create lots of jobs for
# upper right and lower left corners, orientated NS
upper_lon = Decimal(sys.argv[4]).quantize(Decimal('.1'))
upper_lat = Decimal(sys.argv[5]).quantize(Decimal('.1'))
lower_lon = Decimal(sys.argv[2]).quantize(Decimal('.1'))
lower_lat = Decimal(sys.argv[3]).quantize(Decimal('.1'))

# Coordinate String
coords = str(lower_lon)+'_'+str(lower_lat)+'_'+str(upper_lon)+'_'+str(upper_lat)

# the above is a 0.5x0.5 degree box
# create jobs that work on 0.1x0.1 degree tiles
grid_space = Decimal(sys.argv[1]).quantize(Decimal('.1'))

# the small grid we want to work with, in kilometers (1km x 1km)
small_grid = Decimal(sys.argv[6])

#  get the numnber of x,y tiles we will loop over
n_lon = int(np.ceil((upper_lon - lower_lon)/grid_space ))
n_lat = int(np.ceil((upper_lat - lower_lat)/grid_space ))

# total number of jobs we will generate through this script
num_jobs = n_lon*n_lat

# Set up a CSV file that will contain a row for each segment of the selected region with the coordinates and status
# each job created by this script will add lines to this file
header = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
          'Percent Vegetation Loss', 'Percent Bare Initial', 'Percent Significant VH Values', 'Average NIR/G', 'Average SWIR1/B']

# Open the file in the write mode
# gee_dcr_squareSize_lonMin_latMin_lonMax_latMax
f = open('/scratch/nason.e/gee/results_csv/'+'gee_dcr_'+str(small_grid)+'_'+coords+'.csv', 'w', newline='')

writer = csv.writer(f)
writer.writerow(header)

f.close()

# let's start from the bottom left 
for i in range(n_lon):
    lon_min = i*grid_space + lower_lon
    lon_max = (i+1)*grid_space + lower_lon
    for j in range(n_lat):
        lat_min = j*grid_space + lower_lat
        lat_max = (j+1)*grid_space + lower_lat
        # filename is the highest res we will work with, plus the large square bounds, sent to bash_files folder
        bash_filename = 'bash_files/inner/gee_dcr_'+str(small_grid)+'_'+str(lon_min)+'_'+str(lat_min)+'_'+str(lon_max)+'_'+str(lat_max)+'.sh'
        with open(bash_filename,'w') as f:
            # one node, one hour
            # name of job is DCR_i_j
            # 2 GB memory
            # load up conda with personal environment name (emily -> newEnv)
            # execute 'drc_mines_base.py'
            # the arguments passed are the bounding box (.05x.05 degree for now) plus the high res sample size
            # output files sent to output_files/inner folder, with file names [job ID].out
            f.write('#!/bin/bash'+'\n')
            f.write('#SBATCH --nodes=1'+'\n')
            f.write('#SBATCH --time=01:00:00'+'\n')
            f.write('#SBATCH --job-name=DCR_'+str(i)+'_'+str(j)+'\n')
            f.write('#SBATCH --partition=short'+'\n')
            f.write('#SBATCH --mem=2GB'+'\n')
            f.write('#SBATCH --output=/scratch/nason.e/gee/output_files/inner/%j.out'+'\n')
            f.write('module load anaconda3/2022.01'+'\n')
            f.write('source activate '+'\n')
            f.write('source activate newEnv'+'\n')
            f.write('conda activate newEnv'+'\n')
            f.write('conda init bash'+'\n')
            f.write('python3 drc_mines_base.py '+str(small_grid)+' '+str(lon_min)+' '+str(lat_min)+' '+str(lon_max)+' '+str(lat_max)+' '+coords+' '+str(num_jobs)+' \n')
        # now we will submit the job (the bash_filename) written above
        os.system("sbatch "+str(bash_filename))
