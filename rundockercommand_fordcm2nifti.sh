# docker build -t sharmaatul11/yashengcsfinfarctseg1 .
# docker push  sharmaatul11/yashengcsfinfarctseg1 
# docker run -v $PWD/workinginput:/workinginput -v $PWD/workingoutput:/workingoutput -v $PWD/ZIPFILEDIR:/ZIPFILEDIR -v$PWD/output:/output  -it sharmaatul11/yashengcsfinfarctseg1  /Stroke_CT_Processing/call_preproc_segm_session_level_1.sh SNIPR_E03523 
# docker build -t sharmaatul11/dicom2nifti_nwu_1 .
./builddockerimage.sh
# directorytocreate=(output ZIPFILEDIR NIFTIFILEDIR DICOMFILEDIR working input ) 
mkdir working
mkdir input
mkdir ZIPFILEDIR
mkdir output
mkdir NIFTIFILEDIR
mkdir DICOMFILEDIR
sessionID=SNIPR_E03614 #SNIPR_E03516
#docker run -v $PWD/NIFTIFILEDIR:/NIFTIFILEDIR  -v $PWD/DICOMFILEDIR:/DICOMFILEDIR  -v $PWD/working:/working -v $PWD/input:/input -v $PWD/ZIPFILEDIR:/ZIPFILEDIR -v $PWD/output:/output  -it sharmaatul11/dicom2nifti_nwu_1   /software/dicom2nifti_call_sessionlevel_selected.sh ${sessionID} $XNAT_USER $XNAT_PASS $XNAT_HOST #https://snipr-dev-test1.nrg.wustl.edu