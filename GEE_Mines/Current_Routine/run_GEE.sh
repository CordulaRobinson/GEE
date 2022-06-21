#!/bin/bash
# The GEE Code expects a couple of input variables from us to begin
lon_min='29'
lat_min='2.5'
lon_max='30'
lat_max='3.5'
# count means nothing 
count='0'
# desired pixel resolution in km
pixres='0.25'
# system will be 'Cluster' or 'cloud'. Right now, cluster is the only option
system='Cluster'
# username for job tracking
username='eah.r'
# name of submitted jobs
jobname='routine'
# working directory
wd='/scratch/eah.r/gee_new/GEE_Mines/GEE_Modularize'
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
assetid='users/raymondeah/FinalResults'
# description of feature 
featgeedescription='compiled_results'
# Multiple = True will run mutliple jobs in your region,
# Else False will just run one job in your region, possibly at high res
multiple='True'
# max target area (kmxkm)per job. Not used if multiple = False as it is used in the creation of multiple jobs
targetarea='10'
# name of conda environment
conda_env_name='ee'

source activate
source activate $conda_env_name
conda activate $conda_env_name
conda init bash

python3 GEE_Module.py $lon_min $lat_min $lon_max $lat_max $count $pixres $system $username $jobname $wd $outputdir $resultsdir $jobdir $compiledfilename $makefeaturecollection $assetid $featgeedescription $multiple $targetarea $conda_env_name
