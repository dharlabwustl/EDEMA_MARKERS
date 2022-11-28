#!/bin/bash
cd /software/
git clone https://github.com/dharlabwustl/dcm2niftiwithedemabiomarkers.git
mv dcm2niftiwithedemabiomarkers/* /software/ 
chmod +x /software/*.sh 

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
TYPE_OF_PROGRAM=${5}

/software/script_to_call_main_program.sh $SESSION_ID $XNAT_USER $XNAT_PASS ${TYPE_OF_PROGRAM}