# Introduction to condor batch system

See the follwoing link for a condor review: http://uscms.org/uscms_at_work/physics/computing/setup/batch_systems.shtml

# Structure and job submission

1. To submit the condor jobs, first run the script batchMaker.py that will create several .jdl files corresponding to each dataset and its parameters listed in a dictionary in the script.

python batchMaker.py

2. One can extend the dictionary to the desired datasets and the number of jobs. The script will first create the .txt files corresponding to the desired number of jobs, and will setup the input, output directory paths to the output .jdl files. It will also create output directories that will contain the stdout, stderr, and condor output files for each dataset. These directories are very important for monitoring and debugging.

3. Once the .jdl files are created, submit the condor jobs, e.g;

condor_submit batch_tt-4p-0-600.jdl

4. To check the status

condor_q <USERNAME>

5. After the jobs are done, run the script hadd.py to hadd all the histograms. I
 usually create a new directory to keep the histograms and make a soft link to the script to run it from there:

mkdir Histo_Aug4
cd Histo_Aug4
ln -s ../hadd.py hadd.py
