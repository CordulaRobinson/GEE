from csv import *
import ee
ee.Initialize()

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
          'Percent Vegetation Loss', 'Percent Bare Initial', 'Percent Significant VH Values', \
              'Average NIR/G', 'Average SWIR1/B', 'NASA Elev', 'GEDI Elev', 'Elev Loss', 'Status' \
                  'B8 Value', 'B9 Value']
    csv_writer.writerow(header_list)
    # Read each row of the input csv file as list
    for row in csv_reader:
        # Calculate Status and append to the end of the row/list
        status = (((float(row[4]) > 20) or (float(row[5]) > 10))and (float(row[6]) > 5) and (float(row[7]) <= 0.45) and (float(row[8]) < 0.65) \
                 and (float(row[11]) < 0))
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
            if row[12] == "Pass":
                csv_writer.writerow(row)
                
# Convert to a Feature Collection
# Create a list of Geometries for areas that passed as possible mines
with open('results/compiled_passing.csv', 'r') as r:
    csv_reader = reader(r)
    # Skip Header in input file
    header = next(csv_reader)
    region_list = []
    if header != None:
        # Convert each region to a Geometry and add to a list
        for row in csv_reader:
            region = ee.Geometry.Polygon([[[float(row[0]), float(row[3])],
                      [float(row[0]), float(row[1])],
                      [float(row[2]), float(row[1])],
                      [float(row[2]), float(row[3])]]])
            region_list.append(region)

# Wrap geometry list in a Feature Collection
fc = ee.FeatureCollection(region_list)

# Export the Feature Collection to Google Earth Engine (GEE)
task = ee.batch.Export.table.toAsset(**{
  'collection': fc,
  'description':'compiled_results',
  'assetId': 'users/EmilyNason/compiledResults', # change to your GEE Asset path and a unique name (will not overwrite already existing assets, so old names cannot be reused)
})

task.start()
