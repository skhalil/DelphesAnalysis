#!/bin/bash

echo "input parameters: cluster, process, run path, input path, out path, sample name" $1 $2 $3 $4 $5 $6 

echo 
CLUSTER=$1
PROCESS=$2
RUNPATH=$3
INPATH=$4
OUTPATH=$5
SAMPLE=$6

echo ""
echo "parameter set:"
echo "CLUSTER: $CLUSTER"
echo "PROCESS: $PROCESS"
echo "RUNPATH: $RUNPATH"
echo "INPATH:  $INPATH"
echo "OUTPATH: $OUTPATH"
echo "SAMPLE:  $SAMPLE"

START_TIME=`/bin/date`
echo "started at $START_TIME"

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $RUNPATH
eval `scramv1 runtime -sh`

cd ${_CONDOR_SCRATCH_DIR}
echo "executing ..."
echo "tar -xvf Delphes333pre16.tar"
tar -xvf Delphes333pre16.tar
echo "ls -lrt"
ls -lrt

echo "cd Delphes"
cd Delphes
echo "cp ../MinBias_100k.pileup ."
echo "cp ../hadronizer.py ."
cp ../MinBias_100k.pileup .
cp ../hadronizer.py .
echo "ls -lrt"
ls -lrt

# loop over all lhe files in interval of 20k events 
# ==================================================

counter=0
max=14
for i in `seq 0 $max`; do
    if test $counter -eq $PROCESS; then
        let "skip=$i*20000"
        echo "cmsRun hadronizer.py skipEvents=$skip outputFile=genout_$PROCESS.root inputFiles="$INPATH""
        cmsRun hadronizer.py skipEvents=$skip outputFile=genout_$PROCESS.root inputFiles="$INPATH" 
        echo "./DelphesCMSFWLite cards/CMS_PhaseII/CMS_PhaseII_Substructure_PIX4022_200PU.tcl treeout_$PROCESS.root genout_$PROCESS.root"
        ./DelphesCMSFWLite cards/CMS_PhaseII/CMS_PhaseII_Substructure_PIX4022_200PU.tcl treeout_$PROCESS.root genout_$PROCESS.root 
        #echo "./DelphesCMSFWLite cards/CMS_PhaseII/CMS_PhaseII_Substructure_PIX4022_200PU.tcl treeout_$PROCESS.root root://cmseos.fnal.gov/$OUTPATH/$SAMPLE/gen/genout_$PROCESS.root"
        #./DelphesCMSFWLite cards/CMS_PhaseII/CMS_PhaseII_Substructure_PIX4022_200PU.tcl treeout_$PROCESS.root root://cmseos.fnal.gov/$OUTPATH/$SAMPLE/gen/genout_$PROCESS.root
        
    fi
    let "counter+=1"   
done

# copy the output root files and clean your mess:
# ===============================================
ls -lrt

echo "xrdcp genout*.root root://cmseos.fnal.gov/$OUTPATH/$SAMPLE/gen/"
xrdcp genout*.root root://cmseos.fnal.gov/$OUTPATH/$SAMPLE/gen/
echo "xrdcp treeout*.root root://cmseos.fnal.gov/$OUTPATH/$SAMPLE/tree/"
xrdcp treeout*.root root://cmseos.fnal.gov/$OUTPATH/$SAMPLE/tree/
rm *.root
rm *.py
cd ../
rm Delphes333pre16.tar
rm -rf Delphes

rm -rf $SAMPLE

ls

exitcode=$?

echo ""
END_TIME=`/bin/date`
echo "finished at ${END_TIME}"
exit $exitcode
