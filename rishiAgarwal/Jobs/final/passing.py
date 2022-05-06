from csv import *
import sys
import ee
ee.Initialize()

file_name = sys.argv[1]

header_list = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
                   'Percent Vegetation Loss', 'Percent Bare Initial', 'Percent Significant VH Values', \
                   'Average NIR/G', 'Average SWIR1/B', 'NASA Elev', 'GEDI Elev', 'Elev Loss','GEDI Qual. Flag',\
                   'B5 Value', 'B6 Value', 'Center Lon', 'Center Lat','Elevation Score', \
                   'Band Variation Score','Status']

# Create a file of only passing statuses
with open('results/' + file_name + '_status.csv', 'r') as r, \
        open('results/' + file_name + '_status_passing.csv', 'w', newline='') as w:
    # Create a csv.reader object from the input file object
    csv_reader = reader(r)
    # Create a csv.writer object from the output file object
    csv_writer = writer(w)
    # Add header to output file, with status column
    csv_writer.writerow(header_list)
    # Skip Header in input file
    header = next(csv_reader)
    if header != None:
        # Add passing rows to new file
        for row in csv_reader:
            if row[19] == "Pass":
                csv_writer.writerow(row)