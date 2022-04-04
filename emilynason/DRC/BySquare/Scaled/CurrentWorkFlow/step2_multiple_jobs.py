import os
import sys
import math
import ee
ee.Initialize()

"""
sys:
2 3 4 5
l r u d
job:
coordinates, job number
"""

# Selected Region
region = ee.Geometry.Polygon(
        [[[ee.Number.parse(sys.argv[1]), ee.Number.parse(sys.argv[3])],
          [ee.Number.parse(sys.argv[1]), ee.Number.parse(sys.argv[4])],
          [ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[4])],
          [ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[3])]]])

# Function to divide region into smaller squares
"""
Segment the given geometry into squares of given size (in km)
:param geometry: rectangle form geometry object
:return: run bash file on each square
"""
def create_segments(geometry, size):
    r_earth, dy, dx, pi = ee.Number(6378), ee.Number(size), ee.Number(size), ee.Number(math.pi)
    
    coords = ee.List(geometry.coordinates().get(0)).slice(0, -1)
    
    top = ee.Number(ee.List(coords.get(2)).get(1))
    left = ee.Number(ee.List(coords.get(0)).get(0))
    
    width = int(ee.Geometry.Point(coords.get(0)).distance(ee.Geometry.Point(coords.get(1))).divide(1000 * size).getInfo())
    height = int(ee.Geometry.Point(coords.get(1)).distance(ee.Geometry.Point(coords.get(2))).divide(1000 * size).getInfo())

    count = 0
    for y in range(height + 1):
        left = ee.Number(ee.List(coords.get(0)).get(0))
        for x in range(width + 1):
            first = top
            second = dx.divide(r_earth)
            third = ee.Number(180).divide(pi)
            con = pi.divide(ee.Number(180))
            fourth = left.multiply(con).multiply(con).cos()
            
            new_lon = first.subtract(second.multiply(third).divide(fourth))
            new_lat = left.add((dy.divide(r_earth)).multiply((ee.Number(180).divide(pi))))
            
            # Create and submit jobs here
            # 'batch' folder must be created beforehand
            bash_filename = 'batch/routine_job_' + str(1000000 + count) + '.sh'
            with open(bash_filename,'w') as f:
                # one node, one hour
                # name of job is routine_job
                # 16 GB memory
                # load up conda
                # execute 'step3_mine_detection.py'
                # the arguments passed are the smaller bounding box (lon min, lat min, lat max, lon max) and the job count (start at 0)
                f.write('#!/bin/bash'+'\n')
                f.write('#SBATCH --nodes=1'+'\n')
                f.write('#SBATCH --time=01:00:00'+'\n')
                f.write('#SBATCH --job-name=routine_job'+'\n')
                f.write('#SBATCH --partition=short'+'\n')
                f.write('#SBATCH --mem=16GB'+'\n')
                f.write('#SBATCH --output=output/slurm-%j.out'+'\n') # 'output' folder must be created beforehand
                f.write('module load anaconda3/3.7'+'\n')
                f.write('source activate '+'\n')
                f.write('source activate newEnv'+'\n') # change to your own anaconda environment
                f.write('conda activate newEnv'+'\n') # change to your own anaconda environment
                f.write('conda init bash'+'\n')
                f.write('python3 step3_mine_detection.py ' + str(left.getInfo()) + ' ' + str(new_lat.getInfo()) + ' ' \
                        + str(top.getInfo()) + ' ' + str(new_lon.getInfo()) + ' ' + str(count) + '\n')

            # Now we will submit the job (the bash_filename) written abobe
            os.system("sbatch "+str(bash_filename))

            count += 1
            left = new_lat
        top = new_lon

# Create jobs on 10km by 10km squares
create_segments(region, 10)

os.system('squeue -u nason.e > queue.txt') # change to your own username
while not os.system('grep routine queue.txt'):
    os.system('squeue -u nason.e > queue.txt') # change to your own username

# All jobs are finished after exiting the loop

# Rerun failed jobs
os.system('python3 step4_rerun_failed_jobs.py')

os.system('squeue -u nason.e > queue.txt') # change to your own username
while not os.system('grep routine queue.txt'):
    os.system('squeue -u nason.e > queue.txt') # change to your own username

# Compile results and delete individual files
os.system('python3 step5_compile.py')