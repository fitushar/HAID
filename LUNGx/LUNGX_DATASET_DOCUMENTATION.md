# LUNGx Dataset Processing Pipeline - Documentation

This document provides documentation for the **LUNGx (SPIE-AAPM Lung CT Challenge)** dataset processing pipeline - a diagnostic CT dataset for lung cancer prediction challenge.

---

## 📂 Dataset Information

**Dataset Name**: LUNGx (SPIE-AAPM Lung CT Challenge)  
**Source**: The Cancer Imaging Archive (TCIA)  
**DOI**: 10.7937/K9/TCIA.2015.UZLSU3FL  
**Original Dataset**: https://doi.org/10.7937/K9/TCIA.2015.UZLSU3FL  
**Total Patients**: 73 (Test Set) + 10 (Calibration Set) = 83 unique patients  
**Total CT Scans**: 83 diagnostic chest CT scans  
**Total Nodule Annotations**: 94 nodules with pathology-confirmed diagnoses  
**Clinical Task**: Benign vs. malignant lung nodule classification  
**Processed By**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID

### Dataset Characteristics
- **Test Set**: 73 patients with ground truth diagnoses
- **Calibration Set**: 10 patients for algorithm calibration
- **Pathology-confirmed labels**: All nodules have histological confirmation
- **Challenge context**: SPIE-AAPM diagnostic performance evaluation
- **Scanner**: Philips CT scanners (multi-site data)
- **Contrast**: Mixed (infused and non-infused chest CT)

### Diagnosis Distribution
- **Primary Lung Cancer**: 37 nodules (~39%)
- **Benign Nodules**: 57 nodules (~61%)

---

## 🔄 Complete Processing Pipeline

### 1️⃣ **DICOM to NIfTI Conversion**
**Purpose**: Convert DICOM series to standardized NIfTI format for processing

**Input**:
- DICOM series from TCIA (organized by patient/study/series)
- Metadata CSV from NBIA Data Retriever

**Process**:
```python
import SimpleITK as sitk
img_reader = sitk.ImageSeriesReader()
dicom_names = img_reader.GetGDCMSeriesFileNames(dicom_path)
img_reader.SetFileNames(dicom_names)
image = img_reader.Execute()
sitk.WriteImage(image, output_path)
```

**Output**:
- NIfTI volumes: `LUNGx_nifti/`
- Format: `LUNGx-CTXXX_0000.nii.gz` (83 files)
- Preserves original DICOM spacing and orientation

---

### 2️⃣ **Metadata Integration**
**Purpose**: Merge test set and calibration set annotations with DICOM metadata

**Input**:
- TestSet_NoduleData_PublicRelease_wTruth.xlsx (73 patients)
- CalibrationSet_NoduleData.xlsx (10 patients)
- metadata.csv (DICOM paths and identifiers)

**Process**:
1. Load test set with ground truth diagnoses
2. Load calibration set annotations
3. Merge with DICOM paths and series UIDs
4. Create unified annotation file

**Output**:
- [LungX_TestSet_NoduleData_PublicRelease_wTruth_and_CalibrationSet_cccloc.csv](metadata/LungX_TestSet_NoduleData_PublicRelease_wTruth_and_CalibrationSet_cccloc.csv)
- Contains: Scan Number, Nodule Number, DICOM xy coordinates, slice number, diagnosis, paths

---

### 3️⃣ **World Coordinate Conversion**
**Purpose**: Convert DICOM pixel coordinates to world coordinates (mm) for spatial consistency

**Challenge**: LUNGx annotations are in DICOM pixel space - need transformation to physical coordinates

**Input**:
- DICOM pixel coordinates (x, y) and slice number
- DICOM ImagePositionPatient and PixelSpacing metadata

**Coordinate Transformation**:
```python
# DICOM to world coordinates
world_x = ImagePositionPatient[0] + dicom_x * PixelSpacing[1]
world_y = ImagePositionPatient[1] + dicom_y * PixelSpacing[0]
world_z = ImagePositionPatient[2]  # Z from slice position

# Transform to NIfTI coordinate system
nifti_img = sitk.ReadImage(nifti_path)
voxel_coords = nifti_img.TransformPhysicalPointToIndex([world_x, world_y, world_z])
```

**Coordinate System Handling**:
- DICOM uses (x, y, z) in mm from patient origin
- NIfTI may have different coordinate conventions (LPS vs RAS)
- Implemented coordinate flipping detection for proper alignment
- Validated transformations to ensure nodules fall within volume bounds

**Output**:
- [LungX_nodule_world_coordinates_sitk.csv](metadata/LungX_nodule_world_coordinates_sitk.csv)
- Columns: Scan Number, Nodule Number, Diagnosis, DICOM x/y/slice, World x/y/z (mm)

---

### 4️⃣ **Image Resampling**
**Purpose**: Resample CT volumes to uniform spacing for deep learning

**Target Spacing**: [0.703125, 0.703125, 1.25] mm (standardized across all HAID datasets)

**Input**:
- Original NIfTI volumes with variable spacing
- Original spacing: ~0.6-0.9 mm in-plane, ~1.0 mm slice thickness

**Process**:
- B-spline interpolation (order 3) for smooth CT intensity transitions
- Maintains anatomical structures and HU values

**Output**:
- Resampled volumes: `LUNGx_nifti_resampled/`
- Format: `LUNGx-CTXXX_0000.nii.gz`
- Updated world coordinates adjusted for new spacing

---

### 5️⃣ **Diagnostic Patch Extraction**
**Purpose**: Extract 64×64×64 voxel patches centered on nodules for classification

**Input**:
- Resampled CT volumes
- World coordinates of nodule centers

**Process**:
1. Transform world coordinates to resampled voxel coordinates
2. Extract 64³ voxel patches centered on nodules
3. Apply lung window clipping (-1000 to 500 HU)
4. Normalize to uint8 range

**Output**:
- Diagnostic patches: `LUNGx_cts_nifti_resampled_diagnostic_64Q_patches/`
- Format: `LUNGx-CTXXX_noduleN_64x64x64.nii.gz`
- Ready for CNN-based classification

---

## 📊 Dataset Statistics

### Patient and Scan Counts
- **Test Set Patients**: 73
- **Calibration Set Patients**: 10
- **Total Scans**: 83 chest CT volumes
- **Total Nodules**: 94 (1.13 nodules per patient on average)
- **Multi-nodule Cases**: 11 patients with 2 nodules each

### Diagnosis Distribution
| Diagnosis | Count | Percentage |
|-----------|-------|------------|
| **Benign Nodule** | 57 | 60.6% |
| **Primary Lung Cancer** | 37 | 39.4% |

### Scanner Information
- **Manufacturer**: Philips (all scans)
- **Modality**: CT (Computed Tomography)
- **Protocols**: HIGH RES, HI-RES variations
- **Contrast**: Mixed infused and non-infused chest CT
- **Matrix Size**: 512 × 512 in-plane (typical)
- **Slice Count**: 200-470 slices per scan

---

## 🗂️ File Structure

```
LUNGx/
├── LUNGx-Processing-HAID.ipynb                 # Processing notebook
├── 044506_1.pdf                                 # Original challenge paper
│
├── LUNGx_nifti/                                 # Converted NIfTI volumes
│   ├── LUNGx-CT001_0000.nii.gz
│   ├── LUNGx-CT002_0000.nii.gz
│   └── ... (83 files)
│
├── LUNGx_nifti_resampled/                       # Resampled to [0.7, 0.7, 1.25] mm
│   ├── LUNGx-CT001_0000.nii.gz
│   └── ... (83 files)
│
├── LUNGx_cts_nifti_resampled_diagnostic_64Q_patches/  # Nodule patches
│   ├── LUNGx-CT001_nodule1_64x64x64.nii.gz
│   └── ...
│
└── metadata/
    ├── metadata.csv                             # DICOM metadata from NBIA
    ├── TestSet_NoduleData_PublicRelease_wTruth.xlsx  # 73 test patients
    ├── CalibrationSet_NoduleData.xlsx           # 10 calibration patients
    ├── LungX_TestSet_NoduleData_PublicRelease_wTruth_and_CalibrationSet_cccloc.csv
    └── LungX_nodule_world_coordinates_sitk.csv  # World coordinates
```

---

## 🛠️ Software Dependencies

### Core Libraries
- **SimpleITK** 2.0.0+ (DICOM reading, NIfTI I/O, coordinate transformations)
- **pydicom** 2.0.0+ (DICOM metadata parsing)
- **pydicom_seg** (Segmentation reading, if applicable)
- **numpy** 1.20.0+ (Array operations)
- **pandas** 1.3.0+ (Metadata management)

### Visualization
- **matplotlib** 3.4.0+ (Nodule visualization)
- **cv2** (OpenCV for image processing)

### Installation
```bash
pip install SimpleITK>=2.0.0 pydicom>=2.0.0 numpy>=1.20.0 pandas>=1.3.0
pip install matplotlib>=3.4.0 opencv-python
```

---

## 📈 Processing Notes

**Challenge Context**: SPIE-AAPM Lung CT Challenge for diagnostic performance evaluation  
**Processing Date**: January 2026  
**Coordinate System**: LPS (Left-Posterior-Superior)  
**HU Window**: Lung window (-1000 to 500 HU) for visualization  
**Patch Size**: 64×64×64 voxels for classification  
**Resampling Target**: [0.703125, 0.703125, 1.25] mm

### Key Processing Features
- **SimpleITK-based workflow**: Consistent coordinate handling throughout
- **DICOM to world coordinate mapping**: Proper transformation with flip detection
- **Multi-slice coordinate extraction**: Handles variable slice positioning
- **Validation**: Ensures nodule coordinates fall within volume bounds

---

## 🔗 Related Resources

- **Original Challenge**: SPIE-AAPM Lung CT Challenge
- **TCIA Page**: https://doi.org/10.7937/K9/TCIA.2015.UZLSU3FL
- **Challenge Paper**: Armato et al., 2015 (044506_1.pdf)
- **Processing Code**: https://github.com/fitushar/HAID
- **Processed By**: Fakrul Islam Tushar

---

## 📝 Citation

If you use this pre-processed dataset, please cite:

1. **Original LUNGx Challenge**:
   ```
   Armato III, S. G., et al. (2015). 
   LUNGx Challenge for computerized lung nodule classification. 
   Journal of Medical Imaging, 3(4), 044506.
   TCIA: https://doi.org/10.7937/K9/TCIA.2015.UZLSU3FL
   ```

2. **Pre-processed Dataset**:
   ```
   Fakrul Islam Tushar. (2026). 
   LUNGx Pre-processed Dataset with World Coordinates.
   GitHub: https://github.com/fitushar/HAID
   ```

---

## 📌 Notes

**Dataset Purpose**: Diagnostic performance evaluation for lung cancer prediction  
**Ground Truth**: Pathology-confirmed diagnoses (gold standard)  
**Clinical Relevance**: Real-world diagnostic challenge with benign/malignant classification  
**Unique Features**: DICOM coordinate annotations requiring careful transformation to NIfTI space

---

**Document Version**: 1.0  
**Last Updated**: January 18, 2026  
**Processed By**: Fakrul Islam Tushar  
**Contact**: GitHub - https://github.com/fitushar/HAID
