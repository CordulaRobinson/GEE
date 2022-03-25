# import ee
# ee.Initialize()

# s2 = ee.ImageCollection("COPERNICUS/S2_SR")
# neu = ee.Geometry.Polygon(
#         [[[42.35, -71.10],
#           [42.35, -71.08],
#           [42.37, -71.08],
#           [42.37, -71.10]]])

# test = ee.Number(2).add(ee.Number(3))

import os
import ee
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
  'bands': ['B4', 'B3', 'B2']
}

composite = s2.filter(ee.Filter.bounds(geometry)) \
  .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
  .select('B.*') \
  .median() \
  .clip(geometry) \

visualized = composite.visualize(['B4', 'B3', 'B2'], None, None, 0, 3000)

# task = ee.batch.Export.image.toDrive(**{
#     'image': composite,
#     'description': 'Boston_Commons_Visualized',
#     'folder': 'earthengine',
#     'fileNamePrefix': 'boston_commons_visualized',
#     'region': geometry,
#     'scale': 20,
#     'maxPixels': 1e9
# })

# task.start()

link = visualized.getDownloadUrl({
  'name': 'boston_commons',
  'bands': ['vis-red', 'vis-green', 'vis-blue'],
  'scale': 20,
  'region': geometry,
  'filePerBand': False
})

os.system("wget -O boston_commons.zip "+link)
#os.system("cd output")
os.system("unzip boston_commons.zip")
os.system("mv boston_commons.tif output")
os.system("rm -rf boston_commons")
