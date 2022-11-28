#!/bin/bash 

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
TYPE_OF_PROGRAM=${4}
echo ${TYPE_OF_PROGRAM}::TYPE_OF_PROGRAM
if [[ ${TYPE_OF_PROGRAM} == 2 ]] ;
then 
    /software/nwucalculation_session_level_allsteps_November14_2022.sh $SESSION_ID $XNAT_USER $XNAT_PASS https://snipr-dev-test1.nrg.wustl.edu /input /output
fi 
if [[ ${TYPE_OF_PROGRAM} == 1 ]] ;
then 
    /software/dicom2nifti_call_sessionlevel_selected.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS https://snipr-dev-test1.nrg.wustl.edu
fi 
