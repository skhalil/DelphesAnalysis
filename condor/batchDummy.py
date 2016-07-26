universe = vanilla
Executable = SCRIPT
x509userproxy = /tmp/x509up_u44569
Requirements = (Memory >= 499 && OpSys == "LINUX" && (Arch != "DUMMY" ))
transfer_input_files = ANALYZER
should_transfer_files = YES
WhenTOTransferOutput  = ON_EXIT
request_disk = 10000000
request_memory = 2100

notification = never
myPath = PATH
myLogFolder = LOGDIR
Output = $(myPath)/$(myLogFolder)/batch_$(cluster)_$(process).stdout
Error  = $(myPath)/$(myLogFolder)/batch_$(cluster)_$(process).stderr
Log    = $(myPath)/$(myLogFolder)/batch_$(cluster)_$(process).condor
inPath = INPATH
Arguments = $(cluster) $(process) $(myPath) $(inPath)
notify_user = skhalil@FNAL.GOV
Queue NJOBS
