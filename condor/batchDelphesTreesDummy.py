universe = vanilla
Executable = condor_delphes_tree.sh
x509userproxy = $ENV(X509_USER_PROXY)
Requirements = OpSys == "LINUX" && (Arch != "DUMMY" ) 
transfer_input_files = hadronizer.py, Delphes333pre16.tar, MinBias_100k.pileup
should_transfer_files = YES
WhenTOTransferOutput  = ON_EXIT
request_memory = 2100
request_disk = 10000000 
notification = never
inPath = INDIR
runPath = RUNPATH
sample = SAMPLE
outPath = OUTDIR
myLogFolder = LOGDIR
Output = $(runPath)/$(myLogFolder)/batch_$(cluster)_$(process).stdout
Error  = $(runPath)/$(myLogFolder)/batch_$(cluster)_$(process).stderr
Log    = $(runPath)/$(myLogFolder)/batch_$(cluster)_$(process).condor
Arguments = $(cluster) $(process) $(runPath) $(inPath) $(outPath) $(sample)
Queue 15
