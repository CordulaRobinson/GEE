import os
import csv
#import ee
import ast
import pandas as pd
import glob

# Put all relevant CSV files into a list
os.chdir("/scratch/nason.e/gee/results") # change to your own path to the 'results' folder
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
os.chdir("/scratch/nason.e/gee") # change to your own path
os.system("rm -rf results/job*")
os.system("rm -rf output/slurm*")
os.system("rm -rf batch/routine*")
os.system("rm queue.txt")
os.system("rm failed.txt")
os.system("rm -rf slurm*")
os.system("rm start_routine.sh")

# Convert to a Feature Collection
with open('results/compiled_status.csv', 'r') as r, \
        open('results/compiled_fc.csv', 'w', newline='') as w:
    csv_reader = reader(r)
    csv_writer = writer(w)
    csv_writer.writerow(header_list)
    # Skip Header 
    header = next(csv_reader)
    if header != None:
        # Add passing rows to new file
        new_header = ['Coordinates', 'Percent Vegetation Loss', 'Percent Bare Initial',\
                       'Percent Significant VH Values', 'Average NIR/G', 'Average SWIR1/B', 'Status']
        csv_writer.writerow(new_header)
        for row in csv_reader:
            region = [[[float(row[0]), float(row[3])],
                      [float(row[0]), float(row[1])],
                      [float(row[2]), float(row[1])],
                      [float(row[2]), float(row[3])]]]
            new_row = [region, row[4], row[5], row[6], row[7], row[8], row[9]]
            csv_writer.writerow(new_row)