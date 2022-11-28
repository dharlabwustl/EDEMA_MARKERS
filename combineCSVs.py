#!/usr/bin/python

import os, sys, errno, shutil, uuid,subprocess
import math
import glob
import re
import requests
import pydicom as dicom

from xnatSession import XnatSession
import DecompressDCM
# import label_probability

catalogXmlRegex = re.compile(r'.*\.xml$')
XNAT_HOST_URL='https://snipr-dev-test1.nrg.wustl.edu'
XNAT_HOST = XNAT_HOST_URL #os.environ['XNAT_HOST']
XNAT_USER =os.environ['XNAT_USER']
XNAT_PASS =os.environ['XNAT_PASS'] 
def get_slice_idx(nDicomFiles):
    return min(nDicomFiles-1, math.ceil(nDicomFiles*0.7)) # slice 70% through the brain

def get_metadata_session(sessionId):
    url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    xnatSession.close_httpsession()
    metadata_session=response.json()['ResultSet']['Result']
    return metadata_session
def get_metadata_project(projectId):
    url= '/data/projects/' + projectId + '/subjects/?format=json' ##  > ../DATA/CSV/atul.csv' #+ subject + '/experiments/'+ sessionname+ '/scans/?format=csv    >  ../DATA/CSV/' + sessionname+ '.csv' #https://central.xnat.org/data/projects/'+project_name+'/subjects/'+subject + '/experiments/session'+ str(sessionnumber)+ '/scans/'+reconstruction_name + '/resources/DICOM/files/' + filename_base 
    # url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    # xnatSession.close_httpsession()
    metadata_projects=response.json()['ResultSet']['Result']
    return metadata_projects
def get_metadata_subject(projectId,subjLabel):
    url= '/data/projects/' + projectId + '/subjects/'+ subjLabel+'/experiments/?format=json' 
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    metadata_subject=response.json()['ResultSet']['Result']
    return metadata_subject

def decide_image_conversion(metadata_session,scanId):
    decision=False 
    usable=False
    brain_type=False
    for x in metadata_session:
        if x['ID']  == scanId:
            print(x['ID'])
            # result_usability = response.json()['ResultSet']['Result'][0]['quality']
            result_usability = x['quality']
#             print(result)
            if 'usable' in result_usability.lower():
                print(True)
                usable=True
            result_type= x['type']
            if 'z-axial-brain' in result_type.lower() or 'z-brain-thin' in result_type.lower():
                print(True)
                brain_type=True
            break
    if usable==True and brain_type==True:
        decision =True
    return decision


def get_dicom_from_filesystem(sessionId, scanId):
    # Handle DICOM files that are not stored in a directory matching their XNAT scanId
    print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" % 
        (sessionId, scanId))
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    if response.status_code != 200:
        raise Exception("Error querying XNAT for %s DICOM files: %s %s %s" % (scanId, 
                                                                              response.status_code, 
                                                                              response.reason, 
                                                                              response.text))
    result = response.json()['ResultSet']['Result']
    # print(result[0]) #['absolutePath'])
    nDicomFiles = len(result)
    # print(nDicomFiles)
    if nDicomFiles == 0:
        raise Exception("No DICOM files for %s stored in XNAT" % scanId)

    # Get 70% file and ensure it exists
    selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
    selDicomAbs_split=selDicomAbs.split('/')
    print(selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3])
    command='dcm2niix -o /output/ -f ' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '  -m 1 ' + '    /input/DICOM'
    subprocess.call(command,shell=True)


def get_dicom_using_xnat(sessionId, scanId):
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    
    # Handle DICOM files that are not stored in a directory matching their XNAT scanId
#####################################################################
    url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" % 
        (sessionId, scanId))
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    if response.status_code != 200:

        return False
        # raise Exception("Error querying XNAT for %s DICOM files: %s %s %s" % (scanId, 
        #                                                                       response.status_code, 
        #                                                                       response.reason, 
        #                                                                       response.text))
    result = response.json()['ResultSet']['Result']
    # print(result[0]) #['absolutePath'])
    nDicomFiles = len(result)
    # print(nDicomFiles)
    if nDicomFiles == 0:
        return False
        # raise Exception("No DICOM files for %s stored in XNAT" % scanId)

    # Get 70% file and ensure it exists
    selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
    selDicomAbs_split=selDicomAbs.split('/')
    print(selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3])
    ######################################################################################

    # print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    url = ("/data/experiments/%s/scans/%s/resources/DICOM/files?format=zip" % 
        (sessionId, scanId))

    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    zipfilename=sessionId+scanId+'.zip'
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    command = 'unzip -d /output ' + zipfilename
    subprocess.call(command,shell=True)
    command='dcm2niix -o /output/ -f ' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '  -m 1 ' + '    /output/*'
    subprocess.call(command,shell=True)
    # command = 'cp /output/' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '.nii   ' + '/output/'
    # subprocess.call(command,shell=True)
    url = ("/data/experiments/%s/scans/%s/resources/NIFTI/files/" % 
        (sessionId, scanId))
    allniftifiles=glob.glob('/output/' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '*.nii')
    for eachniftifile in allniftifiles:
        files={'file':open(eachniftifile,'rb')}
        response = xnatSession.httpsess.post(xnatSession.host + url,files=files)
        print(response)
    xnatSession.close_httpsession()
    for eachniftifile in allniftifiles:
        command= 'rm  ' + eachniftifile
        subprocess.call(command,shell=True)
    return True 




if __name__ == '__main__':
    # Get user args
    # if len(sys.argv) != 6:
    #     sys.stderr.write("Usage: %s [session directory] [working directory] [XNAT session ID] \
    #         [XNAT session directory] [quoted space-delimited list of scan ids]" % sys.argv[0])
    #     exit(1)
    # projectId=sys.argv[1]
    projectId=sys.argv[1] 
    metadata_projects=get_metadata_project(projectId)
    # url= '/data/projects/' + projectId + '/subjects/?format=json' ##  > ../DATA/CSV/atul.csv' #+ subject + '/experiments/'+ sessionname+ '/scans/?format=csv    >  ../DATA/CSV/' + sessionname+ '.csv' #https://central.xnat.org/data/projects/'+project_name+'/subjects/'+subject + '/experiments/session'+ str(sessionnumber)+ '/scans/'+reconstruction_name + '/resources/DICOM/files/' + filename_base 
    # # url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    # xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    # xnatSession.renew_httpsession()
    # response = xnatSession.httpsess.get(xnatSession.host + url)
    # # xnatSession.close_httpsession()
    # metadata_Subjects=response.json()['ResultSet']['Result']
    # # metadata_Subjects
    for each_subj in metadata_projects:
        subjLabel=each_subj['ID']
    #     print(each_subj['ID'])
        # url= '/data/projects/' + projectId + '/subjects/'+ subjLabel+'/experiments/?format=json' 
        # xnatSession.renew_httpsession()
        # response = xnatSession.httpsess.get(xnatSession.host + url)
        # metadata_Sessions=response.json()['ResultSet']['Result']
        metadata_subject=get_metadata_subject(projectId,subjLabel)
        for each_session in metadata_subject:
            print(each_session['ID'])
            sessionId=each_session['ID']
            metadata_session=get_metadata_session(sessionId)
            for x in metadata_session:
                # if int(x['ID']) == scanId:
                scanId=x['ID']

    xnatSession.close_httpsession()


