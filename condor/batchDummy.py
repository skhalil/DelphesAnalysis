universe = vanilla
Executable = condor.sh
x509userproxy = $ENV(X509_USER_PROXY)
Requirements = Memory >= 499 && OpSys == "LINUX" && (Arch != "DUMMY" ) && Disk > 10000000 
transfer_input_files = RunAnalyzer.C, DelphesVLQAnalaysis.h, DelphesVLQAnalaysis.C, delphes.tar
should_transfer_files = YES
WhenTOTransferOutput  = ON_EXIT
request_memory = 2100
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
