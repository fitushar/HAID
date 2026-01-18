###Import Files
import numpy as np
import os
import pandas as pd
import dicom2nifti
import pandas as pd
import sys
import dicom
import scipy.ndimage
from skimage import measure, morphology
import pydicom.uid
import cv2
from glob import glob
import png
from imutils import build_montages
from imutils import paths


def getting_dicom_details(SCAN_PATH_OF_INTEREST):
    try:
        slice_select_list=[file for file in os.listdir(SCAN_PATH_OF_INTEREST) if file.endswith('.dcm')]
        #print(slice_select_list)
        middleIndex = int((len(slice_select_list) - 1)/2)
        #print(middleIndex)
        im=SCAN_PATH_OF_INTEREST+slice_select_list[middleIndex]
        #print('Reached1')
        ds = pydicom.read_file(im,force=True)
        img_type=ds.ImageType
        #print('Reached2')

        #Series Deccription
        try:
           Series_Description=ds.SeriesDescription
        except:
           Series_Description='None'

        #--Study Description
        try:
           Study_description=ds.StudyDescription
        except:
           Study_description='None'

        #---ThickNess
        try:
            SliceThickness=ds.SliceThickness
        except:
            SliceThickness='None'
        #---Orientation
        try:
           ImageOrientation=img_type[2]
        except:
           ImageOrientation='None'

        ImageType=img_type[0]
        
    except:
        print('try')
    return Series_Description,Study_description,SliceThickness,ImageOrientation,ImageType

def scan_slice_count(Directory,csv_save_name,nifty_save_path):
    patient_DI_name_list=[]
    patient_report_number_list=[]
    Report_path=[]
    Series_Description_list=[]
    Study_description_list=[]
    SliceThickness_list=[]
    ImageOrientation_list=[]
    ImageType_list=[]
    nifty_name_list=[]


    problem_list_id=[]
    problem_list_scan=[]

    raw_data_path=Directory
    raw_list=next(os.walk(raw_data_path))[1]
    #print(raw_list)
    #raw_list[:] = [d for d in raw_list if d not in 'Exceptions']


    for patient in range(0,len(raw_list)):
    #for patient in range(0,1):

            #print(raw_list[patient])
            patient_path=raw_data_path+raw_list[patient]+'/'
            #print(patient_path)
            #patient_report_list=os.listdir(patient_path)
            patient_report_list=[dI for dI in os.listdir(patient_path) if os.path.isdir(os.path.join(patient_path,dI))]
            #print(patient_report_list)

            for patient_reports in range(0,len(patient_report_list)):
                report_path=patient_path+patient_report_list[patient_reports]+'/'
                #print(report_path)
                patient_scans_list=[dI for dI in os.listdir(report_path) if os.path.isdir(os.path.join(report_path,dI))]

                #patient_scans_list.sort(key=lambda f: int(filter(str.isdigit, f)))
                #print(patient_scans_list)

                scans_lenght=[]
                scans_lenght_path=[]
                scan_name=[]
                for l in range(0,len(patient_scans_list)):
                    scans_path2=report_path+patient_scans_list[l]+'/'
                    #print(scans_path2)
                    length=os.listdir(scans_path2)
                    nifti_name=raw_list[patient]+'pt'+patient_report_list[patient_reports]+'rt'+patient_scans_list[l]+'.nii.gz'
                    nifti_name=nifti_name.replace(" ", "_")
                    #print(nifti_name)
                    Series_Description,Study_description,SliceThickness,ImageOrientation,ImageType=getting_dicom_details(scans_path2)


                    try:
                       print('{}--Starting the case:{}'.format(patient,nifti_name))
                       output_file=nifty_save_path+nifti_name
                       scans_path=scans_path2
                       #print(scans_path)
                       #print(output_file)
                       dicom2nifti.dicom_series_to_nifti(scans_path,output_file, reorient_nifti=False)
                       patient_DI_name_list.append(raw_list[patient])
                       patient_report_number_list.append(patient_report_list[patient_reports])
                       Report_path.append(patient_scans_list[l])
                       Series_Description_list.append(Series_Description)
                       Study_description_list.append(Study_description)
                       SliceThickness_list.append(SliceThickness)
                       ImageOrientation_list.append(ImageOrientation)
                       ImageType_list.append(ImageType)
                       nifty_name_list.append(nifti_name)
                       print('!!!!!-----SAVED NIFTI------!!!!')
                    except:
                       problem_list_id.append(raw_list[patient])
                       problem_list_scan.append(patient_scans_list[l])
                       print('!!!!!-----Problem------!!!!')



    Inf0_data=pd.DataFrame(list(zip(patient_DI_name_list,patient_report_number_list,Report_path,Series_Description_list,
    Study_description_list,SliceThickness_list,ImageOrientation_list,ImageType_list,nifty_name_list)),columns=['id','report','scan','Series_Description','Study_description','SliceThickness','ImageOrientation','ImageType','nifty_name'])
    Inf0_data.to_csv(csv_save_name+'Dicom2nifti.csv', encoding='utf-8', index=False)

    Inf1_data=pd.DataFrame(list(zip(problem_list_id,problem_list_scan)),columns=['id','scan'])
    Inf1_data.to_csv(csv_save_name+'Dicom2nifti-Failed.csv', encoding='utf-8', index=False)


    return
#D='/image_data2/COVID_19_Publicdata/MIDRC_RICORD/MIDRC_RICORD_1a/MIDRC_RICORD_1a/MIDRC-RICORD-1A/'
#N='/image_data2/COVID_19_Publicdata/MIDRC_RICORD/MIDRC_RICORD_1a/MIDRC_RICORD_1a/MIDRC-RICORD-1A/'

if __name__ == '__main__':

    Directory= sys.argv[1]
    csv_save_name=sys.argv[2]
    nifty_save_path=sys.argv[3]
    scan_slice_count(Directory,csv_save_name,nifty_save_path)
