# IMPORTS
import os
import sys
import csv
import math
import ee
ee.Initialize()

# DATASETS
ls5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
s2 = ee.ImageCollection("COPERNICUS/S2_SR")
admin = ee.FeatureCollection("FAO/GAUL/2015/level0")

training_region = ee.Geometry.Polygon(
        [[[29.554129272985683, 3.1591674847348235],
          [29.554129272985683, 3.092319151883147],
          [29.625197083044277, 3.092319151883147],
          [29.625197083044277, 3.1591674847348235]]])

# system arguments
left, right, top, bot = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] 
#job_num = sys.argv[5]
#print('JOB NUMBER: ' + job_num) # records job number in slurm file so we know which to rerun
region = ee.Geometry.Polygon(
        [[[ee.Number.parse(left), ee.Number.parse(top)],
          [ee.Number.parse(left), ee.Number.parse(bot)],
          [ee.Number.parse(right), ee.Number.parse(bot)],
          [ee.Number.parse(right), ee.Number.parse(top)]]])

# TRAINING DATA
# landsat
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

# sentinel
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

# CLOUD MASKING FUNCTIONS
# landsat
def mask_ls5_clouds(image):
    qaMask = image.select('QA_PIXEL').bitwiseAnd(int('11111', 2)).eq(0)
    saturationMask = image.select('QA_RADSAT').eq(0)

    opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)

    return image.addBands(opticalBands, None, True) \
        .updateMask(qaMask) \
        .updateMask(saturationMask)

# sentinel
def mask_s2_clouds(image):
    qa = image.select('QA60')

    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11

    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))

    return image.updateMask(mask).divide(10000).select("B.*") \
        .copyProperties(image, ["system:time_start"])

# TRAINING CLASSIFIERS
# landsat
training = bare.merge(vegetation)
composite1985 = ls5 \
        .filter(ee.Filter.bounds(training_region)) \
        .filter(ee.Filter.date('1985-01-01', '1986-01-01')) \
        .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
        .map(mask_ls5_clouds) \
        .select('SR_B.*') \
        .median() \
        .clip(training_region)

# overlay the point on the image to get training data
training = composite1985.sampleRegions(**{
  'collection': training,
  'properties': ['landcover'],
  'scale': 1
})

# train a classifier
classifier_ls = ee.Classifier.smileRandomForest(50).train(**{
  'features': training,
  'classProperty': 'landcover',
  'inputProperties': composite1985.bandNames()
})

# sentinel
training = bare_s.merge(vegetation_s)

composite2021 = s2 \
        .filter(ee.Filter.bounds(training_region)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(mask_s2_clouds) \
        .select('B.*') \
        .median() \
        .clip(training_region) \

# overlay the point on the image to get training data
training = composite2021.sampleRegions(**{
  'collection': training,
  'properties': ['landcover'],
  'scale': 1
})

# train a classifier
classifier_s2 = ee.Classifier.smileRandomForest(50).train(**{
  'features': training,
  'classProperty': 'landcover',
  'inputProperties': composite2021.bandNames()
})

# VERTICAL FILTER CALCULATIONS
# vegetation percentage change
def calculate_percentage_change(feature):
    g = feature.geometry()
    
    composite_ls = ls5 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('1985-01-01', '1990-12-31')) \
        .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
        .map(mask_ls5_clouds) \
        .select('SR_B.*') \
        .median() \
        .clip(g)

    composite_s2 = s2 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(mask_s2_clouds) \
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

# sar
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
    
    #area of image
    total_area = g.area()
    total_SqKm = ee.Number(total_area).divide(1e6)
    
    #area of possible mines
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

# nir/g
def calculate_nir_g(feature):
    g = feature.geometry()
    
    # Images and Bands
    composite_s2 = s2 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(mask_s2_clouds) \
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

# swir1/b
def calculate_swir1_b(feature):
    g = feature.geometry()
    composite_s2 = s2 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(mask_s2_clouds) \
        .select('B.*') \
        .median() \
        .clip(g) 
    swirb = composite_s2.normalizedDifference(['B11', 'B2']).rename('SWIR1/B')
    stats = swirb.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': g,
        'scale': 30,
        'maxPixels': 1e10
    })
    swirb_val = stats.get('SWIR1/B')
    
    return feature.set('swir/b', swirb_val)


def get_NASADEM(feature):
    """
    Here we use the more modern NASA DEM that merges SRTM with IceSAT, ASTER and PRISM data 
    We will call it: NASADEM in the output .csv file.
    """
    g = feature.geometry()
    srtm = ee.Image('NASA/NASADEM_HGT/001').select('elevation')
    red_srtm = srtm.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': g,
        'scale': 30
    })
    mean = ee.Number(red_srtm.get('elevation'))
    return feature.set('elevation',mean)


def calc_gedi_loss(feature):
    """
    Here we will get the GEDI highest elevation score and 
    subtract the NASA SRTM DEM (not the updated one from NASA).
    Hence, elevation loss with time will be negative (new - old < 0) == potential mine
    I commented out a few extra bands from the GEDI collection that may be useful
    such as landsat water, time of collection, non-veg from modis etc. 
    """
    g = feature.geometry()
    """
    gedi_coll = ee.ImageCollection("LARSE/GEDI/GEDI02_A_002_MONTHLY")\
                  .filter(ee.Filter.bounds(g))\
                  .select('elev_highestreturn','digital_elevation_model','elev_lowestmode','digital_elevation_model_srtm','quality_flag'
                         ,'landsat_water_persistence','delta_time','modis_nonvegetated','modis_treecover','urban_proportion').median().clip(g)
    """
    gedi_coll = ee.ImageCollection("LARSE/GEDI/GEDI02_A_002_MONTHLY")\
                  .filter(ee.Filter.bounds(g))\
.select('elev_highestreturn','digital_elevation_model','digital_elevation_model_srtm','quality_flag').median().clip(g)
                  
    
    x = gedi_coll
    srtm = x.select('digital_elevation_model_srtm')
    gedi = x.select('elev_highestreturn')

    loss = gedi.subtract(srtm).rename('loss')
    
    # Averaging Loss
    avg_loss = loss.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': g,
        'scale': 30
    })
    loss = ee.Number(avg_loss.get('loss'))
    
    # Avergaing GEDI
    avg_gedi = gedi.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': g,
        'scale': 30
    })
    gedi_mean = ee.Number(avg_gedi.get('elev_highestreturn'))

    return feature.set('loss',loss).set('GEDI',gedi_mean)

"""
Segment the given geometry into squares of given size (in km)
:param geometry: rectangle form geometry object
:return:         list of all created squares
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

def filter_by_vh_percent(squares, threshold):
    with_change = squares.map(calculate_sar_vh)
    passed = with_change.filter(ee.Filter.gt('vh_percent', threshold))
    return passed

def filter_by_nir_g(squares, threshold):
    with_change = squares.map(calculate_nir_g)
    passed = with_change.filter(ee.Filter.lte('nir/g', threshold))
    return passed

def filter_by_swir1_b(squares, threshold):
    with_swir1_b = squares.map(calculate_swir1_b)
    passed = with_swir1_b.filter(ee.Filter.lte('swir/b', threshold))
    return passed

####################################################################################################################
# old routine (coordinates of passing squares only)

# def apply_routine(geometry, zoom, square_size):
#     drc = admin.filter(ee.Filter.eq('ADM0_NAME', 'Democratic Republic of the Congo'))
#     segments = ee.FeatureCollection(create_segments(geometry, square_size)).filter(ee.Filter.bounds(drc))
    
#     passed_vegetation_loss = filter_by_vegetation_loss(segments, 0.1, 0.1)
#     passed_sar_vh = filter_by_vh_percent(passed_vegetation_loss, 5)
#     passed_swir_b = filter_by_swir1_b(passed_sar_vh, 0.62)
#     passed_nir_g = filter_by_nir_g(passed_swir_b, 0.45)
#     return passed_nir_g
#     # return passed_vegetation_loss

# test_run = apply_routine(region, 12, 0.25).getInfo()['features']

# # csv file
# if test_run:
#   save_path = os.getcwd()
#   file_name = 'job_' + str(1000000 + int(job_num))
#   complete_path = save_path + '/results/' + file_name + '.csv'

#   f = open(complete_path, 'a')
#   writer = csv.writer(f)

#   rows = []
#   for element in test_run:
#     row = []
#     for c in element['geometry']['coordinates'][0][1:]:
#       row.append(c[0])
#       row.append(c[1])
#     rows.append(row)

#   #rows = [[[c[0]] + [c[1]] for c in element['geometry']['coordinates'][0][1:]] for element in test_run]
#   writer.writerows(rows)

#   f.close()

########################################################################################################################################
# # new routine (storing all information)

def passing_mine(feature):
  veg = calculate_percentage_change(feature)
  sar = calculate_sar_vh(feature)
  nir_g = calculate_nir_g(feature)
  swir1_b = calculate_swir1_b(feature)
  NASADEM = get_NASADEM(feature)
  GEDI = calc_gedi_loss(feature)
  return ee.Feature(feature \
    .set('vegetation loss', veg.get('percent loss')) \
    .set('percent bare', veg.get('percent bare')) \
    .set('vh', sar.get('vh_percent')) \
    .set('nir/g', nir_g.get('nir/g')) \
    .set('swir1/b', swir1_b.get('swir/b'))\
    .set('NASADEM Elevation',NASADEM.get('elevation')) \
    .set('GEDI Elevation',GEDI.get('GEDI'))\
    .set('GEDI-SRTM Elevation',GEDI.get('loss')))

def create_results(feature):
    coords = ee.List(feature.geometry().coordinates().get(0))
    lon_min = ee.List(coords.get(0)).get(0)
    lon_max = ee.List(coords.get(1)).get(0)
    lat_min = ee.List(coords.get(0)).get(1)
    lat_max = ee.List(coords.get(2)).get(1)
    veg_loss = feature.get('vegetation loss')
    bare_init = feature.get('percent bare')
    vh = feature.get('vh')
    nir_g = feature.get('nir/g')
    swir1_b = feature.get('swir1/b')
    nasadem = feature.get('NASADEM Elevation')
    gedi_elev = feature.get('GEDI Elevation')
    gedi_loss = feature.get('GEDI-SRTM Elevation')
    row = ee.Array([lon_min, 
                   lat_min, 
                   lon_max,
                   lat_max,
                   veg_loss,
                   bare_init, 
                   vh,
                   nir_g,
                   swir1_b,
                   nasadem,
                   gedi_elev, 
                   gedi_loss])
    new_feature = ee.Feature(None, {'info': row})
    return new_feature

## ------------------- ##

# regions = create_segments(region, 0.25)
# segments = ee.FeatureCollection(regions)
# v = filter_by_vegetation_loss(segments, 0.1, 0.1)
# results = v.map(passing_mine)

# file_name = 'job_' + str(1000000 + int(job_num)) + '.csv'
# link = results.getDownloadURL('csv', filename=file_name)
# os.chdir('results')
# os.system("wget -O " + file_name + " " +link)
# # os.system('curl -o ' + file_name + ' ' + link)

## ------------------- ##

# Calculate values for 250m x 250m squares
regions = create_segments(region, 0.25)
segments = ee.FeatureCollection(regions)
results = segments.map(passing_mine)

# Create above array for each segment, and transform into format that can be written to a CSV file
data_set = results.map(create_results)
data_set2 = data_set.aggregate_array('info')
data_set3 = data_set2.getInfo() # <- slow

# CSV name
save_path = os.getcwd()
file_name = 'job_' + str(1000000 + int(job_num))
# 'results' folder must be created beforehand
complete_path = save_path + '/results/' + file_name + '.csv'

# CSV header
#header_list = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
 #     'Percent Vegetation Loss', 'Percent Bare Initial','Percent Significant VH Values', 'Average NIR/G', 'Average SWIR1/B', 'NASADEM Elevation', GEDI Elevation,'GEDI-SRTM Elevation']

# Create CSV and add header & data
with open(complete_path, 'w') as f:
    writer = csv.writer(f)
    #writer.writerow(header_list)
    writer.writerows(data_set3)

f.close()

