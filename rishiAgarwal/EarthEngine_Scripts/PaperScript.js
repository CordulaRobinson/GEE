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
    rayroi1 = 
    /* color: #d63000 */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[29.554129272985683, 3.1591674847348235],
          [29.554129272985683, 3.092319151883147],
          [29.625197083044277, 3.092319151883147],
          [29.625197083044277, 3.1591674847348235]]]),
    rayline = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.LineString(
        [[29.5632273259612, 3.142541215764356],
         [29.590864807650654, 3.09600420367024]]),
    visualization = {"min":0,"max":3000,"bands":["B4","B3","B2"]},
    elevation = ee.Image("NASA/NASADEM_HGT/001"),
    elevationVis = {"opacity":1,"bands":["elevation"],"min":798.4562741273492,"max":913.6388202122735,"palette":["ffffff","000000"]},
    ls5 = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2"),
    rishiline = 
    /* color: #ffc82d */
    /* shown: false */
    ee.Geometry.LineString(
        [[27.393809280395935, -7.546264139871036],
         [27.409516296387146, -7.530863060720725]]),
    ls8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2"),
    emily_mine = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[25.885, -10.655],
          [25.885, -10.677],
          [25.914, -10.677],
          [25.914, -10.655]]]),
    DRC_1 = 
    /* color: #98ff00 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[22.280781101531133, -2.3971644195509354],
          [22.280781101531133, -10.814518184692893],
          [28.213398289031133, -10.814518184692893],
          [28.213398289031133, -2.3971644195509354]]], null, false),
    DRC_2 = 
    /* color: #0b4a8b */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[18.896992039031133, 4.277843412506412],
          [18.896992039031133, -2.3971644195509354],
          [29.443867039031133, -2.3971644195509354],
          [29.443867039031133, 4.277843412506412]]], null, false),
    DRC_3 = 
    /* color: #ffc82d */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[25.543720554656133, 0.6343495229935494],
          [25.543720554656133, -4.152037780823043],
          [28.707783054656133, -4.152037780823043],
          [28.707783054656133, 0.6343495229935494]]], null, false),
    table = ee.FeatureCollection("users/rishiAgarwal/Congo_Active_Mines"),
    mojaveline = /* color: #d619c3 */ee.Geometry.LineString(
        [[-115.80489660476239, 34.89453802554642],
         [-115.38054968093427, 35.03184163656472]]),
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
          [-115.07206070871891, 35.379488360140314]]], null, false);

//Scripts
Map.addLayer(table)

//Cloud Masking Function for the Sentinel 2 Images
function maskL457sr(image) {
// Bit 0 - Fill
// Bit 1 - Dilated Cloud
// Bit 2 - Unused
// Bit 3 - Cloud
// Bit 4 - Cloud Shadow
var qaMask = image.select('QA_PIXEL').bitwiseAnd(parseInt('11111', 2)).eq(0);
var saturationMask = image.select('QA_RADSAT').eq(0);
// Apply the scaling factors to the appropriate bands.
var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
var thermalBand = image.select('ST_B6').multiply(0.00341802).add(149.0);
// Replace the original bands with the scaled ones and apply the masks.
return image.addBands(opticalBands, null, true)
.addBands(thermalBand, null, true)
.updateMask(qaMask)
.updateMask(saturationMask);
}
    
//Cloud Masking Function for the Sentinel 2 Images
function maskS2clouds(image) {
  var qa = image.select('QA60');

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));

  return image.updateMask(mask);
}

//Choose which Area you want to analyze, either defined above or from imports
//Choose which Line you want to use to create charts
var area = rayroi1
var line =  rayline
//Centers the view around defined area
Map.centerObject(area, 13.5);
//Creates and Adds a 2021 Median Composite Image of selected Area 
//Cloud Masked as well, and filter by Cloud Pixel Percentage
function s2Composite(geometry) {
  var filtered = s2
  .filter(ee.Filter.bounds(geometry))
  .filter(ee.Filter.date('2021-01-01', '2021-12-31'))
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
  .map(maskS2clouds)
  .select('B.*');
  var composite = filtered.median().clip(geometry)
  return composite
}
var composite = s2Composite(area)
Map.addLayer(composite, visualization, '2021 Median Composite');

//Function for adding specfic indicies to the Composite Image
var addIndices = function(image) {
  var nirg = image.normalizedDifference(['B8', 'B3']).rename(['nirg'])
  var swirb = image.normalizedDifference(['B11', 'B2']).rename(['swirb'])
  var b5ndb6 = image.normalizedDifference(['B5','B6']).rename('NDB5B6')
  var ndmi = image.normalizedDifference(['B8', 'B11']).rename('ndmi')
  return image.addBands(nirg).addBands(swirb).addBands(b5ndb6).addBands(ndmi)
}
var withIndicies = addIndices(composite)

//Function to make a Cross Section give a ee.Geometry.Line
function makeCrossSection(section) {
  //Creating a Cross Section
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
  return points
}

var points = makeCrossSection(line)
Map.addLayer(points, {min:1, max:1, palette:['red']}, 'Cross Section', false);

// Select band values at every point
// Select which bands you want to use in the Graph
var ratios = withIndicies.select(withIndicies.bandNames()
.filter(ee.Filter.or(
  ee.Filter.eq('item', 'NDB5B6'))))

//Function to Add a constant line onto the chart defined below
//Takes in the collection of points, the threshold value, the item to be named in the Legend
function add_constant(collection, level, message) {
  function set_constant(x) {
    return x.set(message, level)
  }  
  return collection.map(set_constant)
}

//Addes the NIRG and SWIRB thresholds to the Chart
// points = add_constant(points, 0.30, "GNDVI Threshold")
// points = add_constant(points, 0.65, "SWIR/B Threshold")
//Choose which image will be used for the cross section
//Rename the bands needed 
var image = ratios.rename(['GNDVI'])
var bands = image.reduceRegions(points, ee.Reducer.first(), 10);
// text style variables
var textStyleTicks = {
color: 'black',
fontName: 'arial',
fontSize: 16,
bold: false,
italic: false
}
var textStyleTitles = {
color: 'black',
fontName: 'arial',
fontSize: 30,
bold: true,
italic: false
}
var textStyleLegend = {
color: 'black',
fontName: 'arial',
fontSize: 20,
bold: true,
italic: false
}
// Display a chart of band values along the cross section
var chartStyle = {
  //title: 'Blue, Green, Near Infrared, Shortwave 1 Bands over Mining, Vegetation and Urban Areas',
  legend: {textStyle: textStyleLegend},
  hAxis: {
    title: 'Cross Section Points',
    titleTextStyle: textStyleTitles,
    textStyle: textStyleTicks,
    gridlines: {color: 'FFFFFF'},
    viewWindow: {min: 0, max: 1000}
  },
  vAxis: {
    title: 'Normalized Difference Band Values',
    titleTextStyle: textStyleTitles,
    textStyle: textStyleTicks,
    gridlines: {color: 'FFFFFF'},
    format: 'short',
    baselineColor: 'FFFFFF',
    viewWindow: {min: -0.6, max: 0.8}
  },
  series: {
    0: {lineWidth: 2, color: 'green'},
    1: {lineWidth: 2, color: 'red'},
    2: {lineWidth: 2, color: 'blue'},
    3: {lineWidth: 2, color: 'orange'},
  },
  chartArea: {backgroundColor: 'EBEBEB'}
  
}
print(ui.Chart.feature.byFeature(bands).setOptions(chartStyle));

//Selecting specfic bands and adding them to the Map
var nirgVis = {min: -0.5, max: 0.8, palette: ['white', 'black']}
var swirbVis = {min: -0.5, max: 0.8, palette: ['white', 'blue']}
var ndb5b6Vis = {min: -0.6, max: 0.3, palette: ['white', 'red']}
Map.addLayer(withIndicies.select(['nirg']), nirgVis, "NIRG", false)
Map.addLayer(withIndicies.select(['swirb']), swirbVis, "SWIRB", false)
Map.addLayer(withIndicies.select(['NDB5B6']), ndb5b6Vis, "Band Variation", false)


//Creates and adds a rectangle given the coordinates to the Map
// var rec = ee.Geometry.Rectangle(29.565, 3.10, 29.59, 3.125)
// var rec2 = ee.Geometry.Rectangle(27.385,-7.55, 27.41, -7.525)
// var results = ee.Geometry.Rectangle(25.75, 0.5, 28.75, -2.5)
// var results_1 = ee.Geometry.Rectangle(25.75, 0.5, 26.75, -2.5)
// var results_2 = ee.Geometry.Rectangle(26.75, 0.5, 27.75, -2.5)
// var results_3 = ee.Geometry.Rectangle(27.75, 0.5, 28.75, -2.5)
// Map.addLayer(results)
// Map.addLayer(results_1)
// Map.addLayer(results_2)
// Map.addLayer(results_3)

/*
Function to create a Time Series Chart from specified coordinates, ratio and dates
'lon_min', 'lat_min', 'lon_max', 'lat_max' -> Coordinates of the area to chart, Ints
'bands', 'ratio' -> Bands (Array of Strings) are the bands to normalize difference to create the Ratio (String)
'date_start', 'date_end' -> Dates to Chart (String) , Formatted = 'YYYY-MM-DD'
Haxis_title, Vaxis_title -> Axis titles (String), H for Horizantal, V for Vertical 
*/
function SeriesChart(lon_min, lat_min, lon_max, lat_max, bands, ratio, date_start, date_end, Haxis_title, Vaxis_title) {
  //Creates the Rectangle given the coordinates from the parameters
  //Adds to the Map
  var rec = ee.Geometry.Rectangle(lon_min, lat_min, lon_max, lat_max)
  Map.addLayer(rec, {color: 'yellow'},'Mining region_' + lon_min.toString() + '_' + lat_min.toString(), false)
  
  //Given the bands and the name of the ratio defines a function that will be used to add 
  //The ratio to the imagecollection for the Time Series
  function addBand(image) {
    var band = image.normalizedDifference(bands).rename(ratio)
    return image.addBands(band) 
  }

  //Filters the Landsat 5 Collection to the dates that have been given
  var filteredl5 = ls5
  .filter(ee.Filter.bounds(rec))
  .filter(ee.Filter.date(date_start, date_end))
  .filter(ee.Filter.lt('CLOUD_COVER', 20))
  .map(maskL457sr)
  filteredl5 = filteredl5.map(addBand)
  
  //Filters the Landsat 8 Collection to the dates that have been given
  var filteredl8 = ls8
    .filter(ee.Filter.bounds(rec))
    .filter(ee.Filter.date(date_start, date_end))
    .filter(ee.Filter.lt('CLOUD_COVER', 20))
  filteredl8 = filteredl8.map(addBand)

  //Merges Landsat 5 and Landsat 8 data
  var filtered = filteredl5.merge(filteredl8)
  
  //Creates the chart given titles for the axis, ratio, and image collections of dates
  var chart = ui.Chart.image.series({
    imageCollection: filtered.select(ratio),
    region: rec,
    reducer: ee.Reducer.mean(),
    scale: 20
  }).setOptions({
        lineWidth: 1,
        interpolateNulls: true,
        vAxis: {title: Vaxis_title},
        hAxis: {title: Haxis_title, format: 'YYYY-MMM'}
      })
  print(chart)
}

// //Ray Region
// print("Ray Region")
// SeriesChart(29.565, 3.10, 29.59, 3.125, 
// ['SR_B4', 'SR_B5'], 'ndmi', '2010-01-01', '2021-01-01', 'Date', 'NDMI Values')
// //Rishi Region
// print("Rishi Region")
// SeriesChart(27.395,-7.545, 27.405, -7.535, 
// ['SR_B4', 'SR_B5'], 'ndmi', '2010-01-01', '2021-01-01', 'Date', 'NDMI Values')
// //Emily Region
// print("Emily Region")
// SeriesChart(25.90070162963844,-10.666253244366473, 25.903619873046644, -10.659505353198321, 
// ['SR_B4', 'SR_B5'], 'ndmi', '2010-01-01', '2021-01-01', 'Date', 'NDMI Values')



// /*
// * Legend setup
// */
// // current legend - CHANGE THIS to name of whatever visualization variable is being shown on map
// var vis = ndb5b6Vis

// // Creates a color bar thumbnail image for use in legend from the given color
// // palette.
// function makeColorBarParams(palette) {
// return {
// bbox: [0, 0, 1, 0.1],
// dimensions: '100x10',
// format: 'png',
// min: 0,
// max: 1,
// palette: palette,
// };
// }

// // Create the color bar for the legend.
// var colorBar = ui.Thumbnail({
// image: ee.Image.pixelLonLat().select(0),
// params: makeColorBarParams(vis.palette),
// style: {stretch: 'horizontal', margin: '0px 8px', maxHeight: '24px'},
// });
// // Create a panel with three numbers for the legend.
// var legendLabels = ui.Panel({
// widgets: [
// ui.Label(vis.min, {margin: '4px 8px'}),
// ui.Label(
// ((vis.max-vis.min) / 2+vis.min).round,
// {margin: '4px 8px', textAlign: 'center', stretch: 'horizontal'}),
// ui.Label(vis.max, {margin: '4px 8px'})
// ],
// layout: ui.Panel.Layout.flow('horizontal')
// });

// var legendTitle = ui.Label({
// value: 'Map Legend: Band Variation of Band 5 and Band 6',
// style: {fontWeight: 'bold'}
// });
// // Add the legendPanel to the map.
// var legendPanel = ui.Panel([legendTitle, colorBar, legendLabels]);
// Map.add(legendPanel);