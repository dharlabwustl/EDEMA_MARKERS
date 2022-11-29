#!/usr/bin/env bash
echo 'FROM sharmaatul11/fsl502py369ltx:latest' > Dockerfile
# FROM ubuntu:latest
##sharmaatul11/py310xmltodict:latest 
#ubuntu:latest 
directory_of_software='software'
echo 'RUN apt update' >> Dockerfile
# echo 'RUN mkdir -p /run' >> Dockerfile
# echo 'RUN mkdir -p /ZIPFILEDIR' >> Dockerfile
# echo 'RUN chmod -R 777 /ZIPFILEDIR' >> Dockerfile
# echo 'RUN mkdir -p /NIFTIFILEDIR' >> Dockerfile
# echo 'RUN chmod -R 777 /NIFTIFILEDIR' >> Dockerfile
# cat createdirectories.txt >> Dockerfile
echo "COPY scct_strippedResampled1.nii.gz   /templatenifti/" >> Dockerfile
echo "COPY  midlinecssfResampled1.nii.gz   /templatemasks/" >> Dockerfile
ubuntupackagestoinstall=(dcm2niix vim zip unzip curl tree)
echo ${ubuntupackagestoinstall[0]}
len_array=${#ubuntupackagestoinstall[@]}
last_num=$((len_array -1))
echo $last_num
echo "RUN apt install -y \\" >> Dockerfile 
for x in ${ubuntupackagestoinstall[@]} ; do 
	if [[ $x = ${ubuntupackagestoinstall[last_num]} ]] ; then
		echo "  ${x}  " >> Dockerfile
	else 
		echo "  ${x}  \\ " >> Dockerfile
fi 
done


pipinstall=(nibabel numpy xmltodict pandas requests pydicom python-gdcm glob2 scipy pypng PyGithub)
len_array=${#pipinstall[@]}
last_num=$((pipinstall -1))
echo "RUN pip install \\" >> Dockerfile 
for x in ${pipinstall[@]} ; do 
	if [[ $x = ${pipinstall[last_num]} ]] ; then
		echo "  ${x}  " >> Dockerfile
	else 
		echo "  ${x}  \\ " >> Dockerfile
fi 
done


# copyfiles_sh=(dicom2nifti_call_projectlevel_selected  dicom2nifti_call_scanlevel_selected  dicom2nifti_call_sessionlevel_selected dicom2nifti_call_subjectlevel_selected)
# len_array=${#copyfiles_sh[@]}
# last_num=$((copyfiles_sh -1))
# echo "COPY  \\" >> Dockerfile 
# for x in ${copyfiles_sh[@]} ; do 
 
# 		echo "  ${x}.sh  \\ " >> Dockerfile

# done
# echo "/run/  " >> Dockerfile 
# copyfiles_sh=(dicom2nifti_call_projectlevel_selected  dicom2nifti_call_scanlevel_selected  dicom2nifti_call_sessionlevel_selected dicom2nifti_call_subjectlevel_selected)
# len_array=${#copyfiles_sh[@]}
# last_num=$((copyfiles_sh -1))
echo "COPY  \\" >> Dockerfile 
for x in *.sh; do 
 
		echo "  ${x}  \\ " >> Dockerfile

done
echo "/${directory_of_software}/  " >> Dockerfile 

# copyfiles_py=(dicom2nifiti_projectlevel_selected dicom2nifiti_subjectlevel_selected dicom2nifiti_subjectlevel_selected  dicom2nifiti_alllevels_selected dicom2nifiti_projectlevel_selected dicom2nifiti_sessionlevel_selected dicom2nifiti_scanlevel_selected DecompressDCM dicom2nifiti_sessionlevel xnatSession dicom2nifiti_scanlevel writetowebpagetable label_session_Atul downloadwithrequest label_probability)
# len_array=${#copyfiles_py[@]}
# last_num=$((copyfiles_py -1))
echo "COPY  \\" >> Dockerfile 
for x in *.py ; do 
 
		echo "  ${x}  \\ " >> Dockerfile

done
echo "/${directory_of_software}/  " >> Dockerfile 
# echo "COPY stroke_edema_template.xml /run/" >> Dockerfile

# changemodes_sh=(dicom2nifti_call_projectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_alllevels_selected dicom2nifti_call_projectlevel_selected dicom2nifti_call_sessionlevel_selected dicom2nifti_call_scanlevel_selected dicom2nifti_call_scanlevel writetowebpagetable_call  label_session_call  call_downloadwithrequest )

# len_array=${#changemodes_sh[@]}
# last_num=$((changemodes_sh -1))
echo "RUN  \\" >> Dockerfile 
# for x in ${changemodes_sh[@]} ; do 
counter=0

total_num_sh_files=$(ls -l *.sh | grep ^- | wc -l)
total_num_sh_files=$((total_num_sh_files-1))
for x in *.sh ; do 
	# if [[ $x = ${changemodes_sh[last_num]} ]] ; then
		if [[ $counter -eq ${total_num_sh_files} ]] ; then
		echo " chmod +x  /${directory_of_software}/${x}  " >> Dockerfile
	else 
		echo " chmod +x /${directory_of_software}/${x}  &\\ " >> Dockerfile
fi 
counter=$((counter+1))
done

