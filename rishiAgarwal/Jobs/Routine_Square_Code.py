import ee
import math
import csv
import sys
import argparse

ee.Initialize()

region = ee.Geometry.Polygon(
    [[[ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[5])],
      [ee.Number.parse(sys.argv[2]), ee.Number.parse(sys.argv[3])],
      [ee.Number.parse(sys.argv[4]), ee.Number.parse(sys.argv[3])],
      [ee.Number.parse(sys.argv[4]), ee.Number.parse(sys.argv[5])]]])


#Imported Satellites and Feature Collections
ls5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
s2 = ee.ImageCollection("COPERNICUS/S2_SR")
admin = ee.FeatureCollection("FAO/GAUL/2015/level0")
active_mines = ee.FeatureCollection("users/rishiAgarwal/Congo_Active_Mines")
s1 = ee.ImageCollection('COPERNICUS/S1_GRD')

#Regions
rayroi1 = ee.Geometry.Polygon(
        [[[29.554129272985683, 3.1591674847348235],
          [29.554129272985683, 3.092319151883147],
          [29.625197083044277, 3.092319151883147],
          [29.625197083044277, 3.1591674847348235]]])

rayroi2 = ee.Geometry.Polygon(
        [[[30.246670960050185, 1.7911944738716732],
          [30.246670960050185, 1.7103797163160706],
          [30.356362579923232, 1.7103797163160706],
          [30.356362579923232, 1.7911944738716732]]])

rayall = ee.Geometry.Polygon(
        [[[22.92587933089792, 5.5911393992628495],
          [22.92587933089792, -13.776973382582892],
          [31.45126995589792, -13.776973382582892],
          [31.45126995589792, 5.5911393992628495]]])

emily_area = ee.Geometry.Polygon(
        [[[25.599767416235804, -10.585427828449394],
          [25.599767416235804, -10.82359555219894],
          [25.977297323462366, -10.82359555219894],
          [25.977297323462366, -10.585427828449394]]])

emily_area1 = ee.Geometry.Polygon(
        [[[25.75, -10.75],
          [25.75, -10.8],
          [25.9, -10.8],
          [25.9, -10.75]]])
emily_area2 = ee.Geometry.Polygon(
        [[[25.8, -10.6],
          [25.8, -10.7],
          [25.95, -10.7],
          [25.95, -10.6]]])
emily_area3 = ee.Geometry.Polygon(
        [[[26, -10.5],
          [26, -10.75],
          [26.25, -10.75],
          [26.25, -10.5]]])
emily_area4 = ee.Geometry.Polygon(
        [[[25.95, -10.6],
          [25.95, -10.7],
          [26.05, -10.7],
          [26.05, -10.6]]])

focus = ee.Geometry.Polygon(
        [[[27.350233348102517, -7.518171474050515],
          [27.350233348102517, -7.57841301205225],
          [27.436407359332986, -7.57841301205225],
          [27.436407359332986, -7.518171474050515]]])

geometry = ee.Geometry.Polygon(
        [[[-75.17882512894244, 39.96166702064832],
          [-75.17882512894244, 39.93337275121306],
          [-75.14191793289751, 39.93337275121306],
          [-75.14191793289751, 39.96166702064832]]])

#Visualizations
rgb_vis_ls5 = {
    'min': 8211.7,
    'max': 11077.3,
    'bands': ['SR_B3', 'SR_B2', 'SR_B1']
}

rgb_vis_s2 = {
  'min': 0.0,
  'max': 3000,
  'bands': ['B4', 'B3', 'B2'],
}

rgb_vis_s2_scaled = {
  'min': 0.0,
  'max': 0.3,
  'bands': ['B4', 'B3', 'B2']
}

vvVis = {
    'opacity': 1,
    'bands': ["VV"],
    'min': -13.375350094403828,
    'max': -3.6299557970059952,
    'gamma': 1
}

vhVis = {
    'opacity': 1,
    'bands': ["VH"],
    'min': -21.945806268850372,
    'max': -10.8330283399149,
    'gamma': 1
}

#Classification Points
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

#Cloud Masking Function
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

#Training the Classifier 
training = bare.merge(vegetation)
composite1985 = ls5 \
        .filter(ee.Filter.bounds(rayroi1)) \
        .filter(ee.Filter.date('1985-01-01', '1986-01-01')) \
        .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
        .map(maskL457sr) \
        .select('SR_B.*') \
        .median() \
        .clip(rayroi1)

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

# Classify the image.
classified = composite1985.classify(classifier_ls)

training = bare_s.merge(vegetation_s)

composite2021 = s2 \
        .filter(ee.Filter.bounds(rayroi1)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(maskS2clouds) \
        .select('B.*') \
        .median() \
        .clip(rayroi1) \

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

# Classify the image.
classified = composite2021.classify(classifier_s2)

#Calculation Methods
#Calculating Percentange Change in Vegetation Loss
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
        .clip(g) \
    
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
    
    
    total_area = g.area()
    total_SqKm = ee.Number(total_area).divide(1e6)
    
    bare_image = bare.multiply(ee.Image.pixelArea())
    
    area3 = bare_image.reduceRegion(**{
        'reducer': ee.Reducer.sum(),
        'geometry': g,
        'scale': 50,
        'maxPixels': 1e10
    })
    
    area_bare = ee.Number(area3.get('remapped')).divide(1e6)
    
    percent_bare = area_bare.divide(total_SqKm).multiply(100)
    
    return feature.set('percent loss',  percent_loss).set('percent bare', percent_bare)

#Calculate NIR/G Value in a Region
def calculate_nirg_value(feature):
    g = feature.geometry()
    composite_s2 = s2 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(maskS2clouds) \
        .select('B.*') \
        .median() \
        .clip(g) 
    nirg = composite_s2.normalizedDifference(['B8', 'B3']).rename('nirg')
    stats = nirg.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': g,
        'scale': 100,
        'maxPixels': 1e10
    })
    nirg_val = stats.get('nirg')
    
    return feature.set('nirg', nirg_val)

#Calculate SWIR/B Value 
def calculate_swirb_value(feature):
    g = feature.geometry()
    composite_s2 = s2 \
        .filter(ee.Filter.bounds(g)) \
        .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(maskS2clouds) \
        .select('B.*') \
        .median() \
        .clip(g) 
    swirb = composite_s2.normalizedDifference(['B11', 'B2']).rename('swirb')
    stats = swirb.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': g,
        'scale': 100,
        'maxPixels': 1e10
    })
    swirb_val = stats.get('swirb')
    
    return feature.set('swirb', swirb_val)


#Calculate SAR Value
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

#Divide GIven Geometry to Specficed Square Size (Km)
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


segments = ee.FeatureCollection(create_segments(region, ee.Number.parse(sys.argv[1]).getInfo()))


def passing_mine(region):
    region_veg = calculate_percentage_change(region)
    region_vh = calculate_sar_vh(region)
    region_nir_g = calculate_nirg_value(region)
    region_swir1_b = calculate_swirb_value(region)
    status = ((((ee.Number(region_veg.get('percent loss'))).gt(20)).Or((ee.Number(region_veg.get('percent bare'))).gt(10))) \
        .And(ee.Number(region_vh.get('vh_percent')).gt(5)) \
        .And(ee.Number(region_nir_g.get('nir/g')).lte(0.45)) \
        .And(ee.Number(region_swir1_b.get('swir1/b')).lt(0.65)))
    return ee.Feature(region.set('status', status))

results = segments.map(passing_mine)

def create_results(feature):
    coords = ee.List(feature.geometry().coordinates().get(0))
    lon_min = ee.List(coords.get(0)).get(0)
    lon_max = ee.List(coords.get(1)).get(0)
    lat_min = ee.List(coords.get(0)).get(1)
    lat_max = ee.List(coords.get(2)).get(1)
    status = feature.get('status')
    row = ee.Array([lon_min, 
           lat_min, 
           lon_max,
           lat_max,
           status])
    new_feature = ee.Feature(None, {'info': row})
    return new_feature

data_set = results.map(create_results)
data_set2 = data_set.aggregate_array('info')
data_set3 = data_set2.getInfo()

header = ['min long', 'min lat', 'max long', 'max lat', 'status']

f = open('/scratch/agarwal.rishi/gee/'+'gee_drc_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'_'+sys.argv[5]+'.csv', 'a', newline='')

writer = csv.writer(f)

writer.writerow(header)
writer.writerows(data_set3)

f.close()

"""

#Filtering Methods


########## Filter by Veg Loss
def filter_by_vegetation_loss(squares, threshold1, threshold2):
    with_percent_change = squares.map(calculate_percentage_change)
    passed = with_percent_change.filter((ee.Filter.gt('percent loss', threshold1)).Or(ee.Filter.gt('percent bare', threshold2)))
    return passed

########## Filter by NIR/G Value
def filter_by_nirg(squares, threshold):
    with_nirg = squares.map(calculate_nirg_value)
    passed = with_nirg.filter(ee.Filter.lte('nirg', threshold))
    return passed

########## Filter by SWIR/B Value
def filter_by_swirb(squares, threshold):
    with_swirb = squares.map(calculate_swirb_value)
    passed = with_swirb.filter(ee.Filter.lte('swirb', threshold))
    return passed

########## Filter by SAR Value
def filter_by_vh_percent(squares, threshold):
    with_change = squares.map(calculate_sar_vh)
    passed = with_change.filter(ee.Filter.gt('vh_percent', threshold))
    return passed

def applyRoutine_squares(geometry, square_size):
    drc = admin.filter(ee.Filter.eq('ADM0_NAME', 'Democratic Republic of the Congo'))

    segments = ee.FeatureCollection(create_segments(geometry, square_size)).filter(ee.Filter.bounds(drc))

    passed_vegetation_loss = filter_by_vegetation_loss(segments, 20, 10)
    passed_sar_vh = filter_by_vh_percent(passed_vegetation_loss, 5)
    passed_nirg = filter_by_nirg(passed_sar_vh, 0.45)
    passed_swirb = filter_by_swirb(passed_nirg, 0.65)
    completed = passed_swirb
    
    return completed

def create_csv(passed):
    header = ['Point 1', 'Point 2', 'Point 3', 'Point 4']
    with open('/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/square_points.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for square in passed:
            coords = [square.coordinates().getInfo()[0]]
            writer.writerow([coords[0], coords[1], coords[2], coords[3]])

def main(square_size, minlong, minlat, maxlong, maxlat):
  geometry = ee.Geometry.Polygon(
    [[[minlong, maxlat],
      [minlong, minlat],
      [maxlong, minlat],
      [maxlong, maxlat]]])
  print(geometry)
  passed_squares = applyRoutine_squares(geometry, square_size)
  create_csv(passed_squares)

if __name__ == '__main__':
  print(sys.argv[5])
  main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])


#main(0.5, 27.350233348102517, -7.57841301205225, 27.436407359332986, -7.518171474050515)

"""