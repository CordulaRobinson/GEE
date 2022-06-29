//Imports
var IPIS = ee.FeatureCollection("users/rishiAgarwal/Congo_Active_Mines");

//Script


var box = ee.Geometry.Polygon(
[[[29, -8],
[29, -9],
[30, -9],
[30, -8]]], null, false)
var ipis_filtered = IPIS.filter(ee.Filter.bounds(box)).select('longitude', 'latitude')

print(ipis_filtered)

Export.table.toDrive({
collection: ipis_filtered,
description:'ipis_26_-8',
fileFormat: 'CSV'
});

