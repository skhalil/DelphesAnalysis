!/bin/bash

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
echo "SAMPLE:  $SAMPLE"


START_TIME=`/bin/date`
echo "started at $START_TIME"

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $RUNPATH
eval `scramv1 runtime -sh`

cd ${_CONDOR_SCRATCH_DIR}
echo "executing ..."
echo "cp -r $INPATH ."
cp -r $INPATH .
echo "tar -xzvf delphes.tar.gz"
tar -xzvf delphes.tar.gz
echo "ls -lrt"
ls -lrt

# assuming INPATH directory name is same as $SAMPLE,
# loop over all the .txt files inside the directory
# ==================================================

counter=0
for txt in `ls $SAMPLE`; do
    if test -f $SAMPLE/$txt; then        
        name=`basename $txt .txt`
        #echo "output root file name: $name "
        if test $counter -eq $PROCESS; then
            echo "input file  $SAMPLE/$txt  exists"
            echo "output file name ${name}"
            #echo "new name: `$SAMPLE`_${counter}"
            echo "root -b -q -l RunAnalyzer.C'("$SAMPLE/$txt","${name}")' "
            root -b -q -l RunAnalyzer.C'("$SAMPLE/$txt", "${name}")'
            #echo "root -b -q -l RunAnalyzer.C'("$SAMPLE/$txt","$SAMPLE_${counter}")' "
            #root -b -q -l RunAnalyzer.C'("$SAMPLE/$txt", "$SAMPLE_${counter}")'
        fi
        let "counter+=1"
    fi
done

# copy the output root files and clean your mess:
# ===============================================

echo "xrdcp *.root root://cmseos.fnal.gov/$OUTPATH/$SAMPLE"
xrdcp *.root root://cmseos.fnal.gov/$OUTPATH/$SAMPLE
rm *.root
rm *.C
rm *.h
rm delphes.tar.gz
rm -rf delphes
rm -rf $SAMPLE

ls

exitcode=$?

echo ""
END_TIME=`/bin/date`
echo "finished at ${END_TIME}"
exit $exitcode
