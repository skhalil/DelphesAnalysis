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
echo "tar -xzf delphes.tar"
tar -xzf delphes.tar
echo "ls -lrt"
ls -lrt

######################################################
# assuming INPATH directory name is same as $SAMPLE,
# loop over all the .txt files inside the directory,
# and run the root macro
######################################################
count = 0
for txt in `ls $SAMPLE`; do
    echo "going here: "$txt
    if test -f $SAMPLE/$txt; then
        echo "file   $SAMPLE/$txt   exists"
        name=`basename $txt .txt`
        echo "output file name: $name "
        if test $count -eq $PROCESS; then
            echo "${name}"
            echo "root -b -q -l RunAnalyzer.C'($SAMPLE/$txt)"
            root -b -q -l RunAnalyzer.C'("$SAMPLE/$txt")'
        fi
        let "count+=1"
    fi
done

echo "*.root root://cmseos.fnal.gov/$OUTPUT/$SAMPLE"
xrdcp *.root root://cmseos.fnal.gov/$OUTPUT/$SAMPLE
echo "rm *.root" 
rm *.root
rm *.C
rm delphes.tgz
rm -rf delphes

ls

exitcode=$?

echo ""
END_TIME=`/bin/date`
echo "finished at ${END_TIME}"
exit $exitcode
