FROM sharmaatul11/fsl502py369ltx:latest
RUN apt update
COPY scct_strippedResampled1.nii.gz   /templatenifti/
COPY  midlinecssfResampled1.nii.gz   /templatemasks/
RUN mkdir -p /callfromgithub
RUN chmod 755 /callfromgithub
COPY downloadcodefromgithub.sh /callfromgithub/
RUN chmod +x /callfromgithub/downloadcodefromgithub.sh
RUN apt install -y \
  dcm2niix  \ 
  vim  \ 
  zip  \ 
  unzip  \ 
  curl  \ 
  git \
  tree  
RUN pip install \
  nibabel  \ 
  numpy  \ 
  xmltodict  \ 
  pandas  \ 
  requests  \ 
  pydicom  \ 
  python-gdcm  \ 
  glob2  \ 
  scipy  \ 
  pypng  \
  PyGithub 
LABEL org.nrg.commands="[{\"name\": \"edema_biomarkers_allstepsSessionUsingGitHub\", \"description\": \"Apply edema_biomarkers_allstepsSessionUsingGitHub\", \"version\": \"1.0\", \"schema-version\": \"1.0\", \"image\": \"sharmaatul11/dicom2nifti_nwu_1:latest\", \"type\": \"docker\", \"working-directory\": \"/callfromgithub\", \"command-line\": \" /callfromgithub/downloadcodefromgithub.sh #SESSION_ID# \$XNAT_USER \$XNAT_PASS  https://snipr-dev-test1.nrg.wustl.edu 2 /input /output \", \"override-entrypoint\": true, \"mounts\": [{\"name\": \"out\", \"writable\": true, \"path\": \"/output\"}, {\"name\": \"in\", \"writable\": false, \"path\": \"/input\"}, {\"name\": \"ZIPFILEDIR\", \"writable\": true, \"path\": \"/ZIPFILEDIR\"}, {\"name\": \"software\", \"writable\": true, \"path\": \"/software\"}, {\"name\": \"NIFTIFILEDIR\", \"writable\": true, \"path\": \"/NIFTIFILEDIR\"}, {\"name\": \"DICOMFILEDIR\", \"writable\": true, \"path\": \"/DICOMFILEDIR\"}, {\"name\": \"working\", \"writable\": true, \"path\": \"/working\"}, {\"name\": \"workinginput\", \"writable\": true, \"path\": \"/workinginput\"}, {\"name\": \"workingoutput\", \"writable\": true, \"path\": \"/workingoutput\"}, {\"name\": \"outputinsidedocker\", \"writable\": true, \"path\": \"/outputinsidedocker\"}], \"environment-variables\": {}, \"ports\": {}, \"inputs\": [{\"name\": \"SESSION_ID\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null, \"select-values\": [], \"multiple-delimiter\": null}, {\"name\": \"PROJECT\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null, \"select-values\": [], \"multiple-delimiter\": null}], \"outputs\": [], \"xnat\": [{\"name\": \"edema_biomarkers_allstepsSessionUsingGitHub\", \"label\": \"edema_biomarkers_allstepsSessionUsingGitHub batch\", \"description\": \"edema_biomarkers_allstepsSessionUsingGitHub\", \"contexts\": [\"xnat:imageSessionData\"], \"external-inputs\": [{\"name\": \"session\", \"label\": null, \"description\": \"Input session\", \"type\": \"Session\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": null, \"provides-files-for-command-mount\": null, \"via-setup-command\": null, \"user-settable\": null, \"load-children\": false}], \"derived-inputs\": [{\"name\": \"project\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"PROJECT\", \"provides-files-for-command-mount\": null, \"user-settable\": false, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"project-id\", \"via-setup-command\": null, \"multiple\": false, \"parser\": null}, {\"name\": \"session-id\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"SESSION_ID\", \"provides-files-for-command-mount\": null, \"user-settable\": false, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"id\", \"via-setup-command\": null, \"multiple\": false, \"parser\": null}], \"output-handlers\": []}], \"container-labels\": {}, \"generic-resources\": {}, \"ulimits\": {}}]"
