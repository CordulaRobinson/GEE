# import ee
# ee.Initialize()

# s2 = ee.ImageCollection("COPERNICUS/S2_SR")
# neu = ee.Geometry.Polygon(
#         [[[42.35, -71.10],
#           [42.35, -71.08],
#           [42.37, -71.08],
#           [42.37, -71.10]]])

# test = ee.Number(2).add(ee.Number(3))

import ee
import geemap
ee.Initialize()

geometry = ee.Geometry.Polygon(
        [[[-71.0731810860198, 42.35812148338074],
          [-71.0731810860198, 42.351271273134635],
          [-71.06144373937063, 42.351271273134635],
          [-71.06144373937063, 42.35812148338074]]])
s2 = ee.ImageCollection("COPERNICUS/S2_SR")

rgbVis = {
  'min': 0.0,
  'max': 3000,
  'bands': ['B4', 'B3', 'B2'],
}

composite = s2.filter(ee.Filter.bounds(geometry)) \
  .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
  .select('B.*') \
  .median() \
  .clip(geometry) \

# Map.centerObject(geometry, 15)
# Map.addLayer(composite, rgbVis, 'Boston Commons') 


visualized = composite.visualize(rgbVis)
# Map = geemap.Map()
# Map.centerObject(geometry, 15)
# Map.addLayer(composite, rgbVis,'BC')
# Map
# print(visualized)
# // Now the 'visualized' image is RGB image, no need to give visParams
# Map.addLayer(visualized, {}, 'Visualized Image') 

task = ee.batch.Export.image.toDrive(**{
    'image': composite,
    'description': 'Boston_Commons_Visualized',
    'folder': 'earthengine',
    'fileNamePrefix': 'boston_commons_visualized',
    'region': geometry,
    'scale': 20,
    'maxPixels': 1e9
})

task.start()
