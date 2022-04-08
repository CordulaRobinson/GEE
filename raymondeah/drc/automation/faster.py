import ee
import os
ee.Initialize()

g = ee.Geometry.Polygon(
        [[[29.554129272985683, 3.1591674847348235],
          [29.554129272985683, 3.092319151883147],
          [29.625197083044277, 3.092319151883147],
          [29.625197083044277, 3.1591674847348235]]])

f = ee.Feature(g).set('veg loss', 3).set('nir/g', 42)

fc = ee.FeatureCollection(f)

link = fc.getDownloadURL('csv', filename='test_csv')

os.chdir('routine')
os.system("wget -O work.csv "+link)
# #os.system("cd output")
# os.system("unzip boston_commons.zip")
# os.system("mv boston_commons.tif output")
# os.system("rm -rf boston_commons*")


