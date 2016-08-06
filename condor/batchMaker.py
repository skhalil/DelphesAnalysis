#!/usr/bin/python

##################################################################################
# Reads the input root files stored in eos
# Split the files into desired number of jobs and writes them to text files
# Write the condor batch (.jdl) files 
# Usage: python batchMaker.py
##################################################################################

import sys, math, itertools, os, re, subprocess
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--inputPath', metavar='F', type='string', action='store',
                  default = '/eos/uscms/store/user/snowmass/DelphesFromLHE_2016June',
                  dest='inputPath',
                  help='Input path for the datasets')

parser.add_option('--outTextDir', metavar='F', type='string', action='store',
                  default = '/uscms_data/d2/skhalil/Delphes2/CMSSW_8_0_4/src/DelphesAnalysis/FileLists',
                  dest='outTextDir',
                  help='output directory containing lists input txt file')

parser.add_option('--outRootDir', metavar='F', type='string', action='store',
                  default = '/store/user/skhalil/DelphesHists',
                  dest='outRootDir',
                  help='output directory holding the final root files')

parser.add_option('--scriptPath', metavar='P', type='string', action='store',
                  default = '/uscms_data/d2/skhalil/Delphes2/CMSSW_8_0_4/src/DelphesAnalysis/condor',
                  dest='scriptPath',
                  help='Input path for the scripts')

parser.add_option('--delphesTag', metavar='T', type='string', action='store',
                  default = "v1510_14TEV_200PU",
                  dest='delphesTag',
                  help='default delphes tag in production')

# Parse and get arguments
(options, args) = parser.parse_args()

def makeFilenameList(inputDir):
    if not os.path.isdir(inputDir):
        print ('%s is not a directory'%(inputDir))
        sys.exit(1)

    filenamelist = []
    for filename in os.listdir(inputDir):
        if not os.path.isfile(os.path.join(inputDir,filename)):
            continue
        filenamelist.append(filename)

    return filenamelist


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
scriptPath = options.scriptPath
tag = options.delphesTag
inputPath = options.inputPath
outTextDir = options.outTextDir
outRootDir = options.outRootDir
#print 'scriptPath: ', scriptPath, ',tag: ', tag, ', inputPath: ', inputPath, ', outTextDir: ', outTextDir, ', outRootDir: ', outRootDir  
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

toMake = [{'name':'tt-4p-0-600',       'jobs': 10},
          {'name':'tt-4p-600-1100',    'jobs': 10},
          {'name':'tt-4p-1100-1700',   'jobs': 10},
          {'name':'tt-4p-1700-2500',   'jobs': 10},
          {'name':'tt-4p-2500-100000', 'jobs': 10}, 
          {'name':'tj-4p-0-500',       'jobs': 10},
          {'name':'tj-4p-500-1000',    'jobs': 10},
          {'name':'tj-4p-1000-1600',   'jobs': 10},
          {'name':'tj-4p-1600-2400',   'jobs': 10},
          {'name':'tj-4p-2400-100000', 'jobs': 10},
          {'name': 'Bj-4p-0-300',      'jobs': 15}, 
          {'name': 'Bj-4p-300-600',    'jobs': 15},
          {'name': 'Bj-4p-600-1100',   'jobs': 15},
          {'name': 'Bj-4p-1100-1800',  'jobs': 15},
          {'name': 'Bj-4p-1800-2700',  'jobs': 15},
          {'name': 'Bj-4p-2700-3700',  'jobs': 15},
          {'name': 'Bj-4p-3700-100000', 'jobs': 15}, 
          {'name':'BB-4p-0-300',       'jobs': 10},
          {'name':'BB-4p-300-700',     'jobs': 10},
          {'name':'BB-4p-700-1300',    'jobs': 10},
          #{'name':'BB-4p-1300-2100',   'jobs': 10}, #found this one missing
          {'name':'BB-4p-2100-100000', 'jobs': 10},
  
          ]

for s in toMake:
    
    outDir = outTextDir+'/'+s['name']
    if not os.path.isdir(outDir):
        subprocess.call( ['mkdir '+outDir], shell=True )
    maxJobs = s['jobs']
    
    #list all root files in the input directory and decide on number of jobs you wish to split the files
    inputDir = (inputPath+'/'+s['name']+'-'+tag).rstrip('/')+'/'
    filenamelist = makeFilenameList(inputDir)
    numInputFiles  = sum(1 for line in filenamelist)        
    inputsPerJob = math.ceil(numInputFiles / maxJobs)
        
    # now split them into several files
    for job in range(0, maxJobs):
        lines = []
        for line in itertools.islice(filenamelist, job * inputsPerJob, (job + 1) * inputsPerJob):
            lines.append(line.strip())
               
        if lines:
            with open(outDir+'/'+s['name']+'_200PU'+'_'+str(job)+'.txt', 'w') as output_:
                for line in lines:
                    preprend = 'root://cmseos.fnal.gov//'+inputDir.split('/',3)[3]
                    output_.write(preprend+'/'+line+'\n') 
            output_.close() 
            
         
    inputFile = open('batchDummy.py')
    outputFile = open('batch_'+str(s['name'])+'.jdl', 'w')
    condorLogDir = 'condorLog_'+s['name']
    if not os.path.isdir(condorLogDir):
        subprocess.call( ['mkdir '+condorLogDir], shell=True )
   
    for line in inputFile:
        line = line.replace('RUNPATH', scriptPath )
        line = line.replace('NJOBS',  str(s['jobs']))
        line = line.replace('SAMPLE', s['name'])
        line = line.replace('INTEXTDIR', outDir)
        line = line.replace('LOGDIR', condorLogDir)
        line = line.replace('OUTPUTDIR',outRootDir)
        #print line
        outputFile.writelines(line)
    inputFile.close()
    outputFile.close()
    
    # create the output directories where you like to store the output histograms in /eos directory
    subprocess.call( ['eos root://cmseos.fnal.gov mkdir -p /eos/uscms/store/user/skhalil/DelphesHists/'+str(s['name'])], shell=True )
    
