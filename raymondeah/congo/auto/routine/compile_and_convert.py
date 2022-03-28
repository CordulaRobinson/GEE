import os
import csv

import ast

# os.system("cat output/*csv > output/compiled.csv")
# os.system("rm -rf slurm*")
# os.system("rm -rf output/square*")
# os.system("rm batch/*")

path = "c:/Users/r.eah/OneDrive - Northeastern University/gee/raymondeah/congo/auto/routine/output/compiled.csv"

restore = []
with open(path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        restore.append(row)

for row in restore[:5]:
    print(row)


