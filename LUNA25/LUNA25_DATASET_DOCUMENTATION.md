# LUNA25 Dataset Processing Pipeline - Documentation

This document provides documentation for the **LUNA25** dataset - an extended version of LUNA16 with comprehensive nodule segmentation masks generated using deep learning and combined with organ segmentation.

---

## 📂 Dataset Information

**Dataset Name**: LUNA25 (Extended LUNA16 with Comprehensive Segmentations)  
**Source**: LUNA16 Challenge (Grand Challenge)  
**Original Dataset**: https://luna16.grand-challenge.org/  
**Total Patients**: ~1,000+ unique patients  
**Total Nodule Annotations**: 5,884 nodules with world coordinates  
**Segmentation Approach**: PiNS deep learning + MONAI Vista3D organ segmentation  
**Processed By**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID  
**Zenodo Segmentations**: https://doi.org/10.5281/zenodo.18291811

### Dataset Characteristics
- **Original LUNA16**: Public lung nodule detection benchmark
- **Extended annotations**: Deep learning-based nodule segmentation masks
- **Multi-class segmentation**: Nodules + organs + body regions
- **Clinical metadata**: Age, gender, study dates included
- **World coordinates**: 3D spatial coordinates (x, y, z) in mm

### Dataset Splits
- **Training Set**: ~4,700 nodules (~80%)
- **Validation Set**: ~590 nodules (~10%)
- **Test Set**: ~590 nodules (~10%)

### Label Distribution
- **Label 0**: All nodules are benign (LUNA16 screening dataset)
- **Label 1**: Small subset with confirmed malignancy

---

## 🔄 Complete Processing Pipeline

### 1️⃣ **PiNS Nodule Segmentation**
**Purpose**: Generate precise 3D segmentation masks for all annotated nodules using deep learning

**Model**: PiNS (Precise Nodule Segmentation)  
**Repository**: https://github.com/fitushar/PiNS

**Input**:
- LUNA16 CT volumes (NIfTI format)
- Nodule world coordinates (x, y, z) in mm
- 5,884 nodule annotations from LUNA16 challenge

**Process**:
```python
# PiNS deep learning-based segmentation
# Input: CT volume + nodule center coordinates
# Output: Precise 3D segmentation mask
nodule_mask = pins_model.segment(ct_volume, nodule_center_xyz)
```

**PiNS Features**:
- **Deep learning-based**: Trained on expert-annotated nodules
- **Precise boundaries**: Accurate nodule delineation
- **Size-adaptive**: Handles small to large nodules
- **2mm KNN expansion**: Extended segmentation with 2mm K-nearest-neighbor dilation for complete coverage

**Output**:
- Nodule segmentation masks: `LUNA25_PiNS_NoduleSegmentation_masks/`
- Format: `luna25_{SeriesInstanceUID}_mask.nii.gz`
- Binary masks: 1 = nodule, 0 = background
- Additional: KNN 2mm expanded masks for margin inclusion

---

### 2️⃣ **MONAI Vista3D Organ Segmentation**
**Purpose**: Generate comprehensive multi-organ segmentation using foundation model

**Model**: MONAI Vista3D  
**Repository**: https://github.com/Project-MONAI/VISTA

**Input**:
- LUNA25 CT volumes (all ~1,000+ scans)

**Process**:
1. Apply Vista3D foundation model to each CT scan
2. Segment multiple anatomical structures (lungs, airways, vessels, etc.)
3. Generate multi-class organ masks

**Vista3D Capabilities**:
- **Foundation model**: Pre-trained on diverse medical imaging data
- **Multi-organ**: Simultaneous segmentation of 100+ anatomical structures
- **Zero-shot**: Generalizes to new data without fine-tuning
- **High accuracy**: State-of-the-art organ segmentation

**Output**:
- Vista3D segmentations: `LUNA25_Vista3Dauto_OrganSegmentation_masks/`
- Format: `luna25_{SeriesInstanceUID}_0000_seg.nii.gz`
- Multi-class masks with organ-specific labels

---

### 3️⃣ **Nodule + Organ Segmentation Integration**
**Purpose**: Create comprehensive multi-class segmentation combining nodule and organ annotations

**Input**:
- PiNS nodule segmentations (from Step 1)
- Vista3D organ segmentations (from Step 2)
- Original CT volumes for body mask generation

**Process**:
```python
# Step 1: Load Vista3D organ segmentation
vista3d_mask = load_nifti(vista3d_path)

# Step 2: Load PiNS nodule segmentation with morphological erosion
nodule_mask = load_nifti(pins_nodule_path)
nodule_mask = binary_erosion(nodule_mask, structure=np.ones((3, 3, 3)))

# Step 3: Integrate nodule annotations
# Assign label 23 to nodule regions (highest priority)
final_mask[nodule_mask == 1] = 23

# Step 4: Generate body mask (threshold: -300 HU)
body_mask = get_body_mask(ct_image, threshold=-300)

# Step 5: Fill background regions inside body
# Label 200 for body regions not otherwise classified
final_mask[(body_mask != 0) & (final_mask == 0)] = 200
```

**Morphological Erosion**:
- **Purpose**: Refine nodule boundaries to remove uncertain edge voxels
- **Kernel**: 3×3×3 binary structure element
- **Effect**: Slightly shrinks nodule masks to high-confidence core regions

**Label Scheme**:
- **Label 23**: Pulmonary nodules (PiNS segmentation, eroded)
- **Label 200**: Body/soft tissue regions (not lung, not nodule)
- **Other labels**: Vista3D organ segmentations (lung parenchyma, airways, vessels, etc.)
- **Label 0**: Background (air outside body)

**Body Mask Generation**:
- Thresholding at -300 HU to separate body from air
- Connected component analysis to identify largest body region
- Hole filling using voting-based algorithm (radius=2 voxels)

**Output**:
- Comprehensive segmentations: `LUNA25_Organ_and_Nodule_Segmentation_Marge/`
- Format: `luna25_{SeriesInstanceUID}_0000_seg_sh.nii.gz`
- Multi-class masks: nodule + organ + body labels
- **Zenodo Repository**: https://doi.org/10.5281/zenodo.18291811

---

### 4️⃣ **Metadata Integration and Annotation Matching**
**Purpose**: Link nodule annotations with clinical metadata and split assignments

**Input**:
- LUNA16 nodule annotations (world coordinates)
- Clinical metadata (age, gender, study dates)
- Split assignments (train/val/test)

**Process**:
1. Parse LUNA16 annotation CSV files
2. Extract patient demographics from DICOM metadata
3. Generate unique annotation IDs per nodule
4. Assign train/validation/test splits
5. Link segmentation masks to annotations

**Output Files**:
- [LUNA25_Public_Training_Development_Data_AnnotationID_nifti_splitV1.csv](metadata/LUNA25_Public_Training_Development_Data_AnnotationID_nifti_splitV1.csv)
- Columns: PatientID, SeriesInstanceUID, StudyDate, CoordX/Y/Z, LesionID, AnnotationID, label, Age, Gender, segmentation path, split

**Metadata Fields**:
- **PatientID**: Unique patient identifier
- **SeriesInstanceUID**: DICOM series identifier
- **CoordX/Y/Z**: World coordinates in mm
- **LesionID**: Nodule ID within patient
- **AnnotationID**: Unique annotation identifier
- **label**: 0=benign, 1=malignant
- **Age_at_StudyDate**: Patient age at scan
- **Gender**: Male/Female
- **split**: train/val/test assignment

---

### 5️⃣ **PyRadiomics Feature Extraction** (Optional)
**Purpose**: Extract radiomics features for nodule characterization

**Input**:
- CT volumes
- Nodule segmentation masks (PiNS + KNN expansion)

**Features Extracted**:
- Shape features (volume, diameter, sphericity)
- First-order statistics (mean, variance, skewness, kurtosis)
- Texture features (GLCM, GLRLM, GLSZM)

**Output**:
- PyRadiomics CSV files in `metadata/pyradiomics/`
- Detected nodules: `PyRadiomics_CandidateSeg_DukeLunaCVIT_inference_luna25_pos_n5754_candidate_Detected_knn.csv`
- Undetected nodules: `PyRadiomics_CandidateSeg_DukeLunaCVIT_inference_luna25_pos_n429_candidate_unDetected_knn.csv`

---

## 📊 Dataset Statistics

### Nodule Annotation Counts
- **Total Annotations**: 5,884 nodules
- **Unique Patients**: ~1,000+ (LUNA16 cohort)
- **Annotations per Scan**: Variable (1-10+ nodules per patient)

### Data Splits
```
Training:    ~4,700 nodules (~80%)
Validation:    ~590 nodules (~10%)
Test:          ~590 nodules (~10%)
────────────────────────────────
Total:       5,884 nodules (100%)
```

### Clinical Demographics
- **Age Range**: 55-75 years (typical screening population)
- **Gender**: Mixed male/female cohort
- **Study Dates**: 1999-2001 (LUNA16 original dataset)

### Nodule Characteristics
- **All benign**: LUNA16 is a screening dataset (label=0 for most)
- **Size range**: 3mm - 30mm diameter (screening-detected nodules)
- **World coordinates**: Precise 3D spatial locations in mm

### Segmentation Labels
- **Label 0**: Background (air outside body)
- **Label 23**: Pulmonary nodules (PiNS + erosion)
- **Label 200**: Body/soft tissue regions
- **Other labels**: Vista3D organ segmentations (lungs, airways, vessels, heart, etc.)

---

## 🗂️ File Structure

```
LUNA25/
├── LUNA25_Organ_Nodule_Segmentation_Union_HAID.ipynb  # Processing notebook
├── LUNA24_Added-boxwhw-through-detection-HAID.ipynb   # Detection bounding boxes
├── LUNA25_Matching_to_NLST_and_imageloc_HAID.ipynb    # NLST matching
│
├── LUNA25_PiNS_NoduleSegmentation_masks/              # PiNS nodule masks
│   ├── luna25_{UID}_mask.nii.gz
│   └── ... (5,884 nodule masks)
│
├── LUNA25_Vista3Dauto_OrganSegmentation_masks/        # Vista3D organ masks
│   ├── luna25_{UID}_0000_seg.nii.gz
│   └── ... (~1,000+ scans)
│
├── LUNA25_Organ_and_Nodule_Segmentation_Marge/        # Final combined masks
│   ├── luna25_{UID}_0000_seg_sh.nii.gz
│   └── ... (~1,000+ scans)
│   └── Zenodo: https://doi.org/10.5281/zenodo.18291811
│
└── metadata/
    ├── LUNA25_Public_Training_Development_Data.csv
    ├── LUNA25_Public_Training_Development_Data_AnnotationID_nifti_splitV1.csv
    ├── LUNA25_Public_Training_Development_Data_AnnotationID_lobloc.csv
    └── pyradiomics/                                   # Radiomics features
        ├── PyRadiomics_CandidateSeg_DukeLunaCVIT_inference_luna25_pos_n5754_candidate_Detected_knn.csv
        └── PyRadiomics_CandidateSeg_DukeLunaCVIT_inference_luna25_pos_n429_candidate_unDetected_knn.csv
```

---

## 🛠️ Software Dependencies

### Core Libraries
- **SimpleITK** 2.0.0+ (Image I/O, morphological operations, thresholding)
- **numpy** 1.20.0+ (Array operations)
- **pandas** 1.3.0+ (Metadata management)
- **scipy** 1.7.0+ (Morphological erosion, binary operations)

### Deep Learning Segmentation
- **PiNS**: Custom nodule segmentation model  
  Repository: https://github.com/fitushar/PiNS
- **MONAI Vista3D**: Foundation model for organ segmentation  
  Repository: https://github.com/Project-MONAI/VISTA

### Radiomics (Optional)
- **PyRadiomics** 3.0.0+ (Feature extraction)

### Installation
```bash
# Core dependencies
pip install SimpleITK>=2.0.0 numpy>=1.20.0 pandas>=1.3.0 scipy>=1.7.0

# Deep learning frameworks
pip install torch torchvision monai
pip install git+https://github.com/fitushar/PiNS.git

# Radiomics
pip install pyradiomics
```

---

## 📈 Processing Highlights

### PiNS Nodule Segmentation Advantages
- **Deep learning precision**: Trained on expert annotations
- **Boundary accuracy**: Superior to simple thresholding
- **Adaptive to size**: Handles variable nodule sizes
- **KNN expansion**: 2mm dilation for margin inclusion

### Vista3D Foundation Model Benefits
- **Zero-shot capability**: No dataset-specific training needed
- **Multi-organ coverage**: Comprehensive anatomical context
- **State-of-the-art accuracy**: Pre-trained on large-scale data
- **Efficient inference**: Fast processing for 1,000+ scans

### Integration Strategy
1. **Vista3D baseline**: Start with comprehensive organ segmentation
2. **PiNS nodule override**: Add precise nodule masks (Label 23) - highest priority
3. **Morphological refinement**: Erode nodules to high-confidence core
4. **Body filling**: Label remaining body regions (Label 200)
5. **Background preservation**: Keep air as Label 0

### Morphological Erosion Rationale
- **Purpose**: Remove uncertain boundary voxels
- **Effect**: Ensures only high-confidence nodule core is labeled
- **Trade-off**: Slightly reduced sensitivity for increased specificity
- **Clinical relevance**: Focuses on solid nodule components

---

## 🔗 Related Resources

- **Original LUNA16**: https://luna16.grand-challenge.org/
- **PiNS Segmentation**: https://github.com/fitushar/PiNS
- **MONAI Vista3D**: https://github.com/Project-MONAI/VISTA
- **Zenodo Segmentations**: https://doi.org/10.5281/zenodo.18291811
- **Processing Code**: https://github.com/fitushar/HAID
- **Processed By**: Fakrul Islam Tushar

---

## 📝 Citation

If you use this pre-processed dataset, please cite:

1. **Original LUNA16 Challenge**:
   ```
   Setio, A. A. A., et al. (2017). 
   Validation, comparison, and combination of algorithms for automatic detection of pulmonary nodules in computed tomography images: 
   The LUNA16 challenge. 
   Medical Image Analysis, 42, 1-13.
   ```

2. **PiNS Nodule Segmentation**:
   ```
   Fakrul Islam Tushar. (2024). 
   PiNS: Precise Nodule Segmentation for Lung Cancer Detection.
   GitHub: https://github.com/fitushar/PiNS
   ```

3. **MONAI Vista3D**:
   ```
   MONAI Consortium. (2024). 
   VISTA: Versatile Imaging Segmentation and Annotation.
   GitHub: https://github.com/Project-MONAI/VISTA
   ```

4. **LUNA25 Pre-processed Dataset**:
   ```
   Fakrul Islam Tushar. (2026). 
   LUNA25: Extended LUNA16 with Deep Learning Segmentations.
   Zenodo: https://doi.org/10.5281/zenodo.18291811
   GitHub: https://github.com/fitushar/HAID
   ```

---

## 📌 Notes

**Dataset Extension**: LUNA25 = LUNA16 + Deep Learning Segmentations (PiNS + Vista3D)  
**Label Priority**: Nodule (23) > Body (200) > Organ (Vista3D) > Background (0)  
**Morphological Processing**: 3×3×3 erosion ensures high-confidence nodule cores  
**Clinical Context**: Screening-detected nodules (predominantly benign) with comprehensive anatomical segmentation  
**Zenodo Repository**: All final segmentations publicly available at https://doi.org/10.5281/zenodo.18291811

---

**Document Version**: 1.0  
**Last Updated**: January 18, 2026  
**Processed By**: Fakrul Islam Tushar  
**Contact**: GitHub - https://github.com/fitushar/HAID
