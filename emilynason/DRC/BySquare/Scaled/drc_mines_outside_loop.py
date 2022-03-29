# Imports
import numpy as np
import os
import sys
import time
import glob
import pandas as pd
import csv
from decimal import *

# create a large region of interest, of which we will create lots of jobs for
# upper right and lower left corners, orientated NS

# ray roi1 and surrounding
# upper_lon = Decimal('29.6') #30
# upper_lat = Decimal('3.2') #10
# lower_lon = Decimal('29.5') #28
# lower_lat = Decimal('3') #8

# emily area
upper_lon = Decimal('26').quantize(Decimal('.1'))
upper_lat = Decimal('-10.5').quantize(Decimal('.1'))
lower_lon = Decimal('25').quantize(Decimal('.1'))
lower_lat = Decimal('-11').quantize(Decimal('.1'))

# create jobs that work on 0.1x0.1 degree tiles
grid_space = Decimal('0.5').quantize(Decimal('.1'))

grid_space2 = Decimal('0.1')

# the small grid we want to work with, in kilometers
small_grid = 2 # 5 KM x 5 KM squares

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
        # filename is the next grid size down we will work with, plus the large square bounds, sent to bash_files folder
        bash_filename = 'bash_files/outer/gee_dcr_'+str(grid_space2)+'_'+str(lon_min)+'_'+str(lat_min)+'_'+str(lon_max)+'_'+str(lat_max)+'.sh'
        with open(bash_filename,'w') as f:
            # one node, one hour
            # name of job is DCR_i_j
            # 2 GB memory
            # load up conda with personal environment name (emily -> newEnv)
            # execute 'drc_mines_inside_loop.py'
            # the arguments passed are the bounding box (.1x.1 degree for now) plus the next grid size down (0.05)
            # output files sent to output_files/outer folder, with file names [job ID].out
            f.write('#!/bin/bash'+'\n')
            f.write('#SBATCH --nodes=1'+'\n')
            f.write('#SBATCH --time=01:00:00'+'\n')
            f.write('#SBATCH --job-name=DCR_'+str(i)+'_'+str(j)+'\n')
            f.write('#SBATCH --partition=short'+'\n')
            f.write('#SBATCH --mem=2GB'+'\n')
            f.write('#SBATCH --output=/scratch/nason.e/gee/output_files/outer/%j.out'+'\n')
            f.write('module load anaconda3/2022.01'+'\n')
            f.write('source activate '+'\n')
            f.write('source activate newEnv'+'\n')
            f.write('conda activate newEnv'+'\n')
            f.write('conda init bash'+'\n')
            f.write('python3 drc_mines_inside_loop.py '+str(grid_space2)+' '+str(lon_min)+' '+str(lat_min)+' '+str(lon_max)+' '+str(lat_max)+' '+str(small_grid)+'\n')
        # now we will submit the job (the bash_filename) written above
        os.system("sbatch "+str(bash_filename))
        # wait to move onto the next job until this one has finished adding results to the csv
        while not os.path.exists('/scratch/nason.e/gee/results_csv/gee_dcr_' \
                                 +str(small_grid)+'_'+str(lon_min)+'_'+str(lat_min)+'_'+str(lon_max)+'_'+str(lat_max)+'_done.csv'):
            time.sleep(15)
            
## final bounding box:
## lon_max = upper_lon, lat_max = upper_lat
# if upper_lon >= 0:
#     final_lon_min = (upper_lon - grid_space)
# else:
#     final_lon_min = (upper_lon + grid_space)
# if upper_lat >= 0:
#     final_lat_min = (upper_lat - grid_space)
# else:
#     final_lat_min = (upper_lat + grid_space)

final_lon_min = (upper_lon - grid_space)
final_lat_min = (upper_lat - grid_space)
    
# Once the last csv file is finished, concat into one file called "all_regions.csv"  
# Check if file exists
while not os.path.exists('/scratch/nason.e/gee/results_csv/gee_dcr_' \
                         +str(small_grid)+'_'+str(final_lon_min)+'_'+str(final_lat_min)+'_'+str(upper_lon)+'_'+str(upper_lat)+'_done.csv'):
    time.sleep(30)

# Once it exists copy all regions and their data into new csv file named all_regions.csv
if os.path.isfile('/scratch/nason.e/gee/results_csv/gee_dcr_' \
                  +str(small_grid)+'_'+str(final_lon_min)+'_'+str(final_lat_min)+'_'+str(upper_lon)+'_'+str(upper_lat)+'_done.csv'):
    os.chdir("/scratch/nason.e/gee/results_csv")

    # Pattern for desired file names in selected directory: ends in 'csv'
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # Combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    # Export to csv, file name = all_regions.csv
    combined_csv.to_csv( "all_regions.csv", index=False, encoding='utf-8-sig')
    
else:
    raise ValueError("%s isn't a file!" % file_path)
    
# Wait for above file to be created, then create a new file containing only the passing regions (status == 1)
# Check if file exists yet
while not os.path.exists("/scratch/nason.e/gee/results_csv/all_regions.csv"):
    time.sleep(30)

# Once file exists, copy all passing regions and their data into new csv file named all_regions_passing.csv
if os.path.isfile("/scratch/nason.e/gee/results_csv/all_regions.csv"):
    with open('all_regions.csv','r') as fin, open ('all_regions_passing.csv','w') as fout:
        writer = csv.writer(fout, delimiter=',')
        header = ['min lon', 'min lat', 'max lon', 'max lat', 'status']
        writer.writerow(header)
        for row in csv.reader(fin, delimiter=','):
            if row[4] == '1':
                 writer.writerow(row)
else:
    raise ValueError("%s isn't a file!" % file_path)
