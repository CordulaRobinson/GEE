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

region = ee.Geometry.Polygon(
        [[[ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[4])],
          [ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[5])],
          [ee.Number.parse(sys.argv[3]), ee.Number.parse(sys.argv[5])],
          [ee.Number.parse(sys.argv[3]), ee.Number.parse(sys.argv[4])]]])

# squares
"""
Segment the given geometry into squares of given size (in km)
:param geometry: rectangle form geometry object
:return: list including all squares

edit: remove some stuff from geometry produced
"""
def create_segments(geometry, size):
    segments = []
    r_earth, dy, dx, pi = ee.Number(6378), ee.Number(size), ee.Number(size), ee.Number(math.pi)
    
    coords = ee.List(geometry.coordinates().get(0)).slice(0, -1)
    
    top = ee.Number(ee.List(coords.get(2)).get(1))
    left = ee.Number(ee.List(coords.get(0)).get(0))
    
    width = int(ee.Geometry.Point(coords.get(0)).distance(ee.Geometry.Point(coords.get(1))).divide(1000 * size).getInfo())
    height = int(ee.Geometry.Point(coords.get(1)).distance(ee.Geometry.Point(coords.get(2))).divide(1000 * size).getInfo())

    for y in range(height + 1):
        left = ee.Number(ee.List(coords.get(0)).get(0))
        for x in range(width + 1):
            #
            first = top
            second = dx.divide(r_earth)
            third = ee.Number(180).divide(pi)
            con = pi.divide(ee.Number(180))
            fourth = left.multiply(con).multiply(con).cos()
            
            new_lon = first.subtract(second.multiply(third).divide(fourth))
            #new_lon = top - (dx / r_earth) * (180 / pi) / math.cos(math.radians(left * pi/180))
            #new_lat = left  + (dy / r_earth) * (180 / pi)
            new_lat = left.add((dy.divide(r_earth)).multiply((ee.Number(180).divide(pi))))
            
            square = ee.Geometry.Polygon(
                [[[left, new_lon],
                  [new_lat, new_lon],
                  [new_lat, top],
                  [left, top]]])
            
            segments.append(square)
            
            left = new_lat
        top = new_lon
        
    return segments
