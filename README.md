# Frame work for Delphes analysis #

## CMS environment

<cmsrel CMSSW_8_0_4>
<cd CMSSW_8_0_4/src>
<cmsenv>

## installing delphes

<git clone https://github.com/delphes/delphes> 
<cd delphes>
<git checkout tags/3.3.3pre11>
<./configure>
<make -j 4>
<cd ..>

## checkout analysis framework

git clone https://github.com/skhalil/DelphesAnalysis.git DelphesAnalysis

## test run

`<cd DelphesAnalysis>`
`<root -l DelphesAnalysis/RunAnalyzer.C'("FileLists/tt-4p-0-600_200PU_1.txt")'>`

## to run over full samples using condor

For beginers, see [condor](http://uscms.org/uscms_at_work/physics/computing/setup/batch_systems.shtml")

<cd condor>
<ln -s ../RunAnalyzer.C RunAnalyzer.C>
<ln -s ../DelphesVLQAnalaysis.C DelphesVLQAnalaysis.C>
<ln -s ../DelphesVLQAnalaysis.h DelphesVLQAnalaysis.h>
<ln -s ../../delphes delphes>
<tar -czf delphes.tar delphes>
<python batchMaker.py>

More details can be found in condor/ReadMeCondor.txt file.

