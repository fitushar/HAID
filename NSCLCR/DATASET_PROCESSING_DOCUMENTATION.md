# NSCLC-Radiomics Dataset Processing Pipeline - Complete Documentation

This document provides comprehensive documentation for the processing pipeline implemented in `NSCLCR_HAID_processing.ipynb`, which processes the **NSCLC-Radiomics dataset** comprising pre-treatment CT scans from 422 patients diagnosed with non-small cell lung cancer (NSCLC).

---

## 📂 Dataset Information

**Dataset Name**: NSCLC-Radiomics  
**Source**: TCIA (The Cancer Imaging Archive)  
**Reference**: Aerts, H. J. W. L. et al. *Data From NSCLC-Radiomics*, doi: 10.7937/K9/TCIA.2015.PF0M9REI  
**Initial Patients**: 422  
**Final Cohort**: 421 patients (1 excluded due to segmentation mask errors)
**Orifinal Data Source**: https://www.cancerimagingarchive.net/collection/nsclc-radiomics/ 
**Pre-processed Data Repository**: Available on Zenodo at **[xxx]** (replace with your DOI)  
**Metadata & Annotations**: All generated CSV files saved in `./metadata/` folder

---

## 🔄 Complete Processing Pipeline

### 1️⃣ **DICOM to NIfTI Conversion**
**Purpose**: Convert raw DICOM CT scans and DICOM-SEG segmentation masks to NIfTI format for easier processing

**Process**:
- Reads metadata from TCIA manifest CSV (`metadata.csv`)
- Extracts Study UID and Series UID for each patient
- Uses SimpleITK ImageSeriesReader to load DICOM CT series
- Uses pydicom_seg to read DICOM segmentation files
- Converts and saves as NIfTI format with standardized naming

**Outputs**:
- CT images: `NSCLC-Radiomics-NIFTI/{PatientID}/NSCLC_{ID}_0000.nii.gz`
- Individual segmentation masks: `seg-{StructureName}.nii.gz`
  - `seg-GTV-1.nii.gz` (Gross Tumor Volume)
  - `seg-Esophagus.nii.gz`
  - `seg-Heart.nii.gz`
  - `seg-Lung-Left.nii.gz`
  - `seg-Lung-Right.nii.gz`
  - `seg-Spinal-Cord.nii.gz`

---

### 2️⃣ **Segmentation Mask Combination**
**Purpose**: Combine multiple single-label segmentation files into unified multi-label segmentation masks

**Process**:
- Reads all individual segmentation files per patient
- Assigns unique integer labels to each structure:
  - Label 1: Esophagus
  - Label 2: GTV-1 (Gross Tumor Volume)
  - Label 3: Heart
  - Label 4: Lung-Left
  - Label 5: Lung-Right
  - Label 6: Spinal-Cord
- Creates single combined mask using `np.maximum()` to avoid overlap
- Preserves spatial information (origin, spacing, direction)

**Outputs**:
- Combined mask: `segmentation.nii.gz` in each patient folder

---

### 3️⃣ **Visualization & Quality Control**
**Purpose**: Visual inspection of CT scans with segmentation overlays for quality assurance

**Visualizations Created**:
- **Axial view**: CT slice at maximum GTV-1 extent
- **Coronal view**: Front-to-back cross-section
- **Sagittal view**: Left-to-right cross-section
- Overlay of all segmentation labels with transparency
- Separate visualization of CT alone, CT+segmentation, and CT+bounding box

**Quality Checks**:
- Validates GTV-1 presence in all patients
- Confirms spatial alignment between CT and segmentation
- Identifies outliers or annotation errors

---

### 4️⃣ **3D Bounding Box Annotation Extraction**
**Purpose**: Extract 3D bounding boxes from GTV-1 segmentation masks for object detection tasks

**Process**:
- Identifies all voxels with label=2 (GTV-1)
- Computes min/max coordinates in voxel space (x, y, z)
- Converts center coordinates to world coordinate system (mm) using:
  - `center_world = image.TransformIndexToPhysicalPoint(center_voxel)`
- Calculates bounding box dimensions in mm:
  - Width (w), Height (h), Depth (d)
- Stores CT and segmentation file paths for reference

**Outputs**:
- **File**: `./metadata/NSCLC_bounding_boxes_annotations.csv`
- **Columns**:
  - `Patient`: Patient ID
  - `ct_path`: Relative path to CT image
  - `seg_path`: Relative path to segmentation mask
  - `Label`: Segmentation label (2 for GTV-1)
  - `coordX`, `coordY`, `coordZ`: Center coordinates in world space (mm)
  - `w`, `h`, `d`: Bounding box dimensions (mm)

---

### 5️⃣ **Annotation Validation**
**Purpose**: Visual verification that bounding boxes accurately capture tumor regions

**Process**:
- Loads CT images and segmentation masks
- Overlays bounding boxes on axial slices
- Displays full CT slice and zoomed 124×124×124mm region around tumor
- Merges with clinical metadata to show histology labels
- Validates alignment in original image space

**Visualizations**:
- Full axial CT slice with bounding box overlay
- Zoomed tumor region (124×124 mm) with bounding box
- Segmentation mask overlay with transparency
- Histology label annotation

---

### 6️⃣ **Image Resampling**
**Purpose**: Standardize image spacing across the dataset for consistent processing

**Target Spacing**: `[0.703125, 0.703125, 1.25]` mm (X, Y, Z)

**Process**:
- Uses SimpleITK ResampleImageFilter
- **For CT images**:
  - Interpolation: B-spline (smooth, preserves intensity gradients)
  - Maintains Hounsfield Unit accuracy
- **For segmentation masks**:
  - Interpolation: Nearest-neighbor (preserves discrete labels)
  - Prevents label mixing at boundaries
- Recalculates output size based on spacing ratio
- Preserves origin and direction cosines

**Outputs**:
- Resampled CT images (stored on NAS in notebook paths)
- Resampled segmentation masks (separate directory)

---

### 7️⃣ **Post-Resampling Verification**
**Purpose**: Confirm that bounding box annotations remain valid after resampling

**Process**:
- Loads resampled CT images
- Applies original world-coordinate bounding boxes
- Transforms world coordinates back to resampled voxel space
- Verifies spatial alignment with visual inspection
- Confirms tumor regions are correctly localized

**Validation**:
- Bounding boxes overlay correctly on resampled images
- No spatial drift or misalignment detected
- Tumor dimensions preserved in world coordinates

---

### 8️⃣ **Clinical Metadata Integration & Dataset Splitting**
**Purpose**: Merge clinical data with annotations and create stratified train/val/test splits

**Clinical Variables Included**:
- **Demographics**: Age, Gender
- **TNM Staging**: Clinical T-stage, N-stage, M-stage, Overall stage
- **Histology**: Adenocarcinoma, Squamous cell carcinoma, Large cell, NOS, Unknown

**Splitting Strategy**:
- **Method**: Stratified split by histological subtype
- **Ratios**: 80% Training / 10% Validation / 10% Test
- **Random Seed**: 42 (for reproducibility)
- **Handling Missing Data**: Missing histology labeled as "unknown"

**Process**:
- Merges `NSCLC_bounding_boxes_annotations.csv` with `NSCLC-Radiomics-Lung1.clinical-version3-Oct-2019.csv`
- Groups by histology type
- Applies `train_test_split` within each histology group
- Adds `fitSplit` column indicating train/validation/test

**Outputs**:
- `./metadata/NSCLCRadiomics_merged_with_fitSplit.csv` (complete dataset with split labels)
- `./metadata/NSCLCRadiomics_train_split.csv` (training subset)
- `./metadata/NSCLCRadiomics_validation_split.csv` (validation subset)
- `./metadata/NSCLCRadiomics_test_split.csv` (test subset)

---

### 9️⃣ **Demographic & Clinical Summary Tables**
**Purpose**: Generate comprehensive statistics for publication and dataset documentation

**Statistics Computed**:
- **Patient counts**: Unique patients per split
- **Age**: Mean ± SD, Maximum age
- **Gender distribution**: Female/Male counts and percentages
- **TNM staging distribution**: T, N, M, and Overall stage frequencies
- **Histology distribution**: Counts per subtype
- **Nodule characteristics**: 
  - Diameter computed as: `sqrt(w² + h² + d²)`
  - Mean ± SD diameter per split and histology type

**Visualizations**:
- Violin plots of nodule diameter by histology
- Bar charts of demographic distributions
- Age histograms with KDE overlays
- Combined subplot figures for publication

**Outputs**:
- `./metadata/NSCLCRadiomics_clinical_summary_table.csv`
- Publication-ready figures: `violin_nodule_size_by_histology.png`

---

### 🔟 **Dataset Descriptor JSON Generation**

#### **A. Object Detection Dataset**
**Purpose**: Format for 3D nodule detection models (e.g., YOLO, Faster R-CNN)

**JSON Structure**:
```json
{
  "name": "NSCLCRadiomics Detection Dataset",
  "numTraining": X,
  "numValidation": Y,
  "numTest": Z,
  "training": [
    {
      "image": "NSCLC_Radiomics_NIFTI_resampled/NSCLC_001_0000.nii.gz",
      "box": [[coordX, coordY, coordZ, w, h, d]],
      "label": [0]
    }
  ],
  "validation": [...],
  "testing": [...]
}
```

**Output**: `./metadata/NSCLCRadiomics_fold1.json`

---

#### **B. Generative Modeling / Diffusion Dataset**
**Purpose**: List of CT images for unconditional synthesis or diffusion models

**JSON Structure**:
```json
{
  "name": "Experiments_NSCLCRadiomics_512xy_256z_111p25m",
  "description": "NSCLCRadiomics Dataset",
  "tensorImageSize": "3D",
  "file_ending": ".nii.gz",
  "channel_names": {"0": "CT"},
  "numTraining": 421,
  "training": [
    {"image": "NSCLC_Radiomics_NIFTI_resampled/NSCLC_001_0000.nii.gz"}
  ]
}
```

**Output**: `./metadata/Experiments_NSCLCRadiomics_512xy_256z_111p25m.json`

---

#### **C. Classification / Diagnostic Dataset**
**Purpose**: Annotation-level CSV for histology classification tasks

**Process**:
- Assigns unique annotation IDs: `{PatientID}_{AnnotationIndex}`
- Links each nodule to its histology label
- Includes split information (train/val/test)
- Stores bounding box coordinates and dimensions

**Columns**:
- `UNIQUE_ANNOTATION_ID`: Unique identifier per nodule
- `nifti_name`: CT filename
- `coordX`, `coordY`, `coordZ`: Center coordinates
- `w`, `h`, `d`: Dimensions
- `lesion_level_GT`: Ground truth label
- `histology`: Histological subtype
- `Split`: train/validation/test
- Clinical metadata columns

**Output**: `./metadata/NSCLCRadiomics_bounding_boxes_annotations_metadata_trvalts.csv`

---

## 📊 Complete Output Summary

| Output Type | File Name | Location | Description |
|------------|-----------|----------|-------------|
| **Converted Images** | `NSCLC_{ID}_0000.nii.gz` | `NSCLC-Radiomics-NIFTI/{PatientID}/` | Original CT scans in NIfTI format |
| **Combined Masks** | `segmentation.nii.gz` | `NSCLC-Radiomics-NIFTI/{PatientID}/` | Multi-label segmentation masks |
| **Resampled CT** | `NSCLC_{ID}_0000.nii.gz` | External NAS path | CT scans at 0.703125×0.703125×1.25mm |
| **Resampled Masks** | `NSCLC_{ID}_0000.nii.gz` | External NAS path | Resampled segmentation masks |
| **Bounding Boxes** | `NSCLC_bounding_boxes_annotations.csv` | `./metadata/` | 3D bounding box annotations |
| **Train Split** | `NSCLCRadiomics_train_split.csv` | `./metadata/` | Training set (80%) |
| **Validation Split** | `NSCLCRadiomics_validation_split.csv` | `./metadata/` | Validation set (10%) |
| **Test Split** | `NSCLCRadiomics_test_split.csv` | `./metadata/` | Test set (10%) |
| **Merged Dataset** | `NSCLCRadiomics_merged_with_fitSplit.csv` | `./metadata/` | Complete dataset with split labels |
| **Clinical Summary** | `NSCLCRadiomics_clinical_summary_table.csv` | `./metadata/` | Summary statistics table |
| **Detection JSON** | `NSCLCRadiomics_fold1.json` | `./metadata/` | Object detection dataset descriptor |
| **Generative JSON** | `Experiments_NSCLCRadiomics_512xy_256z_111p25m.json` | `./metadata/` | Diffusion/generation dataset list |
| **Classification CSV** | `NSCLCRadiomics_bounding_boxes_annotations_metadata_trvalts.csv` | `./metadata/` | Annotation-level classification dataset |

---

## 🔬 Final Dataset Characteristics

### Cohort Summary
- **Total Patients**: 421
- **Total Nodule Annotations**: 421 (one GTV-1 per patient)
- **Image Modality**: CT (Computed Tomography)
- **Segmentation Type**: Manual delineation by radiation oncologist

### Image Properties
- **Original Spacing**: Variable across patients
- **Resampled Spacing**: 0.703125 × 0.703125 × 1.25 mm³
- **Image Format**: NIfTI (.nii.gz)
- **Intensity Unit**: Hounsfield Units (HU)

### Clinical Variables
- **Age**: Mean ± SD (years)
- **Gender**: Female, Male
- **TNM Staging**: Clinical T, N, M stages
- **Overall Stage**: I, II, III, IV
- **Histological Subtypes**:
  - Adenocarcinoma
  - Squamous cell carcinoma
  - Large cell carcinoma
  - NOS (Not Otherwise Specified)
  - Unknown

### Dataset Split
- **Training**: 337 patients (80%)
- **Validation**: 42 patients (10%)
- **Test**: 42 patients (10%)
- **Stratification**: By histological subtype

---

## ⚙️ Software Dependencies

### Core Libraries
```python
# Medical Image I/O
SimpleITK >= 2.0.0          # Medical image reading/writing/processing
pydicom >= 2.0.0            # DICOM file handling
pydicom-seg                 # DICOM segmentation reading

# Data Processing
pandas >= 1.3.0             # DataFrame operations
numpy >= 1.20.0             # Numerical operations

# Visualization
matplotlib >= 3.4.0         # Plotting
seaborn >= 0.11.0           # Statistical visualizations
opencv-python >= 4.5.0      # Image processing for visualization

# Machine Learning
scikit-learn >= 0.24.0      # Dataset splitting

# Utilities
tqdm                        # Progress bars
tabulate                    # Table formatting
```

### Installation
```bash
pip install SimpleITK pydicom pydicom-seg pandas numpy matplotlib seaborn opencv-python scikit-learn tqdm tabulate
```

---

## 📖 Citation & License

### Dataset Citation
If you use this dataset or processing pipeline, please cite:

**Primary Reference**:
> Aerts, H. J. W. L. et al. (2015). *Data From NSCLC-Radiomics*.  
> The Cancer Imaging Archive.  
> DOI: [10.7937/K9/TCIA.2015.PF0M9REI](https://doi.org/10.7937/K9/TCIA.2015.PF0M9REI)

### Original Publication
> Aerts, H. J. W. L. et al. (2014). *Decoding tumour phenotype by noninvasive imaging using a quantitative radiomics approach*.  
> Nature Communications, 5, 4006.  
> DOI: [10.1038/ncomms5006](https://doi.org/10.1038/ncomms5006)

### Pre-processed Data
Pre-processed and resampled CT images with annotations are available at:
**Zenodo Repository**: [xxx] (replace with your DOI after upload)

---

## 🔒 Data Usage & Ethics

### TCIA Data Usage Agreement
This dataset is publicly available through TCIA (The Cancer Imaging Archive) under the Creative Commons Attribution 3.0 Unported License. Users must:
- Acknowledge TCIA and the dataset creators
- Follow ethical guidelines for medical data usage
- Not attempt to re-identify patients

---
## 📝 Processing Notes & Recommendations

### Known Issues
1. **Patient LUNG1-128**: Excluded from final cohort due to missing/corrupted segmentation mask
2. **Missing Histology**: Some patients lack histology information → labeled as "unknown"
3. **Spacing Variability**: Original CT scans have variable spacing → resampling required for uniform analysis

### Recommendations for Use
1. **Verify bounding box alignment** if using different coordinate systems


---

## 👨‍💻 Processing Information

**Processing Date**: January 2026  
**Processed By**: Fakrul Islam Tushar, PhD 
**Notebook Version**: 1.0  
**Processing Environment**: Python 3.8+, Windows/Linux  
**Hardware Requirements**: Minimum 16GB RAM, 100GB disk space for full dataset

---

## 🔗 Related Resources

- **TCIA Portal**: https://www.cancerimagingarchive.net/
- **Dataset DOI**: https://doi.org/10.7937/K9/TCIA.2015.PF0M9REI
- **Original Publication**: https://doi.org/10.1038/ncomms5006
- **Pre-processed Data**: 
- **Processing Notebook**: `NSCLCR_HAID_processing.ipynb`

---

## 📂 Repository Structure

```
HAID/NSCLCR/
├── NSCLCR_HAID_processing.ipynb          # Main processing notebook
├── DATASET_PROCESSING_DOCUMENTATION.md   # This documentation file
├── metadata/                             # All CSV and JSON outputs
│   ├── NSCLC_bounding_boxes_annotations.csv
│   ├── NSCLCRadiomics_train_split.csv
│   ├── NSCLCRadiomics_validation_split.csv
│   ├── NSCLCRadiomics_test_split.csv
│   ├── NSCLCRadiomics_merged_with_fitSplit.csv
│   ├── NSCLCRadiomics_clinical_summary_table.csv
│   ├── NSCLCRadiomics_fold1.json
│   ├── Experiments_NSCLCRadiomics_512xy_256z_111p25m.json
│   └── NSCLCRadiomics_bounding_boxes_annotations_metadata_trvalts.csv
├── NSCLC-Radiomics-NIFTI/                # Converted NIfTI images
│   ├── LUNG1-001/
│   ├── LUNG1-002/
│   └── ...
├── NSCLC-Radiomics-ct/                   # Original DICOM CONVERTED TO NIFTI CT scans
├── NSCLC-Radiomics-mask/                 # Original DICOM CONVERTED TO NIFTI segmentations
```

---


