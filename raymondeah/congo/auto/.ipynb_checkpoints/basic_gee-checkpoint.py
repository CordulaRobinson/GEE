import ee
ee.Initialize()

s2 = ee.ImageCollection("COPERNICUS/S2_SR")
neu = ee.Geometry.Polygon(
        [[[42.35, -71.10],
          [42.35, -71.08],
          [42.37, -71.08],
          [42.37, -71.10]]])

test = ee.Number(2).add(ee.Number(3))
