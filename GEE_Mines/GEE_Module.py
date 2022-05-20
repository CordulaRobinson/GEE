import os
import sys
import ee
import time
from csv import reader,writer
from scipy.interpolate import LinearNDInterpolator
import numpy as np
import filelock
import glob

class GEE_Mine(object):

    def __init__(self,system = 'Cluster', username='e.conway', jobname='routine', wd='/scratch/e.conway/', outputdir='outputs', \
                resultsdir='results', jobdir='batch', compiledfilename='compiled', assetid = 'users/EmilyNason/FinalResults', \
                featgeedescription='compiled_results', makefeaturecollection='False', conda_env_name='gee'):
        self.system = system
        self.username = username
        self.jobname = jobname
        self.conda_env_name = conda_env_name
        self.wd = wd
        self.outputdir = outputdir
        self.resultsdir = resultsdir
        self.jobdir = jobdir
        self.compiledfilename = compiledfilename
        self.assetid = assetid
        self.featgeedescription = featgeedescription
        self.makefeaturecollection = True if makefeaturecollection == 'True' else False

    def start_process(self, lon_min, lat_min, lon_max, lat_max, size, multiple, count, pixres):
        """
        args:
        bounding region, in lon/lat
        size: desired target size in km**2, only imortant when multiple == True i.e for creating large regions
        pixres: pixel resolution in km. Must be entered regardless of multiple=True/False
        multiple: 
        True: are we going to run multiple jobs on this bounding region at a desired target resolution of size, or, 
        False: have we already divided the areas up into size*size and want to run the routine on size*size for pixres
        """
        
        ee.Initialize()

        self.lon_min = lon_min
        self.lat_min = lat_min
        self.lon_max = lon_max
        self.lat_max = lat_max
        self.multiple = True if multiple == 'True' else False
        self.size=size
        self.count=count
        self.pixres=pixres

        self.outputdir = os.path.basename(self.outputdir)
        self.resultsdir = os.path.basename(self.resultsdir)
        self.jobdir = os.path.basename(self.jobdir)
        self.compiledfilename = os.path.basename(self.compiledfilename).split('.csv')[0]
        
        # this is for capturing failed jobs - the code will search and get this line when GEE exceptions are detected
        print("input= ",self.lon_min,' ',self.lat_min,' ',self.lon_max,' ',self.lat_max,' ',self.count,' ',\
             self.pixres,' ',self.system,' ',self.username,' ',self.jobname,' ',self.wd,' ',self.outputdir,' ',\
             self.resultsdir,' ',self.jobdir,' ',self.compiledfilename,' ',self.makefeaturecollection,' ',\
             self.assetid,' ',self.featgeedescription,' ',\
             self.multiple,' ',self.size,self.conda_env_name+'\n')
        
        self.outputdir = os.path.join(self.wd,self.outputdir)
        if not os.path.exists(self.outputdir):
            os.mkdir(self.outputdir)
            
        self.resultsdir = os.path.join(self.wd,self.resultsdir)
        if not os.path.exists(self.resultsdir):
            os.mkdir(self.resultsdir)

        self.jobdir = os.path.join(self.wd,self.jobdir)
        if not os.path.exists(self.jobdir):
            os.mkdir(self.jobdir)
            
        self.compiledfilename = os.path.join(self.resultsdir,self.compiledfilename+'.csv')
        
        #region of interest
        self.region = ee.Geometry.Polygon(
                [[[ee.Number.parse(self.lon_min), ee.Number.parse(self.lat_max)],
                  [ee.Number.parse(self.lon_min), ee.Number.parse(self.lat_min)],
                  [ee.Number.parse(self.lon_max), ee.Number.parse(self.lat_min)],
                  [ee.Number.parse(self.lon_max), ee.Number.parse(self.lat_max)]]])
        
        # setting up for running lots of jobs
        if self.multiple:
            # execute the GEE Mine Routine i.e. submit lots of jobs
            # the code will keep appending to one single file, unless an issue happens
            # when it will write a unique file rather than starting again
            self.create_large_squares()
        else:
            # we just want to run one job, on one area
            self.main_routine()
            # check for failures
            keep_running = self.check_failures()
            time.sleep(10)
            if not keep_running:
                # check if there are any others running in queue
                complete=self.check_status()
                if complete:
                    # if keep running is False and no more in queue (complete==True), then we can run analysis
                    # but first ensure only one csv in folder of results
                    # else there were filelock errors, and the smaller one needs to be appended to larger one
                    try:
                        glob_files = glob.glob(self.resultsdir+'/*.csv')
                        if len(glob_files) > 1:
                            for file in glob_files:
                                if file != self.compiledfilename:
                                    with open(file,'r') as f:
                                        csv_reader = reader(f)
                                    with open(self.compiledfilename,'a') as g:
                                        csv_writer = writer(g)
                                        for row in csv_reader:
                                            csv_writer.writerow(row)
                                    os.system("rm "+str(file))
                    except:
                        print('Error on merging .csv files, exitting')
                        exit()
                    
                    #No running jobs, no failures, now we analyze
                    self.convert()
                    if self.makefeaturecollection:
                        self.geefeature()

                    # Remove accumulated files
                    os.system('rm failed.txt queue.txt queue.txt.lock number.txt number.txt.lock slurm*')
                    os.chdir(wd)
                    os.system('rm ' + self.outputdir + '/* ' + self.jobdir + '/*')
                    os.system('rm ' + self.compiledfilename + '.lock')
                    os.chdir('..')
        return 
    
    def main_routine(self):

        # DATASETS
        self.ls5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
        self.s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
        self.s2 = ee.ImageCollection("COPERNICUS/S2_SR")
        admin = ee.FeatureCollection("FAO/GAUL/2015/level0")

        training_region = ee.Geometry.Polygon(
                [[[29.554129272985683, 3.1591674847348235],
                  [29.554129272985683, 3.092319151883147],
                  [29.625197083044277, 3.092319151883147],
                  [29.625197083044277, 3.1591674847348235]]])

        # system arguments
        left, right, top, bot = self.lon_min, self.lon_max, self.lat_max, self.lat_min 
        job_num = self.count

        # TRAINING DATA
        # landsat
        bare = ee.FeatureCollection(
                [ee.Feature(
                    ee.Geometry.Point([29.566649352977876, 3.131936594576548]),
                    {
                      "landcover": 0,
                      "system:index": "0"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.594069479589553, 3.143136886698536]),
                    {
                      "landcover": 0,
                      "system:index": "1"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.578229613742543, 3.109209943820683]),
                    {
                      "landcover": 0,
                      "system:index": "2"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.581158585986806, 3.1067030888196494]),
                    {
                      "landcover": 0,
                      "system:index": "3"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.55884031463487, 3.11517956941471]),
                    {
                      "landcover": 0,
                      "system:index": "4"
                    })])

        vegetation = ee.FeatureCollection(
                [ee.Feature(
                    ee.Geometry.Point([29.581819366025293, 3.132088091449441]),
                    {
                      "landcover": 1,
                      "system:index": "0"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.595938514279688, 3.131445322675145]),
                    {
                      "landcover": 1,
                      "system:index": "1"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.59962923388418, 3.1347448648629315]),
                    {
                      "landcover": 1,
                      "system:index": "2"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.565039466428125, 3.104877202480009]),
                    {
                      "landcover": 1,
                      "system:index": "3"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.607741346488673, 3.1193612914096605]),
                    {
                      "landcover": 1,
                      "system:index": "4"
                    })])

        # sentinel
        bare_s = ee.FeatureCollection(
                [ee.Feature(
                    ee.Geometry.Point([29.588761955782978, 3.110552597531067]),
                    {
                      "landcover": 0,
                      "system:index": "0"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.590113789126484, 3.1101669284095776]),
                    {
                      "landcover": 0,
                      "system:index": "1"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.570400011069342, 3.114240974803364]),
                    {
                      "landcover": 0,
                      "system:index": "2"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.56574369621949, 3.114048140935224]),
                    {
                      "landcover": 0,
                      "system:index": "3"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.566300979571633, 3.1296952794920045]),
                    {
                      "landcover": 0,
                      "system:index": "4"
                    })])

        vegetation_s = ee.FeatureCollection(
                [ee.Feature(
                    ee.Geometry.Point([29.61279975505381, 3.134623171579494]),
                    {
                      "landcover": 1,
                      "system:index": "0"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.620696178393654, 3.1514206812868597]),
                    {
                      "landcover": 1,
                      "system:index": "1"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.60730659099131, 3.15656272195781]),
                    {
                      "landcover": 1,
                      "system:index": "2"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.609366527514748, 3.1041127202608414]),
                    {
                      "landcover": 1,
                      "system:index": "3"
                    }),
                ee.Feature(
                    ee.Geometry.Point([29.561301341967873, 3.0982847807562592]),
                    {
                      "landcover": 1,
                      "system:index": "4"
                    })])

        # TRAINING CLASSIFIERS
        # landsat
        training = bare.merge(vegetation)
        composite1985 = self.ls5 \
                .filter(ee.Filter.bounds(training_region)) \
                .filter(ee.Filter.date('1985-01-01', '1986-01-01')) \
                .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
                .map(self.mask_ls5_clouds) \
                .select('SR_B.*') \
                .median() \
                .clip(training_region)

        # overlay the point on the image to get training data
        training = composite1985.sampleRegions(**{
          'collection': training,
          'properties': ['landcover'],
          'scale': 1
        })

        # train a classifier
        self.classifier_ls = ee.Classifier.smileRandomForest(50).train(**{
          'features': training,
          'classProperty': 'landcover',
          'inputProperties': composite1985.bandNames()
        })

        # sentinel
        training = bare_s.merge(vegetation_s)

        composite2021 = self.s2 \
                .filter(ee.Filter.bounds(training_region)) \
                .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                .map(self.mask_s2_clouds) \
                .select('B.*') \
                .median() \
                .clip(training_region) \

        # overlay the point on the image to get training data
        training = composite2021.sampleRegions(**{
          'collection': training,
          'properties': ['landcover'],
          'scale': 1
        })

        # train a classifier
        self.classifier_s2 = ee.Classifier.smileRandomForest(50).train(**{
          'features': training,
          'classProperty': 'landcover',
          'inputProperties': composite2021.bandNames()
        })

        # Calculate values for pixresxpixres squares
        regions = self.create_segments()
        segments = ee.FeatureCollection(regions)
        results = segments.map(self.passing_mine)

        # Create above array for each segment, and transform into format that can be written to a CSV file
        data_set = results.map(self.create_results)
        data_set2 = data_set.aggregate_array('info')
        Pass = True
        try:
            data_set3 = data_set2.getInfo() # <- slow
        except Exception as e:
            Pass = False
            print(f'Caught error {e} on getinfo - trying to re-run with smaller target area')
            x.start_process(self.lon_min,self.lat_min,self.lon_max,self.lat_max,\
                            self.size*0.5,self.multiple,self.count,self.pixres)
        if Pass:
            with_scores = self.check_false_positive(data_set3)
            # CSV header
            header_list = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
                  'Percent Vegetation Loss', 'Percent Bare Initial','Percent Significant VH Values', 'Average NIR/G', 'Average SWIR1/B', 'NASADEM Elevation', 'GEDI Elevation','GEDI-SRTM Elevation','GEDI Quality Flag', 'B5', 'B6', 'NDMI']

            # Create CSV and add header & data
            # new file if not already existing
            if not os.path.exists(self.compiledfilename):
                lockname=self.compiledfilename+'.lock'
                lock = filelock.FileLock(lockname)
                try:
                    with lock.acquire(timeout=60):
                        with open(self.compiledfilename, 'w') as f:
                            csv_writer = writer(f)
                            csv_writer.writerow(header_list)
                            csv_writer.writerows(with_scores)

                except Exception as e:
                    print('Could not get file lock on target, writing to specific file instead, append to main later')
                    newfilename = str(self.username)+'_'+str(self.jobname)+'_'+str(self.lon_min)\
                    +'_'+str(self.lon_max)+'_'+str(self.lat_min)+'_'+str(self.lat_max)+\
                    +'_'+str(self.pixres)+'_'+str()+'_'+str()+'_'+str()
                    with open(os.path.join(self.resultsdir,newfilename), 'w') as f:
                        csv_writer = writer(f)
                        csv_writer.writerows(with_scores)
            
            else:
                # append file
                lockname=self.compiledfilename+'.lock'
                lock = filelock.FileLock(lockname)
                try:
                    with lock.acquire(timeout=60):
                        with open(self.compiledfilename, 'a') as f:
                            csv_writer = writer(f)
                            csv_writer.writerows(with_scores)

                except Exception as e:
                    print('Could not get file lock on target, writing to specific file instead, append to main later')
                    newfilename = str(self.username)+'_'+str(self.jobname)+'_'+str(self.lon_min)\
                    +'_'+str(self.lon_max)+'_'+str(self.lat_min)+'_'+str(self.lat_max)+\
                    +'_'+str(self.pixres)+'_'+str()+'_'+str()+'_'+str()
                    with open(os.path.join(self.resultsdir,newfilename), 'w') as f:
                        csv_writer = writer(f)
                        csv_writer.writerows(with_scores)

        return 
    
    def create_segments(self):
        # grab the top left coordinate of the bounding box
        coords = ee.List(self.region.coordinates().get(0)).slice(0, -1)
        top = ee.Number(ee.List(coords.get(2)).get(1))
        left = ee.Number(ee.List(coords.get(0)).get(0))
        top_left_point = ee.Geometry.Point([left, top])
        

        # calculate square pixel width and height
        width = int(ee.Geometry.Point(coords.get(0)).distance(ee.Geometry.Point(coords.get(1))).divide(1000 * self.pixres).getInfo()) # how many squares can fit in the width of the bounding box
        height = int(ee.Geometry.Point(coords.get(1)).distance(ee.Geometry.Point(coords.get(2))).divide(1000 * self.pixres).getInfo()) # how many squares can fit in the height of the bounding box

        # create a point buffer and use it to find the km distance to lat/lon degree conversion
        buff = top_left_point.buffer(self.pixres*1000, 0.1) # create the buffer with a max % error of 0.1
        buff_list = ee.List(buff.coordinates().get(0)) 
        buff_length = buff_list.length()
        right_pt = ee.List(buff_list.get(buff_length.multiply(0.75).int().subtract(1)))
        bottom_pt = ee.List(buff_list.get(buff_length.multiply(0.5).int().subtract(1)))
        new_lat = ee.Number(right_pt.get(0)) # given distance east of the top left point
        new_lon = ee.Number(bottom_pt.get(1)) # given distance south of the top left point

        diff_lon = top.subtract(new_lon) # given size converted to degrees
        diff_lat = new_lat.subtract(left)

        # build the list of squares
        segments = []
        for y in range(height + 1): # +1 to guarantee we will cover the whole region (squares may extend slightly past the bounding box)
            left = ee.Number(ee.List(coords.get(0)).get(0))
            for x in range(width + 1):
                new_lat = left.add(diff_lat)
                new_lon = top.subtract(diff_lon)

                square = ee.Geometry.Polygon(
                    [[[left, new_lon],
                      [new_lat, new_lon],
                      [new_lat, top],
                      [left, top]]])

                segments.append(square)

                left = new_lat
            top = new_lon

        return segments
    
    # CLOUD MASKING FUNCTIONS
    # landsat
    def mask_ls5_clouds(self,image):
        qaMask = image.select('QA_PIXEL').bitwiseAnd(int('11111', 2)).eq(0)
        saturationMask = image.select('QA_RADSAT').eq(0)

        opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)

        return image.addBands(opticalBands, None, True) \
                .updateMask(qaMask) \
                .updateMask(saturationMask)

    # sentinel
    def mask_s2_clouds(self,image):
        qa = image.select('QA60')

        cloudBitMask = 1 << 10
        cirrusBitMask = 1 << 11

        mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))

        return image.updateMask(mask).divide(10000).select("B.*").copyProperties(image, ["system:time_start"])
    
    def passing_mine(self,feature):
        veg = self.calculate_percentage_change(feature)
        sar = self.calculate_sar_vh(feature)
        bands_and_indices = self.get_s2_bands_and_indices(feature)
        NASADEM = self.get_NASADEM(feature)
        GEDI = self.calc_gedi_loss(feature)
        return ee.Feature(feature \
            .set('vegetation loss', veg.get('percent loss')) \
            .set('percent bare', veg.get('percent bare')) \
            .set('vh', sar.get('vh_percent')) \
            .set('nir/g', bands_and_indices.get('NIR/G')) \
            .set('swir1/b', bands_and_indices.get('SWIR1/B'))\
            .set('NASADEM Elevation',NASADEM.get('elevation')) \
            .set('GEDI Elevation',GEDI.get('GEDI'))\
            .set('GEDI-SRTM Elevation',GEDI.get('loss'))\
            .set('GEDI Quality Flag',GEDI.get('quality flag'))\
            .set('B5 value', bands_and_indices.get('B5'))\
            .set('B6 value', bands_and_indices.get('B6'))\
            .set('NDMI', bands_and_indices.get('NDMI')))
            

    def create_results(self,feature):
            coords = ee.List(feature.geometry().coordinates().get(0))
            lon_min = ee.List(coords.get(0)).get(0)
            lon_max = ee.List(coords.get(1)).get(0)
            lat_min = ee.List(coords.get(0)).get(1)
            lat_max = ee.List(coords.get(2)).get(1)
            veg_loss = feature.get('vegetation loss')
            bare_init = feature.get('percent bare')
            vh = feature.get('vh')
            nir_g = feature.get('nir/g')
            swir1_b = feature.get('swir1/b')
            nasadem = feature.get('NASADEM Elevation')
            gedi_elev = feature.get('GEDI Elevation')
            gedi_loss = feature.get('GEDI-SRTM Elevation')
            gedi_qual = feature.get('GEDI Quality Flag')
            b5_val = feature.get('B5 value')
            b6_val = feature.get('B6 value')
            ndmi = feature.get('NDMI')
            row = ee.Array([lon_min, 
                           lat_min, 
                           lon_max,
                           lat_max,
                           veg_loss,
                           bare_init, 
                           vh,
                           nir_g,
                           swir1_b,
                           nasadem,
                           gedi_elev, 
                           gedi_loss,
                           gedi_qual,
                           b5_val,
                           b6_val,
                           ndmi])
            new_feature = ee.Feature(None, {'info': row})
            return new_feature

    def geefeature(self):
            
        # Convert to a Feature Collection
        # Create a list of Geometries for areas that passed as possible mines
        tempname = (os.path.basename(self.compiledfilename)).split('.csv')[0]
        with open(os.path.join(self.resultsdir, tempname + '_status_passing.csv'), 'r') as r:
            csv_reader = reader(r)
            # Skip Header in input file
            header = next(csv_reader)
            self.region_list = []
            if header != None:
                # Convert each region to a Geometry and add to a list
                for row in csv_reader:
                    region = ee.Geometry.Polygon([[[float(row[0]), float(row[3])],
                                  [float(row[0]), float(row[1])],
                                  [float(row[2]), float(row[1])],
                                  [float(row[2]), float(row[3])]]])
                    f = ee.Feature(region).set('elevation score', float(row[17])).set('b5/b6 score', float(row[18]))
                    self.region_list.append(f)


        # Wrap geometry list in a Feature Collection
        fc = ee.FeatureCollection(self.region_list)

        # Export the Feature Collection to Google Earth Engine (GEE)
        task = ee.batch.Export.table.toAsset(**{
              'collection': fc,
              'description':self.featgeedescription,
              'assetId': self.assetid, # change to your GEE Asset path and a unique name (will not overwrite already existing assets, so old names cannot be reused)
            })

        task.start()
        return
    
    def convert(self):

        # For a given CSV file of region coordinates and test values, calculate and document whether this region may be a mining location
        # All results will be saved in "[file_name]_status.csv"
        # Passing region results only will be saved in "[file_name]_status_passing.csv"

        # Open the input file in read mode and output file in write mode
        tempname = (os.path.basename(self.compiledfilename)).split('.csv')[0]
        with open(os.path.join(self.resultsdir, tempname + '.csv'), 'r') as read_obj, \
                open(os.path.join(self.resultsdir, tempname + '_status.csv'), 'w', newline='') as write_obj:
            # Create a csv.reader object from the input file object
            csv_reader = reader(read_obj)
            next(csv_reader) # skip header
            # Create a csv.writer object from the output file object
            csv_writer = writer(write_obj)
            # Add header to output file, with status column
            # Add header to output file, with status column
            header_list = ['Mininum Longitude', 'Minimum Latitude', 'Maximum Longitude', 'Maximum Latitude', \
                           'Percent Vegetation Loss', 'Percent Bare Initial', 'Percent Significant VH Values', \
                           'Average NIR/G', 'Average SWIR1/B', 'NASA Elev', 'GEDI Elev', 'Elev Loss','GEDI Qual. Flag',\
                           'B5 Value', 'B6 Value', 'NDMI', 'Center Lon', 'Center Lat','Elevation Score', \
                           'Band Variation Score','Status']
            csv_writer.writerow(header_list)
            # Read each row of the input csv file as list
            for row in csv_reader:
                """
                Calculate Status and append to the end of the row/list
                Passing Criteria:
                If Vegetation Loss < 20% and Bare Earth > 20%: 
                    SAR VH > 25% and NIR/G <= 0.3 and SWIR1/B < 0.65 and Elevation Score >= 5 and B5/B6 Score >= 4
                Else: 
                    Vegetation Loss > 20% and SAR VH > 25% and NIR/G <= 0.3 and SWIR1/B < 0.65
                """
                vegetation_loss = float(row[4])
                percent_bare = float(row[5])
                sar_vh = float(row[6])
                nir_g = float(row[7])
                swir1_b = float(row[8])
                elevation_score = float(row[17])
                b5_b6_score = float(row[18])
                
                if vegetation_loss < 20 and percent_bare > 20:
                    status = sar_vh > 25 and nir_g <= 0.3 and swir1_b < 0.65 and elevation_score >= 5 and b5_b6_score >= 4
                else: 
                    status = vegetation_loss > 20 and sar_vh > 25 and nir_g <= 0.3 and swir1_b < 0.65

                if status:
                    row.append('Pass')
                else: 
                    row.append('Fail')

                # Add the updated row / list to the output file
                csv_writer.writerow(row)

        # Create a file of only passing statuses
        tempname = (os.path.basename(self.compiledfilename)).split('.csv')[0]
        with open(os.path.join(self.resultsdir , tempname + '_status.csv'), 'r') as r, \
                open(os.path.join(self.resultsdir , tempname + '_status_passing.csv'), 'w', newline='') as w:
            # Create a csv.reader object from the input file object
            csv_reader = reader(r)
            # Create a csv.writer object from the output file object
            csv_writer = writer(w)
            # Add header to output file, with status column
            csv_writer.writerow(header_list)
            # Skip Header in input file
            header = next(csv_reader)
            if header != None:
                # Add passing rows to new file
                for row in csv_reader:
                    if row[19] == "Pass":
                        csv_writer.writerow(row)
        
        return
    
    def check_false_positive(self, arr):
        arr = self.add_centers(arr)
        arr = np.array(arr)

        # columns
        lons = arr[:,15]
        lats = arr[:,16]
        nasa_dem = arr[:,9]
        b5_vals = arr[:,13]
        b6_vals = arr[:,14]

        # create interpolators
        interp_elev = LinearNDInterpolator((lons, lats), nasa_dem)
        interp_b5 = LinearNDInterpolator((lons, lats), b5_vals)
        interp_b6 = LinearNDInterpolator((lons, lats), b6_vals)

        # calculate scores
        elev_scores = []
        b5_b6_scores = []
        for row in arr:
            center_lon = row[15]
            center_lat = row[16]
            center_elev = row[9]
            center_b5 = row[13]
            center_b6 = row[14]
            center_nd_b5_b6 = (center_b5 - center_b6) / (center_b5 + center_b6)

            elev_score = 0
            b5_b6_score = 0
            neighbors = self.get_neighbors(center_lon, center_lat, 250)
            for neighbor_lon, neighbor_lat in neighbors:
                # elevation scores
                interpolated_elev = interp_elev(neighbor_lon, neighbor_lat)
                if center_elev < interpolated_elev:
                    elev_score += 1

                # b5/b6 scores
                interpolated_b5 = interp_b5(neighbor_lon, neighbor_lat)
                interpolated_b6 = interp_b6(neighbor_lon, neighbor_lat)
                interp_nd_b5_b6 = (interpolated_b5 - interpolated_b6) / (interpolated_b5 + interpolated_b6)
                if abs(center_nd_b5_b6 - interp_nd_b5_b6) > 0.02:
                    b5_b6_score += 1

            elev_scores.append([elev_score])
            b5_b6_scores.append([b5_b6_score])

        # append scores
        combined_scores = np.append(np.array(elev_scores), np.array(b5_b6_scores), axis=1)
        arr_with_scores = np.append(arr, combined_scores, axis=1)

        return arr_with_scores

    def add_centers(self, arr):
        for row in arr:
            min_lon = row[0]
            min_lat = row[1]
            max_lon = row[2]
            max_lat = row[3]

            center_lon = (min_lon + max_lon) / 2
            center_lat = (min_lat + max_lat) / 2
            
            row += [center_lon, center_lat]

        return arr

    def get_neighbors(self, lon, lat, dist):
        deg_offset = dist * 0.00001 # rough meters to degree approximation

        neighbors = [(lon, lat + deg_offset),              # N
                     (lon + deg_offset, lat + deg_offset), # NE
                     (lon + deg_offset, lat),              # E
                     (lon + deg_offset, lat - deg_offset), # SE
                     (lon, lat - deg_offset),              # S
                     (lon - deg_offset, lat - deg_offset), # SW 
                     (lon - deg_offset, lat),              # W
                     (lon - deg_offset, lat + deg_offset)] # NW
    
        return neighbors

    def reduce_region(self, image, reducer, geometry, scale):
        reduced = image.reduceRegion(**{
            'reducer': reducer,
            'geometry': geometry,
            'scale': scale
        })
    
        return reduced
    
    # VERTICAL FILTER CALCULATIONS
    # vegetation percentage change
    def calculate_percentage_change(self,feature):
        g = feature.geometry()

        composite_ls = self.ls5 \
                .filter(ee.Filter.bounds(g)) \
                .filter(ee.Filter.date('1985-01-01', '1990-12-31')) \
                .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
                .map(self.mask_ls5_clouds) \
                .select('SR_B.*') \
                .median() \
                .clip(g)

        composite_s2 = self.s2 \
                .filter(ee.Filter.bounds(g)) \
                .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                .map(self.mask_s2_clouds) \
                .select('B.*') \
                .median() \
                .clip(g)

        left_classified = composite_ls.classify(self.classifier_ls)
        right_classified = composite_s2.classify(self.classifier_s2)

        # Reclassify from 0-1 to 1-2
        left_classes = left_classified.remap([0, 1], [1, 2])
        right_classes = right_classified.remap([0, 1], [1, 2])

        initial_vegetation = left_classes.eq(2)
        bare = right_classes.eq(1)
        vegetation_to_bare = initial_vegetation.And(bare)

        area_image = vegetation_to_bare.multiply(ee.Image.pixelArea())
        area = self.reduce_region(area_image, ee.Reducer.sum(), g, 100)
        area_vegetation_to_bare = ee.Number(area.get('remapped')).divide(1e6)

        area_initial_vegetation = left_classified.eq(1).multiply(ee.Image.pixelArea())
        area2 = self.reduce_region(area_initial_vegetation, ee.Reducer.sum(), g, 100)
        area_initial_vegetation = ee.Number(area2.get('classification')).divide(1e6)

        percent_loss = area_vegetation_to_bare.divide(area_initial_vegetation).multiply(100)

        # account for loss of vegetation from before 1985
        #area of image
        total_area = g.area()
        total_SqKm = ee.Number(total_area).divide(1e6)
        #area of bare earth 2021
        bare_image = bare.multiply(ee.Image.pixelArea())
        area3 = self.reduce_region(bare_image, ee.Reducer.sum(), g, 100)
        area_bare = ee.Number(area3.get('remapped')).divide(1e6)

        percent_bare = area_bare.divide(total_SqKm).multiply(100)

        return feature.set('percent loss',  percent_loss).set('percent bare', percent_bare)

    # sar
    def calculate_sar_vh(self,feature):
        g = feature.geometry()

        # Images and Bands
        filtered = self.s1 \
                .filter(ee.Filter.eq('instrumentMode','IW')) \
                .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')) \
                .filter(ee.Filter.eq('resolution_meters',10)) \
                .filter(ee.Filter.intersects('.geo', g)) \
                .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
                .select('VH')

        composite = filtered.median().clip(g)

        #area of image
        total_area = g.area()
        total_SqKm = ee.Number(total_area).divide(1e6)

        #area of possible mines
        area_mines = composite.lt(-19).rename('mines')
        area_mines = area_mines.multiply(ee.Image.pixelArea())

        area = self.reduce_region(area_mines, ee.Reducer.sum(), g, 30)
    
        mines_SqKm = ee.Number(area.get('mines')).divide(1e6)

        percent_mine = ee.Number(mines_SqKm.divide(total_SqKm).multiply(100))

        return feature.set('vh_percent', percent_mine)

    # nir/g
    def get_s2_bands_and_indices(self,feature):
        g = feature.geometry()

        # Images and Bands
        composite_s2 = self.s2 \
                .filter(ee.Filter.bounds(g)) \
                .filter(ee.Filter.date('2021-01-01', '2021-12-31')) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                .map(self.mask_s2_clouds) \
                .select('B.*') \
                .median() \
                .clip(g)

        nir_g = composite_s2.normalizedDifference(['B8', 'B3']).rename('NIR/G')
        swir1_b = composite_s2.normalizedDifference(['B11', 'B2']).rename('SWIR1/B')
        b5 = composite_s2.select('B5').rename('B5')
        b6 = composite_s2.select('B6').rename('B6')
        ndmi = composite_s2.normalizedDifference(['B8', 'B11']).rename('NDMI') # moisture

        # Average Values   
        stats_nir_g = self.reduce_region(nir_g, ee.Reducer.mean(), g, 30)
        stats_swir1_b = self.reduce_region(swir1_b, ee.Reducer.mean(), g, 30)
        stats_b5 = self.reduce_region(b5, ee.Reducer.mean(), g, 30)
        stats_b6 = self.reduce_region(b6, ee.Reducer.mean(), g, 30)
        stats_ndmi = self.reduce_region(ndmi, ee.Reducer.mean(), g, 30)
        
        avg_nir_g = ee.Number(stats_nir_g.get('NIR/G'))
        avg_swir1_b = ee.Number(stats_swir1_b.get('SWIR1/B'))
        avg_b5 = ee.Number(stats_b5.get('B5'))
        avg_b6 = ee.Number(stats_b6.get('B6'))
        avg_ndmi = ee.Number(stats_ndmi.get('NDMI'))
        
        return feature.set('NIR/G', avg_nir_g).set('SWIR1/B', avg_swir1_b).set('B5', avg_b5).set('B6', avg_b6).set('NDMI', avg_ndmi)

    def get_NASADEM(self,feature):
        """
            Here we use the more modern NASA DEM that merges SRTM with IceSAT, ASTER and PRISM data 
            We will call it: NASADEM in the output .csv file.
        """
        g = feature.geometry()
        srtm = ee.Image('NASA/NASADEM_HGT/001').select('elevation')
        red_srtm = self.reduce_region(srtm, ee.Reducer.mean(), g, 30)
        mean = ee.Number(red_srtm.get('elevation'))
        mean = ee.Algorithms.If(mean, mean, -999) # null values replaced with -999
        return feature.set('elevation',mean)

    def calc_gedi_loss(self,feature):
        """
            Here we will get the GEDI highest elevation score and 
            subtract the NASA SRTM DEM (not the updated one from NASA).
            Hence, elevation loss with time will be negative (new - old < 0) == potential mine
            I commented out a few extra bands from the GEDI collection that may be useful
            such as landsat water, time of collection, non-veg from modis etc. 
        """
        g = feature.geometry()

        gedi_coll = ee.ImageCollection("LARSE/GEDI/GEDI02_A_002_MONTHLY")\
                          .filter(ee.Filter.bounds(g))\
        .select('elev_highestreturn','digital_elevation_model','digital_elevation_model_srtm','quality_flag').median().clip(g)

        x = gedi_coll
        srtm = x.select('digital_elevation_model_srtm')
        gedi = x.select('elev_highestreturn')
        quality = x.select('quality_flag')
        loss = gedi.subtract(srtm).rename('loss')

        # Averaging Loss
        avg_loss = self.reduce_region(loss, ee.Reducer.mean(), g, 30)
        loss = ee.Number(avg_loss.get('loss'))
        loss = ee.Algorithms.If(loss, loss, -999) # null values replaced with -999

        # Averaging GEDI
        avg_gedi = self.reduce_region(gedi, ee.Reducer.mean(), g, 30)
        gedi_mean = ee.Number(avg_gedi.get('elev_highestreturn'))
        gedi_mean = ee.Algorithms.If(gedi_mean, gedi_mean, -999) # null values replaced with -999

        # Averaging GEDI Quality Flag
        avg_qual = self.reduce_region(quality, ee.Reducer.mean(), g, 30)
        qual = ee.Number(avg_qual.get('quality_flag'))
        qual = ee.Algorithms.If(qual, qual, -999) # null values replaced with -999

        return feature.set('loss',loss).set('GEDI',gedi_mean).set('quality flag',qual)

    def check_failures(self):
        # remove all slurm files with no exceptions
        os.system("find | grep -l -L -E exception "+str(self.outputdir)+"/slurm* | xargs rm -f")
        # create a txt file containing job numbers of all failed jobs
        # and while there exist failed cases, re-submit the job
        keep_running=False
        if os.system("grep exception "+str(self.outputdir)+"/slurm* > failed.txt") == 0:
            keep_running = True
            with open('failed.txt') as file:
                for line in file:
                    # read output of failed job
                    with open(os.path.join(self.outputdir,line)) as f: 
                        data=f.readlines
                    for i in range(len(data)):
                        if data[i][0:6] == 'input=':
                            commands = data[i].split(' ')
                            lon_min = commands[1]
                            lat_min = commands[2]
                            lon_max = commands[3]
                            lat_max = commands[4]

                            count = int(commands[5])
                            pixres = np.float64(commands[6])

                            system = commands[7]
                            username = commands[8]
                            jobname = commands[9]
                            wd = commands[10]
                            outputdir = commands[11]
                            resultsdir = commands[12]
                            jobdir = commands[13]
                            compiledfilename = commands[14]
                            makefeaturecollection = commands[15]
                            assetid = commands[16]
                            featgeedescription= commands[17]
                            multiple = commands[18]
                            # reduce size of target area if failed
                            target_area = np.float64(commands[19]) * 0.5

                            x = GEE_Mine(system,username,jobname,wd,outputdir,resultsdir,jobdir,\
                                         compiledfilename,assetid,featgeedescription,makefeaturecollection,conda_env_name)


                            x.start_process(lon_min,lat_min,lon_max,lat_max,target_area,multiple,count=count,pixres=pixres)
                        os.system("rm "+os.path.join(self.resultsdir,line))

        return keep_running

    def check_status(self):
        """
        This routine will patiently run until all jobs that have been submitted are complete
        i.e. no more jobs in the queue.
        """
        # get jobs in queue
        qname = 'queue.txt'
        lockname=qname+'.lock'
        lock = filelock.FileLock(lockname)
        with lock.acquire(timeout=60):
            with open(qname, 'w') as f:
                os.system('squeue -u '+str(self.username)+' >'+str(qname))
            # get list of local jobs in queue
            # if empty, then !=0 == False, else if still some running then it successfully ran a grep == 0 == True
            file='number.txt'
            lockname1=file+'.lock'
            lock1 = filelock.FileLock(lockname1)
            with lock1.acquire(timeout=60):
                os.system('grep '+str(self.jobname)+' '+str(qname)+' | wc -l > '+str(file))
                with open(file,'r') as f:
                    data=f.readlines()
                njobs = int(data[0].split('\n')[0])
                print('njobs ',njobs)
                return njobs <= 1 # if >1 jobs, jobs are not finished so return False, else return True
    
    
    def create_large_squares(self):
            """
            This routine will submit jobs to cluster, that run the GEE Step3 routine on a small region
            It divides the bounding region into regions of size*size km, and submits a job for that region 
            """
            # grab the top left coordinate of the bounding box
            coords = ee.List(self.region.coordinates().get(0)).slice(0, -1)
            top = ee.Number(ee.List(coords.get(2)).get(1))
            left = ee.Number(ee.List(coords.get(0)).get(0))
            top_left_point = ee.Geometry.Point([left, top])
    
            # calculate square pixel width and height
            width = int(ee.Geometry.Point(coords.get(0)).distance(ee.Geometry.Point(coords.get(1))).divide(1000 * self.size).getInfo()) 
            # how many squares can fit in the width of the bounding box
            height = int(ee.Geometry.Point(coords.get(1)).distance(ee.Geometry.Point(coords.get(2))).divide(1000 * self.size).getInfo()) 
            # how many squares can fit in the height of the bounding box

            # create a point buffer and use it to find the km distance to lat/lon degree conversion
            buff = top_left_point.buffer(self.size*1000, 0.1) # create the buffer with a max % error of 0.1
            buff_list = ee.List(buff.coordinates().get(0)) 
            buff_length = buff_list.length()
            right_pt = ee.List(buff_list.get(buff_length.multiply(0.75).int().subtract(1)))
            bottom_pt = ee.List(buff_list.get(buff_length.multiply(0.5).int().subtract(1)))
            new_lat = ee.Number(right_pt.get(0)) # given distance east of the top left point
            new_lon = ee.Number(bottom_pt.get(1)) # given distance south of the top left point

            diff_lon = top.subtract(new_lon) # given size converted to degrees
            diff_lat = new_lat.subtract(left)

            count = 0
            multiple=False
            for y in range(height + 1): 
                left = ee.Number(ee.List(coords.get(0)).get(0))
                for x in range(width + 1):
                    new_lat = left.add(diff_lat)
                    new_lon = top.subtract(diff_lon)

                    bash_filename = str(self.jobname)+'_job_' + str(1000000 + count) + '.sh'
                    with open(os.path.join(self.jobdir,bash_filename),'w') as f:
                        f.write('#!/bin/bash'+'\n')
                        f.write('#SBATCH --nodes=1'+'\n')
                        f.write('#SBATCH --time=02:00:00'+'\n')
                        f.write('#SBATCH --job-name='+str(self.jobname)+'_job'+'\n')
                        f.write('#SBATCH --partition=short'+'\n')
                        f.write('#SBATCH --mem=16GB'+'\n')
                        f.write('#SBATCH --output='+str(self.outputdir)+'/slurm-%j.out'+'\n')
                        f.write('module load anaconda3/3.7'+'\n')
                        f.write('source activate '+'\n')
                        f.write('source activate '+str(self.conda_env_name)+'\n')
                        f.write('conda activate '+str(self.conda_env_name)+'\n')
                        f.write('conda init bash'+'\n')
                        f.write('python3 GEE_Module.py ' + str(left.getInfo()) + ' ' +\
                                str(new_lon.getInfo()) + ' ' + \
                                str(new_lat.getInfo()) + ' ' + str(top.getInfo()) + ' ' +\
                                str(count) +' '+str(self.pixres)+' '+\
                                str(self.system)+' '+str(self.username)+' '+str(self.jobname)+' '+\
                                str(self.wd)+' '+\
                                str(os.path.basename(self.outputdir))+' '+str(os.path.basename(self.resultsdir))+' '+str(os.path.basename(self.jobdir))+' '+\
                                str(os.path.basename(self.compiledfilename)).split('.csv')[0]+' '+str(self.makefeaturecollection)+' '+\
                                str(self.assetid)+' '+str(self.featgeedescription)+' '+\
                                str(multiple)+' '+str(self.size)+' '+str(self.conda_env_name)+'\n')

                    os.system("sbatch "+str(os.path.join(self.jobdir,bash_filename)))
                    # wait 5 seconds to give adequate time spacing between jobs
                    time.sleep(5)

                    count += 1
                    left = new_lat
                top = new_lon
            return

 
# here we will run the individual jobs that HPC will execute
if __name__ == '__main__':
    lon_min = sys.argv[1]
    lat_min = sys.argv[2]
    lon_max = sys.argv[3]
    lat_max = sys.argv[4]
    
    count = int(sys.argv[5])
    pixres = np.float64(sys.argv[6])
    
    system = sys.argv[7]
    username = sys.argv[8]
    jobname = sys.argv[9]
    wd = sys.argv[10]
    outputdir = sys.argv[11]
    resultsdir = sys.argv[12]
    jobdir = sys.argv[13]
    compiledfilename = sys.argv[14]
    makefeaturecollection = sys.argv[15]
    assetid = sys.argv[16]
    featgeedescription= sys.argv[17]
    multiple = sys.argv[18]
    target_area = np.float64(sys.argv[19])
    conda_env_name = sys.argv[20]
        
    x = GEE_Mine(system,username,jobname,wd,outputdir,resultsdir,jobdir,\
                 compiledfilename,assetid,featgeedescription,makefeaturecollection,conda_env_name)
    
    x.start_process(lon_min,lat_min,lon_max,lat_max,target_area,multiple,count=count,pixres=pixres)
