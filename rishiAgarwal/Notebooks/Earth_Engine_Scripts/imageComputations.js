//THIS CODE HAS BEEN ALTERED TO BE USED FOR THE LANDSAT 8 DATASET
var admin1 = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level1");
var landsat8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
var karnataka = admin1.filter(ee.Filter.eq('ADM1_NAME', 'Karnataka'))
var geometry = karnataka.geometry()
var rgbVis = {bands: ['B4', 'B3', 'B2'], min: 0.0, max: 3000};

var filtered = landsat8//.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 100))
  .filter(ee.Filter.date('2019-01-01', '2020-01-01'))
  .filter(ee.Filter.bounds(geometry))
  .sort('CLOUD_COVER')
  
var composite = filtered.median().clip(geometry)
Map.addLayer(composite, rgbVis, 'Karnataka Composite')  

// This function calculates both NDVI an d NDWI indices
// and returns an image with 2 new bands added to the original image.
function addIndices(image) {
  var ndvi = image.normalizedDifference(['B5', 'B4']).rename('ndvi');
  var ndwi = image.normalizedDifference(['B3', 'B5']).rename('ndwi');
  return image.addBands(ndvi).addBands(ndwi);
}

// Map the function over the collection
var withIndices = filtered.map(addIndices);

// Composite
var composite = withIndices.median()
print(composite)

// Extract the 'ndwi' band and display a NDWI map
// use the palette ['white', 'blue']
// Hint: Use .select() function to select a band
var ndwiComposite = composite.select('ndwi').clip(karnataka)

var ndwiVis = {min: 0.0, max: 0.5, palette: ['white', 'blue']}

Map.addLayer(ndwiComposite, ndwiVis, 'ndwi')
