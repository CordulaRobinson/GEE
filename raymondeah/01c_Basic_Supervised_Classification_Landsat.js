/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var water = /* color: #004199 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([-73.92248733723311, 42.840002104836216]),
            {
              "landcover": 2,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.87833689884148, 42.8434873062219]),
            {
              "landcover": 2,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.67799949658993, 42.77882181682225]),
            {
              "landcover": 2,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.69141795572185, 42.733842839818706]),
            {
              "landcover": 2,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.70344724823367, 42.705408767865364]),
            {
              "landcover": 2,
              "system:index": "4"
            })]),
    vegetation = /* color: #069900 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([-73.9685131912996, 42.84656309090184]),
            {
              "landcover": 3,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.89660127849335, 42.83820079504835]),
            {
              "landcover": 3,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.85999923848745, 42.793061133893715]),
            {
              "landcover": 3,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.7387137387191, 42.71262483889057]),
            {
              "landcover": 3,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.74030569964846, 42.702023882108854]),
            {
              "landcover": 3,
              "system:index": "4"
            })]),
    urban = /* color: #8f8f8f */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([-73.75997890872162, 42.65129974253547]),
            {
              "landcover": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.77006401461762, 42.66373465171052]),
            {
              "landcover": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.69163085333942, 42.72844449211221]),
            {
              "landcover": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.69205845675366, 42.72230251134041]),
            {
              "landcover": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.94512985688002, 42.81566229638801]),
            {
              "landcover": 0,
              "system:index": "4"
            })]),
    bare = /* color: #845858 */ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([-73.94128219774784, 42.833593908781]),
            {
              "landcover": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.98533497071573, 42.831812869971095]),
            {
              "landcover": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.9883390448124, 42.844085760399615]),
            {
              "landcover": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.7409375901836, 42.74575972040888]),
            {
              "landcover": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([-73.72706154186245, 42.649938833871545]),
            {
              "landcover": 1,
              "system:index": "4"
            })]);
/***** End of imports. If edited, may not auto-convert in the playground. *****/
var ls = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2");
var urbanAreas = ee.FeatureCollection("users/ujavalgandhi/e2e/ne_10m_urban_areas");

// Perform supervised classification for your city
// Find the feature id by adding the layer to the map and using Inspector.
var city = urbanAreas.filter(ee.Filter.eq('system:index', '00000000000000001205'));
var geometry = city.geometry();
Map.centerObject(geometry);

var filtered = ls
.filter(ee.Filter.lt('CLOUD_COVER', 30))
  .filter(ee.Filter.date('2019-01-01', '2019-12-31'))
  .filter(ee.Filter.bounds(geometry))
  .select('SR_B.*');

var composite = filtered.median().clip(geometry);

// Display the input composite.

var rgbVis = {min: 1, max: 65455, bands: ['SR_B4', 'SR_B3', 'SR_B2']};
Map.addLayer(composite, rgbVis, 'image');

// Exercise
// Add training points for 4 classes
// Assign the 'landcover' property as follows

// urban: 0
// bare: 1
// water: 2
// vegetation: 3

// After adding points, uncomments lines below

var gcps = urban.merge(bare).merge(water).merge(vegetation);

// Overlay the point on the image to get training data.
var training = composite.sampleRegions({
   collection: gcps, 
   properties: ['landcover'], 
   scale: 10,
   tileScale: 16
});

print(training);

// Train a classifier.
var classifier = ee.Classifier.smileRandomForest(50).train({   
  features: training,  
  classProperty: 'landcover', 
  inputProperties: composite.bandNames()
});

// Classify the image.
var classified = composite.classify(classifier);
Map.addLayer(classified, {min: 0, max: 3, palette: ['gray', 'brown', 'blue', 'green']}, '2019'); 


