from csv import reader,writer
import numpy as np
import ee
ee.Initialize()

# For a given CSV file of region coordinates and test values, calculate and document whether this region may be a mining location
# All results will be saved in "[file_name]_status.csv"
# Passing region results only will be saved in "[file_name]_status_passing.csv"

# Open the input file in read mode and output file in write mode
with open('compiled_25.75_-11.csv', 'r') as read_obj, \
        open('compiled_25.75_-11_status.csv', 'w', newline='') as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    next(csv_reader) # skip header
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Add header to output file, with status column
    # Add header to output file, with status column
    header_list = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
                   'Percent Vegetation Loss', 'Percent Bare Initial', 'Percent Significant VH Values', \
                   'Average NIR/G', 'Average SWIR1/B', 'NASA Elev', 'GEDI Elev', 'Elev Loss','GEDI Qual. Flag',\
                   'B5 Value', 'B6 Value', 'NDMI', 'Center Lon', 'Center Lat','Elevation Score', \
                   'Band Variation Score','Status']
    csv_writer.writerow(header_list)
    # Read each row of the input csv file as list
    for row in csv_reader:
        """
        Calculate Status and append to the end of the row/list
        Passing Criteria:
        If Vegetation Loss < 20% and Bare Earth > 20%: 
            SAR VH > 25% and NIR/G <= 0.3 and SWIR1/B < 0.65 and Elevation Score >= 5 and B5/B6 Score >= 4
        Else: 
            Vegetation Loss > 20% and SAR VH > 25% and NIR/G <= 0.3 and SWIR1/B < 0.65
        """
        vegetation_loss = float(row[4])
        percent_bare = float(row[5])
        sar_vh = float(row[6])
        nir_g = float(row[7])
        swir1_b = float(row[8])
        elevation_score = float(row[18])
        b5_b6_score = float(row[19])

        if vegetation_loss < 20 and percent_bare > 20:
            status = sar_vh > 25 and nir_g <= 0.3 and swir1_b < 0.65 and elevation_score >= 5 and b5_b6_score >= 4
        else: 
            status = vegetation_loss > 20 and sar_vh > 25 and nir_g <= 0.3 and swir1_b < 0.65

        if status:
            row.append('Pass')
        else: 
            row.append('Fail')
        # Add the updated row / list to the output file
        csv_writer.writerow(row)

# Create a file of only passing statuses
with open('compiled_25.75_-11_status.csv', 'r') as r, \
        open('compiled_25.75_-11_passing.csv', 'w', newline='') as w:
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
            if row[20] == "Pass":
                csv_writer.writerow(row)
                

task.start()