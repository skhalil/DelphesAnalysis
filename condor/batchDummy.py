universe = vanilla
Executable = condor.sh
x509userproxy = $ENV(X509_USER_PROXY)
Requirements = OpSys == "LINUX" && (Arch != "DUMMY" ) 
transfer_input_files = RunAnalyzer.C, DelphesVLQAnalaysis.h, DelphesVLQAnalaysis.C, BTagEfficiencyMediumOP.h, delphes.tar.gz
should_transfer_files = YES
WhenTOTransferOutput  = ON_EXIT
request_memory = 2100
request_disk = 10000000 
notification = never
inPath = INTEXTDIR
runPath = RUNPATH
sample = SAMPLE
outPath = OUTPUTDIR
myLogFolder = LOGDIR
Output = $(runPath)/$(myLogFolder)/batch_$(cluster)_$(process).stdout
Error  = $(runPath)/$(myLogFolder)/batch_$(cluster)_$(process).stderr
Log    = $(runPath)/$(myLogFolder)/batch_$(cluster)_$(process).condor
Arguments = $(cluster) $(process) $(runPath) $(inPath) $(outPath) $(sample)
Queue NJOBS
