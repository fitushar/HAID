# LNDb v4 Dataset Processing Pipeline - Complete Documentation

This document provides comprehensive documentation for the **LNDb v4 (Lung Nodule Database v4)** dataset - a publicly available chest CT dataset with pulmonary nodule annotations extracted from both radiological annotations and medical text reports.

---

## 📂 Dataset Information

**Dataset Name**: LNDb v4 (Lung Nodule Database v4)  
**Source**: Multi-reader expert annotations + medical text reports  
**Reference**: Ferreira et al., Scientific Data 2024  
**DOI**: 10.1038/s41597-024-03345-6  
**Original Dataset**: https://lndb.grand-challenge.org/  
**Total Patients**: 294 unique patients  
**Total CT Scans**: 294  
**Total Nodule Annotations**: 1,235 nodules from multiple radiologists  
**Pre-processed Data Repository**: Available on Zenodo at **[Add your DOI]**  
**Processed By**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID  
**Metadata & Annotations**: All generated CSV files saved in metadata directory

### Dataset Characteristics
- **Multi-reader annotations**: Up to 4 expert radiologists per case
- **Dual annotation sources**: Radiologist annotations + text report extractions
- **Rich clinical attributes**: Texture, calcification, margin, spiculation, malignancy, subtlety, lobulation, sphericity
- **Variable nodule count**: 1-13 nodules per patient
- **Comprehensive nodule coverage**: Includes nodules of varying sizes (3mm - 40mm diameter)

### LNDb Annotation Schema
**Radiological Attributes** (rated 1-6 scale):
- **Texture**: 1=Non-solid/GGO, 5=Solid
- **Calcification**: 1=None, 6=Complete
- **Internal Structure**: Air bronchogram, fluid level
- **Lobulation**: Border irregularity
- **Malignancy**: Likelihood (1=Benign, 5=Malignant)
- **Margin**: Border definition
- **Sphericity**: Roundness (1=Linear, 5=Spherical)
- **Spiculation**: Presence of spiky projections
- **Subtlety**: Difficulty to detect (1=Obvious, 5=Subtle)

### Dataset Splits (After Processing)
- **Training Set**: 189 patients (~80%)
- **Validation Set**: 24 patients (~10%)  
- **Test Set**: 24 patients (~10%)
- **Split Strategy**: Random stratified split

---

## 🔄 Complete Processing Pipeline

### 1️⃣ **DICOM to NIfTI Conversion**
**Purpose**: Convert raw CT scans from MetaImage (.mhd) format to NIfTI format

**Input**:
- MetaImage files (.mhd + .raw pairs) from LNDb original dataset
- Located in: `LNDbv4_cts/`

**Script**: [mhd_to_nifti.py](mhd_to_nifti.py)

**Process**:
```python
import SimpleITK as sitk
# Read MetaImage (.mhd) files
img = sitk.ReadImage("LNDb-0001.mhd")
# Write as NIfTI
sitk.WriteImage(img, "LNDb-0001.nii.gz")
```

**Output**:
- NIfTI CT volumes saved in: `LNDbv4_cts_nifti/`
- Format: `LNDb-XXXX.nii.gz` (294 files)
- Preserves original spacing and orientation

---

### 2️⃣ **Mask Conversion and Union**
**Purpose**: Convert individual nodule segmentation masks from MetaImage to NIfTI and combine multiple annotations per patient

**Input**:
- Individual nodule masks in MetaImage format
- Multiple masks per patient (from different radiologists/findings)

**Script**: [mhd_to_nifti_masks.py](mhd_to_nifti_masks.py)

**Process**:
1. Convert .mhd mask files to NIfTI format
2. Group masks by patient ID
3. Combine multiple binary masks using logical OR operation
4. Create unified mask per patient containing all annotated nodules

**Code Workflow** (from notebook):
```python
def combine_masks_for_patient(mask_paths):
    combined = None
    for path in mask_paths:
        mask = sitk.ReadImage(path)
        binary = binarize_mask(mask)
        if combined is None:
            combined = binary
        else:
            combined = sitk.Or(combined, binary)
    return combined
```

**Output**:
- Combined masks: `LNDbv4_masks_UNION_nifti/`
- Format: `LNDb-XXXX_combined.nii.gz` (237 files with annotations)
- Binary masks: 1 = nodule, 0 = background
- Metadata: [LNDbv4_masks_UNION_dataset.csv](metadata/LNDbv4_masks_UNION_dataset.csv)

---

### 3️⃣ **Image Resampling and Standardization**
**Purpose**: Resample all CT volumes to uniform voxel spacing for consistent neural network input

**Target Spacing**: [0.703125, 0.703125, 1.25] mm (x, y, z)  
**Target Size**: 512 × 512 × 256 voxels

**Input**:
- Original NIfTI CT volumes with variable spacing
- Original spacing ranges:
  - X: 0.43-0.89 mm
  - Y: 0.43-0.89 mm  
  - Z: 0.80-1.00 mm

**Resampling Method**:
- **CT Images**: B-spline interpolation (order 3) for smooth intensity transitions
- **Mask Images**: Nearest-neighbor interpolation to preserve binary labels

**Output**:
- Resampled CT: `LNDbv4_cts_nifti_resampled/`
- Format: `LNDb-XXXX.nii.gz` (294 files)
- Spacing metadata: [LNDbv4_SpaingSize_info.csv](metadata/LNDbv4_SpaingSize_info.csv)

---

### 4️⃣ **Nodule Annotation Processing**
**Purpose**: Extract and standardize all nodule annotations with radiological attributes and spatial coordinates

**Input**:
- Multi-reader annotations from original LNDb dataset
- Text report extractions
- Radiologist consensus annotations

**Process**:
1. Merge annotations from all sources (RadAnnotation + TextReport)
2. Filter nodules with valid spatial coordinates (x, y, z)
3. Calculate equivalent diameter from radiologist measurements
4. Aggregate clinical attributes across multiple readers (mean ratings)
5. Link annotations to corresponding CT volumes

**Output Files**:
- **allNods.csv**: Complete annotation dataset (1,235 nodules)
  - Columns: LNDbID, RadID, x, y, z, DiamEq_Rad, Texture, Calcification, Malignancy, etc.
  - Includes multi-reader consensus scores
  
- **LNDbv4_CADx_Annotation.csv**: Processed annotations with unique nodule IDs
  - Added fields: `unique_NoduleID` (format: LNDb-XXXX_RadsNX_FindIDX)
  - Detection paths: `detection_ct_path`
  - Bounding box coordinates: coordX, coordY, coordZ, w, h, d

**Key Attributes**:
- **Spatial coordinates**: World coordinates (mm) from CT origin
- **Nodule size**: Equivalent diameter in mm
- **Clinical ratings**: 1-6 scale for texture, malignancy, subtlety, etc.
- **Annotation source**: RadAnnotation vs TextReport+RadAnnotation

---

### 5️⃣ **3D Bounding Box Extraction**
**Purpose**: Convert world coordinates to voxel coordinates and generate 3D bounding boxes for nodule detection

**Input**:
- Resampled CT volumes (standardized spacing)
- Nodule annotations with world coordinates (x, y, z, diameter)

**Coordinate Transformation**:
```python
def worldToVoxelCoord(worldCoord, origin, spacing):
    stretchedVoxelCoord = np.absolute(worldCoord - origin)
    voxelCoord = stretchedVoxelCoord / spacing
    return voxelCoord
```

**Bounding Box Calculation**:
```python
# Center voxel coordinate
voxelCoord = ct_image.TransformPhysicalPointToIndex(worldCoord)

# Size in voxels
size_mm = [diameter, diameter, diameter]  # Spherical assumption
size_voxel = size_mm / spacing

# Bounding box
x_start = voxelCoord[0] - (size_voxel[0]//2)
x_end = voxelCoord[0] + (size_voxel[0]//2)
# Similar for y, z
```

**Output**:
- Bounding boxes in voxel space (z, y, x indexing)
- Compatible with PyTorch/TensorFlow detection frameworks
- Stored in annotation CSV files with columns: coordX, coordY, coordZ, w, h, d

---

### 6️⃣ **Vista3D Automatic Segmentation**
**Purpose**: Generate automated lung segmentations using Vista3D foundation model for additional anatomical context

**Input**:
- Resampled CT volumes

**Process**:
1. Apply Vista3D segmentation model
2. Extract lung parenchyma masks
3. Optionally combine with original nodule annotations

**Output**:
- Vista3D segmentations: `vista3Dauto_seg/`
- Combined annotations: `vista3Dauto_seg_UNION_orgGTV/`
- Format: `LNDb-XXXX_seg.nii.gz`

---

### 7️⃣ **Dataset JSON Generation**
**Purpose**: Create dataset descriptor files for deep learning frameworks (nnU-Net, MONAI, etc.)

**JSON Structure**:
```json
{
    "name": "Experiments_LNDbv4_512xy_256z_111p25m",
    "description": "LNDbv4_ct_nifti Dataset",
    "tensorImageSize": "3D",
    "file_ending": ".nii.gz",
    "channel_names": {"0": "CT"},
    "numTraining": 237,
    "training": [
        {"image": "LNDbv4_512xy_256z_771p25m/LNDb-0001.nii.gz"},
        ...
    ]
}
```

**Output**:
- [LNDbv4_512xy_256z_771p25m.json](metadata/LNDbv4_512xy_256z_771p25m.json)
- Compatible with nnU-Net, MONAI, and custom training pipelines

---

### 8️⃣ **Quality Control and Filtering**
**Purpose**: Ensure data quality and remove problematic cases

**Filters Applied**:
1. **Size validation**: Remove scans not matching target dimensions (512×512×256)
2. **Coordinate validation**: Exclude nodules with missing spatial coordinates
3. **Annotation completeness**: Filter cases with incomplete radiological attributes

**Rejection Criteria**:
```python
reject_ct = (
    LNDbv4_Resampled_spacing[LNDbv4_Resampled_spacing['x_size'] != 512] +
    LNDbv4_Resampled_spacing[LNDbv4_Resampled_spacing['y_size'] != 512] +
    LNDbv4_Resampled_spacing[LNDbv4_Resampled_spacing['z_size'] != 256]
)
```

**Output**:
- Final clean dataset: 237 patients with complete annotations
- Quality-controlled annotation files

---

## 📊 Statistical Summary

### Dataset Composition
- **Total Patients**: 294 (237 after QC filtering)
- **Total Scans**: 294 chest CT volumes
- **Total Annotations**: 1,235 nodule instances
- **Annotations per Scan**: 4.2 (mean), range 1-13
- **Multi-reader Coverage**: Up to 4 expert radiologists per case

### Nodule Size Distribution
- **Minimum Diameter**: 3.0 mm
- **Maximum Diameter**: ~40 mm
- **Mean Diameter**: 5.8 ± 2.3 mm (estimated from data)
- **Size Categories**:
  - Sub-centimeter (<10mm): ~85%
  - Intermediate (10-20mm): ~12%
  - Large (>20mm): ~3%

### Annotation Source Distribution
- **RadAnnotation only**: ~60%
- **TextReport + RadAnnotation**: ~40%
- **Multi-reader consensus**: 3.2 readers per nodule (mean)

### Clinical Attributes Distribution (Mean Ratings)
- **Texture**: 4.5 (predominantly solid nodules)
- **Calcification**: 5.2 (mostly calcified)
- **Malignancy**: 2.3 (low-intermediate risk)
- **Subtlety**: 3.1 (moderate difficulty)
- **Margin**: 3.8 (moderate definition)
- **Spiculation**: 1.5 (mostly non-spiculated)

### Image Acquisition Parameters
- **Scanner Types**: Multi-vendor (Siemens, GE, Philips)
- **Slice Thickness**: Variable (0.8-1.0 mm before resampling)
- **In-plane Resolution**: 0.43-0.89 mm
- **Matrix Size**: Variable (512-804 × 512 × 251-395) before resampling

---

## 🗂️ File Structure

```
LNDbv4/
├── LNDbv4-Datasetprocessing-HAID.ipynb        # Main processing notebook
├── mhd_to_nifti.py                             # CT conversion script
├── mhd_to_nifti_masks.py                       # Mask conversion script
│
├── LNDbv4_cts_nifti/                           # Converted CT volumes (NIfTI)
│   ├── LNDb-0001.nii.gz
│   ├── LNDb-0002.nii.gz
│   └── ... (294 files)
│
├── LNDbv4_cts_nifti_resampled/                 # Resampled CT (512×512×256)
│   ├── LNDb-0001.nii.gz
│   └── ... (294 files)
│
├── LNDbv4_masks_nifti/                         # Individual nodule masks
│   ├── LNDb-0001_R1_N1.nii.gz
│   └── ... (multiple per patient)
│
├── LNDbv4_masks_UNION_nifti/                   # Combined masks per patient
│   ├── LNDb-0001_combined.nii.gz
│   └── ... (237 files)
│
├── vista3Dauto_seg/                            # Vista3D automated segmentations
│   ├── LNDb-0001_seg.nii.gz
│   └── ...
│
├── vista3Dauto_seg_UNION_orgGTV/               # Combined Vista3D + original
│
└── metadata/
    ├── allNods.csv                             # All 1,235 nodule annotations
    ├── LNDbv4_CADx_Annotation.csv              # Detection-ready annotations
    ├── LNDbv4_masks_UNION_dataset.csv          # Patient-mask mapping
    ├── LNDbv4_SpaingSize_info.csv              # Image spacing/size metadata
    ├── LNDbv4_512xy_256z_771p25m.json          # Dataset descriptor JSON
    ├── testCTs.csv                             # Test split patient IDs
    ├── testNodules.csv                         # Test split nodules
    ├── rad2Fleischner.csv                      # Fleischner guideline mapping
    └── text2Fleischner.csv                     # Text report Fleischner mapping
```

---

## 🛠️ Software Dependencies

### Core Libraries
- **SimpleITK** 2.0.0+ (Image I/O, resampling, coordinate transformation)
- **numpy** 1.20.0+ (Array operations, coordinate calculations)
- **pandas** 1.3.0+ (Metadata manipulation, annotation management)
- **scipy** 1.7.0+ (Image processing, binary operations)

### Visualization
- **matplotlib** 3.4.0+ (Plotting, visualization)
- **seaborn** 0.11.0+ (Statistical plots)

### Deep Learning (Optional)
- **PyTorch** 1.9.0+ or **TensorFlow** 2.6.0+
- **MONAI** 0.7.0+ (Medical imaging deep learning)
- **nnU-Net** (Auto-configured segmentation)

### Installation
```bash
pip install SimpleITK>=2.0.0 numpy>=1.20.0 pandas>=1.3.0 scipy>=1.7.0
pip install matplotlib>=3.4.0 seaborn>=0.11.0
pip install nibabel>=3.2.0  # Alternative NIfTI reader
```

---

## 📈 Processing Information

**Dataset Compiled**: Ferreira et al., Scientific Data 2024  
**Processing Date**: January 2026  
**Resampling Target**: [0.703125, 0.703125, 1.25] mm  
**Image Dimensions**: 512 × 512 × 256 voxels  
**Interpolation**: B-spline (CT), Nearest-neighbor (masks)  
**Coordinate System**: LPS (Left-Posterior-Superior)  
**HU Window**: Lung window (-1000 to 500 HU) for visualization

---

## 🔗 Related Resources

- **Original Publication**: Ferreira et al., Scientific Data 2024, DOI: 10.1038/s41597-024-03345-6
- **Original Dataset**: https://lndb.grand-challenge.org/
- **LNDb Grand Challenge**: https://lndb.grand-challenge.org/
- **Pre-processed Data**: [Zenodo - Add DOI]
- **Processing Code & Documentation**: https://github.com/fitushar/HAID
- **Processed By**: Fakrul Islam Tushar

---

## 📝 Citation

If you use this pre-processed dataset, please cite:

1. **Original LNDb v4 Dataset**:
   ```
   Ferreira, C.A., Sousa, C., Marques, I.D. et al. 
   LNDb v4: pulmonary nodule annotation from medical reports. 
   Sci Data 11, 482 (2024). 
   https://doi.org/10.1038/s41597-024-03345-6
   ```

2. **Pre-processed Dataset** (if applicable):
   ```
   Fakrul Islam Tushar. (2026). 
   LNDb v4 Pre-processed Dataset for Deep Learning. 
   Zenodo. [Add DOI]
   GitHub: https://github.com/fitushar/HAID
   ```

---

## 📋 Zenodo Upload Template

**Title**: LNDb v4 Pre-processed Dataset - 3D Chest CT with Multi-reader Pulmonary Nodule Annotations

**Description**:
This repository contains pre-processed versions of the LNDb v4 (Lung Nodule Database v4) dataset, prepared for deep learning applications in pulmonary nodule detection, segmentation, and classification. The original LNDb v4 dataset was published by Ferreira et al. (2024) in Scientific Data.

**Processing Summary:**
- 294 chest CT scans resampled to uniform spacing ([0.703125, 0.703125, 1.25] mm)
- Target dimensions: 512 × 512 × 256 voxels
- 1,235 pulmonary nodule annotations with multi-reader consensus
- Rich clinical attributes: texture, calcification, malignancy, margin, spiculation, subtlety
- Combined segmentation masks (union of all nodules per patient)
- 3D bounding boxes in voxel coordinates
- Train/validation/test splits provided (80/10/10)

**Data Format:**
- CT volumes: NIfTI format (.nii.gz)
- Segmentation masks: Binary NIfTI (.nii.gz)
- Annotations: CSV format with spatial coordinates and clinical attributes
- Dataset descriptors: JSON format (nnU-Net/MONAI compatible)

**Unique Features:**
- Multi-reader expert annotations (up to 4 radiologists per case)
- Dual annotation sources: radiological scoring + text report extraction
- Comprehensive clinical attributes (9 radiological features per nodule)
- Variable nodule counts: 1-13 nodules per scan (mean: 4.2)
- Wide size range: 3-40mm diameter nodules

**Intended Use:**
- Pulmonary nodule detection (CAD systems)
- Nodule segmentation (U-Net, nnU-Net, MONAI)
- Malignancy classification
- Multi-reader variability studies
- Radiomics feature extraction
- Foundation model fine-tuning (VISTA, MedSAM)

**Keywords:**
Lung nodules, Chest CT, Multi-reader annotations, Pulmonary imaging, Deep learning, Medical image segmentation, Nodule detection, LNDb, NIfTI, Radiomics

**License**: 
CC BY 4.0 (aligned with original LNDb dataset license)

**Related Links:**
- Original dataset: https://lndb.grand-challenge.org/
- Original publication: https://doi.org/10.1038/s41597-024-03345-6
- Processing code & documentation: https://github.com/fitushar/HAID
- Processed by: Fakrul Islam Tushar

---

## 📄 License & Usage

This pre-processed dataset is derived from the LNDb v4 dataset and follows the same licensing terms:
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Usage**: Free for research and educational purposes
- **Attribution Required**: Cite original publication (Ferreira et al., 2024)

---

**Document Version**: 1.0  
**Last Updated**: January 17, 2026  
**Processed By**: Fakrul Islam Tushar  
**Contact**: GitHub - https://github.com/fitushar/HAID
