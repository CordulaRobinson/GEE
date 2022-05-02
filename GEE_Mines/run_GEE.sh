#!bin/bash
# The GEE Code expects a couple of input variables from us to begin
source activate
source activate gee
conda activate gee
conda init bash

lon_min='25.505'
lat_min='3.0'
lon_max='25.51'
lat_max='3.005'
# count means nothing 
count='0'
# desired pixel resolution in km
pixres='0.7'
# system will be 'Cluster' or 'cloud'. Right now, cluster is the only option
system='Cluster'
# username for job tracking
username='e.conway'
# name of submitted jobs
jobname='routine'
# working directory
wd='/scratch/e.conway/GEDI/GEE_Gedi/GEE_Modularize'
# output directory
outputdir='outputs'
# results directory
resultsdir='results'
# job output directory
jobdir='batch'
# compiled file name
compiledfilename='compiled'
# do we make a feature collection once done: string
makefeaturecollection='False'
# asset ID if making a feature collection 
assetid='users/econway/FinalResults'
# description of feature 
featgeedescription='compiled_results'
# Multiple = True will run mutliple jobs in your region,
# Else False will just run one job in your region, possibly at high res
multiple='True'
# max target area (kmxkm)per job. Not used if multiple = False as it is used in the creation of multiple jobs
targetarea='1.1'
# name of conda environment
conda_env_name='gee'

python3 GEE_Module.py $lon_min $lat_min $lon_max $lat_max $count $pixres $system $username $jobname $wd $outputdir $resultsdir $jobdir $compiledfilename $makefeaturecollection $assetid $featgeedescription $multiple $targetarea $conda_env_name
