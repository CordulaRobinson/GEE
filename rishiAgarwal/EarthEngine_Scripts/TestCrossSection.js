//Imports
var mines = ee.FeatureCollection("users/rishiAgarwal/Congo_Active_Mines"),
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
    s2 = ee.ImageCollection("COPERNICUS/S2_SR"),
    visualization = {"min":0,"max":0.3,"bands":["B4","B3","B2"]},
    rayroi1 = 
    /* color: #d63000 */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[29.554129272985683, 3.1591674847348235],
          [29.554129272985683, 3.092319151883147],
          [29.625197083044277, 3.092319151883147],
          [29.625197083044277, 3.1591674847348235]]]),
    rayroi2 = 
    /* color: #00ffff */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[30.246670960050185, 1.7911944738716732],
          [30.246670960050185, 1.7103797163160706],
          [30.356362579923232, 1.7103797163160706],
          [30.356362579923232, 1.7911944738716732]]]),
    rayline = 
    /* color: #98ff00 */
    /* shown: false */
    ee.Geometry.LineString(
        [[29.584357669394308, 3.099094656316075],
         [29.57959406618386, 3.1264342491817576]]),
    emilyline = 
    /* color: #37d66c */
    /* shown: false */
    ee.Geometry.LineString(
        [[25.7876962904855, -10.783991079147425],
         [25.83610479878628, -10.78820679367607]]),
    emily_area1 = 
    /* color: #d63000 */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[25.75, -10.75],
          [25.75, -10.8],
          [25.9, -10.8],
          [25.9, -10.75]]]),
    emily_area2 = 
    /* color: #98ff00 */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[25.8, -10.6],
          [25.8, -10.7],
          [25.95, -10.7],
          [25.95, -10.6]]]),
    emily_area3 = 
    /* color: #0b4a8b */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[26, -10.5],
          [26, -10.75],
          [26.25, -10.75],
          [26.25, -10.5]]]),
    emily_area4 = 
    /* color: #ffc82d */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[25.95, -10.6],
          [25.95, -10.7],
          [26.05, -10.7],
          [26.05, -10.6]]]),
    rishiline = 
    /* color: #ff0000 */
    /* shown: false */
    ee.Geometry.LineString(
        [[27.395013010807165, -7.542752969325824],
         [27.40788761407865, -7.5362862321228965]]),
    mojave = 
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-115.84659684153141, 35.379488360140314],
          [-115.84659684153141, 34.88081647081126],
          [-115.07206070871891, 34.88081647081126],
          [-115.07206070871891, 35.379488360140314]]], null, false),
    mojaveline = 
    /* color: #d619c3 */
    /* shown: false */
    ee.Geometry.LineString(
        [[-115.59340978835614, 34.89003237359311],
         [-115.36956335280927, 35.22278225045704]]),
    canyon = 
    /* color: #98ff00 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-112.33870397910384, 36.22484938749377],
          [-112.33870397910384, 36.03184794616349],
          [-112.05031286582259, 36.03184794616349],
          [-112.05031286582259, 36.22484938749377]]], null, false),
    canyonline = 
    /* color: #0b4a8b */
    /* shown: false */
    ee.Geometry.LineString(
        [[-112.23367900878893, 36.0481853223429],
         [-112.12510369226801, 36.193781847393]]),
    mojave_dune = 
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-115.83972803952076, 35.09736482769548],
          [-115.83972803952076, 34.88360273192419],
          [-115.55408350827076, 34.88360273192419],
          [-115.55408350827076, 35.09736482769548]]], null, false),
    mojave_mountain = 
    /* color: #98ff00 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-115.43048731686451, 35.33745902259608],
          [-115.43048731686451, 35.12657303664835],
          [-115.07343165280201, 35.12657303664835],
          [-115.07343165280201, 35.33745902259608]]], null, false),
    emily_area = ee.FeatureCollection("users/rishiAgarwal/emily_area"),
    line = /* color: #3dd62f */ee.Geometry.LineString(
        [[26.60679167577026, -10.865850843828397],
         [26.620543563068807, -10.85961398566366]]);

//Scripts
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

var rec = ee.Geometry.Rectangle(26.25, -11.1, 27.25, -10.30)

var area = rec
var line =  line

Map.centerObject(area, 10);

var filtered = s2
  .filter(ee.Filter.bounds(area))
  .filter(ee.Filter.date('2020-01-01', '2020-12-31'))
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
  .map(maskS2clouds)
  .select('B.*');
  
var composite = filtered.median().clip(area);

Map.addLayer(composite, visualization, '2020 Median Composite 1');


var addIndices = function(image) {
  var nirg = image.normalizedDifference(['B8', 'B3']).rename(['nirg'])
  var swirb = image.normalizedDifference(['B11', 'B2']).rename(['swirb'])
  var b5_b6 = image.select('B5').divide(image.select('B6')).rename(['5over6'])
  var b5ndb6 = image.normalizedDifference(['B5','B6']).rename('NDB5B6')
  return image.addBands(nirg).addBands(swirb).addBands(b5_b6).addBands(b5ndb6)
}

var withIndicies = addIndices(composite)

var crossSection = crossSection; // single line
var numPoints = 1000; // divide the line into this many sections

// Divide the cross section among the specified number of points
var point1 = ee.List(line.coordinates().get(0));
var point2 = ee.List(line.coordinates().get(1));
var xMapList = ee.List.sequence(point1.get(0), point2.get(0), null, numPoints);
var yMapList = ee.List.sequence(point1.get(1), point2.get(1), null, numPoints);

// Construct a feature collection with points equally spaced
var points = ee.FeatureCollection(xMapList.map(function(Xcoord){
  var Ycoord = yMapList.get(xMapList.indexOf(Xcoord));
  return ee.Feature(ee.Geometry.Point([Xcoord, Ycoord]));
}));

Map.addLayer(points, {min:1, max:1, palette:['red']}, 'Cross Section');

// Select band values at every point

var ratios = withIndicies.select(withIndicies.bandNames()
.filter(ee.Filter.or(ee.Filter.eq('item', 'NDB5B6'))))

print(composite.bandNames())
print(withIndicies.bandNames())
print(ratios.bandNames())

var image = composite//ratios.rename(['NDB5B6'])
var bands = image.reduceRegions(points, ee.Reducer.first(), 10);

Map.addLayer(emily_area, {'color': 'red'}, "emily area passing")



// Display a chart of band values along the cross section
var chartStyle = {
  colors: ['green', 'blue', 'orange', 'red', 'yellow', 'brown', 'black', 'grey', 'pink', 'cyan', 'violet']
}

print(ui.Chart.feature.byFeature(bands).setOptions(chartStyle));

//Map.addLayer(composite.select(["B11"]), {min: 0, max: 0.7, palette: ['white', 'blue']}, "SWIR1")
Map.addLayer(composite.select(["B11"]), {min: 0.3, max: 0.7, palette: ['white', 'blue']}, "SWIR1")

