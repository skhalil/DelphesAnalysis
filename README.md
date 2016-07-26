Frame work for Delphes analysis

# CMS environment
cmsrel CMSSW_8_0_4
cd CMSSW_8_0_4/src
cmsenv

# installing delphes
git clone https://github.com/delphes/delphes 
cd delphes
git checkout tags/3.3.3pre11
./configure
make -j 4
cd ..

# checkout analysis framework
git clone https://github.com/skhalil/DelphesAnalysis.git DelphesAnalysis
