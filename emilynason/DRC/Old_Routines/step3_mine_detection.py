import os
import sys
import csv
import math
import ee
ee.Initialize()

# Job Number
job_num = sys.argv[5]

# Datasets
ls5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
s2 = ee.ImageCollection("COPERNICUS/S2_SR")
admin = ee.FeatureCollection("FAO/GAUL/2015/level0")

# Regions
roi1 = ee.Geometry.Polygon(
        [[[29.554129272985683, 3.1591674847348235],
          [29.554129272985683, 3.092319151883147],
          [29.625197083044277, 3.092319151883147],
          [29.625197083044277, 3.1591674847348235]]])

region = ee.Geometry.Polygon(
        [[[ee.Number.parse(sys.argv[1]), ee.Number.parse(sys.argv[3])],
          [ee.Number.parse(sys.argv[1]), ee.Number.parse(sys.argv[4])],
          [ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[4])],
          [ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[3])]]])

drc = admin.filter(ee.Filter.eq('ADM0_NAME', 'Democratic Republic of the Congo'))

# Training data - Landsat5
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

# Training data - Sentinel-2
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

# Cloud masking functions

# cloud mask Landsat5
def maskL457sr(image):
    qaMask = image.select('QA_PIXEL').bitwiseAnd(int('11111', 2)).eq(0)
    saturationMask = image.select('QA_RADSAT').eq(0)

    opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)

    return image.addBands(opticalBands, None, True) \
        .updateMask(qaMask) \
        .updateMask(saturationMask)

# Cloud mask Sentinel-2
def maskS2clouds(image):
    qa = image.select('QA60')

    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11

    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))

    return image.updateMask(mask).divide(10000).select("B.*") \
        .copyProperties(image, ["system:time_start"])

# Training classifiers

# landsat5
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

# Sentinel-2
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

# Vegetation percentage change
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
    
    # Account for loss of vegetation from before 1985
    
    # Area of image
    total_area = g.area()
    total_SqKm = ee.Number(total_area).divide(1e6)
    
    # Area of bare earth in 2021
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

# SAR VH band
def calculate_sar_vh(feature):
    g = feature.geometry()
    
    # Images and Bands
    filtered = s1 \
        .filter(ee.Filter.eq('instrumentMode','IW')) \
        .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')) \
        .filter(ee.Filter.eq('resolution_meters',10)) \
        .filter(ee.Filter.intersects('.geo', g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .select('VH')

    composite = filtered.median().clip(g)
    
    # Area of image
    total_area = g.area()
    total_SqKm = ee.Number(total_area).divide(1e6)
    
    # Area of possible mines
    area_mines = composite.lt(-19).rename('mines')
    connect = area_mines.connectedPixelCount(25);
    area_mines = area_mines.updateMask(connect.gt(8));
    area_mines = area_mines.multiply(ee.Image.pixelArea())

    area = area_mines.reduceRegion(**{
      'reducer': ee.Reducer.sum(),
      'geometry': g,
      'scale': 30,
      'maxPixels': 1e10
    })

    mines_SqKm = ee.Number(area.get('mines')).divide(1e6)

    percent_mine = ee.Number(mines_SqKm.divide(total_SqKm).multiply(100))
    
    return feature.set('vh_percent', percent_mine)

# NIR/G
def calculate_nir_g(feature):
    g = feature.geometry()
    
    # Images and Bands
    composite_s2 = s2 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(maskS2clouds) \
        .select('B.*') \
        .median() \
        .clip(g)

    nir_g_s2 = composite_s2.normalizedDifference(['B8', 'B3']).rename('NIR/G')

    # Average NIR/G   
    stats_s2 = nir_g_s2.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': nir_g_s2.geometry(),
        'scale': 30
    })
    
    avg_s2 = ee.Number(stats_s2.get('NIR/G'))
    
    return feature.set('nir/g',  avg_s2)

# SWIR1/B
def calculate_swir1_b(feature):
    g = feature.geometry()
    composite_s2 = s2 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(maskS2clouds) \
        .select('B.*') \
        .median() \
        .clip(g) 
    swir1_b = composite_s2.normalizedDifference(['B11', 'B2']).rename('SWIR1/B')
    stats = swir1_b.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': g,
        'scale': 30,
        'maxPixels': 1e10
    })
    swir1_b_val = stats.get('SWIR1/B')
    
    return feature.set('swir1/b', swir1_b_val)

# Function to divide region into squares
"""
Segment the given geometry into squares of given size (in km)
:param geometry: rectangle form geometry object
:return: list including all squares
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
            first = top
            second = dx.divide(r_earth)
            third = ee.Number(180).divide(pi)
            con = pi.divide(ee.Number(180))
            fourth = left.multiply(con).multiply(con).cos()
            
            new_lon = first.subtract(second.multiply(third).divide(fourth))
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

# Calculate Values for each criteria for a region
def passing_mine(region):
    region_veg = calculate_percentage_change(region)
    region_vh = calculate_sar_vh(region)
    region_nir_g = calculate_nir_g(region)
    region_swir1_b = calculate_swir1_b(region)
    return ee.Feature(region.set('veg loss', region_veg.get('percent loss')).set('bare initial', region_veg.get('percent bare')) \
                      .set('vh', region_vh.get('vh_percent')) \
                      .set('nir/g', region_nir_g.get('nir/g')).set('swir1/b', region_swir1_b.get('swir1/b')))

# Create a property that is an array of the coordinates and values
def create_results(feature):
    coords = ee.List(feature.geometry().coordinates().get(0))
    lon_min = ee.List(coords.get(0)).get(0)
    lon_max = ee.List(coords.get(1)).get(0)
    lat_min = ee.List(coords.get(0)).get(1)
    lat_max = ee.List(coords.get(2)).get(1)
    veg_loss = feature.get('veg loss')
    bare_init = feature.get('bare initial')
    vh = feature.get('vh')
    nir_g = feature.get('nir/g')
    swir1_b = feature.get('swir1/b')
    row = ee.Array([lon_min, 
                   lat_min, 
                   lon_max,
                   lat_max,
                   veg_loss,
                   bare_init, 
                   vh,
                   nir_g,
                   swir1_b])
    new_feature = ee.Feature(None, {'info': row})
    return new_feature

# Calculate values for 250m x 250m squares
regions = create_segments(region, 0.25)
segments = ee.FeatureCollection(regions)
results = segments.map(passing_mine)

# Create above array for each segment, and transform into format that can be written to a CSV file
data_set = results.map(create_results)
data_set2 = data_set.aggregate_array('info')
data_set3 = data_set2.getInfo()

# CSV name
save_path = os.getcwd()
file_name = 'job_' + str(1000000 + int(job_num))
# 'results' folder must be created beforehand
complete_path = save_path + '/results/' + file_name + '.csv'

# CSV header
header_list = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
      'Percent Vegetation Loss', 'Percent Bare Initial','Percent Significant VH Values', 'Average NIR/G', 'Average SWIR1/B']

# Create CSV and add header & data
f = open(complete_path, 'w')
writer = csv.writer(f)

writer.writerow(header_list)
writer.writerows(data_set3)

f.close()
