import SimpleITK as sitk
import os

# Input and output folders
input_folder = "/NAS/shared_data/for_VNLST/ft42/ct_public/LNDbv4/LNDbv4_cts/"
output_folder = "/NAS/shared_data/for_VNLST/ft42/ct_public/LNDbv4/LNDbv4_cts_nifti/"

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop over all .mhd files
for fname in os.listdir(input_folder):
    if fname.endswith(".mhd"):
        input_path = os.path.join(input_folder, fname)
        output_fname = fname.replace(".mhd", ".nii.gz")
        output_path = os.path.join(output_folder, output_fname)
        
        # Read and write using SimpleITK
        img = sitk.ReadImage(input_path)
        sitk.WriteImage(img, output_path)
        print(f"Converted {fname} to {output_fname}")
