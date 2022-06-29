//Imports
var rgbVis = {"min":0,"max":3000,"bands":["B4","B3","B2"]},
    ndviVis = {"min":0,"max":1,"palette":["white","green"]},
    mines = ee.FeatureCollection("users/rishiAgarwal/Congo_Active_Mines"),
    l8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2"),
    l8Vis = {"bands":["SR_B4","SR_B3","SR_B2"],"min":0,"max":0.3},
    focus = 
    /* color: #d63000 */
    /* shown: false */
    /* locked: true */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[27.350233348102517, -7.518171474050515],
          [27.350233348102517, -7.57841301205225],
          [27.436407359332986, -7.57841301205225],
          [27.436407359332986, -7.518171474050515]]], null, false),
    bare = 
    /* color: #f1ff95 */
    /* shown: false */
    /* locked: true */
    ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([27.395754099225957, -7.544871597505669]),
            {
              "landcover": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([27.377386331891973, -7.537681635986378]),
            {
              "landcover": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([27.38732880169815, -7.566302012094373]),
            {
              "landcover": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([27.367398564311944, -7.595602221406222]),
            {
              "landcover": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([27.41147788842375, -7.504780000398128]),
            {
              "landcover": 0,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([27.38004521428371, -7.493526432742291]),
            {
              "landcover": 0,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([27.34360148453469, -7.611271305729875]),
            {
              "landcover": 0,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([27.386131211016085, -7.6173522431103375]),
            {
              "landcover": 0,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([27.34001258905849, -7.595285013747063]),
            {
              "landcover": 0,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([27.44478484800152, -7.495163786969747]),
            {
              "landcover": 0,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([27.40378180987822, -7.556625837882082]),
            {
              "landcover": 0,
              "system:index": "10"
            })]),
    water = 
    /* color: #0b4a8b */
    /* shown: false */
    /* locked: true */
    ee.FeatureCollection([]),
    vegetation = 
    /* color: #08ff2c */
    /* shown: false */
    /* locked: true */
    ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([27.390402765244296, -7.537287014310612]),
            {
              "landcover": 2,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([27.422554914632553, -7.537967726465308]),
            {
              "landcover": 2,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([27.457745496907943, -7.548858975333595]),
            {
              "landcover": 2,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([27.43834776131224, -7.588167291752283]),
            {
              "landcover": 2,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([27.45637220589232, -7.604161856424537]),
            {
              "landcover": 2,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([27.326406003555217, -7.5358430396748135]),
            {
              "landcover": 2,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([27.391122342666545, -7.509056702441429]),
            {
              "landcover": 2,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([27.36554479750053, -7.502759654732929]),
            {
              "landcover": 2,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([27.3737674008712, -7.573578776003551]),
            {
              "landcover": 2,
              "system:index": "8"
            })]),
    nearMine = 
    /* color: #ff1dee */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[27.37902567836914, -7.548035163718408],
          [27.38016297449657, -7.54912002352839],
          [27.382158577354655, -7.550375048098138],
          [27.38400397496404, -7.550630365397892],
          [27.386793531738753, -7.546546097400271],
          [27.3884672335244, -7.544206147372354],
          [27.38623562873057, -7.543567953372247],
          [27.384690652806846, -7.543833883324707],
          [27.38108573339982, -7.54375945961597],
          [27.379626557022572, -7.545727136809308],
          [27.379154457120602, -7.546881150366418]]]),
    outlier = 
    /* color: #1488ff */
    /* shown: false */
    ee.Geometry.MultiPolygon(
        [[[[27.40117714611331, -7.528029420400128],
           [27.40143463817874, -7.529901416251066],
           [27.40237877575198, -7.5338155632667805],
           [27.404009558833035, -7.535347176386731],
           [27.403837897456082, -7.531603223645428],
           [27.402807929194363, -7.53075232078353],
           [27.402464606440457, -7.527518874674277]]],
         [[[27.401692130244168, -7.537219140622778],
           [27.40160629955569, -7.538835830496198],
           [27.402207114375027, -7.539516540215821],
           [27.40564034191409, -7.539091096766489],
           [27.40564034191409, -7.538410386377943]]],
         [[[27.38813088146487, -7.548791103460967],
           [27.38890335766116, -7.549046363857512],
           [27.391821601069363, -7.5484507560311345],
           [27.389761664545926, -7.546749014863657]]]]),
    WesternMine = 
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[27.35316117125328, -7.538673727373273],
          [27.35316117125328, -7.562838275361878],
          [27.372730568225936, -7.562838275361878],
          [27.372730568225936, -7.538673727373273]]], null, false),
    EasternMine = 
    /* color: #98ff00 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[27.37513382750328, -7.523187286499756],
          [27.37513382750328, -7.550926343072451],
          [27.41959412413414, -7.550926343072451],
          [27.41959412413414, -7.523187286499756]]], null, false),
    City = 
    /* color: #0b4a8b */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[27.39710648375328, -7.549224611648793],
          [27.39710648375328, -7.563008443442283],
          [27.413242653186874, -7.563008443442283],
          [27.413242653186874, -7.549224611648793]]], null, false),
    rishiroi_big = 
    /* color: #d63000 */
    /* shown: false */
    /* locked: true */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[26.869328146223438, -7.099221433164478],
          [26.869328146223438, -7.94332844727659],
          [28.017399435285938, -7.94332844727659],
          [28.017399435285938, -7.099221433164478]]], null, false);

//Scripts
Map.setCenter(27.3954, -7.55, 13) //Kanunka Village

//Helps for visiblity of the Landsat8 images
function applyScaleFactors(image) {
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);
  return image.addBands(opticalBands, null, true)
              .addBands(thermalBands, null, true);
}
var landsat8 = l8.map(applyScaleFactors)

var area = EasternMine.area({'maxError': 1}).divide(1e6)
print(area)

//ADDING INDICIES TO THE ROI IMAGE
var addIndices = function(image) {
  var ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename(['ndvi']);
  var ndbi = image.normalizedDifference(['SR_B6', 'SR_B5']).rename(['ndbi']);
  var mndwi = image.normalizedDifference(['SR_B5', 'SR_B6']).rename(['mndwi']); 
  var bsi = image.expression(
      '(( X + Y ) - (A + B)) /(( X + Y ) + (A + B)) ', {
        'X': image.select('SR_B6'), //swir1
        'Y': image.select('SR_B4'),  //red
        'A': image.select('SR_B5'), // nir
        'B': image.select('SR_B2'), // blue
  }).rename('bsi');
  return image.addBands(ndvi).addBands(ndbi).addBands(mndwi).addBands(bsi)
}

//Establishs our roi over the 2013 time period
var roi = landsat8
.filter(ee.Filter.lt('CLOUD_COVER', 25))
.filter(ee.Filter.date('2013-01-01', '2014-01-01'))
.filter(ee.Filter.bounds(focus))

var roi2013 = roi.median().clip(focus)
var roi2013 = addIndices(roi2013)

Map.addLayer(roi2013, l8Vis, '2013')

//TRAINING DATA
var training = bare.merge(water).merge(vegetation)

//CLASSIFICATION PROCESS FOR 2013
// Overlay the point on the image to get training data.
var training = roi2013.sampleRegions({
  collection: training, 
  properties: ['landcover'], 
  scale: 10
});

// Classifiers Both Random Forest and SVM.
// Train a classifier.
var classifierRF = ee.Classifier.smileRandomForest(50).train({
  features: training,  
  classProperty: 'landcover', 
  inputProperties: roi2013.bandNames()
});

var classifierSVM = ee.Classifier.libsvm().train({
  features: training,  
  classProperty: 'landcover', 
  inputProperties: roi2013.bandNames()
})

//Classification for 2013 year
var classifiedRF2013 = roi2013.classify(classifierRF);
Map.addLayer(classifiedRF2013,{min: 0, max: 2, palette: ['brown', 'blue', 'green']}, '2013_classified_RF');

var classifedSVM2013 = roi2013.classify(classifierSVM)
Map.addLayer(classifiedRF2013,{min: 0, max: 2, palette: ['brown', 'blue', 'green']}, '2013_classified_SVM');
///


// Calculate Area by Class
var areaImage = ee.Image.pixelArea().divide(1e6).addBands(classifiedRF2013);

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
print("Vegetation Area in 2013: ", classAreas.get(1))

//ROI for the 2020 year
var roi2020 = landsat8
  .filter(ee.Filter.lt('CLOUD_COVER', 25))
  .filter(ee.Filter.date('2020-01-01', '2021-01-01'))
  .filter(ee.Filter.bounds(focus))
  .median()
  .clip(focus)
var roi2020 = addIndices(roi2020)
Map.addLayer(roi2020, l8Vis, '2020');

//CLASSIFICATION 2020
// Classify the image.
var classifiedRF2020 = roi2020.classify(classifierRF);
Map.addLayer(classifiedRF2020, {min: 0, max: 2, palette: ['brown', 'blue', 'green']}, '2020_classified_RF');

var classifedSVM2020 = roi2020.classify(classifierSVM)
Map.addLayer(classifiedRF2020,{min: 0, max: 2, palette: ['brown', 'blue', 'green']}, '2020_classified_SVM');

var areaImage = ee.Image.pixelArea().divide(1e6).addBands(classifiedRF2020);

// Calculate Area by Class
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
print("Vegetation Area in 2020: ", classAreas.get(1))

// Reclassify from 0-3 to 1-4
var beforeClasses = classifiedRF2013.remap([0, 1, 2], [1, 2, 3])
var afterClasses = classifiedRF2020.remap([0, 1, 2], [1, 2, 3])

// Show all changed areas
var changed = afterClasses.subtract(beforeClasses).eq(-2)

Map.addLayer(changed, {min:0, max:1, palette: ['white', 'red']}, 'Change')

var areaImage = ee.Image.pixelArea().divide(1e6).addBands(changed);

// Calculate Area by Class
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
print("Area of Vegetation Loss", classAreas.get(1))

// We multiply the before image with 100 and add the after image
// The resulting pixel values will be unique and will represent each unique transition
// i.e. 102 is urban to bare, 103 urban to water etc.
var merged = beforeClasses.multiply(100).add(afterClasses).rename('transitions')

// Use a frequencyHistogram to get a pixel count per class
var transitionMatrix = merged.reduceRegion({
  reducer: ee.Reducer.frequencyHistogram(), 
  geometry: focus,
  maxPixels: 1e10,
  scale:10,
  tileScale: 16
})
// This prints number of pixels for each class transition
print(transitionMatrix.get('transitions'))  

//SHOWS MINE POINTS ON THE MAP
var visParams = {'color': 'blue'}
var coltanMines = mines
    .filterMetadata('mineral1', 'equals', 'Coltan')
    .merge(mines.filterMetadata('mineral2', 'equals', 'Coltan'))
    .merge(mines.filterMetadata('mineral3', 'equals', 'Coltan'))

Map.addLayer(coltanMines, visParams, 'Coltan')


