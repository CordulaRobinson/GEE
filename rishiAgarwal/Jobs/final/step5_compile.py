import os
import csv
#import ee
import ast
import pandas as pd
import glob

# Put all relevant CSV files into a list
os.chdir("/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/final/results") # change to your own path to the 'results' folder
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# Header
header_list = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
      'Percent Vegetation Loss', 'Percent Bare Initial','Percent Significant VH Values', 'Average NIR/G', 'Average SWIR1/B']

# Combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# Export to csv, file name = compiled.csv, with header
combined_csv.to_csv( "compiled.csv", header=header_list, index=False, encoding='utf-8-sig')

# Remove extraneous files
os.chdir("/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/final/") # change to your own path
os.system("rm -rf results/job*")
os.system("rm -rf output/slurm*")
os.system("rm -rf batch/routine*")
os.system("rm queue.txt")
os.system("rm failed.txt")
os.system("rm -rf slurm*")
os.system("rm start_routine.sh")
