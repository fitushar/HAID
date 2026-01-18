import os
import argparse
import numpy as np
import SimpleITK as sitk

def resample_img(itk_image, out_spacing, is_label=False):
    # Resample images to the specified spacing
    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()

    out_size = [
        int(np.round(original_size[0] * (original_spacing[0] / out_spacing[0]))),
        int(np.round(original_size[1] * (original_spacing[1] / out_spacing[1]))),
        int(np.round(original_size[2] * (original_spacing[2] / out_spacing[2])))
    ]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    return resample.Execute(itk_image)

def process_folder(input_folder, output_folder, new_spacing, start_idx, end_idx, is_label=False, extension=".nii.gz"):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get a sorted list of files with the desired extension
    input_files = sorted([f for f in os.listdir(input_folder) if f.endswith(extension)])

    # Apply the range
    input_files = input_files[start_idx:end_idx + 1]

    for filename in input_files:
        input_path = os.path.join(input_folder, filename)

        # Read the image
        image = sitk.ReadImage(input_path)

        # Resample the image
        resampled_image = resample_img(image, new_spacing, is_label)

        # Construct the output filename (keep the same name)
        output_path = os.path.join(output_folder, filename)

        # Save the resampled image
        sitk.WriteImage(resampled_image, output_path)
        print(f"Saved resampled image to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Resample 3D images with a given spacing.")
    parser.add_argument("input_folder", type=str, help="Path to input folder.")
    parser.add_argument("output_folder", type=str, help="Path to output folder.")
    parser.add_argument("--spacing", type=float, nargs=3, required=True, help="Desired spacing (x y z).")
    parser.add_argument("--start", type=int, default=0, help="Start index (default: 0).")
    parser.add_argument("--end", type=int, default=None, help="End index (default: all files).")
    parser.add_argument("--is_label", action="store_true", help="Flag if input is label (nearest neighbor interpolation).")
    parser.add_argument("--extension", type=str, default=".nii.gz", help="File extension to process (default: .nii.gz).")

    args = parser.parse_args()

    if args.end is None:
        args.end = len([f for f in os.listdir(args.input_folder) if f.endswith(args.extension)]) - 1

    process_folder(
        args.input_folder,
        args.output_folder,
        args.spacing,
        args.start,
        args.end,
        args.is_label,
        args.extension
    )

if __name__ == "__main__":
    main()
