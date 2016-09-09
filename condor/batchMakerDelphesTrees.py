#!/usr/bin/python

##################################################################################
# Reads the input lhe files stored in eos
# Split the files into desired number of jobs and writes the corresponding .cmnd files.
# Write the condor batch (.jdl) files 
# Usage: python batchMakerDelphesTrees.py
##################################################################################

import sys, math, itertools, os, re, subprocess
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--inputPath', metavar='F', type='string', action='store',
                  default = 'file:/uscms_data/d3/easmith/DelphesThings/LHEFiles',
                  dest='inputPath',
                  help='Input path for the lhe files')

parser.add_option('--scriptPath', metavar='P', type='string', action='store',
                  default = '/uscms_data/d2/skhalil/Delphes2/CMSSW_8_0_4/src/DelphesAnalysis/condor',
                  dest='scriptPath',
                  help='Input path for the scripts')

parser.add_option('--outputPath', metavar='F', type='string', action='store',
                  default = '/store/user/skhalil/DelphesGenVLQ',
                  dest='outputPath',
                  help='output directory holding the final root files')

# Parse and get arguments
(options, args) = parser.parse_args()
inDir = options.inputPath
outDir = options.outputPath
scriptPath = options.scriptPath
toMake = [#{'name':'WbT_leftHanded_M1_events'},
          #{'name':'WbT_leftHanded_M1.5_events'},
          #{'name':'WbT_leftHanded_M2_events'},
          #{'name':'WbT_leftHanded_M2.5_events'},
          #{'name':'WbT_leftHanded_M3_events'},
          {'name':'ZtT_rightHanded_M1_events'},
          {'name':'ZtT_rightHanded_M1.5_events'},
          {'name':'ZtT_rightHanded_M2_events'},
          {'name':'ZtT_rightHanded_M2.5_events'},
          {'name':'ZtT_rightHanded_M3_events'},
          ]

for s in toMake:
    inputFile = open('batchDelphesTreesDummy.py')
    outputFile = open('batch_'+str(s['name'])+'.jdl', 'w')
    condorLogDir = 'log/condorLog_'+s['name']
    
    if not os.path.isdir(condorLogDir):
        os.makedirs('log/condorLog_'+s['name']+'/')

    for line in inputFile:
        line = line.replace('RUNPATH', scriptPath )  
        line = line.replace('SAMPLE', s['name']) 
        line = line.replace('INDIR', inDir+'/'+s['name']+'.lhe') 
        line = line.replace('OUTDIR',outDir)
        line = line.replace('LOGDIR', condorLogDir)
        outputFile.writelines(line)
    inputFile.close()
    outputFile.close()

    # create the output directories where you like to store the output histograms in /eos directory
    subprocess.call( ['eos root://cmseos.fnal.gov mkdir -p /eos/uscms/store/user/skhalil/DelphesGenVLQ/'+str(s['name'])+'/gen'], shell=True )
    subprocess.call( ['eos root://cmseos.fnal.gov mkdir -p /eos/uscms/store/user/skhalil/DelphesGenVLQ/'+str(s['name'])+'/tree'], shell=True ) 
    subprocess.call( ['condor_submit batch_'+str(s['name'])+'.jdl'], shell=True )



