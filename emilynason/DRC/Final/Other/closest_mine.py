import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from csv import *
 
# For each mine (data point) in the IPIS file (gdf2), find the nearest identified mine from our routine result file (gdf) 
# and calculate the distance in meters

# File containing passing regions and their coordinates from our routine
FILE_NAME = "results_drc2_retry/compiled_status_passing.csv"
USE_COLS = ['Center Lon', 'Center Lat']
 
df = pd.read_csv(
    FILE_NAME, delimiter=",", usecols=USE_COLS)
df.columns = [
    'x',
    'y'
]
gdf = GeoDataFrame(
    df.drop(['x', 'y'], axis=1),
    crs={'init': 'epsg:4326'},
    geometry=[Point(xy) for xy in zip(df.x, df.y)])


# File containing IPIS data point locations WITHIN THE BOUNDS OF THE REGION TESTED IN OUR ROUTINE
FILE_NAME_2 = "drc2_mapbox_mines.csv"
USE_COLS_2 = ['longitude', 'latitude']
 
df2 = pd.read_csv(
    FILE_NAME_2, delimiter=",", usecols=USE_COLS_2)
df2.columns = [
    'x',
    'y'
]
gdf2 = GeoDataFrame(
    df2.drop(['x', 'y'], axis=1),
    crs={'init': 'epsg:4326'},
    geometry=[Point(xy) for xy in zip(df2.x, df2.y)])


from sklearn.neighbors import BallTree
import numpy as np

def get_nearest(src_points, candidates, k_neighbors=1):
    """Find nearest neighbors for all source points from a set of candidate points"""

    # Create tree from the candidate points
    tree = BallTree(candidates, leaf_size=15, metric='haversine')

    # Find closest points and distances
    distances, indices = tree.query(src_points, k=k_neighbors)

    # Transpose to get distances and indices into arrays
    distances = distances.transpose()
    indices = indices.transpose()

    # Get closest indices and distances (i.e. array at index 0)
    # note: for the second closest points, you would take index 1, etc.
    closest = indices[0]
    closest_dist = distances[0]

    # Return indices and distances
    return (closest, closest_dist)

def nearest_neighbor(left_gdf, right_gdf, return_dist=False):
    """
    For each point in left_gdf, find closest point in right GeoDataFrame and return them.

    NOTICE: Assumes that the input Points are in WGS84 projection (lat/lon).
    """

    left_geom_col = left_gdf.geometry.name
    right_geom_col = right_gdf.geometry.name

    # Ensure that index in right gdf is formed of sequential numbers
    right = right_gdf.copy().reset_index(drop=True)

    # Parse coordinates from points and insert them into a numpy array as RADIANS
    left_radians = np.array(left_gdf[left_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())
    right_radians = np.array(right[right_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())

    # Find the nearest points
    # -----------------------
    # closest ==> index in right_gdf that corresponds to the closest point
    # dist ==> distance between the nearest neighbors (in meters)

    closest, dist = get_nearest(src_points=left_radians, candidates=right_radians)

    # Return points from right GeoDataFrame that are closest to points in left GeoDataFrame
    closest_points = right.loc[closest]

    # Ensure that the index corresponds the one in left_gdf
    closest_points = closest_points.reset_index(drop=True)

    # Add distance if requested
    if return_dist:
        # Convert to meters from radians
        earth_radius = 6371000  # meters
        closest_points['distance'] = dist * earth_radius

    return closest_points

# Find closest identified mine for each IPIS data point and get also the distance based on haversine distance
# Note: haversine distance which is implemented here is a bit slower than using e.g. 'euclidean' metric
# but useful as we get the distance between points in METERS
closest_mine = nearest_neighbor(gdf2, gdf, return_dist=True)
#print(closest_mine.head(3))

#closest_mine.to_file("results/closest_mine.csv")

df1 = pd.DataFrame(closest_mine)
df1.to_csv("closest_mine.csv")

# Open the input file in read mode and output file in write mode
with open('closest_mine.csv', 'r') as read_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    total_mines = 0
    close_enough = 0
    # Skip Header in input file
    header = next(csv_reader)
    if header != None:
        for row in csv_reader:
            total_mines = total_mines+1
            if (float(row[2]) < 5000):
                close_enough = close_enough+1
    percent_correct = close_enough / total_mines
    print('within 5 km:' + str(percent_correct))