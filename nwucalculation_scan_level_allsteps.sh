#!/usr/bin/env bash
output_directory=/workingdir
final_output_directory=/output

eachfile_basename_noext=''
originalfile_basename=''
original_ct_file=''
for eachfile in /input/NIFTI/*.nii ; 
do
original_ct_file=${eachfile}
eachfile_basename=$(basename ${eachfile})
originalfile_basename=${eachfile_basename}
eachfile_basename_noext=${eachfile_basename%.nii*}
 

############## files basename ##################################
grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz
infarctfilename=${eachfile_basename_noext}_resaved_infarct_auto_removesmall.nii.gz
################################################
############## copy those files to the image ##################################
cp /input/MASKS/${betfilename}  ${output_directory}/
cp /input/MASKS/${csffilename}  ${output_directory}/
cp /input/MASKS/${infarctfilename}  ${output_directory}/
####################################################################################
source /software/bash_functions_forhost.sh

cp ${original_ct_file}  ${output_directory}/${grayfilename}
grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii
###########################################################################

#### originalfiel: .nii
#### betfile: *bet.nii.gz


# original_ct_file=$original_CT_directory_names/
levelset_infarct_mask_file=${output_directory}/${infarctfilename}
echo "levelset_infarct_mask_file:${levelset_infarct_mask_file}"
## preprocessing infarct mask:
python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}"  "${levelset_infarct_mask_file}"  "${output_directory}"


## preprocessing bet mask:
levelset_bet_mask_file=${output_directory}/${betfilename}
echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}"  "${levelset_bet_mask_file}"  "${output_directory}"

#### preprocessing csf mask:
levelset_csf_mask_file=${output_directory}/${csffilename}
echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}"  "${levelset_csf_mask_file}"  "${output_directory}"


lower_threshold=0 
upper_threshold=20 
templatefilename=scct_strippedResampled1.nii.gz 
mask_on_template=midlinecssfResampled1.nii.gz


run_IML_NWU_CSF_CALC()

{
this_filename=${1} 
this_betfilename=${2}
this_csfmaskfilename=${3}
this_infarctmaskfilename=${4}
echo "BET USING LEVELSET MASK"
 
/software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}

echo "bet_withlevelset successful" > ${output_directory}/success.txt 
this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
# cp ${this_filename_brain} ${output_directory}/ #  ${final_output_directory}/
echo "LINEAR REGISTRATION TO TEMPLATE"
/software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz 
echo "linear_rigid_registration successful" >> ${output_directory}/success.txt 
echo "RUNNING IML FSL PART"
/software/ideal_midline_fslpart.sh ${this_filename} # ${templatefilename} ${mask_on_template}  #$9 #${10} #$8 
echo "ideal_midline_fslpart successful" >> ${output_directory}/success.txt 
echo "RUNNING IML PYTHON PART"
 
/software/ideal_midline_pythonpart.sh  ${this_filename} #${templatefilename}  #$3 #$8 $9 ${10}
echo "ideal_midline_pythonpart successful" >> ${output_directory}/success.txt 

echo "RUNNING NWU AND CSF VOLUME CALCULATION "

/software/nwu_csf_volume.sh  ${this_filename}   ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename}  ${lower_threshold} ${upper_threshold}
echo "nwu_csf_volume successful" >> ${output_directory}/success.txt
thisfile_basename=$(basename $this_filename)
for texfile in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.tex ; 
do 
pdflatex -output-directory=${output_directory} $texfile   ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
rm ${output_directory}/*.aux
rm ${output_directory}/*.log
done 

for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*_brain_f.nii.gz ; 
do 
cp ${filetocopy} ${final_output_directory}/
done 

for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.mat ; 
do 
cp ${filetocopy} ${final_output_directory}/
done 

for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.pdf ; 
do 
cp ${filetocopy} ${final_output_directory}/
done 
for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.csv ; 
do 
cp ${filetocopy} ${final_output_directory}/
done 

}

x=$grayimage
bet_mask_filename=${output_directory}/${betfilename}
infarct_mask_filename=${output_directory}/${infarctfilename}
csf_mask_filename=${output_directory}/${csffilename}
run_IML_NWU_CSF_CALC  $x ${bet_mask_filename} ${csf_mask_filename} ${infarct_mask_filename}  

# 
# cp ${output_directory}/*.pdf ${final_output_directory}/

done


for f in ${output_directory}/*; do
    # if [ -d "$f" ]; then
        # $f is a directory
        rm -r $f 
    # fi
done

