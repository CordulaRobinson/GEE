/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var s2 = ee.ImageCollection("COPERNICUS/S2_SR"),
    admin = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level1"),
    miningPermits = ee.FeatureCollection("users/raymondeah/Democratic_Republic_of_the_Congo_mining_permits"),
    activeMines = ee.FeatureCollection("users/raymondeah/cod_mines_curated_all_opendata_p_ipis"),
    minesGrouped = 
    /* color: #ff0000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[28.84879973081211, -5.016248778035446],
          [28.84879973081211, -5.037794913801396],
          [28.874162699256935, -5.037794913801396],
          [28.874162699256935, -5.016248778035446]]], null, false),
    water = /* color: #00ffff */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([28.85818756937104, -5.023243104634987]),
            {
              "landcover": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([28.865483177891548, -5.022623221835797]),
            {
              "landcover": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([28.866041077366646, -5.029848026118908]),
            {
              "landcover": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([28.858101738682564, -5.027753268628657]),
            {
              "landcover": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([28.869774712315376, -5.031964151841523]),
            {
              "landcover": 0,
              "system:index": "4"
            })]),
    vegetation = /* color: #42ff31 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([28.85595597147065, -5.022665972392595]),
            {
              "landcover": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([28.86797226785737, -5.022152965525988]),
            {
              "landcover": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([28.871555699101265, -5.020507065770843]),
            {
              "landcover": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([28.860891236058052, -5.033631397564143]),
            {
              "landcover": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([28.859002960911567, -5.032904649953931]),
            {
              "landcover": 1,
              "system:index": "4"
            })]),
    bare = /* color: #bf04c2 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([28.852780235997017, -5.031130527378187]),
            {
              "landcover": 2,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([28.872027767887886, -5.034123020487134]),
            {
              "landcover": 2,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([28.870568646183784, -5.034849766736094]),
            {
              "landcover": 2,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([28.86217299426854, -5.018909704650508]),
            {
              "landcover": 2,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([28.852795978693162, -5.033203542518063]),
            {
              "landcover": 2,
              "system:index": "4"
            })]);
/***** End of imports. If edited, may not auto-convert in the playground. *****/

var congo = admin.filter(ee.Filter.eq('ADM0_NAME', 'Democratic Republic of the Congo'));
Map.centerObject(minesGrouped, 12)

// Function to remove cloud and snow pixels from Sentinel-2 SR image
function maskCloudAndShadowsSR(image) {
  var cloudProb = image.select('MSK_CLDPRB');
  var snowProb = image.select('MSK_SNWPRB');
  var cloud = cloudProb.lt(10);
  var scl = image.select('SCL'); 
  var shadow = scl.eq(3); // 3 = cloud shadow
  var cirrus = scl.eq(10); // 10 = cirrus
  // Cloud probability less than 10% or cloud shadow classification
  var mask = cloud.and(cirrus.neq(1)).and(shadow.neq(1));
  return image.updateMask(mask);
}

var filtered = s2
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .filter(ee.Filter.date('2019-01-01', '2019-12-31'))
  .map(maskCloudAndShadowsSR)
  .filter(ee.Filter.bounds(minesGrouped))
  .select('B.*');

var composite = filtered.median().clip(minesGrouped);

var rgbVis = {
  min: 0,
  max: 3000,
  bands: ['B4', 'B3', 'B2']
};

Map.addLayer(composite, rgbVis, 'Composite');

// Calculate  Normalized Difference Vegetation Index (NDVI)
// 'NIR' (B8) and 'RED' (B4)
var ndvi = composite.normalizedDifference(['B8', 'B4']).rename(['ndvi']);
var ndviVis = {min:0, max:1, palette: ['white', 'green']};
//Map.addLayer(ndvi, ndviVis, 'NDVI');

//Map.addLayer(miningPermits, {color: 'blue'}, 'Mines');
Map.addLayer(activeMines, {color: 'purple'}, 'Active Coltan Mines');

var minesTa = miningPermits.filter(ee.Filter.stringContains('resource', 'Ta'));

//Map.addLayer(minesTa, {color: 'red'}, 'Coltan Mines');

var training = bare.merge(water).merge(vegetation);

// Overlay the point on the image to get training data.
var training = composite.sampleRegions({
  collection: training, 
  properties: ['landcover'], 
  scale: 10
});

// Train a classifier.
var classifier = ee.Classifier.smileRandomForest(50).train({
  features: training,  
  classProperty: 'landcover', 
  inputProperties: composite.bandNames()
});

// // Classify the image.
var beforeClassified = composite.classify(classifier);
Map.addLayer(beforeClassified,
  {min: 0, max: 2, palette: ['blue', 'green', 'brown']}, 'before_classified');
  
  
// 2020 Jan
var filtered = s2
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .filter(ee.Filter.date('2021-01-01', '2021-12-31'))
  .map(maskCloudAndShadowsSR)
  .filter(ee.Filter.bounds(minesGrouped))
  .select('B.*');
  
var compositeA = filtered.median().clip(minesGrouped);

Map.addLayer(compositeA, rgbVis, 'after');

// Classify the image.
var afterClassified= compositeA.classify(classifier);
Map.addLayer(afterClassified,
  {min: 0, max: 2, palette: ['blue', 'green', 'brown']}, 'after_classified');
  
// Reclassify from 0-3 to 1-4
var beforeClasses = beforeClassified.remap([0, 1, 2], [1, 2, 3])
var afterClasses = afterClassified.remap([0, 1, 2], [1, 2, 3])

// Show all changed areas
var class3 = beforeClasses.eq(2);
var notclass3 = afterClasses.eq(2).not();
var waterChanged = class3.and(notclass3);

Map.addLayer(waterChanged, {min: 0, max: 1, palette: ['white', 'red']}, 'veggie_change');


// We multiply the before image with 100 and add the after image
// The resulting pixel values will be unique and will represent each unique transition
// i.e. 102 is urban to bare, 103 urban to water etc.
var merged = beforeClasses.multiply(100).add(afterClasses).rename('transitions')

// Use a frequencyHistogram to get a pixel count per class
var transitionMatrix = merged.reduceRegion({
  reducer: ee.Reducer.frequencyHistogram(), 
  geometry: minesGrouped,
  maxPixels: 1e10,
  scale:10,
  tileScale: 16
})

// This prints number of pixels for each class transition
print(transitionMatrix.get('transitions'))          