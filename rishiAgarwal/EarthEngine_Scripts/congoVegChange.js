//Imports
var rgbVis = {"bands":["B4","B3","B2"],"min":0,"max":3000},
    countries = ee.FeatureCollection("FAO/GAUL/2015/level0"),
    s2 = ee.ImageCollection("COPERNICUS/S2_SR"),
    alos = ee.Image("JAXA/ALOS/AW3D30/V2_2"),
    brazzaville = 
    /* color: #bf04c2 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[15.19271324933364, -4.219361948772525],
          [15.19271324933364, -4.313856413961041],
          [15.301889885075827, -4.313856413961041],
          [15.301889885075827, -4.219361948772525]]], null, false),
    urban = 
    /* color: #ff0000 */
    /* shown: false */
    ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([15.25335567090841, -4.249052690490503]),
            {
              "landcover": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([15.265629459360559, -4.255472271891917]),
            {
              "landcover": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([15.282151866892297, -4.254659127872957]),
            {
              "landcover": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([15.289747882822473, -4.247084008150158]),
            {
              "landcover": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([15.281808544138391, -4.257569323556526]),
            {
              "landcover": 0,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([15.240533220033287, -4.27394444057341]),
            {
              "landcover": 0,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([15.233097078884485, -4.268854454910741]),
            {
              "landcover": 0,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([15.226960184658411, -4.273562031939577]),
            {
              "landcover": 0,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([15.284912687307818, -4.262835576062512]),
            {
              "landcover": 0,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([15.237896794946643, -4.246672683734577]),
            {
              "landcover": 0,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([15.231802816064807, -4.239910646023037]),
            {
              "landcover": 0,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([15.249140615137073, -4.233833321140168]),
            {
              "landcover": 0,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([15.243276456673653, -4.2574486629976285]),
            {
              "landcover": 0,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([15.25160203345588, -4.250515530559424]),
            {
              "landcover": 0,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([15.257908852084382, -4.250067024810591]),
            {
              "landcover": 0,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([15.27049062580294, -4.2528459711512205]),
            {
              "landcover": 0,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([15.233553632040365, -4.246839485141161]),
            {
              "landcover": 0,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([15.25339323622219, -4.237011508203967]),
            {
              "landcover": 0,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([15.263631369246076, -4.228831059108713]),
            {
              "landcover": 0,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([15.2522162115537, -4.261893667176565]),
            {
              "landcover": 0,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([15.252403966184742, -4.261433602794862]),
            {
              "landcover": 0,
              "system:index": "20"
            }),
        ee.Feature(
            ee.Geometry.Point([15.25144909977544, -4.2605348715807345]),
            {
              "landcover": 0,
              "system:index": "21"
            }),
        ee.Feature(
            ee.Geometry.Point([15.248675695654041, -4.260433229293995]),
            {
              "landcover": 0,
              "system:index": "22"
            }),
        ee.Feature(
            ee.Geometry.Point([15.243151119446935, -4.259842847717782]),
            {
              "landcover": 0,
              "system:index": "23"
            }),
        ee.Feature(
            ee.Geometry.Point([15.252849987244787, -4.252010995669346]),
            {
              "landcover": 0,
              "system:index": "24"
            }),
        ee.Feature(
            ee.Geometry.Point([15.254137447571935, -4.2532949112996645]),
            {
              "landcover": 0,
              "system:index": "25"
            }),
        ee.Feature(
            ee.Geometry.Point([15.25779180791007, -4.245120611925904]),
            {
              "landcover": 0,
              "system:index": "26"
            }),
        ee.Feature(
            ee.Geometry.Point([15.259165098925696, -4.246447336561576]),
            {
              "landcover": 0,
              "system:index": "27"
            }),
        ee.Feature(
            ee.Geometry.Point([15.26379995610343, -4.240327265212853]),
            {
              "landcover": 0,
              "system:index": "28"
            }),
        ee.Feature(
            ee.Geometry.Point([15.262426665087805, -4.247046501778417]),
            {
              "landcover": 0,
              "system:index": "29"
            })]),
    bare = 
    /* color: #f1ff56 */
    /* shown: false */
    ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([15.243132466943713, -4.2370859798342355]),
            {
              "landcover": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([15.243432874353381, -4.238648107108132]),
            {
              "landcover": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([15.223842019708606, -4.234475294333901]),
            {
              "landcover": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([15.235858316095324, -4.229596284710326]),
            {
              "landcover": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([15.239892358453723, -4.228098336992722]),
            {
              "landcover": 1,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([15.265469903619739, -4.238840697923346]),
            {
              "landcover": 1,
              "system:index": "5"
            })]),
    water = 
    /* color: #0000ff */
    /* shown: false */
    ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([15.224130049072686, -4.300309273133212]),
            {
              "landcover": 2,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([15.21951664956707, -4.29602980852907]),
            {
              "landcover": 2,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([15.215074911438409, -4.297527623873044]),
            {
              "landcover": 2,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([15.222849998875088, -4.292381160718441]),
            {
              "landcover": 2,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([15.21954551736874, -4.290155818995288]),
            {
              "landcover": 2,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([15.215640221043056, -4.291782030892548]),
            {
              "landcover": 2,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([15.236702898298379, -4.310366363552459]),
            {
              "landcover": 2,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([15.2436766417371, -4.310986875724962]),
            {
              "landcover": 2,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([15.266850927625772, -4.300031551920122]),
            {
              "landcover": 2,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([15.257924536024209, -4.308761588343863]),
            {
              "landcover": 2,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([15.272508176552648, -4.292131304055968]),
            {
              "landcover": 2,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([15.20727685331046, -4.295640484740183]),
            {
              "landcover": 2,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([15.204616101967687, -4.298978470897244]),
            {
              "landcover": 2,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([15.20727685331046, -4.288279745712967]),
            {
              "landcover": 2,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([15.210292328047531, -4.278089575548152]),
            {
              "landcover": 2,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([15.210206497359055, -4.2701295208721906]),
            {
              "landcover": 2,
              "system:index": "15"
            })]),
    vegetation = 
    /* color: #0cfd24 */
    /* shown: false */
    ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([15.240774025727871, -4.278628285323307]),
            {
              "landcover": 3,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([15.238370766450528, -4.278007746834144]),
            {
              "landcover": 3,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([15.2405809066788, -4.277151830851753]),
            {
              "landcover": 3,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([15.248219837953213, -4.279034844750474]),
            {
              "landcover": 3,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([15.260477340067403, -4.273295040142228]),
            {
              "landcover": 3,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([15.257054990152822, -4.270810079856971]),
            {
              "landcover": 3,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([15.256754582743154, -4.2726075171864775]),
            {
              "landcover": 3,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([15.250886391924725, -4.270493992029373]),
            {
              "landcover": 3,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([15.221382092760907, -4.243724506284634]),
            {
              "landcover": 3,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([15.21912742150529, -4.25549968948669]),
            {
              "landcover": 3,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([15.203469759373318, -4.253805710389074]),
            {
              "landcover": 3,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([15.26678688287567, -4.223109818829358]),
            {
              "landcover": 3,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([15.265928575990904, -4.221697456388399]),
            {
              "landcover": 3,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([15.299020852714621, -4.225709299044857]),
            {
              "landcover": 3,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([15.281940545707785, -4.226522473528492]),
            {
              "landcover": 3,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([15.282541360527121, -4.22810602139093]),
            {
              "landcover": 3,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([15.253104110180521, -4.2435681849010525]),
            {
              "landcover": 3,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([15.259093395467884, -4.260839798360406]),
            {
              "landcover": 3,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([15.25033773897721, -4.262482767142557]),
            {
              "landcover": 3,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([15.248615760789649, -4.262391824274908]),
            {
              "landcover": 3,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([15.249688644395606, -4.261872914765387]),
            {
              "landcover": 3,
              "system:index": "20"
            })]),
    southCongo = 
    /* color: #ff00ff */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[11.582226004118436, -2.8591209442150407],
          [13.449901785368436, -4.875896693734427],
          [14.834179129118436, -4.821161621108238],
          [15.504345144743436, -4.05443008958573],
          [15.899852957243436, -3.944834397450982],
          [16.185497488493436, -2.5957479883627426],
          [11.944774832243436, -2.398181941613441]]]);

//Scripts

Map.setCenter(15.2536, -4.2651, 13);

//Function for Cloud Masking
function maskS2clouds(image) {
  var qa = image.select('QA60')
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0).and(
             qa.bitwiseAnd(cirrusBitMask).eq(0))
  return image.updateMask(mask)//.divide(10000)
      .select("B.*")
      .copyProperties(image, ["system:time_start"])
} 

var congo = countries.filter(ee.Filter.eq('ADM0_NAM E', 'Congo'))
var congoGeometry = congo.geometry()

var filtered = s2
  .filter(ee.Filter.date('2000-01-01', '2000-01-31'))
  .filter(ee.Filter.bounds(southCongo))
  .select('B.*')

var image = filtered.median(); 
var image = ee.Image(maskS2clouds(image))
var before = image.clip(southCongo)

Map.addLayer(before, rgbVis, 'before')

//Adds the indicies to improve classification
var addIndicies = function(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename(['ndvi']);
  var ndbi = image.normalizedDifference(['B11', 'B8']).rename(['ndbi']);
  var mndwi = image.normalizedDifference(['B3', 'B11']).rename(['mndwi']);
  
  return image.addBands(ndvi).addBands(ndbi).addBands(mndwi)
  
}

var before = addIndicies(before)

//Calculate slope and elevation
var elev = alos.select('AVE_DSM').rename('elev')
var slope = ee.Terrain.slope(alos.select('AVE_DSM')).rename('slope')

var before = before.addBands(elev).addBands(slope)

//Function to normalize image
function normalize(image){
  var bandNames = image.bandNames();
  // Compute min and max of the image
  var minDict = image.reduceRegion({
    reducer: ee.Reducer.min(),
    geometry: southCongo,
    scale: 20,
    maxPixels: 1e9,
    bestEffort: true,
    tileScale: 16
  });
  var maxDict = image.reduceRegion({
    reducer: ee.Reducer.max(),
    geometry: southCongo,
    scale: 20,
    maxPixels: 1e9,
    bestEffort: true,
    tileScale: 16
  });
  var mins = ee.Image.constant(minDict.values(bandNames));
  var maxs = ee.Image.constant(maxDict.values(bandNames));

  var normalized = image.subtract(mins).divide(maxs.subtract(mins))
  return normalized
}

var before = normalize(before)

var gcps = urban.merge(bare).merge(water).merge(vegetation).randomColumn()

var trainingGcp = gcps.filter(ee.Filter.lt('random', 0.6))
var validationGcp = gcps.filter(ee.Filter.gte('random', 0.6))

var training = before.sampleRegions({
  collection: trainingGcp,
  properties: ['landcover'],
  scale: 10,
  tileScale: 16
})

var classifier = ee.Classifier.smileRandomForest(50)
.train({
  features: training,
  classProperty: 'landcover',
  inputProperties: before.bandNames()
})

var beforeClassified = before.classify(classifier)
Map.addLayer(beforeClassified, {min: 0, max: 3, palette: ['gray', 'brown', 'blue', 'green']}, 'Bclassifer')

var after = s2
  .filter(ee.Filter.date('2020-01-01', '2020-01-31'))
  .filter(ee.Filter.bounds(southCongo))
  .select('B.*')
  .median()
  .clip(southCongo)

Map.addLayer(after, rgbVis, 'after')

var afterClassified = after.classify(classifier)
Map.addLayer(afterClassified, {min: 0, max: 3, palette: ['gray', 'brown', 'blue', 'green']}, 'Aclassifer')





/*
// Use classification map to assess accuracy using the validation fraction
// of the overall training set created above.
var test = classified.sampleRegions({
  collection: validationGcp,
  properties: ['landcover'],
  tileScale: 16,
  scale: 10,
});

var testConfusionMatrix = test.errorMatrix('landcover', 'classification')
// Printing of confusion matrix may time out. Alternatively, you can export it as CSV
print('Confusion Matrix', testConfusionMatrix);
print('Test Accuracy', testConfusionMatrix.accuracy());

*/