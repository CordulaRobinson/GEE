import os
import sys
import csv
import ee
import geemap
import math

ee.Initalize

def bounding_box_func(feature):
	intermediate_buffer = feature.buffer(5000)
	intermediate_box = intermediate_buffer.bounds()
	return intermediate_box

def makeBoxGee(long, lat):
	point = [long, lat]
	pointCollection = ee.FeatureCollection(point)
	bounding_box = bounding_box_func(point)
	row = bouding_box

	f = open('/scratch/agarwal.rishi/testcsv.csv', 'w')
	writer = csv.writer(f)
	writer.writerow(row)
	f.close()

if __name__ == '__main__':
	makeBoxGee(int(sys.argv[1]), int(sys.argv[2]))

