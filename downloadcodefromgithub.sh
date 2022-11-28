#!/bin/bash
cd /software/
git clone https://github.com/dharlabwustl/EDEMA_MARKERS.git
mv EDEMA_MARKERS/* /software/
chmod +x /software/*.sh 

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
TYPE_OF_PROGRAM=${5}

/software/script_to_call_main_program.sh $SESSION_ID $XNAT_USER $XNAT_PASS ${TYPE_OF_PROGRAM}
