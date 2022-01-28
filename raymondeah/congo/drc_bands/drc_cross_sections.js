/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var s2 = ee.ImageCollection("COPERNICUS/S2_SR"),
    ls7 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2"),
    ls8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2"),
    hyperion = ee.ImageCollection("EO1/HYPERION"),
    admin = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level1"),
    miningPermits = ee.FeatureCollection("users/raymondeah/Democratic_Republic_of_the_Congo_mining_permits"),
    activeMines = ee.FeatureCollection("users/raymondeah/cod_mines_curated_all_opendata_p_ipis"),
    points = /* color: #00ffff */ee.Geometry.MultiPoint(
        [[29.58905590753292, 3.1265733505900184],
         [29.783181537630476, 3.1489109666499777],
         [30.305007154636336, 1.7496889115779437]]),
    roi1 = 
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[29.554129272985683, 3.1591674847348235],
          [29.554129272985683, 3.092319151883147],
          [29.625197083044277, 3.092319151883147],
          [29.625197083044277, 3.1591674847348235]]], null, false),
    roi2 = 
    /* color: #0b4a8b */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[29.76168993261876, 3.1680250077194825],
          [29.76168993261876, 3.1272312365091772],
          [29.803832800660754, 3.1272312365091772],
          [29.803832800660754, 3.1680250077194825]]], null, false),
    roi3 = 
    /* color: #ffc82d */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[30.246670960050185, 1.7911944738716732],
          [30.246670960050185, 1.7103797163160706],
          [30.356362579923232, 1.7103797163160706],
          [30.356362579923232, 1.7911944738716732]]], null, false),
    crossSection = /* color: #e744ff */ee.Geometry.LineString(
        [[29.55981299542722, 3.1123355474817584],
         [29.597149344914524, 3.1077503687720403]]),
    sar = ee.ImageCollection("COPERNICUS/S1_GRD"),
    modis = ee.ImageCollection("MODIS/006/MOD13Q1");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
Map.addLayer(activeMines, {color: 'red'}, 'Active Coltan Mines');
Map.centerObject(roi1, 12);
var rgbVis = {
  min: 8097.96,
  max: 12128.04,
  bands: ['SR_B4', 'SR_B3', 'SR_B2']
};

var filtered = ls8
  .filter(ee.Filter.bounds(roi1))
  .filter(ee.Filter.date('2020-01-01', '2020-12-31'))
  .filter(ee.Filter.lt('CLOUD_COVER', 25))
  .select('SR_B.*');
  
var composite = filtered.median().clip(roi1);

Map.addLayer(composite, rgbVis, '2020 Median Composite 1');

// var filtered = ls8
//   .filter(ee.Filter.bounds(roi2))
//   .filter(ee.Filter.date('2016-01-01', '2016-12-31'))
//   .filter(ee.Filter.lt('CLOUD_COVER', 25))
//   .select('SR_B.*');
  
// var composite = filtered.median().clip(roi2);

// Map.addLayer(composite, rgbVis, '2016 Median Composite 2');

// var filtered = ls8
//   .filter(ee.Filter.bounds(roi3))
//   .filter(ee.Filter.date('2016-01-01', '2016-12-31'))
//   .filter(ee.Filter.lt('CLOUD_COVER', 25))
//   .select('SR_B.*');
  
// var composite = filtered.median().clip(roi3);

// Map.addLayer(composite, rgbVis, '2016 Median Composite 3');

// 
var crossSection = crossSection; // single line
var numPoints = 100; // divide the line into this many sections

// Divide the cross section among the specified number of points
var point1 = ee.List(crossSection.coordinates().get(0));
var point2 = ee.List(crossSection.coordinates().get(1));
var xMapList = ee.List.sequence(point1.get(0), point2.get(0), null, numPoints);
var yMapList = ee.List.sequence(point1.get(1), point2.get(1), null, numPoints);

// Construct a feature collection with points equally spaced
var points = ee.FeatureCollection(xMapList.map(function(Xcoord){
  var Ycoord = yMapList.get(xMapList.indexOf(Xcoord));
  return ee.Feature(ee.Geometry.Point([Xcoord, Ycoord]));
}));

Map.addLayer(points, {min:1, max:1, palette:['red']}, 'Cross Section');

// Select band values at every point
var image = composite.rename(['Ultra Blue, Coastal Aerosol', 'Blue', 'Green', 'Red', 'NIR', 'SWIR 1', 'SWIR 2']);
var bands = image.reduceRegions(points, ee.Reducer.first(), 10);

// Display a chart of band values along the cross section
var chartStyle = {
  colors: ['blue', 'green', 'magenta', 'red', 'orange', 'yellow', 'brown']
}
print(ui.Chart.feature.byFeature(bands).setOptions(chartStyle));


var mys = composite.normalizedDifference(['SR_B3', 'SR_B5'])
Map.addLayer(mys, {min: 0.0, max: 1.0, palette: ['white', 'red']}, "G/NIR index")
