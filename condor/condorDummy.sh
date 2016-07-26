!/bin/bash

export X509_USER_PROXY x509up_u44569

echo "Grid Init: " 
ls -l -h x509up_u44569

JOB_NUMBER=$1
WORK_DIR=`pwd`

tar -xzf fileLists.tgz