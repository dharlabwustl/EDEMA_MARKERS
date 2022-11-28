#!/usr/bin/python

import os, sys, errno, shutil, uuid,subprocess,csv,json
import math
import glob
import re
import requests
import pandas as pd
import nibabel as nib
# import pydicom as dicom
import pathlib
from xnatSession import XnatSession
catalogXmlRegex = re.compile(r'.*\.xml$')
XNAT_HOST_URL='https://snipr-dev-test1.nrg.wustl.edu'
XNAT_HOST = XNAT_HOST_URL #os.environ['XNAT_HOST']
XNAT_USER = os.environ['XNAT_USER']#
XNAT_PASS =os.environ['XNAT_PASS'] # 
def combinecsvs(inputdirectory,outputdirectory,outputfilename,extension):
    outputfilepath=os.path.join(outputdirectory,outputfilename)
    # extension = 'csv'
    all_filenames = [i for i in glob.glob(os.path.join(inputdirectory,'*{}'.format(extension)))]
#    os.chdir(inputdirectory)
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv(outputfilepath, index=False, encoding='utf-8-sig')

def call_combine_all_csvfiles_of_edema_biomarker():
    working_directory=sys.argv[1]
    working_directory_tocombinecsv=sys.argv[2]
    extension=sys.argv[3]
    outputfilename=sys.argv[4]
    combinecsvs(working_directory,working_directory_tocombinecsv,outputfilename,extension)

def call_get_all_selected_scan_in_a_project():
    projectId=sys.argv[1]
    working_directory=sys.argv[2]
    get_all_selected_scan_in_a_project(projectId,working_directory)


def call_get_all_EDEMA_BIOMARKER_csvfiles_of_allselectedscan():
    working_directory=sys.argv[1]
    get_all_EDEMA_BIOMARKER_csvfiles_of_ascan(working_directory)
    
    
    
def get_all_EDEMA_BIOMARKER_csvfiles_of_ascan(dir_to_receive_the_data):
    for each_csvfile in glob.glob(os.path.join(dir_to_receive_the_data,'SNIPR*.csv')):
        df_selected_scan=pd.read_csv(each_csvfile)
        resource_dir='EDEMA_BIOMARKER'
        # print(df_selected_scan)
        for item_id1, each_selected_scan in df_selected_scan.iterrows():
            scan_URI=each_selected_scan['URI'].split('/resources/')[0] #/data/experiments/SNIPR_E03516/scans/2/resources/110269/files/BJH_002_11112019_1930_2.nii
            print(scan_URI)
            metadata_EDEMA_BIOMARKERS=get_resourcefiles_metadata(scan_URI,resource_dir)
            if len(metadata_EDEMA_BIOMARKERS) >0:
                metadata_EDEMA_BIOMARKERS_df=pd.DataFrame(metadata_EDEMA_BIOMARKERS)
                print(metadata_EDEMA_BIOMARKERS_df)
                for item_id, each_file_inEDEMA_BIOMARKERS in metadata_EDEMA_BIOMARKERS_df.iterrows():
                    if '.csv' in each_file_inEDEMA_BIOMARKERS['URI']:
                        print("YES IT IS CSV FILE FOR ANALYSIS")
                        downloadresourcefilewithuri_py(each_file_inEDEMA_BIOMARKERS,dir_to_receive_the_data)
                    if '.pdf' in each_file_inEDEMA_BIOMARKERS['URI']:
                        print("YES IT IS PDF FILE FOR VISUALIZATION")
                        downloadresourcefilewithuri_py(each_file_inEDEMA_BIOMARKERS,dir_to_receive_the_data)
                        # break
                # break 
            

    
    
# def combine_all_csvfiles_of_edema_biomarker(projectId,dir_to_receive_the_data):

#     ## for each csv file corresponding to the session 
#     for each_csvfile in glob.glob(os.path.join(dir_to_receive_the_data,'*.csv')):
#         df_selected_scan=pd.read_csv(each_csvfile)
#         resource_dir='EDEMA_BIOMARKER'
#         for item_id1, each_selected_scan in df_selected_scan.iterrows():
#             scan_URI=each_selected_scan['URI'].split('/resources/')[0] #/data/experiments/SNIPR_E03516/scans/2/resources/110269/files/BJH_002_11112019_1930_2.nii
#             metadata_EDEMA_BIOMARKERS=get_resourcefiles_metadata(scan_URI,resource_dir)
#             metadata_EDEMA_BIOMARKERS_df=pd.DataFrame(metadata_EDEMA_BIOMARKERS)
#             for item_id, each_file_inEDEMA_BIOMARKERS in sessions_list_df.iterrows():
#                 # print(each_file_inEDEMA_BIOMARKERS['URI'])
#                 if '.csv' in each_file_inEDEMA_BIOMARKERS['URI']:
#                     print("YES IT IS CSV FILE FOR ANALYSIS")
#                     downloadresourcefilewithuri_py(each_file_inEDEMA_BIOMARKERS,dir_to_receive_the_data)
#                 if '.pdf' in each_file_inEDEMA_BIOMARKERS['URI']:
#                     print("YES IT IS CSV FILE FOR ANALYSIS")
#                     downloadresourcefilewithuri_py(each_file_inEDEMA_BIOMARKERS,dir_to_receive_the_data)
                
                                  
#     # get_resourcefiles_metadata(URI,resource_dir)
#     ## download csv files from the EDEMA_BIOMARKER directory:


#     ## combine all the csv files

#     ## upload the combined csv files to the project directory level 


def deleteafile(filename):
    command="rm " + filename
    subprocess.call(command,shell=True)
def get_all_selected_scan_in_a_project(projectId,dir_to_receive_the_data):
    sessions_list=get_allsessionlist_in_a_project(projectId)
    sessions_list_df=pd.DataFrame(sessions_list)
    for item_id, each_session in sessions_list_df.iterrows():
        sessionId=each_session['ID']
        output_csvfile=os.path.join(dir_to_receive_the_data,sessionId+'.csv')
        try:
            decision_which_nifti(sessionId,dir_to_receive_the_data,output_csvfile)
        except:
            pass
def get_allsessionlist_in_a_project(projectId):
    # projectId="BJH" #sys.argv[1]   
    url = ("/data/projects/%s/experiments/?format=json" %    (projectId))
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    xnatSession.close_httpsession()
    sessions_list=response.json()['ResultSet']['Result']
    
    return sessions_list
def call_decision_which_nifti():
    sessionId=sys.argv[1]
    dir_to_receive_the_data=sys.argv[2]
    output_csvfile=sys.argv[3]
    decision_which_nifti(sessionId,dir_to_receive_the_data,output_csvfile)
    
def decision_which_nifti(sessionId,dir_to_receive_the_data="",output_csvfile=""):
    # sessionId=sys.argv[1]
    # dir_to_receive_the_data="./NIFTIFILEDIR" #sys.argv[2]
    # output_csvfile='test.csv' #sys.argv[3]
    this_session_metadata=get_metadata_session(sessionId)
    jsonStr = json.dumps(this_session_metadata)
    # print(jsonStr)
    df = pd.read_json(jsonStr)
    # # df = pd.read_csv(sessionId+'_scans.csv') 
    # sorted_df = df.sort_values(by=['type'], ascending=False)
    # # sorted_df.to_csv('scan_sorted.csv', index=False)
    df_axial=df.loc[(df['type'] == 'Z-Axial-Brain') & (df['quality'] == 'usable')] ##| (df['type'] == 'Z-Brain-Thin')]
    df_thin=df.loc[(df['type'] == 'Z-Brain-Thin')  & (df['quality'] == 'usable') ] ##| (df['type'] == 'Z-Brain-Thin')]
    # print(df_axial)
    list_of_usables=[] 
    list_of_usables_withsize=[]
    if len(df_axial)>0:
        selectedFile=""
        # print(len(df_axial))
        # print("df_axial:{}".format(len(df_axial['URI'])))
        for item_id, each_axial in df_axial.iterrows():
            print(each_axial['URI'])
            URI=each_axial['URI']
            resource_dir='NIFTI'
            nifti_metadata=json.dumps(get_resourcefiles_metadata(URI,resource_dir)) #get_niftifiles_metadata(each_axial['URI'] )) get_resourcefiles_metadata(URI,resource_dir)
            df_scan = pd.read_json(nifti_metadata)

            for each_item_id,each_nifti in df_scan.iterrows():
                print(each_nifti['URI'])
                if '.nii' in each_nifti['Name'] or '.nii.gz' in each_nifti['Name']:
                    list_of_usables.append([each_nifti['URI'],each_nifti['Name'],each_axial['ID']])
                    x=[each_nifti['URI'],each_nifti['Name'],each_axial['ID']]
                    downloadniftiwithuri(x,dir_to_receive_the_data)
                    number_slice=nifti_number_slice(os.path.join(dir_to_receive_the_data,x[1]))
                    list_of_usables_withsize.append([each_nifti['URI'],each_nifti['Name'],each_axial['ID'],number_slice])
                    deleteafile(os.path.join(dir_to_receive_the_data,x[1]))
  
                    
                    
            # break
    elif len(df_thin)>0:
        selectedFile=""
        # print(len(df_axial))
        # print("df_axial:{}".format(len(df_axial['URI'])))
        for item_id, each_thin in df_thin.iterrows():
            print(each_thin['URI'])
            URI=each_thin['URI']
            resource_dir='NIFTI'
            nifti_metadata=json.dumps(get_resourcefiles_metadata(URI,resource_dir)) #json.dumps(get_niftifiles_metadata(each_thin['URI'] ))
            df_scan = pd.read_json(nifti_metadata)

            for each_item_id,each_nifti in df_scan.iterrows():
                print(each_nifti['URI'])
                if '.nii' in each_nifti['Name'] or '.nii.gz' in each_nifti['Name']:
                    x=[each_nifti['URI'],each_nifti['Name'],each_axial['ID']]
                    list_of_usables.append([each_nifti['URI'],each_nifti['Name'],each_thin['ID']])
                    x=[each_nifti['URI'],each_nifti['Name'],each_axial['ID']]
                    downloadniftiwithuri(x,dir_to_receive_the_data)
                    number_slice=nifti_number_slice(os.path.join(dir_to_receive_the_data,x[1]))
                    list_of_usables_withsize.append([each_nifti['URI'],each_nifti['Name'],each_axial['ID'],number_slice])      
                    deleteafile(os.path.join(dir_to_receive_the_data,x[1]))                    
  
            # break
    # dir_to_receive_the_data="./NIFTIFILEDIR"
    # final_ct_file=list_of_usables[0]
    if len(list_of_usables_withsize) > 0:
        jsonStr = json.dumps(list_of_usables_withsize)
        # print(jsonStr)
        df = pd.read_json(jsonStr)
        df.columns=['URI','Name','ID','NUMBEROFSLICES']
        df_maxes = df[df['NUMBEROFSLICES']==df['NUMBEROFSLICES'].max()]
        # return df_maxes
        final_ct_file=''
        if df_maxes.shape[0]>0:
            final_ct_file=df_maxes.iloc[0]
            for item_id, each_scan in df_maxes.iterrows():
                if "tilt" in each_scan['Name']:
                    final_ct_file=each_scan 
                    break
        if len(final_ct_file)> 1: 
            pd.DataFrame(final_ct_file).T.to_csv(os.path.join(dir_to_receive_the_data,output_csvfile),index=False)
            return True
        return False
    else:
        return False
def nifti_number_slice(niftifilename):
    return nib.load(niftifilename).shape[2]

    # pd.DataFrame(final_ct_file).T.to_csv(os.path.join(dir_to_receive_the_data,output_csvfile),index=False)
# def downloadniftiwithuri(URI,dir_to_save,niftioutput_filename):
#     xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
#     # for x in range(df.shape[0]):
#     #     print(df.iloc[x])
        
#     url =   URI #  df.iloc[0][0] #URI_name[0] #("/data/experiments/%s/scans/%s/resources/NIFTI/files?format=zip" % 
#         # (sessionId, scanId))
#     print(url)
#     xnatSession.renew_httpsession()
#     response = xnatSession.httpsess.get(xnatSession.host + url)
#     zipfilename=os.path.join(dir_to_save,niftioutput_filename) #sessionId+scanId+'.zip'
#     with open(zipfilename, "wb") as f:
#         for chunk in response.iter_content(chunk_size=512):
#             if chunk:  # filter out keep-alive new chunks
#                 f.write(chunk)
#     xnatSession.close_httpsession()
    
# def get_urls_csvfiles_in_EDEMA_BIOMARKER_inaproject(sessions_list):
#     jsonStr = json.dumps(sessions_list)
#     # print(jsonStr)
#     df = pd.read_json(jsonStr)
#     for item_id, each_session in df_touse.iterrows():
#         sessionId=each_session['ID']
#         this_session_metadata=get_metadata_session(sessionId)
    
    
#     this_session_metadata=get_metadata_session(sessionId)
#     jsonStr = json.dumps(this_session_metadata)
#     # print(jsonStr)
#     df = pd.read_json(jsonStr)
#     df_touse=df.loc[(df['ID'] == int(scanId))]

#     # print("get_resourcefiles_metadata(df_touse['URI'],resource_foldername ){}".format(get_resourcefiles_metadata(df_touse['URI'],resource_foldername )))
#     for item_id, each_scan in df_touse.iterrows():
#         print("each_scan['URI'] {}".format(each_scan['URI']))
#         nifti_metadata=json.dumps(get_resourcefiles_metadata(each_scan['URI'],resource_foldername ))
#         df_scan = pd.read_json(nifti_metadata)
#         pd.DataFrame(df_scan).to_csv(os.path.join(dir_to_receive_the_data,output_csvfile),index=False)
    

def get_maskfile_scan_metadata():
    sessionId=sys.argv[1]   
    scanId=sys.argv[2]
    resource_foldername=sys.argv[3]
    dir_to_receive_the_data=sys.argv[4]
    output_csvfile=sys.argv[5]
    this_session_metadata=get_metadata_session(sessionId)
    jsonStr = json.dumps(this_session_metadata)
    # print(jsonStr)
    df = pd.read_json(jsonStr)
    df_touse=df.loc[(df['ID'] == int(scanId))]

    # print("get_resourcefiles_metadata(df_touse['URI'],resource_foldername ){}".format(get_resourcefiles_metadata(df_touse['URI'],resource_foldername )))
    for item_id, each_scan in df_touse.iterrows():
        print("each_scan['URI'] {}".format(each_scan['URI']))
        nifti_metadata=json.dumps(get_resourcefiles_metadata(each_scan['URI'],resource_foldername ))
        df_scan = pd.read_json(nifti_metadata)
        pd.DataFrame(df_scan).to_csv(os.path.join(dir_to_receive_the_data,output_csvfile),index=False)
def get_relevantfile_from_NIFTIDIR():
    sessionId=sys.argv[1]
    dir_to_receive_the_data=sys.argv[2]
    output_csvfile=sys.argv[3]
    this_session_metadata=get_metadata_session(sessionId)
    jsonStr = json.dumps(this_session_metadata)
    # print(jsonStr)
    df = pd.read_json(jsonStr)
    # # df = pd.read_csv(sessionId+'_scans.csv') 
    # sorted_df = df.sort_values(by=['type'], ascending=False)
    # # sorted_df.to_csv('scan_sorted.csv', index=False)
    df_axial=df.loc[(df['type'] == 'Z-Axial-Brain') & (df['quality'] == 'usable') ] ##| (df['type'] == 'Z-Brain-Thin')]
    df_thin=df.loc[(df['type'] == 'Z-Brain-Thin') & (df['quality'] == 'usable')] ##| (df['type'] == 'Z-Brain-Thin')]
    # print(df_axial)
    list_of_usables=[] 
    if len(df_axial)>0:
        selectedFile=""
        # print(len(df_axial))
        # print("df_axial:{}".format(len(df_axial['URI'])))
        for item_id, each_axial in df_axial.iterrows():
            print(each_axial['URI'])
            nifti_metadata=json.dumps(get_niftifiles_metadata(each_axial['URI'] ))
            df_scan = pd.read_json(nifti_metadata)

            for each_item_id,each_nifti in df_scan.iterrows():
                print(each_nifti['URI'])
                list_of_usables.append([each_nifti['URI'],each_nifti['Name'],each_axial['ID']])
            break
    elif len(df_thin)>0:
        selectedFile=""
        # print(len(df_axial))
        # print("df_axial:{}".format(len(df_axial['URI'])))
        for item_id, each_thin in df_thin.iterrows():
            print(each_thin['URI'])
            nifti_metadata=json.dumps(get_niftifiles_metadata(each_thin['URI'] ))
            df_scan = pd.read_json(nifti_metadata)

            for each_item_id,each_nifti in df_scan.iterrows():
                print(each_nifti['URI'])
                list_of_usables.append([each_nifti['URI'],each_nifti['Name'],each_thin['ID']])
            break
    final_ct_file=list_of_usables[0]
    for x in list_of_usables:
        if "tilt" in x[0].lower():
            final_ct_file=x 
            break
    # downloadniftiwithuri(final_ct_file,dir_to_receive_the_data)
    pd.DataFrame(final_ct_file).T.to_csv(os.path.join(dir_to_receive_the_data,output_csvfile),index=False)
    
def downloadniftiwithuri_withcsv():
    csvfilename=sys.argv[1]
    dir_to_save=sys.argv[2]
    df=pd.read_csv(csvfilename) 
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    for x in range(df.shape[0]):
        print(df.iloc[x])
        
        url =     df.iloc[x][0] #URI_name[0] #("/data/experiments/%s/scans/%s/resources/NIFTI/files?format=zip" % 
            # (sessionId, scanId))
        print(url)
        xnatSession.renew_httpsession()
        response = xnatSession.httpsess.get(xnatSession.host + url)
        zipfilename=os.path.join(dir_to_save,df.iloc[x][1]) #sessionId+scanId+'.zip'
        with open(zipfilename, "wb") as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        xnatSession.close_httpsession()
        
def downloadmaskswithuri_withcsv():
    csvfilename=sys.argv[1]
    dir_to_save=sys.argv[2]
    df=pd.read_csv(csvfilename) 
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    for item_id, each_scan in df.iterrows():
        # print("each_scan['URI'] {}".format(each_scan['URI']))    
    # for x in range(df.shape[0]):
        # print(df.iloc[x])
        
        url =  each_scan['URI'] #   df.iloc[0][0] #URI_name[0] #("/data/experiments/%s/scans/%s/resources/NIFTI/files?format=zip" % 
            # (sessionId, scanId))
        print(url)
        xnatSession.renew_httpsession()
        response = xnatSession.httpsess.get(xnatSession.host + url)
        zipfilename=os.path.join(dir_to_save,each_scan['Name']) #sessionId+scanId+'.zip'
        with open(zipfilename, "wb") as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        xnatSession.close_httpsession()
def downloadresourcefilewithuri_py(url,dir_to_save):
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url['URI'])
    zipfilename=os.path.join(dir_to_save,url['Name']) #sessionId+scanId+'.zip'
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    xnatSession.close_httpsession()
    
def downloadniftiwithuri(URI_name,dir_to_save):
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    url = URI_name[0] #("/data/experiments/%s/scans/%s/resources/NIFTI/files?format=zip" % 
        # (sessionId, scanId))
    print(url)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    zipfilename=os.path.join(dir_to_save,URI_name[1]) #sessionId+scanId+'.zip'
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    xnatSession.close_httpsession()

def get_niftifiles_metadata(URI):
    url = (URI+'/resources/NIFTI/files?format=json')
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    xnatSession.close_httpsession()
    metadata_nifti=response.json()['ResultSet']['Result']
    return metadata_nifti
def get_resourcefiles_metadata(URI,resource_dir):
    url = (URI+'/resources/' + resource_dir +'/files?format=json')
    print(url)
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    xnatSession.close_httpsession()
    metadata_masks=response.json()['ResultSet']['Result']
    return metadata_masks

def findthetargetscan():
     target_scan=""
     ## find the list of usable scans
     ## Is axial available? If yes, focus on axial, if not go for thin
     ## Is tilt available ? If yes, get the tilt, if not go for non-tilt
     return target_scan

def uploadfile():
    sessionId=str(sys.argv[1])
    scanId=str(sys.argv[2])
    input_dirname=str(sys.argv[3])
    resource_dirname=str(sys.argv[4])
    file_suffix=str(sys.argv[5])
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    url = (("/data/experiments/%s/scans/%s/resources/"+resource_dirname+"/files/") % (sessionId, scanId))
    allniftifiles=glob.glob(os.path.join(input_dirname,'*'+file_suffix) ) #input_dirname + '/*'+file_suffix)
    for eachniftifile in allniftifiles:
        files={'file':open(eachniftifile,'rb')}
        response = xnatSession.httpsess.post(xnatSession.host + url,files=files)
        print(response)
    xnatSession.close_httpsession()
    # for eachniftifile in allniftifiles:
    #     command= 'rm  ' + eachniftifile
    #     subprocess.call(command,shell=True)
    return True 

def uploadfile_projectlevel():
    try:
        projectId=str(sys.argv[1])
        input_dirname=str(sys.argv[2])
        resource_dirname=str(sys.argv[3])
        file_suffix=str(sys.argv[4])
        xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
        xnatSession.renew_httpsession()
        url = (("/data/projects/%s/resources/"+resource_dirname+"/files/") % (projectId))
        allniftifiles=glob.glob(os.path.join(input_dirname,'*'+file_suffix) ) #input_dirname + '/*'+file_suffix)
        for eachniftifile in allniftifiles:
            files={'file':open(eachniftifile,'rb')}
            response = xnatSession.httpsess.post(xnatSession.host + url,files=files)
            print(response)
        xnatSession.close_httpsession()
        # for eachniftifile in allniftifiles:
        #     command= 'rm  ' + eachniftifile
        #     subprocess.call(command,shell=True)
        return True 
    except Exception as e:
        print(e)
        return False

def downloadandcopyfile():
    sessionId=sys.argv[1]
    scanId=sys.argv[2]
    metadata_session=get_metadata_session(sessionId)
    decision=decide_image_conversion(metadata_session,scanId)
    command= 'rm -r /ZIPFILEDIR/*'
    subprocess.call(command,shell=True)
    if decision==True:
        xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
        xnatSession.renew_httpsession()
        outcome=get_nifti_using_xnat(sessionId, scanId)
        if outcome==False:
            print("NO DICOM FILE %s:%s:%s:%s" % (sessionId, scanId))
        xnatSession.close_httpsession()
        try :
            copy_nifti()
            print("COPIED TO WORKINGDIRECTORY")
        except:
            pass
def downloadandcopyallniftifiles():
    sessionId=sys.argv[1]
    scanId=sys.argv[2]
    metadata_session=get_metadata_session(sessionId)
    # decision=decide_image_conversion(metadata_session,scanId)
    command= 'rm -r /ZIPFILEDIR/*'
    subprocess.call(command,shell=True)
    # if decision==True:
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    outcome=get_nifti_using_xnat(sessionId, scanId)
    if outcome==False:
        print("NO DICOM FILE %s:%s:%s:%s" % (sessionId, scanId))
    xnatSession.close_httpsession()
    try :
        copy_nifti()
        print("COPIED TO WORKINGDIRECTORY")
    except:
        pass
def copy_nifti():
    for dirpath, dirnames, files in os.walk('/ZIPFILEDIR'):
    #                print(f'Found directory: {dirpath}')
        for file_name in files:
            file_extension = pathlib.Path(file_name).suffix
            if 'nii' in file_extension:
                command='cp ' + os.path.join(dirpath,file_name) + '  /workinginput/'
                subprocess.call(command,shell=True)
                print(os.path.join(dirpath,file_name))




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
def get_metadata_session_forbash():
    sessionId=sys.argv[1]
    url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    xnatSession.close_httpsession()
    metadata_session=response.json()['ResultSet']['Result']
    print(metadata_session)
    data_file = open('this_sessionmetadata.csv', 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for data in metadata_session:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    data_file.close()
    return metadata_session
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




def get_nifti_using_xnat(sessionId, scanId):
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    url = ("/data/experiments/%s/scans/%s/resources/NIFTI/files?format=zip" % 
        (sessionId, scanId))

    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    zipfilename=os.path.join('/workinginput',sessionId+scanId+'.zip')
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    command = 'unzip -d /ZIPFILEDIR ' + zipfilename
    subprocess.call(command,shell=True)
    command='rm -r ' + zipfilename
    command = 'unzip -d /ZIPFILEDIR ' + zipfilename
    subprocess.call(command,shell=True)

    return True 



def downloadfiletolocaldir():
    print(sys.argv)
    sessionId=str(sys.argv[1])
    scanId=str(sys.argv[2])
    resource_dirname=str(sys.argv[3])
    output_dirname=str(sys.argv[4])

    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    url = (("/data/experiments/%s/scans/%s/resources/" + resource_dirname+ "/files?format=zip")  % 
        (sessionId, scanId))

    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    zipfilename=sessionId+scanId+'.zip'
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    command='rm -r /ZIPFILEDIR/* '
    subprocess.call(command,shell=True)
    command = 'unzip -d /ZIPFILEDIR ' + zipfilename
    subprocess.call(command,shell=True)
    xnatSession.close_httpsession()
    copy_nifti_to_a_dir(output_dirname)

    return True 
# def downloadfiletolocaldir_py(sessionId,scanId,resource_dirname,output_dirname):
#     xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
#     url = (("/data/experiments/%s/scans/%s/resources/" + resource_dirname+ "/files?format=zip")  % 
#         (sessionId, scanId))

#     xnatSession.renew_httpsession()
#     response = xnatSession.httpsess.get(xnatSession.host + url)
#     zipfilename=sessionId+scanId+'.zip'
#     with open(zipfilename, "wb") as f:
#         for chunk in response.iter_content(chunk_size=512):
#             if chunk:  # filter out keep-alive new chunks
#                 f.write(chunk)
#     command='rm -r /ZIPFILEDIR/* '
#     subprocess.call(command,shell=True)
#     command = 'unzip -d /ZIPFILEDIR ' + zipfilename
#     subprocess.call(command,shell=True)
#     xnatSession.close_httpsession()
#     copy_nifti_to_a_dir(output_dirname)

#     return True 
def copy_nifti_to_a_dir(dir_name):
    for dirpath, dirnames, files in os.walk('/ZIPFILEDIR'):
    #                print(f'Found directory: {dirpath}')
        for file_name in files:
            file_extension = pathlib.Path(file_name).suffix
            if 'nii' in file_extension or 'gz' in file_extension:
                command='cp ' + os.path.join(dirpath,file_name) + '  ' + dir_name + '/'
                subprocess.call(command,shell=True)
                print(os.path.join(dirpath,file_name))

# def uploadfile():
#     sessionId=str(sys.argv[1])
#     scanId=str(sys.argv[2])
#     input_dirname=str(sys.argv[3])
#     resource_dirname=str(sys.argv[4])
#     file_suffix=str(sys.argv[5])
#     xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
#     xnatSession.renew_httpsession()
#     url = (("/data/experiments/%s/scans/%s/resources/"+resource_dirname+"/files/") % (sessionId, scanId))
#     allniftifiles=glob.glob(os.path.join(input_dirname,'*'+file_suffix) ) #input_dirname + '/*'+file_suffix)
#     for eachniftifile in allniftifiles:
#         files={'file':open(eachniftifile,'rb')}
#         response = xnatSession.httpsess.post(xnatSession.host + url,files=files)
#         print(response)
#     xnatSession.close_httpsession()
#     # for eachniftifile in allniftifiles:
#     #     command= 'rm  ' + eachniftifile
#     #     subprocess.call(command,shell=True)
#     return True 


# def downloadandcopyfile():
#     sessionId=sys.argv[1]
#     scanId=sys.argv[2]
#     metadata_session=get_metadata_session(sessionId)
#     decision=decide_image_conversion(metadata_session,scanId)
#     command= 'rm -r /ZIPFILEDIR/*'
#     subprocess.call(command,shell=True)
#     if decision==True:
#         xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
#         xnatSession.renew_httpsession()
#         outcome=get_nifti_using_xnat(sessionId, scanId)
#         if outcome==False:
#             print("NO DICOM FILE %s:%s:%s:%s" % (sessionId, scanId))
#         xnatSession.close_httpsession()
#         try :
#             copy_nifti()
#             print("COPIED TO WORKINGDIRECTORY")
#         except:
#             pass

# def copy_nifti():
#     for dirpath, dirnames, files in os.walk('/ZIPFILEDIR'):
#     #                print(f'Found directory: {dirpath}')
#         for file_name in files:
#             file_extension = pathlib.Path(file_name).suffix
#             if 'nii' in file_extension:
#                 command='cp ' + os.path.join(dirpath,file_name) + '  /workinginput/'
#                 subprocess.call(command,shell=True)
#                 print(os.path.join(dirpath,file_name))




# def get_slice_idx(nDicomFiles):
#     return min(nDicomFiles-1, math.ceil(nDicomFiles*0.7)) # slice 70% through the brain

# def get_metadata_session(sessionId):
#     url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
#     xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
#     xnatSession.renew_httpsession()
#     response = xnatSession.httpsess.get(xnatSession.host + url)
#     xnatSession.close_httpsession()
#     metadata_session=response.json()['ResultSet']['Result']
#     return metadata_session
# def get_metadata_session_forbash():
#     sessionId=sys.argv[1]
#     url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
#     xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
#     xnatSession.renew_httpsession()
#     response = xnatSession.httpsess.get(xnatSession.host + url)
#     xnatSession.close_httpsession()
#     metadata_session=response.json()['ResultSet']['Result']
#     print(metadata_session)
#     data_file = open('this_sessionmetadata.csv', 'w')
#     csv_writer = csv.writer(data_file)
#     count = 0
#     for data in metadata_session:
#         if count == 0:
#             header = data.keys()
#             csv_writer.writerow(header)
#             count += 1
#         csv_writer.writerow(data.values())
#     data_file.close()
#     return metadata_session
# def decide_image_conversion(metadata_session,scanId):
#     decision=False 
#     usable=False
#     brain_type=False
#     for x in metadata_session:
#         if x['ID']  == scanId:
#             print(x['ID'])
#             # result_usability = response.json()['ResultSet']['Result'][0]['quality']
#             result_usability = x['quality']
# #             print(result)
#             if 'usable' in result_usability.lower():
#                 print(True)
#                 usable=True
#             result_type= x['type']
#             if 'z-axial-brain' in result_type.lower() or 'z-brain-thin' in result_type.lower():
#                 print(True)
#                 brain_type=True
#             break
#     if usable==True and brain_type==True:
#         decision =True
#     return decision




# def get_nifti_using_xnat(sessionId, scanId):
#     xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
#     url = ("/data/experiments/%s/scans/%s/resources/NIFTI/files?format=zip" % 
#         (sessionId, scanId))

#     xnatSession.renew_httpsession()
#     response = xnatSession.httpsess.get(xnatSession.host + url)
#     zipfilename=sessionId+scanId+'.zip'
#     with open(zipfilename, "wb") as f:
#         for chunk in response.iter_content(chunk_size=512):
#             if chunk:  # filter out keep-alive new chunks
#                 f.write(chunk)
#     command = 'unzip -d /ZIPFILEDIR ' + zipfilename
#     subprocess.call(command,shell=True)

#     return True 


# # if __name__ == '__main__':
# #     sessionId='SNIPR_E03517' #sys.argv[1]
# #     metadata_session=get_metadata_session(sessionId)
# #     for x in metadata_session:
# #         scanId=x['ID']
# #         decision=decide_image_conversion(metadata_session,scanId)

# #         command= 'rm -r /ZIPFILEDIR/*'
# #         subprocess.call(command,shell=True)
# #         if decision==True:
# #             xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
# #             xnatSession.renew_httpsession()
# #             outcome=get_nifti_using_xnat(sessionId, scanId)
# #             if outcome==False:
# #                 print("NO DICOM FILE %s:%s:%s:%s" % (sessionId, scanId))
# #             xnatSession.close_httpsession()
# #             try :
# #                 copy_nifti()
# #             except:
# #                 continue
