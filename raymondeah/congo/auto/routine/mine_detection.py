# py imports
import os
import sys
import csv
import math
import ee
ee.Initialize()

# datasets
ls5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
s2 = ee.ImageCollection("COPERNICUS/S2_SR")
admin = ee.FeatureCollection("FAO/GAUL/2015/level0")

# regions
roi1 = ee.Geometry.Polygon(
        [[[29.554129272985683, 3.1591674847348235],
          [29.554129272985683, 3.092319151883147],
          [29.625197083044277, 3.092319151883147],
          [29.625197083044277, 3.1591674847348235]]])

drc = admin.filter(ee.Filter.eq('ADM0_NAME', 'Democratic Republic of the Congo'))

# visualization parameters

# training data - landsat
bare = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([29.566649352977876, 3.131936594576548]),
            {
              "landcover": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([29.594069479589553, 3.143136886698536]),
            {
              "landcover": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([29.578229613742543, 3.109209943820683]),
            {
              "landcover": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([29.581158585986806, 3.1067030888196494]),
            {
              "landcover": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([29.55884031463487, 3.11517956941471]),
            {
              "landcover": 0,
              "system:index": "4"
            })])

vegetation = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([29.581819366025293, 3.132088091449441]),
            {
              "landcover": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([29.595938514279688, 3.131445322675145]),
            {
              "landcover": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([29.59962923388418, 3.1347448648629315]),
            {
              "landcover": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([29.565039466428125, 3.104877202480009]),
            {
              "landcover": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([29.607741346488673, 3.1193612914096605]),
            {
              "landcover": 1,
              "system:index": "4"
            })])

# training data - sentinel
bare_s = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([29.588761955782978, 3.110552597531067]),
            {
              "landcover": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([29.590113789126484, 3.1101669284095776]),
            {
              "landcover": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([29.570400011069342, 3.114240974803364]),
            {
              "landcover": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([29.56574369621949, 3.114048140935224]),
            {
              "landcover": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([29.566300979571633, 3.1296952794920045]),
            {
              "landcover": 0,
              "system:index": "4"
            })])

vegetation_s = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([29.61279975505381, 3.134623171579494]),
            {
              "landcover": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([29.620696178393654, 3.1514206812868597]),
            {
              "landcover": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([29.60730659099131, 3.15656272195781]),
            {
              "landcover": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([29.609366527514748, 3.1041127202608414]),
            {
              "landcover": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([29.561301341967873, 3.0982847807562592]),
            {
              "landcover": 1,
              "system:index": "4"
            })])

# cloud masking functions

# cloud mask landsat
def maskL457sr(image):
    qaMask = image.select('QA_PIXEL').bitwiseAnd(int('11111', 2)).eq(0)
    saturationMask = image.select('QA_RADSAT').eq(0)

    opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)

    return image.addBands(opticalBands, None, True) \
        .updateMask(qaMask) \
        .updateMask(saturationMask)

# cloud mask sentinel
def maskS2clouds(image):
    qa = image.select('QA60')

    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11

    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))

    return image.updateMask(mask).divide(10000).select("B.*") \
        .copyProperties(image, ["system:time_start"])

# training classifiers
# landsat
training = bare.merge(vegetation)
composite1985 = ls5 \
        .filter(ee.Filter.bounds(roi1)) \
        .filter(ee.Filter.date('1985-01-01', '1986-01-01')) \
        .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
        .map(maskL457sr) \
        .select('SR_B.*') \
        .median() \
        .clip(roi1)

# Overlay the point on the image to get training data.
training = composite1985.sampleRegions(**{
  'collection': training,
  'properties': ['landcover'],
  'scale': 1
})

# Train a classifier.
classifier_ls = ee.Classifier.smileRandomForest(50).train(**{
  'features': training,
  'classProperty': 'landcover',
  'inputProperties': composite1985.bandNames()
})

# sentinel
training = bare_s.merge(vegetation_s)

composite2021 = s2 \
        .filter(ee.Filter.bounds(roi1)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(maskS2clouds) \
        .select('B.*') \
        .median() \
        .clip(roi1) \

# Overlay the point on the image to get training data.
training = composite2021.sampleRegions(**{
  'collection': training,
  'properties': ['landcover'],
  'scale': 1
})

# Train a classifier.
classifier_s2 = ee.Classifier.smileRandomForest(50).train(**{
  'features': training,
  'classProperty': 'landcover',
  'inputProperties': composite2021.bandNames()
})

# vegetation percentage change
def calculate_percentage_change(feature):
    g = feature.geometry()
    
    composite_ls = ls5 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('1985-01-01', '1990-12-31')) \
        .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
        .map(maskL457sr) \
        .select('SR_B.*') \
        .median() \
        .clip(g)

    composite_s2 = s2 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(maskS2clouds) \
        .select('B.*') \
        .median() \
        .clip(g)
    
    left_classified = composite_ls.classify(classifier_ls)
    right_classified = composite_s2.classify(classifier_s2)
    
    # Reclassify from 0-1 to 1-2
    left_classes = left_classified.remap([0, 1], [1, 2])
    right_classes = right_classified.remap([0, 1], [1, 2])

    initial_vegetation = left_classes.eq(2)
    bare = right_classes.eq(1)
    vegetation_to_bare = initial_vegetation.And(bare)
    
    area_image = vegetation_to_bare.multiply(ee.Image.pixelArea())

    area = area_image.reduceRegion(**{
      'reducer': ee.Reducer.sum(),
      'geometry': g,
      'scale': 100,
      'maxPixels': 1e10
    })

    area_vegetation_to_bare = ee.Number(area.get('remapped')).divide(1e6)

    area_initial_vegetation = left_classified.eq(1).multiply(ee.Image.pixelArea())

    area2 = area_initial_vegetation.reduceRegion(**{
      'reducer': ee.Reducer.sum(),
      'geometry': g,
      'scale': 100,
      'maxPixels': 1e10
    })

    area_initial_vegetation = ee.Number(area2.get('classification')).divide(1e6)
    
    percent_loss = area_vegetation_to_bare.divide(area_initial_vegetation).multiply(100)
    
    ## account for loss of vegetation from before 1985
    
    #area of image
    total_area = g.area()
    total_SqKm = ee.Number(total_area).divide(1e6)
    #area of bare earth 2021
    bare_image = bare.multiply(ee.Image.pixelArea())

    area3 = bare_image.reduceRegion(**{
      'reducer': ee.Reducer.sum(),
      'geometry': g,
      'scale': 100,
      'maxPixels': 1e10
    })

    area_bare = ee.Number(area3.get('remapped')).divide(1e6)
    
    percent_bare = area_bare.divide(total_SqKm).multiply(100)
        
    return feature.set('percent loss',  percent_loss).set('percent bare', percent_bare)

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

# routine
def filter_by_vegetation_loss(squares, threshold1, threshold2):
    with_percent_change = squares.map(calculate_percentage_change)
    passed = with_percent_change.filter((ee.Filter.gt('percent loss', threshold1)).Or(ee.Filter.gt('percent bare', threshold2)))
    return passed

def applyRoutine(geometry, zoom, square_size):
    segments = ee.FeatureCollection(create_segments(geometry, square_size)).filter(ee.Filter.bounds(drc))
    
    passed_vegetation_loss = filter_by_vegetation_loss(segments, 20, 20)
    return passed_vegetation_loss

#print('start test run')
test_run = applyRoutine(roi1, 12, 1).getInfo()['features']
# for element in test_run:
#     print(element['geometry']['coordinates'])
#     print()
#print(element for element in test_run)
#print('ran without issues')

# # txt file
# save_path = os.getcwd()
# file_name = 'final_squares'
# complete_path = save_path + '/output/' + file_name + '.txt'
# file = open(complete_path, 'w')
# text = ""
# for element in test_run:
#     coords = element['geometry']['coordinates'][0][1:]
#     for coord in coords:
#         text += str(coord[0]) + ',' + str(coord[1]) + '\n'
#     text += '\n'
# file.write(text)
# file.close()

# csv file
save_path = os.getcwd()
file_name = 'square_coords'
complete_path = save_path + '/output/' + file_name + '.csv'

f = open(complete_path, 'a')
writer = csv.writer(f)
for element in test_run:
  coords = element['geometry']['coordinates'][0][1:]
  row = [c[0] + c[1] for c in coords]
  writer.writerow(row)
f.close()