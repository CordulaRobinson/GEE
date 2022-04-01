import os
import csv
#import ee
import ast

os.system("cat results/*csv > results/compiled.csv")
os.system("rm -rf results/square*")
os.system("rm -rf output/slurm*")
os.system("rm -rf slurm*")
os.system("rm -rf batch/routine*")
os.system("rm test.txt")
os.system("rm failed.txt")
os.system("rm start_routine.sh")

# path = "c:/Users/r.eah/OneDrive - Northeastern University/gee/raymondeah/congo/auto/routine/output/compiled.csv"

# restore = []
# with open(path, newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ')
#     for row in spamreader:
#         coords = row[0].split(',')
#         restore.append(coords)

# for row in restore[:5]:
#     print(row)

# fc = []
# for row in restore:
#     g = ee.Geometry.Polygon(
#         [[[float(row[0]), float(row[1])],
#           [float(row[2]), float(row[3])],
#           [float(row[4]), float(row[5])],
#           [float(row[6]), float(row[7])]]])
#     fc.append(g)

# final = ee.FeatureCollection(fc)

# roi1 = ee.Geometry.Polygon(
#         [[[29.554129272985683, 3.1591674847348235],
#           [29.554129272985683, 3.092319151883147],
#           [29.625197083044277, 3.092319151883147],
#           [29.625197083044277, 3.1591674847348235]]])
