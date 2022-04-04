from csv import *

# For a given CSV file of region coordinates and test values, calculate and document whether this region may be a mining location
# All results will be saved in "compiled_status.csv"
# Passing region results only will be saved in "compiled_status_passing.csv"

# Open the input file in read mode and output file in write mode
with open('results/compiled.csv', 'r') as read_obj, \
        open('results/compiled_status.csv', 'w', newline='') as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Add header to output file, with status column
    header_list = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
          'Percent Vegetation Loss', 'Percent Bare Initial', 'Percent Significant VH Values', 'Average NIR/G', 'Average SWIR1/B', 'Status']
    csv_writer.writerow(header_list)
    # Skip Header in input file
    header = next(csv_reader)
    if header != None:
    # Read each row of the input csv file as list
        for row in csv_reader:
            # Calculate Status and append to the end of the row/list
            status = (((float(row[4]) > 20) or (float(row[5]) > 10))and (float(row[6]) > 5) and (float(row[7]) <= 0.45) and (float(row[8]) < 0.65))
            if status:
                row.append("Pass")
            else: 
                row.append("Fail")
            # Add the updated row / list to the output file
            csv_writer.writerow(row)

# Create a file of only passing statuses
with open('results/compiled_status.csv', 'r') as r, \
        open('results/compiled_passing.csv', 'w', newline='') as w:
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
            if row[9] == "Pass":
                csv_writer.writerow(row)
                
# Convert to a Feature Collection
with open('results/compiled_status.csv', 'r') as r, \
        open('results/compiled_fc.csv', 'w', newline='') as w:
    # Create a csv.reader object from the input file object
    csv_reader = reader(r)
    # Create a csv.writer object from the output file object
    csv_writer = writer(w)
    # Skip Header in input file
    header = next(csv_reader)
    if header != None:
        # Add rows to new file in a Feature Collection set-up
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
