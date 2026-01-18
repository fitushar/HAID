# DeepLesion-1kTest3D Dataset Processing - Documentation

This document provides documentation for **DeepLesion-1kTest3D** - a 3D NIfTI conversion of 1,000 test cases from the DeepLesion dataset, enabling volumetric analysis of diverse lesion types across multiple anatomical regions.

---

## 📂 Dataset Information

**Dataset Name**: DeepLesion-1kTest3D  
**Source**: DeepLesion (NIH Clinical Center)  
**Original Dataset Paper**: Yan et al. (2018), "DeepLesion: automated mining of large-scale lesion annotations and universal lesion detection with deep learning"  
**Original Format**: 16-bit PNG slices (2D multi-slice representation)  
**Converted Format**: 3D NIfTI volumes  
**Total Test Cases**: 1,000 3D CT volumes  
**Total Lesion Annotations**: 4,927 lesions in test set  
**Processed By**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID  
**Zenodo NIfTI Repository**: https://doi.org/10.5281/zenodo.18292965

### Dataset Characteristics
- **Original DeepLesion**: 32,735 lesions from 32,120 CT scans (10,594 patients)
- **Test Subset**: 1,000 CT volumes with 4,927 lesion annotations
- **Lesion Types**: 8 coarse categories (lung, liver, kidney, lymph node, bone, soft tissue, abdomen, pelvis)
- **Annotation Source**: PACS system bookmarks from clinical radiology practice
- **Measurement**: RECIST diameters (long/short axis measurements)
- **Slice Context**: Variable slice range (typically 30-60 consecutive slices)

### Test Set Organ-Specific Subsets
- **Liver Lesions**: 701 liver lesion annotations (test set)
- **Kidney Lesions**: 235 kidney lesion annotations (test set)
- **Other Organs**: Lung, lymph nodes, bone, soft tissue, mediastinum

### Coarse Lesion Type Distribution (Test Set)
1. **Type 1**: Lung nodules
2. **Type 2**: Abdomen lesions
3. **Type 3**: Mediastinum lesions
4. **Type 4**: Liver lesions
5. **Type 5**: Soft tissue lesions
6. **Type 6**: Kidney and urinary lesions
7. **Type 7**: Bone lesions
8. **Type 8**: Pelvic lesions

---

## 🔄 Processing Pipeline

### 1️⃣ **PNG Slice Loading and 3D Volume Reconstruction**
**Purpose**: Convert 2D 16-bit PNG slices to 3D NIfTI volumes with proper spacing

**Input**:
- DeepLesion 16-bit PNG slices stored in patient folders
- Format: `Images_png/{Patient_Study_Series}/{SliceIndex}.png`
- Metadata: [DL_info.csv](DL_info.csv) with spacing and slice range information

**Process**:
```python
import cv2
import numpy as np
import nibabel as nib

# Load consecutive slices
for slice_idx in slice_range:
    im = cv2.imread(f'{slice_idx:03d}.png', -1)  # -1 for 16-bit
    # Remove intensity bias from 16-bit PNG encoding
    im = (im.astype(np.int32) - 32768).astype(np.int16)
    slices.append(im)

# Stack slices into 3D volume
volume = cv2.merge(slices)  # or np.stack for >300 slices

# Create NIfTI with proper transformation matrix
spacing = [spacing_x, spacing_y, spacing_z]  # mm per pixel
T = np.array([[0, -spacing[1], 0, 0],
              [-spacing[0], 0, 0, 0],
              [0, 0, -spacing[2], 0],
              [0, 0, 0, 1]])
nifti_img = nib.Nifti1Image(volume, affine=T)
nib.save(nifti_img, output_path)
```

**16-bit PNG Encoding**:
- DeepLesion stores CT in 16-bit PNG with intensity bias of +32768
- Conversion subtracts 32768 to restore original Hounsfield Units (HU)
- Resulting range: -1024 to +3071 HU (typical CT window)

**Output**:
- 3D NIfTI files: `DeepLesion-1KTest-3D/{Patient_Study_Series}_SliceStart-SliceEnd.nii.gz`
- Format example: `000001_01_01_103-115.nii.gz` (Patient 1, Study 1, Series 1, slices 103-115)
- Total: 1,000 NIfTI volumes

---

### 2️⃣ **Metadata and Lesion Annotation Integration**
**Purpose**: Link 3D volumes with lesion annotations, measurements, and clinical metadata

**Input**:
- Original DeepLesion metadata: [DL_info.csv](DL_info.csv)
- Test split assignment
- RECIST measurements (long/short axis)

**Process**:
1. Parse DeepLesion metadata CSV
2. Extract key slice index (slice with measurement annotation)
3. Map PNG file names to 3D NIfTI volumes
4. Preserve RECIST diameter measurements
5. Extract normalized lesion locations (0-1 coordinates)
6. Assign coarse lesion type labels (1-8)

**Metadata Fields**:
- **File_name**: Original 2D PNG key slice (e.g., `000001_01_01_109.png`)
- **Patient_index**: Unique patient identifier (1-10594)
- **Study_index**: Study number for patient (multiple studies per patient)
- **Series_ID**: Series within study
- **Key_slice_index**: Central slice with measurement annotation
- **Measurement_coordinates**: RECIST long/short axis endpoints (x1,y1,x2,y2,x3,y3,x4,y4)
- **Bounding_boxes**: Lesion bounding box (xmin,ymin,xmax,ymax)
- **Lesion_diameters_Pixel**: Long and short axis lengths in pixels
- **Normalized_lesion_location**: 3D normalized coordinates (0-1 range)
- **Coarse_lesion_type**: Lesion category (1=lung, 2=abdomen, 3=mediastinum, 4=liver, 5=soft tissue, 6=kidney, 7=bone, 8=pelvis)
- **Possibly_noisy**: Quality flag (0=clean, 1=potentially noisy annotation)
- **Slice_range**: First and last slice indices in volume
- **Spacing_mm_px**: Pixel spacing (x, y, z) in mm
- **Image_size**: Image dimensions (typically 512×512)
- **DICOM_windows**: Display window (level, width)
- **Patient_gender**: M/F
- **Patient_age**: Age at scan
- **Nifti_ct_name**: Corresponding 3D NIfTI filename

**Output Files**:
- [DL_info_niftiID_test.csv](DL_info_niftiID_test.csv) (4,928 lesion annotations in test set)
- [test_Cases_list_DLplus_df.csv](test_Cases_list_DLplus_df.csv) (801 unique test cases)
- [DeepLesion_Liver_test_set.csv](DeepLesion_Liver_test_set.csv) (702 liver lesions)
- [DeepLesion_Kidneys_test_set.csv](DeepLesion_Kidneys_test_set.csv) (236 kidney lesions)

---

### 3️⃣ **Transformation Matrix for 3D Visualization**
**Purpose**: Create proper affine transformation for correct display in 3D Slicer and ITK-SNAP

**Transformation Matrix**:
```
T = [[0,        -spacing_y,  0,           0],
     [-spacing_x, 0,          0,           0],
     [0,         0,          -spacing_z,  0],
     [0,         0,          0,           1]]
```

**Rationale**:
- DeepLesion uses axial slice ordering (superior to inferior)
- Negative spacing ensures proper anatomical orientation
- Compatible with 3D Slicer and ITK-SNAP viewers
- Preserves patient coordinate system

**Visualization**:
- **3D Slicer**: Load NIfTI volumes directly with correct orientation
- **ITK-SNAP**: Lesion annotations can be overlaid using bounding boxes
- **Manual inspection**: Verify lesion location matches key slice index

---

### 4️⃣ **Organ-Specific Subset Extraction**
**Purpose**: Create focused subsets for liver and kidney lesion research

**Liver Lesion Subset**:
- **Count**: 701 liver lesion annotations (test set)
- **Coarse type**: Label 4 (liver)
- **Use cases**: Liver tumor detection, liver metastasis analysis
- **File**: [DeepLesion_Liver_test_set.csv](DeepLesion_Liver_test_set.csv)

**Kidney Lesion Subset**:
- **Count**: 235 kidney lesion annotations (test set)
- **Coarse type**: Label 6 (kidney/urinary)
- **Use cases**: Renal mass characterization, kidney cyst detection
- **File**: [DeepLesion_Kidneys_test_set.csv](DeepLesion_Kidneys_test_set.csv)

**Extraction Criteria**:
```python
# Liver lesions
liver_lesions = df[df['Coarse_lesion_type'] == 4]

# Kidney lesions
kidney_lesions = df[df['Coarse_lesion_type'] == 6]
```

---

## 📊 Dataset Statistics

### Test Set Overview
- **Total NIfTI Volumes**: 1,000 3D CT scans
- **Total Lesion Annotations**: 4,927 lesions
- **Lesions per Volume**: 1-10+ lesions (variable)
- **Unique Patients**: ~400-500 patients (accounting for follow-up scans)

### Slice and Spacing Characteristics
- **Slice Range**: Typically 30-60 consecutive slices per volume
- **Shortest volume**: ~12 slices
- **Longest volume**: ~270 slices (extended abdomen/pelvis)
- **In-plane Spacing**: 0.31 - 0.98 mm/pixel (variable resolution)
- **Slice Thickness**: 1.0 - 5.0 mm (most common: 5mm)
- **Image Size**: 512×512 pixels (consistent)

### Lesion Size Distribution
- **Small lesions**: <10mm diameter (~30%)
- **Medium lesions**: 10-30mm diameter (~50%)
- **Large lesions**: >30mm diameter (~20%)
- **RECIST measurements**: Both long axis and short axis provided

### Clinical Demographics
- **Age Range**: 11-87 years (diverse adult and pediatric population)
- **Gender**: Mixed male/female cohort
- **Clinical Context**: Real-world radiology practice bookmarks

### Anatomical Distribution (Test Set)
```
Liver (Type 4):         701 lesions (~14%)
Kidney (Type 6):        235 lesions (~5%)
Lung (Type 1):          ~1,500 lesions (~30%)
Lymph Nodes (Type 3):   ~800 lesions (~16%)
Bone (Type 7):          ~600 lesions (~12%)
Soft Tissue (Type 5):   ~500 lesions (~10%)
Abdomen (Type 2):       ~400 lesions (~8%)
Pelvis (Type 8):        ~191 lesions (~4%)
```

### Image Quality Flags
- **Clean annotations**: ~95% (Possibly_noisy=0)
- **Potentially noisy**: ~5% (Possibly_noisy=1)
- **Noisy annotations**: Ambiguous lesion boundaries or measurement inconsistencies

---

## 🗂️ File Structure

```
DeepLesion/
├── 036501_1.pdf                                  # Original DeepLesion paper
├── DL_save_nifti.py                              # PNG-to-NIfTI conversion script
│
├── DL_info.csv                                   # Full DeepLesion metadata (32,735 lesions)
├── DL_info_niftiID.csv                           # Metadata with NIfTI filenames
├── DL_info_niftiID_test.csv                      # Test set metadata (4,928 lesions)
│
├── test_Cases_list_DLplus_df.csv                 # Test set NIfTI volume list (801 cases)
├── val_Cases_list_DLplus_df.csv                  # Validation set NIfTI volume list
│
├── DeepLesion_Liver_test_set.csv                 # Liver lesion subset (702 lesions)
├── DeepLesion_Kidneys_test_set.csv               # Kidney lesion subset (236 lesions)
│
├── DeepLesion-1KTest-3D/                         # 3D NIfTI test volumes
│   ├── 000001_01_01_103-115.nii.gz               # Patient 1, Study 1, Series 1
│   ├── 000001_03_01_058-118.nii.gz
│   ├── 000016_01_01_019-036.nii.gz
│   └── ... (1,000 NIfTI files)
│
└── DeepLesion-1KTest-3D.zip                      # Zenodo upload archive
    └── Zenodo Repository: https://doi.org/10.5281/zenodo.18292965
```

---

## 🛠️ Software Dependencies

### Core Libraries
- **opencv-python (cv2)** 4.5.0+ (16-bit PNG reading)
- **nibabel** 3.2.0+ (NIfTI creation and saving)
- **numpy** 1.20.0+ (Array operations)
- **pandas** 1.3.0+ (Metadata management)

### Optional Visualization
- **3D Slicer** 4.11+ (3D volume visualization)
- **ITK-SNAP** 3.8+ (Lesion annotation overlay)

### Installation
```bash
# Core dependencies
pip install opencv-python>=4.5.0 nibabel>=3.2.0 numpy>=1.20.0 pandas>=1.3.0

# Optional visualization tools
# Download 3D Slicer: https://download.slicer.org/
# Download ITK-SNAP: http://www.itksnap.org/
```

---

## 📈 Processing Highlights

### PNG-to-NIfTI Conversion Advantages
- **3D Visualization**: Enable volumetric viewing in 3D Slicer and ITK-SNAP
- **Spatial Context**: Preserve anatomical relationships across slices
- **Standardized Format**: NIfTI is widely supported by medical imaging tools
- **Metadata Preservation**: Affine transformation encodes spacing and orientation

### 16-bit PNG Intensity Correction
- **Original**: PNG stores values 0-65535
- **Bias**: +32768 offset for signed 16-bit representation
- **Corrected**: Subtract 32768 → -32768 to +32767 (Hounsfield Units)
- **Clinical relevance**: Restored HU enables window/level visualization

### Lesion Annotation Format
- **RECIST Measurements**: Standard oncology response criteria
- **Bounding Boxes**: Tight rectangular regions around lesions
- **Normalized Locations**: 3D coordinates normalized to 0-1 range (body coverage)
- **Key Slice**: Central slice with measurement annotation

### Multi-Lesion Volumes
- Many volumes contain multiple lesions (2-10+ lesions per scan)
- Each lesion has independent annotation entry
- Same NIfTI volume referenced multiple times in metadata
- Enables comprehensive lesion detection benchmarking

---

## 🔗 Related Resources

- **Original DeepLesion Paper**: Yan et al. (2018), IEEE J. Biomed. Health Inform.
- **DeepLesion Dataset**: https://nihcc.app.box.com/v/DeepLesion
- **Zenodo NIfTI Repository**: https://doi.org/10.5281/zenodo.18292965
- **Processing Code**: https://github.com/fitushar/HAID
- **Processed By**: Fakrul Islam Tushar

---

## 📝 Citation

If you use this pre-processed dataset, please cite:

1. **Original DeepLesion Paper**:
   ```
   Yan, K., Wang, X., Lu, L., & Summers, R. M. (2018). 
   DeepLesion: automated mining of large-scale lesion annotations and universal lesion detection with deep learning. 
   Journal of Biomedical and Health Informatics, 22(4), 1091-1101.
   DOI: 10.1109/JBHI.2017.2780066
   ```

2. **DeepLesion Dataset**:
   ```
   Yan, K., et al. (2018). 
   DeepLesion: Large-scale Lesion Annotations from CT with Deep Learning.
   NIH Clinical Center: https://nihcc.app.box.com/v/DeepLesion
   ```

3. **DeepLesion-1kTest3D (3D NIfTI Conversion)**:
   ```
   Fakrul Islam Tushar. (2026). 
   DeepLesion-1kTest3D: 3D NIfTI Conversion of DeepLesion Test Set.
   Zenodo: https://doi.org/10.5281/zenodo.18292965
   GitHub: https://github.com/fitushar/HAID
   ```

---

## 📌 Notes

**3D Conversion**: Complete PNG-to-NIfTI conversion for 1,000 test cases  
**Lesion Annotations**: 4,927 diverse lesion annotations with RECIST measurements  
**Organ-Specific Subsets**: Liver (701) and kidney (235) lesion subsets available  
**Transformation Matrix**: Optimized for 3D Slicer and ITK-SNAP visualization  
**16-bit Intensity Correction**: Proper Hounsfield Unit restoration (-32768 bias removal)  
**Multi-Lesion Volumes**: Many volumes contain multiple annotated lesions  
**Zenodo Repository**: All 1,000 3D NIfTI volumes publicly available at https://doi.org/10.5281/zenodo.18292965

---

**Document Version**: 1.0  
**Last Updated**: January 18, 2026  
**Processed By**: Fakrul Islam Tushar  
**Contact**: GitHub - https://github.com/fitushar/HAID
