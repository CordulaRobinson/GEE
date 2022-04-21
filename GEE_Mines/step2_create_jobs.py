import os
import sys
import math
import ee
ee.Initialize()

region = ee.Geometry.Polygon(
        [[[ee.Number.parse(sys.argv[1]), ee.Number.parse(sys.argv[3])],
          [ee.Number.parse(sys.argv[1]), ee.Number.parse(sys.argv[4])],
          [ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[4])],
          [ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[3])]]])

"""
slight modification of the 'create_segments' method in our routine:
- original: divides the given geometry into squares of given size and returns a list of squares
- new:      divides the given geometry into squares of given size and submits a job for each square
"""
def create_segments(geometry, size):
    # grab the top left coordinate of the bounding box
    coords = ee.List(geometry.coordinates().get(0)).slice(0, -1)
    top = ee.Number(ee.List(coords.get(2)).get(1))
    left = ee.Number(ee.List(coords.get(0)).get(0))
    top_left_point = ee.Geometry.Point([left, top])
    
    # calculate square pixel width and height
    width = int(ee.Geometry.Point(coords.get(0)).distance(ee.Geometry.Point(coords.get(1))).divide(1000 * size).getInfo()) 
    # how many squares can fit in the width of the bounding box
    height = int(ee.Geometry.Point(coords.get(1)).distance(ee.Geometry.Point(coords.get(2))).divide(1000 * size).getInfo()) 
    # how many squares can fit in the height of the bounding box
    
    # create a point buffer and use it to find the km distance to lat/lon degree conversion
    buff = top_left_point.buffer(size*1000, 0.1) # create the buffer with a max % error of 0.1
    buff_list = ee.List(buff.coordinates().get(0)) 
    buff_length = buff_list.length()
    right_pt = ee.List(buff_list.get(buff_length.multiply(0.75).int().subtract(1)))
    bottom_pt = ee.List(buff_list.get(buff_length.multiply(0.5).int().subtract(1)))
    new_lat = ee.Number(right_pt.get(0)) # given distance east of the top left point
    new_lon = ee.Number(bottom_pt.get(1)) # given distance south of the top left point
    
    diff_lon = top.subtract(new_lon) # given size converted to degrees
    diff_lat = new_lat.subtract(left)
        
    count = 0
    for y in range(height + 1): # +1 to guarantee we will cover the whole region (squares may extend slightly past the bounding box)
        left = ee.Number(ee.List(coords.get(0)).get(0))
        for x in range(width + 1):
            new_lat = left.add(diff_lat)
            new_lon = top.subtract(diff_lon)
            
            # create and submit jobs here
            bash_filename = 'batch/routine_job_' + str(1000000 + count) + '.sh'
            with open(bash_filename,'w') as f:
                f.write('#!/bin/bash'+'\n')
                f.write('#SBATCH --nodes=1'+'\n')
                f.write('#SBATCH --time=01:00:00'+'\n')
                f.write('#SBATCH --job-name=routine_job'+'\n')
                f.write('#SBATCH --partition=short'+'\n')
                f.write('#SBATCH --mem=64GB'+'\n')
                f.write('#SBATCH --output=output/slurm-%j.out'+'\n')
                f.write('module load anaconda3/3.7'+'\n')
                f.write('source activate '+'\n')
                f.write('source activate ee'+'\n')
                f.write('conda activate ee'+'\n')
                f.write('conda init bash'+'\n')
                f.write('python3 step3_routine.py ' + str(left.getInfo()) + ' ' + str(new_lat.getInfo()) + ' ' + str(top.getInfo()) + ' ' + str(new_lon.getInfo()) + ' ' + str(count) + '\n')

            os.system("sbatch "+str(bash_filename))

            count += 1
            left = new_lat
        top = new_lon

# submit jobs with 10x10km size
create_segments(region, 10)

# wait while jobs are still running
os.system('squeue -u eah.r > queue.txt')
while not os.system('grep routine queue.txt'):
    os.system('squeue -u eah.r > queue.txt')

# after all jobs are finished, resubmit failed jobs
os.system('python3 step4_rerun.py')

# wait while jobs are still running
os.system('squeue -u eah.r > queue.txt')
while not os.system('grep routine queue.txt'):
    os.system('squeue -u eah.r > queue.txt')

# after all jobs are finished, compile results
os.system('python3 step5_compile.py')
