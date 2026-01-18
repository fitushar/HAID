# UniToChest Dataset Processing Pipeline - Complete Documentation

This document provides comprehensive documentation for the processing pipeline for the **UniToChest dataset**, a publicly available chest CT resource comprising 715 scans from 623 patients with expert-annotated lung nodule segmentation masks.

---

## 📂 Dataset Information

**Dataset Name**: UniToChest  
**Source**: Zenodo - Publicly available chest CT dataset  
**Reference**: Chaudhry et al. (2022) - ICIAP 2022  
**Total Scans**: 715 CT scans  
**Total Patients**: 623 unique patients  
**Original Data Source**: https://zenodo.org/records/5797912  
**Pre-processed Data Repository**: Available on Zenodo at https://zenodo.org/uploads/18285682  
**Metadata & Annotations**: All generated CSV files saved in local directory

### Dataset Splits
- **Training Set**: 579 scans from 501 patients (80.0%)
- **Validation Set**: 66 scans from 62 patients (9.9%)
- **Test Set**: 70 scans from 63 patients (10.1%)

---

## 🔄 Complete Processing Pipeline

### 1️⃣ **DICOM to NIfTI Conversion**
**Purpose**: Convert raw DICOM CT scans and PNG segmentation masks to unified NIfTI format

**Process**:
- Reads patient metadata from dataset CSV files (`train_dataset.csv`, `val_dataset.csv`, `test_dataset.csv`)
- Groups DICOM slices by patient ID and exam number
- Sorts slices by slice index for proper 3D volume reconstruction
- Uses pydicom to read DICOM CT slices
- Converts PNG masks to binary segmentation volumes
- Uses SimpleITK to create 3D volumes with proper spacing information
- Extracts spacing metadata from DICOM headers:
  - In-plane spacing from `PixelSpacing`
  - Through-plane spacing from `SliceThickness`

**Key Scripts**:
- `trainDataset_nifti.py` - Processes training set
- `valDataset_nifti.py` - Processes validation set  
- `testDataset_nifti.py` - Processes test set
- `Demo_Dicom_to_CT-HAID.ipynb` - Demonstration notebook

**Outputs**:
- CT images: `unitochest_nifti_ct/unitochestPT{PatientID}_exam{ExamID}_0000.nii.gz`
- Segmentation masks: `unitochest_nifti_mask/unitochestPT{PatientID}_exam{ExamID}_mask.nii.gz`

**File Naming Convention**:
```
unitochestPT{patient_id}_exam{exam_id}_0000.nii.gz  # CT scan
unitochestPT{patient_id}_exam{exam_id}_mask.nii.gz  # Segmentation mask
```

---

### 2️⃣ **Image Resampling to Standardized Spacing**
**Purpose**: Standardize image spacing across the entire dataset for consistent downstream processing

**Target Spacing**: `[0.703125, 0.703125, 1.25]` mm (X, Y, Z)

**Resampling Implementation**:

#### CT Image Resampling (`resampled_ct.sh`)
```bash
#!/bin/bash
docker exec -it ft42_g6xai bash -c "python resample_images.py \
  /path/to/unitochest_nifti_ct \
  /path/to/unitochest_nifti_ct_resampled \
  --spacing 0.703125 0.703125 1.25 \
  --start 0 --end 715 \
  --extension .nii.gz"
```

**Interpolation**: B-spline (preserves intensity gradients and Hounsfield Units)

#### Segmentation Mask Resampling (`resampled_mask.sh`)
```bash
#!/bin/bash
docker exec -it ft42_g6xai bash -c "python resample_images.py \
  /path/to/unitochest_nifti_mask \
  /path/to/unitochest_nifti_mask_resampled \
  --spacing 0.703125 0.703125 1.25 \
  --start 0 --end 715 \
  --is_label \
  --extension .nii.gz"
```

**Interpolation**: Nearest-neighbor (preserves discrete label values)

**Resampling Algorithm** (`resample_images.py`):
- Uses SimpleITK ResampleImageFilter
- Calculates output size based on spacing ratio:
  ```python
  out_size = [
      int(round(original_size[i] * (original_spacing[i] / out_spacing[i])))
      for i in range(3)
  ]
  ```
- Preserves spatial metadata (origin, direction cosines)
- Supports batch processing with start/end indices

**Outputs**:
- Resampled CT scans: `unitochest_nifti_ct_resampled/`
- Resampled masks: `unitochest_nifti_mask_resampled/`

---

### 3️⃣ **3D Bounding Box Annotation Extraction**
**Purpose**: Extract 3D bounding boxes from segmentation masks for object detection tasks

**Process**:
- Identifies all non-zero voxels in segmentation masks
- Computes min/max coordinates in voxel space (x, y, z)
- Converts center coordinates to world coordinate system (mm) using SimpleITK:
  - `center_world = image.TransformIndexToPhysicalPoint(center_voxel)`
- Calculates bounding box dimensions in mm:
  - Width (w), Height (h), Depth (d)
- Stores patient ID and file paths for reference

**Nodule Diameter Calculation**:
Diameter computed as 3D Euclidean diagonal:
```
diameter_mm = sqrt(w² + h² + d²)
```

**Outputs**:
- **File**: `filtered_unitochest_bounding_boxes_annotations.csv`
- **Columns**:
  - `Patient`: Patient ID with exam number
  - `ct_path`: Path to CT image
  - `mask_path`: Path to segmentation mask
  - `coordX`, `coordY`, `coordZ`: Center coordinates in world space (mm)
  - `w`, `h`, `d`: Bounding box dimensions (mm)
  - `diameter_mm`: 3D nodule diameter (mm)

---

### 4️⃣ **DICOM Metadata Integration**
**Purpose**: Merge imaging metadata with bounding box annotations for comprehensive dataset characterization

**DICOM Metadata Extracted**:
- **Patient Demographics**:
  - `PatientID`: Unique patient identifier
  - `PatientAge`: Age in years
  - `PatientSex`: Gender (F/M)
- **Acquisition Parameters**:
  - `Manufacturer`: Scanner vendor (GE MEDICAL SYSTEMS, Philips)
  - `ConvolutionKernel`: Reconstruction kernel (STANDARD, LUNG, etc.)
  - `SliceThickness`: Through-plane resolution (mm)
  - `PixelSpacing`: In-plane resolution (mm)
  - `KVP`: Tube voltage (kV)
  - `PatientPosition`: Patient positioning (HFS, FFS)

**Processing** (see `DataAnalysis.ipynb`):
- Loads train/val/test split CSV files with DICOM metadata
- Assigns split labels (Train, Validation, Test)
- Combines all splits into unified dataframe
- Extracts numeric age values from DICOM age strings
- Merges with bounding box annotations

**Outputs**:
- `unitochest_train_dataset_dicom_metadata.csv`
- `unitochest_val_dataset_dicom_metadata.csv`
- `unitochest_test_dataset_dicom_metadata.csv`
- `filtered_unitochest_bounding_boxes_annotations_metadata.csv`

---

### 5️⃣ **Demographic & Technical Summary Statistics**
**Purpose**: Generate comprehensive statistics for publication and dataset documentation

**Statistics Computed**:
- **Patient & Scan Counts**: Unique patients and total scans per split
- **Age Statistics**: Mean ± SD, age range (min-max)
- **Gender Distribution**: Female/Male counts and percentages
- **Scanner Manufacturers**: GE MEDICAL SYSTEMS vs Philips distribution
- **Reconstruction Kernels**: STANDARD, LUNG, and other kernel frequencies
- **Patient Positioning**: HFS (Head-First Supine) vs FFS (Feet-First Supine)

**Visualizations Created**:
1. **Age Distribution**: Histogram with KDE overlay by split
2. **Slice Thickness**: Violin plots with scatter overlay
3. **Manufacturer Distribution**: Count plot by split

**Key Findings** (Table S2):
- Mean patient age: 67.0 ± 10.2 years
- Gender: 40.0% Female, 60.0% Male
- Scanners: 76.2% GE MEDICAL SYSTEMS, 23.8% Philips
- Kernels: 49.8% STANDARD, 21.5% LUNG
- Positioning: 63.9% HFS, 36.1% FFS

**Output Files**:
- Summary tables printed in notebook
- Visualization: `unitochest_clinical_subplots.png`
- Individual plots: `age_distribution_by_split.png`, `slice_thickness_violin.png`, etc.

---

### 6️⃣ **Nodule Annotation Statistics & Characterization**
**Purpose**: Analyze derived 3D bounding box annotations and nodule size distributions

**Nodule Statistics Computed** (Table S3):
- **Total Annotations**: 8,321 nodules across all splits
  - Training: 7,260 nodules
  - Validation: 366 nodules
  - Test: 695 nodules
- **Diameter Statistics**:
  - Overall: 21.4 ± 20.2 mm (mean ± SD), median 16.42 mm
  - Training: 21.2 ± 19.7 mm, median 16.55 mm
  - Validation: 25.0 ± 24.6 mm, median 17.0 mm
  - Test: 22.1 ± 22.3 mm, median 15.44 mm

**Visualizations**:
1. **Violin Plots**: Distribution of nodule diameters by split with overlaid scatter points
2. **KDE Curves**: Kernel density estimation showing normalized size distributions

**Output Files**:
- `nodule_diameter_distribution_by_split.png`
- `nodule_diameter_kde_by_split.png`

---

### 7️⃣ **Diagnostic Dataset Preparation**
**Purpose**: Create annotation-level dataset for nodule classification and diagnostic tasks

**Process**:
- Assigns unique annotation IDs per nodule: `{PatientID}_exam{ExamID}_{AnnotationIndex}`
- Creates `UNIQUE_ANNOTATION_ID` column for each bounding box
- Formats for patch extraction and classification tasks
- Links spatial coordinates with clinical metadata

**Outputs**:
- `filtered_unitochest_bounding_boxes_annotations_metadata_nifty_name_lesionIdX.csv`
- Includes columns:
  - `UNIQUE_ANNOTATION_ID`: Unique identifier
  - `UNIQUE_ANNOTATION_ID_nifti`: NIfTI filename format
  - `annotation-idx`: Sequential annotation number per patient
  - Spatial coordinates and dimensions
  - Split information

---

## 📊 Complete Output Summary

| Output Type | File Name | Location | Description |
|------------|-----------|----------|-------------|
| **Converted CT Images** | `unitochestPT{ID}_exam{E}_0000.nii.gz` | `unitochest_nifti_ct/` | CT scans in NIfTI format |
| **Segmentation Masks** | `unitochestPT{ID}_exam{E}_mask.nii.gz` | `unitochest_nifti_mask/` | Binary lung nodule masks |
| **Resampled CT** | Same naming | `unitochest_nifti_ct_resampled/` | CT at 0.703125×0.703125×1.25mm |
| **Resampled Masks** | Same naming | `unitochest_nifti_mask_resampled/` | Resampled segmentation masks |
| **Bounding Boxes** | `filtered_unitochest_bounding_boxes_annotations.csv` | Working directory | 3D bounding box annotations |
| **DICOM Metadata (Train)** | `unitochest_train_dataset_dicom_metadata.csv` | Working directory | Training set metadata |
| **DICOM Metadata (Val)** | `unitochest_val_dataset_dicom_metadata.csv` | Working directory | Validation set metadata |
| **DICOM Metadata (Test)** | `unitochest_test_dataset_dicom_metadata.csv` | Working directory | Test set metadata |
| **Merged Annotations** | `filtered_unitochest_bounding_boxes_annotations_metadata.csv` | Working directory | Bounding boxes + DICOM metadata |
| **Diagnostic Dataset** | `filtered_unitochest_bounding_boxes_annotations_metadata_nifty_name_lesionIdX.csv` | Working directory | Annotation-level classification dataset |

---

## 🔬 Final Dataset Characteristics

### Cohort Summary
- **Total Patients**: 623 unique patients
- **Total CT Scans**: 715
- **Total Nodule Annotations**: 8,321 expert-annotated nodules
- **Image Modality**: CT (Computed Tomography)
- **Segmentation Type**: Expert manual annotations
- **Annotation Density**: ~11.6 nodules per scan on average

### Image Properties
- **Original Spacing**: Variable across patients
- **Resampled Spacing**: 0.703125 × 0.703125 × 1.25 mm³
- **Image Format**: NIfTI (.nii.gz)
- **Intensity Unit**: Hounsfield Units (HU)

### Clinical & Technical Variables
- **Age Range**: Variable (see Table S2)
- **Gender Distribution**: 40% Female, 60% Male
- **Scanner Manufacturers**: 
  - GE MEDICAL SYSTEMS (76.2%)
  - Philips (23.8%)
- **Reconstruction Kernels**:
  - STANDARD (49.8%)
  - LUNG (21.5%)
  - Others
- **Patient Positioning**:
  - HFS - Head-First Supine (63.9%)
  - FFS - Feet-First Supine (36.1%)

### Dataset Split
- **Training**: 579 scans, 501 patients, 7,260 nodules (80.0%)
- **Validation**: 66 scans, 62 patients, 366 nodules (9.9%)
- **Test**: 70 scans, 63 patients, 695 nodules (10.1%)
- **Split Method**: Pre-defined by dataset creators

### Nodule Size Distribution
- **Overall Diameter**: 21.4 ± 20.2 mm (mean ± SD)
- **Median Diameter**: 16.42 mm
- **Range**: Variable small to large nodules
- **Distribution**: Right-skewed (more small nodules)

---

## ⚙️ Software Dependencies

### Core Libraries
```python
# Medical Image I/O
SimpleITK >= 2.0.0          # Medical image reading/writing/processing
nibabel >= 3.2.0            # NIfTI file handling
pydicom >= 2.0.0            # DICOM file handling

# Data Processing
pandas >= 1.3.0             # DataFrame operations
numpy >= 1.20.0             # Numerical operations
Pillow >= 8.0.0             # PNG mask loading

# Visualization
matplotlib >= 3.4.0         # Plotting
seaborn >= 0.11.0           # Statistical visualizations

# Utilities
tabulate                    # Table formatting
```

### Installation
```bash
pip install SimpleITK nibabel pydicom pandas numpy Pillow matplotlib seaborn tabulate
```

### Docker Environment
The resampling scripts use Docker for reproducible execution:
```bash
docker exec -it ft42_g6xai bash -c "python resample_images.py ..."
```

---

## 📖 Citation & License

### Dataset Citation
If you use this dataset or processing pipeline, please cite:

**Original UniToChest Dataset**:
> Chaudhry, H. A. H. et al. (2022). "Unitochest: A lung image dataset for segmentation of cancerous nodules on CT scans." In *International Conference on Image Analysis and Processing* (ICIAP 2022), pp. 185-196. Springer.  
> Dataset available at: https://zenodo.org/records/5797912

### Pre-processed Data
Pre-processed and resampled CT images with 3D bounding box annotations are available at:
**Zenodo Repository**: https://zenodo.org/uploads/18285682

---

## 🔒 Data Usage & Ethics

### Data Usage Agreement
This dataset is publicly available for research purposes. Users must:
- Acknowledge the dataset creators
- Follow ethical guidelines for medical data usage
- Not attempt to re-identify patients

### IRB & Privacy
- All data is de-identified
- Original study approved by institutional review board
- No protected health information (PHI) included

---

## 📝 Processing Notes & Recommendations

### Key Features of UniToChest Dataset
1. **High Annotation Density**: Average of ~11.6 nodules per scan
2. **Expert Annotations**: Manually delineated by radiologists
3. **Diverse Scanner Types**: Both GE and Philips scanners represented
4. **Multiple Kernels**: Various reconstruction kernels for robustness
5. **Pre-defined Splits**: Consistent train/val/test splits for reproducibility

### Recommendations for Use
1. **Always use resampled images** for model training to ensure consistent spatial resolution
2. **Account for high nodule density** when designing detection models
3. **Verify bounding box alignment** if using different coordinate systems
4. **Apply appropriate lung window** [-1000, 500] HU for visualization and preprocessing
5. **Consider scanner manufacturer** as a potential confounding variable in analysis

### Known Characteristics
1. **Variable slice thickness** in original data → resampling required
2. **Multiple nodules per scan** → requires multi-instance detection
3. **Pre-defined splits** → use provided splits for fair comparison with other studies
4. **Binary segmentation masks** → single class (nodule vs background)

---

## 👨‍💻 Processing Information

**Processing Date**: January 2026  
**Processed By**: Radiology AI Lab  
**Processing Scripts Version**: 1.0  
**Processing Environment**: Python 3.8+, Docker, Linux  
**Hardware Requirements**: Minimum 16GB RAM, 200GB disk space for full dataset

---

## 🔗 Related Resources

- **Original Dataset**: https://zenodo.org/records/5797912
- **Original Publication**: Chaudhry et al., ICIAP 2022
- **Pre-processed Data**: https://zenodo.org/uploads/18285682
- **Processing Notebooks**: 
  - `Demo_Dicom_to_CT-HAID.ipynb` - DICOM to NIfTI conversion demo
  - `DataAnalysis.ipynb` - Statistical analysis and visualization

---

## 📂 Repository Structure

```
UnitoChest/
├── Demo_Dicom_to_CT-HAID.ipynb              # DICOM to NIfTI conversion demo
├── DataAnalysis.ipynb                        # Statistical analysis & visualization
├── trainDataset_nifti.py                     # Training set conversion script
├── valDataset_nifti.py                       # Validation set conversion script
├── testDataset_nifti.py                      # Test set conversion script
├── resample_images.py                        # Resampling utility script
├── resampled_ct.sh                           # Bash script for CT resampling
├── resampled_mask.sh                         # Bash script for mask resampling
├── unitochest_nifti_ct/                      # Converted CT images
├── unitochest_nifti_mask/                    # Converted segmentation masks
├── filtered_unitochest_bounding_boxes_annotations.csv          # Bounding box annotations
├── unitochest_train_dataset_dicom_metadata.csv                 # Training metadata
├── unitochest_val_dataset_dicom_metadata.csv                   # Validation metadata
├── unitochest_test_dataset_dicom_metadata.csv                  # Test metadata
├── filtered_unitochest_bounding_boxes_annotations_metadata.csv # Merged annotations
└── UNITOCHEST_PROCESSING_DOCUMENTATION.md    # This documentation
```

---

## 📊 Summary Tables & Figures

### Table S2: Patient Demographics and Clinical Characteristics
Comprehensive demographic and technical characteristics including age, gender, scanner type, reconstruction kernel, and patient positioning across train/validation/test splits.

### Table S3: Nodule Annotation Statistics
Summary of 8,321 derived 3D bounding box annotations with diameter statistics (mean ± SD, median) across dataset splits.

### Figure S3: Clinical & Technical Metadata Overview
- Left: Age distribution by split with KDE overlay
- Middle: Slice thickness violin plots with scatter points
- Right: Scanner manufacturer distribution

### Figure S4: Example Annotation Visualization
Axial CT slice showing expert segmentation (red) and derived 3D bounding box (yellow) with magnified tumor view.

### Figure S5: Nodule Diameter Distribution
- (a) Violin plots with box plots and scatter points
- (b) KDE curves showing normalized diameter distributions by split

---

## 📦 Zenodo Upload Description Template

**Copy and paste this text into your Zenodo upload description:**

---

### UniToChest Dataset: Converted NIfTI CT Scans with Expert-Annotated Lung Nodule Segmentation Masks

**Description:**

This dataset contains converted NIfTI format CT scans and expert-annotated segmentation masks from the UniToChest collection, a publicly available chest CT resource. The original UniToChest dataset comprises 715 scans from 623 patients with manual lung nodule delineations by expert radiologists. This upload provides the data in standardized NIfTI format for convenient medical imaging research.

**What's Included:**

1. **Converted CT Images** (715 scans)
   - Format: NIfTI (.nii.gz)
   - File naming: `unitochestPT{PatientID}_exam{ExamID}_0000.nii.gz`
   - Original DICOM spacing preserved
   - Hounsfield Unit intensity values maintained

2. **Expert-Annotated Segmentation Masks** (715 masks)
   - Binary masks indicating lung nodule regions
   - File naming: `unitochestPT{PatientID}_exam{ExamID}_mask.nii.gz`
   - Aligned with corresponding CT scans
   - Same spatial resolution as CT images

3. **Pre-defined Dataset Splits**
   - Training set: 579 scans from 501 patients (80%)
   - Validation set: 66 scans from 62 patients (10%)
   - Test set: 70 scans from 63 patients (10%)

4. **DICOM Metadata CSV Files**
   - Patient demographics (age, gender)
   - Acquisition parameters (manufacturer, kernel, slice thickness)
   - Split assignments for reproducibility

**Conversion Process:**

Raw DICOM CT slices and PNG segmentation masks were converted to unified NIfTI format using SimpleITK and nibabel. The conversion process:
- Reconstructed 3D volumes from 2D DICOM slices sorted by slice index
- Extracted spacing information from DICOM headers (PixelSpacing, SliceThickness)
- Converted PNG masks to binary 3D segmentation volumes
- Preserved spatial metadata (origin, spacing, direction)

Complete processing code and detailed documentation available at: [GitHub repository link]

**Intended Use:**

- Lung nodule detection and segmentation
- 3D medical image object detection
- Multi-instance learning (average ~11.6 nodules per scan)
- CAD (Computer-Aided Detection) system development
- Deep learning model training for chest CT analysis
- Medical image segmentation benchmarking

**Dataset Statistics:**

- **Total patients**: 623 unique patients
- **Total CT scans**: 715
- **Total nodule annotations**: 8,321 expert-annotated nodules
- **Annotation density**: ~11.6 nodules per scan (average)
- **Image modality**: CT (Computed Tomography)
- **Training set**: 579 scans, 501 patients, 7,260 nodules
- **Validation set**: 66 scans, 62 patients, 366 nodules
- **Test set**: 70 scans, 63 patients, 695 nodules

**Clinical & Technical Characteristics:**

- **Patient age**: 67.0 ± 10.2 years (mean ± SD)
- **Gender distribution**: 40% Female, 60% Male
- **Scanner manufacturers**: 76.2% GE MEDICAL SYSTEMS, 23.8% Philips
- **Reconstruction kernels**: 49.8% STANDARD, 21.5% LUNG, others
- **Patient positioning**: 63.9% HFS (Head-First Supine), 36.1% FFS (Feet-First Supine)
- **Nodule size**: 21.4 ± 20.2 mm diameter (mean ± SD), median 16.42 mm

**File Structure:**

```
unitochest_nifti_converted.zip
├── unitochest_nifti_ct/                           # 715 CT scans
│   ├── unitochestPT0001_exam1_0000.nii.gz
│   ├── unitochestPT0002_exam1_0000.nii.gz
│   └── ...
├── unitochest_nifti_mask/                         # 715 segmentation masks
│   ├── unitochestPT0001_exam1_mask.nii.gz
│   ├── unitochestPT0002_exam1_mask.nii.gz
│   └── ...
├── unitochest_train_dataset_dicom_metadata.csv    # Training set metadata
├── unitochest_val_dataset_dicom_metadata.csv      # Validation set metadata
├── unitochest_test_dataset_dicom_metadata.csv     # Test set metadata
└── README.txt                                      # Quick start guide
```

**File Format Details:**

- **Image format**: NIfTI-1 (.nii.gz compressed)
- **CT intensity**: Hounsfield Units (HU), typically ranging from -1024 to +3071
- **Mask values**: Binary (0 = background, 1 = nodule)
- **Coordinate system**: RAS (Right-Anterior-Superior) standard
- **Data type**: CT images (int16), Masks (uint8)

**Resampled Version:**

A resampled version with standardized spacing (0.703125 × 0.703125 × 1.25 mm³) and derived 3D bounding box annotations is available separately at: https://zenodo.org/uploads/18285682

**Citation:**

If you use this converted dataset, please cite:

1. **Original UniToChest dataset:**
   Chaudhry, H. A. H. et al. (2022). "Unitochest: A lung image dataset for segmentation of cancerous nodules on CT scans." In *International Conference on Image Analysis and Processing* (ICIAP 2022), pp. 185-196. Springer. DOI/URL: https://zenodo.org/records/5797912

2. **This converted NIfTI version (optional but appreciated):**
   [Your Name/Lab] (2026). UniToChest Dataset: Converted NIfTI CT Scans with Expert-Annotated Lung Nodule Segmentation Masks. Zenodo. https://zenodo.org/uploads/18285682

**Related Links:**

- Original UniToChest dataset: https://zenodo.org/records/5797912
- Original publication: Chaudhry, H. A. H. et al., ICIAP 2022
- Processing code & documentation: [Your GitHub repository]
- Resampled version with 3D bounding boxes: https://zenodo.org/uploads/18285682

**License:**

This converted dataset inherits the license from the original UniToChest collection. All data is de-identified for research use.

**Technical Support:**

For issues with file format, loading instructions, or data quality questions, please refer to:
- Processing documentation in the GitHub repository
- NIfTI format specification: https://nifti.nimh.nih.gov/
- SimpleITK documentation: https://simpleitk.org/

**Loading Examples:**

```python
# Using SimpleITK
import SimpleITK as sitk
ct_image = sitk.ReadImage("unitochestPT0001_exam1_0000.nii.gz")
ct_array = sitk.GetArrayFromImage(ct_image)
spacing = ct_image.GetSpacing()  # (x, y, z) in mm

# Using nibabel
import nibabel as nib
mask_img = nib.load("unitochestPT0001_exam1_mask.nii.gz")
mask_array = mask_img.get_fdata()
affine = mask_img.affine
```

**Quality Assurance:**

- All CT scans verified for proper 3D volume reconstruction
- Segmentation masks confirmed to align spatially with CT images
- Metadata validated against original DICOM headers
- No missing or corrupted files
- Consistent file naming across entire dataset

**Use Cases in Literature:**

This dataset is suitable for research published in:
- Medical image analysis journals
- Computer-aided diagnosis systems
- Deep learning in radiology
- Lung cancer screening algorithms
- 3D object detection benchmarks

**Keywords:** lung nodules, chest CT, segmentation masks, NIfTI format, medical imaging, UniToChest, lung cancer, object detection, computer-aided detection, radiomics, deep learning, CT imaging

---

**Note:** Remember to replace `[GitHub repository link]` and `[Your Name/Lab]` with actual values. The Zenodo repository is at: https://zenodo.org/uploads/18285682

---

**End of Documentation**

For questions or issues with this processing pipeline, please open an issue in the repository or contact the maintainer.

---

**Last Updated**: January 17, 2026
