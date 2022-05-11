from csv import reader
from sklearn.neighbors import BallTree
import math

results_file_path = 'GEE_Mines/backup/ray_extended_native/compiled_status_passing.csv'
mapbox_file_path = 'raymondeah/IPIS.csv'

with open(results_file_path, 'r') as read_obj:
    csv_reader = reader(read_obj)
    next(csv_reader, None) # skip header
    # center lat, center lon
    results = [[math.radians(float(row[16])), math.radians(float(row[15]))] for row in csv_reader] # sklearn requires radian inputs

with open(mapbox_file_path, 'r') as read_obj:
    csv_reader = reader(read_obj)
    next(csv_reader, None) # skip header
    # lat, lon
    mapbox = [[math.radians(float(row[1])), math.radians(float(row[2]))] for row in csv_reader] # sklearn requires radian inputs

# Create tree from detected mine locations
tree = BallTree(results, leaf_size=15, metric='haversine')
# For every mapbox point in 1x1 region, find distance to closest detected mine
distances, indices = tree.query(mapbox)
# Convert distances from radians to meters
distances = [d * 6371000 for d in distances]

# count the total number of mapbox points where a detected mine is <= 1km away
total = len(distances)
count = 0
for d in distances:
    if d <= 1000:
        count += 1

print("% within 1km of mapbox:", (count/total) * 100)
