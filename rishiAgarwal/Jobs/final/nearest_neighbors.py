from csv import reader
from sklearn.neighbors import BallTree
import sys
import math

results_file_path = sys.argv[1]
mapbox_file_path = sys.argv[2]

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
    #This is for distance in metersm
    if d <= 1000:
        count += 1

print("% within 1km of a mapbox point:", (count/total) * 100)

count = 0
for d in distances:
    #This is for distance in metersm
    if d <= 5000:
        count += 1

print("% within 5km of a mapbox point:", (count/total) * 100)

count = 0
for d in distances:
    #This is for distance in metersm
    if d <= 10000:
        count += 1

print("% within 10km of a mapbox point:", (count/total) * 100)
