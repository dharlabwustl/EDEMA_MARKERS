#!/usr/bin/env bash

################ BET GRAY ####################
# input_grayfilename=$1
# input_betfilename=$2
# outputdirectory=$3
# echo " I AM WORKING IN DOCKER"
# echo $input_filename
# result_output_directory=${outputdirectory} #/output #/preprocessing_output   
# yasheng_bet_directory=${outputdirectory} #/output #/preprocessing_output/betmask 
# input_directory=${outputdirectory} #/output #/preprocessing_output/grayctimage 
# output_for_BET=${outputdirectory} #/output #/BET_OUTPUT
# mkdir -p $output_for_BET
# input_grayfilename_path=$input_directory/$input_grayfilename
# input_betfilename_path=$yasheng_bet_directory/$input_betfilename
input_grayfilename_path=${1}
input_betfilename_path=${2}
output_for_BET=$(dirname ${input_betfilename_path}) #${3}
echo "RUNNING BET GRAY for "$input_grayfilename_path
echo "betfile:${input_betfilename_path}:grayfile:${input_grayfilename_path}:output_for_BET:${3}"

start=`date +%s`
python3 -c "
import sys ;
print('I AM HERE')
sys.path.append('/software');
from utilities_simple import * ;  betgrayfrombetbinary1_sh_v3()" $input_grayfilename_path     $input_betfilename_path  $output_for_BET