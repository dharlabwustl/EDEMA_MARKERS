import nibabel as nib 
import sys,os,glob,subprocess


def copyfilewithnibabel1(imagefilename,outputdir):
    imagefilename_nib=nib.load(imagefilename)
    imagefilebasename=os.path.basename(imagefilename)
    imagefileoutputname=os.path.join(outputdir,imagefilebasename)
    imagefilename_nib_data=imagefilename_nib.dataobj.get_unscaled() #""
    array_mask = nib.Nifti1Image(imagefilename_nib_data, affine=imagefilename_nib.affine, header=imagefilename_nib.header)
    # niigzfilenametosave2=os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file)) #.split(".nii")[0]+"RESIZED.nii.gz")
    nib.save(array_mask, imagefilename)


def copyfilewithnibabel():
    imagefilename=sys.argv[1]
    outputdir=sys.argv[2]
    imagefilename_nib=nib.load(imagefilename)
    imagefilebasename=os.path.basename(imagefilename)
    imagefileoutputname=os.path.join(outputdir,imagefilebasename)
    imagefilename_nib_data=imagefilename_nib.get_fdata() #""
    array_mask = nib.Nifti1Image(imagefilename_nib_data, affine=imagefilename_nib.affine, header=imagefilename_nib.header)
    # niigzfilenametosave2=os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file)) #.split(".nii")[0]+"RESIZED.nii.gz")
    nib.save(array_mask, imagefileoutputname)
    print ("For file: {} :saving is done".format(imagefilebasename))

