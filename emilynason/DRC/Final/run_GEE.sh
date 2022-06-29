#!/bin/bash
# The GEE Code expects a couple of input variables from us to begin
lon_min='26.65'
lat_min='-11'
lon_max='27.35'
lat_max='-10.95'
# count means nothing 
count='0'
# desired pixel resolution in km
pixres='0.02'
# system will be 'Cluster' or 'cloud'. Right now, cluster is the only option
system='Cluster'
# username for job tracking
username='nason.e'
# name of submitted jobs
jobname='routine'
# working directory
wd='/scratch/nason.e/gee/GEE/newRoutine'
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
assetid='users/EmilyNason/NativeRes_Eamon_newregion'
# description of feature 
featgeedescription='compiled_results'
# Multiple = True will run mutliple jobs in your region,
# Else False will just run one job in your region, possibly at high res
multiple='True'
# max target area (kmxkm)per job. Not used if multiple = False as it is used in the creation of multiple jobs
targetarea='1'
# name of conda environment
conda_env_name='newEnv'

source activate
source activate $conda_env_name
conda activate $conda_env_name
conda init bash

python3 GEE_Module.py $lon_min $lat_min $lon_max $lat_max $count $pixres $system $username $jobname $wd $outputdir $resultsdir $jobdir $compiledfilename $makefeaturecollection $assetid $featgeedescription $multiple $targetarea $conda_env_name