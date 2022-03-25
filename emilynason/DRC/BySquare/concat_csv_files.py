# Imports and Directory
import os
import glob
import pandas as pd
import csv
import time
os.chdir("/scratch/nason.e/gee/results_csv")

# Pattern for desired file names in selected directory: ends in 'csv'
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# Combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# Export to csv, file name = all_regions.csv
combined_csv.to_csv( "all_regions.csv", index=False, encoding='utf-8-sig')
                
# Wait for above file to be created, then create a new file containing only the passing regions (status == 1)
# Check if file exists yet
while not os.path.exists("/scratch/nason.e/gee/results_csv/all_regions.csv"):
    time.sleep(1)

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