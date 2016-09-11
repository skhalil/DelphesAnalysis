# Frame work for Delphes analysis #

## CMS environment

    cmsrel CMSSW_8_0_4
    cd CMSSW_8_0_4/src
    cmsenv

## installing delphes

    git clone https://github.com/delphes/delphes
    cd delphes
    git checkout tags/3.3.3pre11
    ./configure
    make -j 4
    cd ..

## checkout analysis framework

    git clone https://github.com/skhalil/DelphesAnalysis.git DelphesAnalysis

## test run

    root -l DelphesAnalysis/RunAnalyzer.C'("root://cmseos.fnal.gov//store/user/skhalil/DelphesGenVLQ/WbT_leftHanded_M1_events/tree/treeout_0.root", "signal")'

## to run over full samples using condor

For beginers, see [condor](http://uscms.org/uscms_at_work/physics/computing/setup/batch_systems.shtml")

     cd condor
     ln -s ../RunAnalyzer.C RunAnalyzer.C
     ln -s ../DelphesVLQAnalaysis.C DelphesVLQAnalaysis.C
     ln -s ../DelphesVLQAnalaysis.h DelphesVLQAnalaysis.h
     ln -s ../../delphes delphes
     cd ../../
     tar -zcvf delphes.tar.gz delphes/
     mv delphes.tar.gz DelphesAnalysis/condor/
     cd DelphesAnalysis/condor/
     python batchMaker.py

More details can be found in condor/ReadMeCondor.txt file.

## Plotting scripts

The plotting scripts are in directory `<DelphesAnalysis/macro>`. The main script is `<plot.py>` designed to plot one histogram at a time. All other histograms can be produced by running the script `<runVar.py>`, which has features to control the parameters of `<plot.py>`

     python runVar.py
              