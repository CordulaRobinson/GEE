from csv import *

# Open the input file in read mode and output file in write mode
with open('results_csv/all_regions.csv', 'r') as read_obj, \
        open('results_csv/all_regions_status.csv', 'w', newline='') as write_obj:
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

with open('results_csv/all_regions_status.csv', 'r') as r, \
        open('results_csv/all_regions_status_passing.csv', 'w', newline='') as w:
    csv_reader = reader(r)
    csv_writer = writer(w)
    csv_writer.writerow(header_list)
    # Skip Header 
    header = next(csv_reader)
    if header != None:
        # add passing rows to new file
        for row in csv_reader:
            if row[9] == "Pass":
                csv_writer.writerow(row)
