//Imports
var focus = 
    /* color: #ff2bef */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[27.350233348102517, -7.518171474050515],
          [27.350233348102517, -7.57841301205225],
          [27.436407359332986, -7.57841301205225],
          [27.436407359332986, -7.518171474050515]]], null, false),
    water = 
    /* color: #0f43ff */
    /* shown: false */
    ee.FeatureCollection([]),
    vegetation = /* color: #33ff00 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([27.376517541901784, -7.543591078372139]),
            {
              "landcover": 2,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([27.418746240632252, -7.539506842444226]),
            {
              "landcover": 2,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([27.36587453653069, -7.552780468215639]),
            {
              "landcover": 2,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([27.373770959870534, -7.569967505969657]),
            {
              "landcover": 2,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([27.389392145173268, -7.5590767891937025]),
            {
              "landcover": 2,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([27.428359277741627, -7.523680064445619]),
            {
              "landcover": 2,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([27.375659235017018, -7.522999329851055]),
            {
              "landcover": 2,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([27.38836217691155, -7.531026599579952]),
            {
              "landcover": 2,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([27.356089838044362, -7.564891220186839]),
            {
              "landcover": 2,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([27.403640039460377, -7.56931554740874]),
            {
              "landcover": 2,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([27.35385824014397, -7.522857852300823]),
            {
              "landcover": 2,
              "system:index": "10"
            })]),
    bare = /* color: #d63000 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([27.401675991909222, -7.540000356472741]),
            {
              "landcover": 0,
              "system:index": "0"
            })]),
    modisVis = {"min":0,"max":4000,"gamma":1.4},
    modis = ee.ImageCollection("MODIS/006/MCD43A4");

//Scripts
Map.setCenter(27.3954, -7.55, 13) //Kanunka Village

var area = focus.area({'maxError': 1}).divide(1e6)
print(area)

var roi2000 = modis
//.filter(ee.Filter.lt('CLOUD_COVER', 25))
.filter(ee.Filter.date('2001-01-01', '2002-01-01'))
.filter(ee.Filter.bounds(focus))
.select('Nadir_Reflectance_Band1', 'Nadir_Reflectance_Band4', 'Nadir_Reflectance_Band3')
.median()
.clip(focus)

print(roi2000)
Map.addLayer(roi2000, modisVis, '2000')

var training = bare.merge(water).merge(vegetation)

var training = roi2000.sampleRegions({
  collection: training,
  properties: ['landcover'],
  scale: 10
})

var classifier = ee.Classifier.smileRandomForest(50).train({
  features: training,
  classProperty: 'landcover',
  inputProperties: roi2000.bandNames()
})

var classified2000 = roi2000.classify(classifier)
Map.addLayer(classified2000, {min: 0, max: 2, palette: ['red', 'blue', 'green']}, '2000_classified')

// Calculate Area by Class
var areaImage = ee.Image.pixelArea().divide(1e6).addBands(classified2000);

// Using a Grouped Reducer
var areas = areaImage.reduceRegion({
      reducer: ee.Reducer.sum().group({
      groupField: 1,
      groupName: 'classification',
    }),
    geometry: focus,
    scale: 100,
    tileScale: 4,
    maxPixels: 1e10
    }); 
var classAreas = ee.List(areas.get('groups'))

var vegetation2000 = ee.Number(ee.Dictionary(classAreas.get(1)).get('sum'))
var bare2000 = ee.Dictionary(classAreas.get(0)).get('sum')
print("Vegetation Area in 2000: ", vegetation2000)
print("Bare Area in 2000: ", bare2000)


var roi2020 = modis
.filter(ee.Filter.date('2020-01-01', '2021-01-01'))
.filter(ee.Filter.bounds(focus))
.select('Nadir_Reflectance_Band1', 'Nadir_Reflectance_Band4', 'Nadir_Reflectance_Band3')
.median()
.clip(focus)

Map.addLayer(roi2020, modisVis, '2020')

var classified2020 = roi2020.classify(classifier)
Map.addLayer(classified2020, {min: 0, max: 2, palette: ['red', 'blue', 'green']}, '2020_classified')

// Calculate Area by Class
var areaImage = ee.Image.pixelArea().divide(1e6).addBands(classified2020);

// Using a Grouped Reducer
var areas = areaImage.reduceRegion({
      reducer: ee.Reducer.sum().group({
      groupField: 1,
      groupName: 'classification',
    }),
    geometry: focus,
    scale: 100,
    tileScale: 4,
    maxPixels: 1e10
    }); 
var classAreas = ee.List(areas.get('groups'))
var vegetation2020 = ee.Number(ee.Dictionary(classAreas.get(1)).get('sum'))
var bare2020 = ee.Number(ee.Dictionary(classAreas.get(0)).get('sum'))
print("Vegetation Area in 2020: ", vegetation2020)
print("Bare Area in 2020: ", bare2020)

var percentageLoss = (vegetation2000.subtract(vegetation2020)).divide(vegetation2000)
print("Percentage of Vegetation Lost: ", percentageLoss)

