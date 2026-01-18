import os
import pandas as pd
import numpy as np
import pydicom
import SimpleITK as sitk
from PIL import Image

# Input CSV file (adjust this to your CSV filename)
csv_file      = '/NAS/shared_data/for_VNLST/ft42/ct_public/unitochest/unitochest/val/val_dataset.csv'
# Base directories
base_ct_dir   = '/NAS/shared_data/for_VNLST/ft42/ct_public/unitochest/unitochest/val/images'
base_mask_dir = '/NAS/shared_data/for_VNLST/ft42/ct_public/unitochest/unitochest/val/masks'
Save_Dir_ct   = '/NAS/shared_data/for_VNLST/ft42/ct_public/unitochest/unitochest_nifti_ct/'
Save_Dir_mask = '/NAS/shared_data/for_VNLST/ft42/ct_public/unitochest/unitochest_nifti_mask/'

#--- Dataframe
df      = pd.read_csv(csv_file)
# Group by patient and exam
grouped = df.groupby(['patientID', 'exam'])

for (patient_id, exam_id), group in grouped:
    print(f"Processing patient {patient_id}, exam {exam_id}")
    
    # Sort slices
    group_sorted = group.sort_values('slice')
    
    # Read DICOM slices
    ct_slices = []
    for idx, row in group_sorted.iterrows():
        dcm_path = os.path.join(base_ct_dir, row['image'])
        ds = pydicom.dcmread(dcm_path)
        ct_slices.append(ds.pixel_array)
    
    ct_volume = np.stack(ct_slices, axis=0)
    ct_image = sitk.GetImageFromArray(ct_volume)
    
    # Set spacing (if available from DICOM)
    ds0 = pydicom.dcmread(os.path.join(base_ct_dir, group_sorted.iloc[0]['image']))
    spacing = [float(ds0.PixelSpacing[0]), float(ds0.PixelSpacing[1]), float(ds0.SliceThickness)]
    ct_image.SetSpacing(spacing)
    
    # Prepare mask volume
    mask_slices = []
    for idx, row in group_sorted.iterrows():
        if pd.notna(row['mask']):
            mask_path = os.path.join(base_mask_dir, row['mask'])
            mask_img = Image.open(mask_path).convert('L')
            mask_array = np.array(mask_img) > 0  # binary mask
        else:
            # Empty slice
            mask_array = np.zeros_like(ct_slices[0], dtype=np.uint8)
        mask_slices.append(mask_array.astype(np.uint8))
    
    mask_volume = np.stack(mask_slices, axis=0)
    mask_image = sitk.GetImageFromArray(mask_volume)
    mask_image.SetSpacing(spacing)
    
    # Save NIfTI files
    output_ct_path   = Save_Dir_ct   + f"unitochestPT{patient_id}_exam{exam_id}_0000.nii.gz"
    output_mask_path = Save_Dir_mask + f"unitochestPT{patient_id}_exam{exam_id}_mask.nii.gz"
    sitk.WriteImage(ct_image, output_ct_path)
    sitk.WriteImage(mask_image, output_mask_path)
    print(f"Saved: {output_ct_path}, {output_mask_path}")


