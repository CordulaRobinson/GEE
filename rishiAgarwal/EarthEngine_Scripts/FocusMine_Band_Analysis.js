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
    ee.Geometry.MultiPolygon(
        [[[[27.40659150209595, -7.545617347478231],
           [27.40534695711304, -7.548127419922782],
           [27.406720248128664, -7.551105453076205],
           [27.40835103120972, -7.551488341564595],
           [27.40981015291382, -7.550169502010019],
           [27.409509745504153, -7.548127419922782]]],
         [[[27.40604300537111, -7.536556110485316],
           [27.40803009098612, -7.539267568831433],
           [27.409617958722936, -7.538374136591145],
           [27.409961281476843, -7.534885478762249],
           [27.408974228559362, -7.534332396281891]]],
         [[[27.38228463338587, -7.548630063235868],
           [27.386061183678837, -7.5450138567503675],
           [27.385546199547978, -7.543524821762933],
           [27.3805251042721, -7.543099382253798],
           [27.378636829125615, -7.543269558107644],
           [27.379323474633427, -7.545269119376455]]],
         [[[27.383894057143692, -7.52134116509038],
           [27.384752364028458, -7.5340197199956265],
           [27.388357252944473, -7.537338206679539],
           [27.398828596938614, -7.536912761089743],
           [27.399343581069473, -7.5211709806245075]]],
         [[[27.400373549331192, -7.560651985280287],
           [27.39968690382338, -7.550782071892611],
           [27.3952237080226, -7.5494206868352345],
           [27.39144715772963, -7.552824141438857],
           [27.39093217359877, -7.556567910541829]]],
         [[[27.353166670669083, -7.543634752523532],
           [27.356428236831192, -7.562523839956695],
           [27.35951814161635, -7.5613326606473255],
           [27.35574159132338, -7.542954049281069]]]]),
    TailingPonds = 
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
    crossUnknown = 
    /* color: #00ffff */
    /* shown: false */
    ee.Geometry.LineString(
        [[27.396444391565726, -7.538710029853083],
         [27.404426645594047, -7.545431993373103]]),
    crossTailing = 
    /* color: #0fc211 */
    /* shown: false */
    ee.Geometry.LineString(
        [[27.3991051429085, -7.5361573581314465],
         [27.407774042444633, -7.540326714159248]]),
    MinePile = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.MultiPolygon(
        [[[[27.39990282562306, -7.538976580191123],
           [27.39863682296803, -7.539487112415201],
           [27.398057465820813, -7.54067835192985],
           [27.397799973755383, -7.542380116977695],
           [27.398883584767866, -7.542497115405488],
           [27.4003963520818, -7.542784285193142],
           [27.401705270081067, -7.541890860211821],
           [27.4014048626714, -7.540295453871944],
           [27.400782588904605, -7.539561565404619]]],
         [[[27.40360114464233, -7.528471399345152],
           [27.40287158379028, -7.53102411635294],
           [27.40506026634643, -7.531151751808675],
           [27.40561816582153, -7.528769217103983]]],
         [[[27.400167917103268, -7.535108432289119],
           [27.400554155201412, -7.5369803975571035],
           [27.403300737232662, -7.537108031257986],
           [27.403944467396236, -7.5352360665416755],
           [27.402013276905514, -7.533491728501599]]],
         [[[27.357092737193568, -7.547347692672706],
           [27.357650636668666, -7.550155558119731],
           [27.359431623454554, -7.550389546083809],
           [27.360375761027797, -7.547985845511823],
           [27.35890590547972, -7.545039700922603],
           [27.357500432963832, -7.545135422206587]]]]);

//Script
Map.setCenter(27.3954, -7.55, 13) //Kanunka Village

//Helps for visiblity of the Landsat8 images
function applyScaleFactors(image) {
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);
  return image.addBands(opticalBands, null, true)
              .addBands(thermalBands, null, true);
}
var landsat8 = l8.map(applyScaleFactors)

var addIndices = function(image) {
  var ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename(['ndvi']); // NIR, RED
  var ndbi = image.normalizedDifference(['SR_B6', 'SR_B5']).rename(['ndbi']); // NIR, SWIR1
  var clay = image.normalizedDifference(['SR_B6', 'SR_B7']).rename(['clay']); // SWIR1, SWIR2
  var iron = image.normalizedDifference(['SR_B4', 'SR_B2']).rename(['iron']); // RED, BLUE
  var ndmi = image.normalizedDifference(['SR_B5', 'SR_B6']).rename(['ndmi']); // NIR, SWIR1
  // add in VII & WDI
  var vigs = image.expression(
    '((A-B)/(A+B)) + ((C-B)/(C+B))/2 + ((C-D)/(C+D)) + ((C-D)/(C+D))/2 + ((C-E)/(C+E)) + ((C-E)/(C+E))/2', {
    'A': image.select('SR_B3'), // GREEN
    'B': image.select('SR_B4'), // RED
    'C': image.select('SR_B5'), // NIR
    'D': image.select('SR_B6'), // SWIR1
    'E': image.select('SR_B7'), // SWIR2
    }).rename('vigs');
  return image.addBands(ndvi).addBands(clay).addBands(iron).addBands(ndmi)
    .addBands(vigs);
};

//Establishs our roi over the 2013 time period
var roi = landsat8
.filter(ee.Filter.lt('CLOUD_COVER', 25))
.filter(ee.Filter.date('2013-01-01', '2014-01-01'))
.filter(ee.Filter.bounds(focus))
.select('SR_B.*')

var roi2013 = roi.median().clip(focus)
var roi2013 = addIndices(roi2013)

Map.addLayer(roi2013, l8Vis, '2013')

//ROI for the 2020 year
var roi2020 = landsat8
  .filter(ee.Filter.lt('CLOUD_COVER', 25))
  .filter(ee.Filter.date('2020-01-01', '2021-01-01'))
  .filter(ee.Filter.bounds(focus))
  .select('SR_B.*')
  .median()
  .clip(focus)
var roi2020 = addIndices(roi2020)
Map.addLayer(roi2020, l8Vis, '2020');

//NDVI Layer
var roi2013NDVI = roi2013.select('ndvi')
Map.addLayer(roi2013NDVI, {min: 0, max: 1, palette: ['white', 'green']}, "NDVI2013")

var roi2020NDVI = roi2020.select('ndvi')
Map.addLayer(roi2020NDVI, {min: 0, max: 1, palette: ['white', 'green']}, "NDVI2020")

//IRON COMBINATION 
var roi2013Iron = roi2013.select('iron')
Map.addLayer(roi2013Iron, {min: 0, max: 0.8, palette: ['white', 'purple']}, "Iron2013")

var roi2020Iron = roi2020.select('iron')
Map.addLayer(roi2020Iron, {min: 0, max: 0.8, palette: ['white', 'purple']}, "Iron2020")

//CLAY COMBINATION
var roi2013Clay = roi2013.select('clay')
Map.addLayer(roi2013Clay, {min: 0, max: 0.5, palette: ['white', 'red']}, "Clay2013")

var roi2020Clay = roi2020.select('clay')
Map.addLayer(roi2020Clay, {min: 0, max: 0.5, palette: ['white', 'red']}, "Clay2020")

//Normalized Difference Mositure 
var roi2013Moisture = roi2013.select('ndmi')
Map.addLayer(roi2013Moisture, {min: 0, max: 1, palette: ['white', 'blue']}, "Moisture2013")

var roi2020Moisture = roi2020.select('ndmi')
Map.addLayer(roi2020Moisture, {min: 0, max: 1, palette: ['white', 'blue']}, "Moisture2020")

//Green and Shortwave Infared 
var roi2013VIGS = roi2013.select('vigs')
Map.addLayer(roi2013VIGS, {min: 0, max: 2.5, palette: ['white', 'green']}, "VIGS_2013")

var roi2020VIGS = roi2020.select('vigs')
Map.addLayer(roi2020VIGS, {min: 0, max: 2.5, palette: ['white', 'green']}, "VIGS_2020")



//TIME SERIES CHARTS
var smallerArea = landsat8.filter(ee.Filter.lt('CLOUD_COVER', 25))
.filter(ee.Filter.date('2014-01-01', '2021-01-01'))

var smallerArea = smallerArea.map(addIndices)

function makeChart(imageCollection, region, title) {
  return ui.Chart.image.series({
  imageCollection: imageCollection,
  region: region,
  reducer: ee.Reducer.mean(),
  scale: 20
}).setOptions({
      lineWidth: 1,
      title: title,
      interpolateNulls: true,
      vAxis: {title: 'value'},
      hAxis: {title: '', format: 'YYYY-MMM'}
    })
}

print('Outlier Graphs')

var outlierNDVI = makeChart(smallerArea.select('ndvi'), TailingPonds, 'NDVI Outlier')
var outlierVIGS = makeChart(smallerArea.select('vigs'), TailingPonds, 'VIGS Outlier')
var outlierNDMI = makeChart(smallerArea.select('ndmi'), TailingPonds, 'NDMI Outlier')
var outlierIron = makeChart(smallerArea.select('iron'), TailingPonds, 'Iron Outlier')

print(outlierNDVI)
print(outlierVIGS)
print(outlierNDMI)
print(outlierIron)

print('Veg Near Mine Graphs')

var vegNearMineNDVI = makeChart(smallerArea.select('ndvi'), nearMine, 'NDVI Near Mine')
var vegNearMineVIGS = makeChart(smallerArea.select('vigs'), nearMine, 'VIGS Near Mine')
var vegNearMineNDMI = makeChart(smallerArea.select('ndmi'), nearMine, 'NDMI Near Mine')
var vegNearMineIron = makeChart(smallerArea.select('iron'), nearMine, 'Iron Near Mine')


print(vegNearMineNDVI)
print(vegNearMineVIGS)
print(vegNearMineNDMI)
print(vegNearMineIron)


//vegNearMasked = vegNearWithNDVI.updateMask(vegNearWithNDVI.select('ndvi').lt(.1))

var mys3 = roi2020.normalizedDifference(['SR_B5', 'SR_B7'])
Map.addLayer(mys3, {min: 0, max: 0.5, palette: ['white', 'pink']}, "NIR/SWIR2 index")


//SHOWS MINE POINTS ON THE MAP
var visParams = {'color': 'blue'}
var coltanMines = mines
    .filterMetadata('mineral1', 'equals', 'Coltan')
    .merge(mines.filterMetadata('mineral2', 'equals', 'Coltan'))
    .merge(mines.filterMetadata('mineral3', 'equals', 'Coltan'))

Map.addLayer(coltanMines, visParams, 'Coltan')
