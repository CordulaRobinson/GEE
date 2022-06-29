//Imports
var ls5Vis = {"bands":["SR_B3","SR_B2","SR_B1"],"min":0,"max":0.3},
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
    ls5 = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2"),
    bare = 
    /* color: #d60000 */
    /* shown: false */
    ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([27.40405335247563, -7.5567330312770995]),
            {
              "landcover": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([27.40250840008305, -7.5385244020777895]),
            {
              "landcover": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([27.40022109974336, -7.519829432230856]),
            {
              "landcover": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([27.373375675376277, -7.559572480025075]),
            {
              "landcover": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([27.353977939780574, -7.556764675772063]),
            {
              "landcover": 0,
              "system:index": "4"
            })]),
    vegetation = 
    /* color: #98ff00 */
    /* shown: false */
    ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([27.361652992368207, -7.541417413074763]),
            {
              "landcover": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([27.383453987241253, -7.559455751020543]),
            {
              "landcover": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([27.410576484799847, -7.53971564424165]),
            {
              "landcover": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([27.39306702435063, -7.5351208349795895]),
            {
              "landcover": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([27.423622749448285, -7.567623807204693]),
            {
              "landcover": 1,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([27.367110035117488, -7.554212110610801]),
            {
              "landcover": 1,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([27.421870014365535, -7.539236758064811]),
            {
              "landcover": 1,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([27.371304137907394, -7.530180583825927]),
            {
              "landcover": 1,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([27.392933471403488, -7.545496599788115]),
            {
              "landcover": 1,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([27.40632305880583, -7.549836039097593]),
            {
              "landcover": 1,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([27.418682677946457, -7.552048285512702]),
            {
              "landcover": 1,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([27.427952392301925, -7.534605266299376]),
            {
              "landcover": 1,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([27.3866678311447, -7.5744253716830325]),
            {
              "landcover": 1,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([27.362549407682785, -7.5690651867953935]),
            {
              "landcover": 1,
              "system:index": "13"
            })]),
    s2 = ee.ImageCollection("COPERNICUS/S2_SR"),
    s2Vis = {"min":0,"max":0.3,"bands":["B4","B3","B2"]},
    bareS2 = /* color: #d6d402 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([27.359065163082786, -7.548239947856766]),
            {
              "landcoverS2": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([27.389620888180442, -7.5473890776953105]),
            {
              "landcoverS2": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([27.399062263912864, -7.541432939698623]),
            {
              "landcoverS2": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([27.38241111034841, -7.537008326976507]),
            {
              "landcoverS2": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([27.40412627453298, -7.555897703941403]),
            {
              "landcoverS2": 0,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([27.38764678234548, -7.576998373403404]),
            {
              "landcoverS2": 0,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([27.40163718456716, -7.522566822060052]),
            {
              "landcoverS2": 0,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([27.413224327511497, -7.53277773896205]),
            {
              "landcoverS2": 0,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([27.37545882458181, -7.535330430602268]),
            {
              "landcoverS2": 0,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([27.40936194653005, -7.545881396392517]),
            {
              "landcoverS2": 0,
              "system:index": "9"
            })]),
    vegetationS2 = /* color: #10ffd9 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([27.374257194943137, -7.550050658721788]),
            {
              "landcoverS2": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([27.356921410599337, -7.534191242393263]),
            {
              "landcoverS2": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([27.360955452957736, -7.532404355125728]),
            {
              "landcoverS2": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([27.426776035526974, -7.555727469419223]),
            {
              "landcoverS2": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([27.430981739262325, -7.560322059726264]),
            {
              "landcoverS2": 1,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([27.371659196908073, -7.573904044747139]),
            {
              "landcoverS2": 1,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([27.369084276253776, -7.568884184968875]),
            {
              "landcoverS2": 1,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([27.39672175794323, -7.560861249268245]),
            {
              "landcoverS2": 1,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([27.386422075326042, -7.5289745594589235]),
            {
              "landcoverS2": 1,
              "system:index": "8"
            })]);

//Scripts
 
function applyScaleFactors(image) {
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBand = image.select('ST_B6').multiply(0.00341802).add(149.0);
  return image.addBands(opticalBands, null, true)
              .addBands(thermalBand, null, true);
}

var landsat5 = ls5.map(applyScaleFactors)

var roi2000 = landsat5.filter(ee.Filter.date('2000-01-01', '2001-01-01'))
.filter(ee.Filter.lt('CLOUD_COVER', 25))
.filter(ee.Filter.bounds(focus))
.select('SR_B.*')
.median()
.clip(focus)

print(roi2000)

Map.addLayer(roi2000, ls5Vis, '2000')

var train = bare.merge(vegetation)

var training = roi2000.sampleRegions({
  collection: train,
  properties: ['landcover'],
  scale: 10
})

var classifierls5 = ee.Classifier.smileRandomForest(50).train({
  features: training,
  classProperty: 'landcover',
  inputProperties: roi2000.bandNames()
})

var classifiedls5 = roi2000.classify(classifierls5)

Map.addLayer(classifiedls5, {min: 0, max: 1, palette: ['brown', 'green']}, 'ls5classified')

// Calculate Area by Class
var areaImage = ee.Image.pixelArea().divide(1e6).addBands(classifiedls5);

// Using a Grouped Reducer
var areas = areaImage.reduceRegion({
      reducer: ee.Reducer.sum().group({
      groupField: 1,
      groupName: 'classification',
    }),
    geometry: focus,
    scale: 30,
    tileScale: 4,
    maxPixels: 1e10
    }); 
var classAreas = ee.List(areas.get('groups'))
var vegetation2000 = ee.Number(ee.Dictionary(classAreas.get(1)).get('sum'))
print("Vegetation Area in 2000: ", vegetation2000)



///// 2020 ///////////////////////////////////////////////////////////

function maskS2clouds(image) {
  var qa = image.select('QA60');

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));

  return image.updateMask(mask).divide(10000);
}


var roi2020 = s2
.filterDate('2020-01-01', '2021-01-01')
.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
.map(maskS2clouds)
.filter(ee.Filter.bounds(focus))
.median()
.clip(focus)

print(roi2020)

Map.addLayer(roi2020, s2Vis, "2020")

var trainS2 = bareS2.merge(vegetationS2)

var trainingS2 = roi2020.sampleRegions({
  collection: trainS2,
  properties: ['landcoverS2'],
  scale: 10 
})

var classifierS2 = ee.Classifier.smileRandomForest(50).train({
  features: trainingS2,
  classProperty: 'landcoverS2',
  inputProperties: roi2020.bandNames()
})

var classifiedS2 = roi2020.classify(classifierS2)

Map.addLayer(classifiedS2, {min: 0, max: 1, palette: ['brown', 'green']}, 's2Classified')

// Calculate Area by Class
var areaImage = ee.Image.pixelArea().divide(1e6).addBands(classifiedS2);

// Using a Grouped Reducer
var areas = areaImage.reduceRegion({
      reducer: ee.Reducer.sum().group({
      groupField: 1,
      groupName: 'classification',
    }),
    geometry: focus,
    scale: 30,
    tileScale: 4,
    maxPixels: 1e10
    }); 
var classAreas = ee.List(areas.get('groups'))
var vegetation2020 = ee.Number(ee.Dictionary(classAreas.get(1)).get('sum'))
print("Vegetation Area in 2020: ", vegetation2020)

var percentageLoss = (vegetation2000.subtract(vegetation2020)).divide(vegetation2000)
print("Percentage of Vegetation Lost: ", percentageLoss)

