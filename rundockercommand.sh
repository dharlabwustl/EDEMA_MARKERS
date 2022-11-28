# docker build -t sharmaatul11/yashengcsfinfarctseg1 .
# docker push  sharmaatul11/yashengcsfinfarctseg1 
# docker run -v $PWD/workinginput:/workinginput -v $PWD/workingoutput:/workingoutput -v $PWD/ZIPFILEDIR:/ZIPFILEDIR -v$PWD/output:/output  -it sharmaatul11/yashengcsfinfarctseg1  /Stroke_CT_Processing/call_preproc_segm_session_level_1.sh SNIPR_E03523 
# docker build -t sharmaatul11/dicom2nifti_nwu_1 .
./builddockerimage.sh
mkdir workingoutput
mkdir workinginput
mkdir ZIPFILEDIR
mkdir outputinsidedocker
mkdir software 
sessionID=SNIPR_E03614 #SNIPR_E03516
rm -r workinginput/*
rm -r workingoutput/*
rm -r ZIPFILEDIR/* 
rm -r outputinsidedocker/*
rm -r software/*
# docker run -v $PWD/software:/software -v $PWD/workinginput:/workinginput -v $PWD/workingoutput:/workingoutput -v $PWD/ZIPFILEDIR:/ZIPFILEDIR -v $PWD/outputinsidedocker:/outputinsidedocker  -it sharmaatul11/fsl502py369withpacksnltx  /callfromgithub/downloadcodefromgithub.sh ${sessionID} $XNAT_USER $XNAT_PASS https://snipr-dev-test1.nrg.wustl.edu 2 ##/software/call_combine_all_edemabiomarker_csvfile_projectlevel.sh  #${sessionID} $XNAT_USER $XNAT_PASS $XNAT_HOST #https://snipr-dev-test1.nrg.wustl.edu
