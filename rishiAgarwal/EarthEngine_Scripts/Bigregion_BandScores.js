//Imports 
var visualization = {"min":0,"max":0.3,"bands":["B4","B3","B2"]},
    mines = ee.FeatureCollection("users/rishiAgarwal/Congo_Active_Mines"),
    s2 = ee.ImageCollection("COPERNICUS/S2_SR"),
    rishiroi_big = /* color: #d63000 */ee.Geometry.MultiPoint(),
    scores_27_n7 = ee.FeatureCollection("users/rishiAgarwal/1stBigRegion"),
    scores_28_n7 = ee.FeatureCollection("users/rishiAgarwal/2ndBigRegion"),
    scores_29_n7 = ee.FeatureCollection("users/rishiAgarwal/3rdBigRegion"),
    scores_26_n7 = ee.FeatureCollection("users/rishiAgarwal/4thBigRegion");
    
//Script


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
function makeRec(min_lon, max_lon, max_lat, min_lat) {
  return ee.Geometry.Rectangle(min_lon, min_lat, max_lon, max_lat)
}
function visArea(area, message) {
    var filtered = s2
    .filter(ee.Filter.bounds(area))
    .filter(ee.Filter.date('2021-01-01', '2021-12-31'))
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
    .map(maskS2clouds)
    .select('B.*');
    
  var composite = filtered.median().clip(area);
  Map.addLayer(composite, visualization, message);
}
function visTable(table, message) {
  var table_pass = table
  .filter(ee.Filter.and(
    ee.Filter.gte('elevation score', 5),
    ee.Filter.gte('band score', 5)))
  Map.addLayer(table_pass, {'color': 'red'}, message)
}
//26 -7
visArea(makeRec(26, 27, -7, -8), "26_-7_Composite")
visTable(scores_26_n7, "26_-7_Passing")
//27 -7
visArea(makeRec(27, 28, -7, -8), "27_-7_Composite")
visTable(scores_27_n7, "27_-7_Passing")
//28 -7
visArea(makeRec(28, 29, -7, -8), "28_-7_Composite")
visTable(scores_28_n7, "28_-7_Passing")
//29 -7
visArea(makeRec(29, 30, -7, -8), "29_-7_Composite")
visTable(scores_29_n7, "29_-7_Passing")

visArea(makeRec(27, 28, -8, -9), "27_-8_Composite")

visArea(makeRec(26, 27, -8, -9), "26_-8_Composite")
//Showing coltan mines on the map

var visParams = {'color': 'blue'}

var coltanMines = mines
    // .filterMetadata('mineral1', 'equals', 'Coltan')
    // .merge(mines.filterMetadata('mineral2', 'equals', 'Coltan'))
    // .merge(mines.filterMetadata('mineral3', 'equals', 'Coltan'))

Map.addLayer(coltanMines, visParams, 'Coltan')

/*

Dates for miliseconds from 1970

*/