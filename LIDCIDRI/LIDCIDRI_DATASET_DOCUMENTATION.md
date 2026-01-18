# LIDC-IDRI Dataset Processing Pipeline - Documentation

This document provides documentation for the **LIDC-IDRI (Lung Image Database Consortium and Image Database Resource Initiative)** dataset processing - a comprehensive lung nodule annotation dataset with multi-radiologist consensus segmentations.

---

## 📂 Dataset Information

**Dataset Name**: LIDC-IDRI (Lung Image Database Consortium - Image Database Resource Initiative)  
**Source**: The Cancer Imaging Archive (TCIA)  
**Original Dataset**: https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI  
**Total Patients**: 875 unique patients (after processing)  
**Total CT Scans**: 875 chest CT volumes  
**Annotation Type**: Multi-radiologist consensus segmentations (up to 4 radiologists per case)  
**Clinical Task**: Lung nodule detection and segmentation  
**Processed By**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID

### Dataset Characteristics
- **Multi-reader annotations**: Up to 4 expert radiologists per nodule
- **Consensus approach**: Union of all radiologist annotations for complete nodule coverage
- **Organ segmentation integration**: Combined nodule + organ (lung) segmentation from Vista3D
- **Comprehensive coverage**: Small to large nodules with expert delineation
- **Public benchmark**: Widely used for nodule detection/segmentation research

### Dataset Splits
- **Training Set**: 649 patients (~74%)
- **Validation Set**: 163 patients (~19%)  
- **Test Set**: 63 patients (~7%)
- **Total**: 875 patients

---

## 🔄 Complete Processing Pipeline

### 1️⃣ **Multi-Radiologist Annotation Union**
**Purpose**: Combine annotations from multiple radiologists to create comprehensive nodule segmentation masks

**Input**:
- Original LIDC-IDRI segmentations with individual radiologist annotations
- Multiple segmentation masks per patient (up to 4 radiologists)
- Format: NIfTI binary masks in `labelsTr/` and `labelsTs/`

**Process**:
```python
# Union operation: Combine all radiologist annotations
# If any radiologist marked a voxel as nodule → include in final mask
union_mask = radiologist1_mask | radiologist2_mask | radiologist3_mask | radiologist4_mask
```

**Rationale**:
- Captures maximum nodule extent across expert opinions
- Reduces false negatives by including all expert-identified regions
- Provides comprehensive ground truth for training

**Output**:
- Unified nodule segmentation per patient
- Binary masks: 1 = nodule, 0 = background

---

### 2️⃣ **Vista3D Organ Segmentation**
**Purpose**: Generate automated lung parenchyma segmentation using Vista3D foundation model

**Input**:
- Processed CT volumes from `imagesTr/` and `imagesTs/`

**Process**:
1. Apply Vista3D segmentation model to each CT scan
2. Extract lung parenchyma masks (anatomical context)
3. Generate organ segmentations for all 875 cases

**Output**:
- Vista3D segmentations: `vista3Dauto_seg/`
- Format: `LIDCIDRI_XXXX_0000_seg.nii.gz` (875 files)
- Multi-class segmentation with lung regions identified

---

### 3️⃣ **Nodule + Organ Segmentation Integration**
**Purpose**: Create comprehensive multi-class segmentation masks combining nodule annotations with organ context

**Input**:
- Union of radiologist nodule segmentations (from Step 1)
- Vista3D organ segmentations (from Step 2)
- Original CT volumes for body mask generation

**Process**:
```python
# Step 1: Load Vista3D organ segmentation
vista3d_mask = load_nifti(vista3d_path)

# Step 2: Load union nodule segmentation
nodule_union_mask = load_nifti(nodule_path)

# Step 3: Integrate nodule annotations
# Assign label 23 to nodule regions
final_mask[nodule_union_mask == 1] = 23

# Step 4: Generate body mask (threshold: -300 HU)
body_mask = get_body_mask(ct_image, threshold=-300)

# Step 5: Fill background regions inside body
# Label 200 for body regions not otherwise classified
final_mask[(body_mask != 0) & (final_mask == 0)] = 200
```

**Label Scheme**:
- **Label 23**: Pulmonary nodules (multi-radiologist union)
- **Label 200**: Body/soft tissue regions (not lung, not nodule)
- **Other labels**: Vista3D organ segmentations (lung parenchyma, vessels, etc.)
- **Label 0**: Background (air outside body)

**Body Mask Generation**:
- Thresholding at -300 HU to separate body from air
- Connected component analysis to identify largest body region
- Hole filling to create continuous body mask

**Output**:
- Comprehensive segmentations: `vista3Dauto_seg_plus_orgGT/`
- Format: `LIDCIDRI_XXXX_0000_seg_sh.nii.gz` (875 files)
- Multi-class masks with nodule + organ + body labels

---

### 4️⃣ **Dataset Split Assignment**
**Purpose**: Organize data into training, validation, and test sets based on pre-defined folds

**Input**:
- Original dataset JSON with fold assignments
- `Dataset501_ULNoduleSeg_dataset.json`

**Split Logic**:
```python
# Fold 0 → Validation
# Folds 1-4 → Training
# Test set → Separate test split
fitSplit = "Validation" if fold == 0 else "Train"
```

**Output**:
- Split metadata: [LIDCIDRI_Split_Dataset501_ULNoduleSeg_dataset.csv](LIDCIDRI_Split_Dataset501_ULNoduleSeg_dataset.csv)
- Columns: image, label, fold, fitSplit, Vista3DSegNifti

**Split Distribution**:
| Split | Patients | Percentage |
|-------|----------|------------|
| Training | 649 | 74.2% |
| Validation | 163 | 18.6% |
| Test | 63 | 7.2% |
| **Total** | **875** | **100%** |

---

### 5️⃣ **Image Statistics and Quality Control**
**Purpose**: Analyze spacing and size distributions to ensure data quality

**Process**:
1. Extract spacing (x, y, z) in mm from all NIfTI volumes
2. Extract dimensions (x, y, z) in voxels
3. Generate statistics (mean, median, min, max)
4. Create visualization plots (histograms, scatter plots)

**Output Files**:
- Training statistics: [LIDC_IDRI_tr_SpaingSize_info.csv](LIDC_IDRI_tr_SpaingSize_info.csv)
- Test statistics: [LIDC_IDRI_ts_SpaingSize_info.csv](LIDC_IDRI_ts_SpaingSize_info.csv)

**Quality Control**:
- Verified consistent spacing across dataset
- Identified outliers in volume dimensions
- Ensured proper alignment of CT and segmentation masks

---

### 6️⃣ **Dataset JSON Generation**
**Purpose**: Create dataset descriptor for deep learning frameworks (nnU-Net, MONAI)

**JSON Structure**:
```json
{
    "name": "Experiments_LIDCIDRI_512xy_256z_111p25m",
    "description": "LIDCIDRI Dataset",
    "tensorImageSize": "3D",
    "file_ending": ".nii.gz",
    "channel_names": {"0": "CT"},
    "numTraining": 875,
    "training": [
        {"image": "imagesTr_512xy_256z_771p25m/LIDCIDRI_0001_0000.nii.gz"},
        ...
    ]
}
```

**Output**:
- [LIDCIDRI_512xy_256z_771p25m.json](LIDCIDRI_512xy_256z_771p25m.json)
- Compatible with nnU-Net, MONAI, and custom training pipelines

---

## 📊 Dataset Statistics

### Patient and Annotation Counts
- **Total Patients**: 875
- **Total CT Scans**: 875 chest CT volumes
- **Nodule Annotations**: Multi-radiologist consensus (1-4 readers per nodule)
- **Annotation Coverage**: Nodules ≥3mm diameter

### Data Splits
```
Training:    649 patients (74.2%)
Validation:  163 patients (18.6%)
Test:         63 patients (7.2%)
────────────────────────────
Total:       875 patients (100%)
```

### Image Characteristics
- **Original Spacing**: Variable (typically ~0.6-0.9 mm in-plane, 1.0-2.5 mm slice thickness)
- **Image Dimensions**: Variable matrix sizes
- **Modality**: CT (Computed Tomography)
- **Scanner Types**: Multi-vendor (Siemens, GE, Philips, Toshiba)
- **Scan Protocol**: Chest CT with varied acquisition parameters

### Segmentation Labels
- **Label 0**: Background (air outside body)
- **Label 23**: Pulmonary nodules (multi-radiologist union)
- **Label 200**: Body/soft tissue regions
- **Other labels**: Vista3D organ segmentations (lung parenchyma, airways, vessels)

---

## 🗂️ File Structure

```
LIDC-IDRI/
├── LIDC-IDRI-Segmentation-Processing-HAID.ipynb  # Processing notebook
│
├── Dataset501_ULNoduleSeg/                        # Original dataset
│   ├── imagesTr/                                  # Training CT volumes (649 files)
│   ├── imagesTs/                                  # Test CT volumes (226 files)
│   ├── labelsTr/                                  # Training nodule masks (649 files)
│   ├── labelsTs/                                  # Test nodule masks (226 files)
│   ├── Dataset501_ULNoduleSeg_dataset.json        # Original dataset descriptor
│   └── split_final.json                           # Fold assignments
│
├── vista3Dauto_seg/                               # Vista3D organ segmentations
│   ├── LIDCIDRI_0001_0000_seg.nii.gz
│   └── ... (875 files)
│
├── vista3Dauto_seg_plus_orgGT/                    # Final combined segmentations
│   ├── LIDCIDRI_0001_0000_seg_sh.nii.gz          # Nodule + Organ + Body
│   └── ... (875 files)
│
├── LIDCIDRI_Split_Dataset501_ULNoduleSeg_dataset.csv  # Split metadata
├── LIDCIDRI_512xy_256z_771p25m.json               # Dataset descriptor
├── LIDC_IDRI_tr_SpaingSize_info.csv               # Training image statistics
└── LIDC_IDRI_ts_SpaingSize_info.csv               # Test image statistics
```

---

## 🛠️ Software Dependencies

### Core Libraries
- **SimpleITK** 2.0.0+ (Image I/O, connected components, thresholding)
- **numpy** 1.20.0+ (Array operations)
- **pandas** 1.3.0+ (Metadata management)
- **scipy** 1.7.0+ (Morphological operations)

### Visualization & Analysis
- **matplotlib** 3.4.0+ (Plotting)
- **seaborn** 0.11.0+ (Statistical visualization)

### Deep Learning (Optional)
- **MONAI** 0.7.0+ (Medical imaging deep learning)
- **nnU-Net** (Auto-configured segmentation)

### Installation
```bash
pip install SimpleITK>=2.0.0 numpy>=1.20.0 pandas>=1.3.0 scipy>=1.7.0
pip install matplotlib>=3.4.0 seaborn>=0.11.0
```

---

## 📈 Processing Highlights

### Multi-Radiologist Consensus Approach
- **Union operation** ensures comprehensive nodule coverage
- Captures inter-observer variability
- Reduces false negatives in training data
- Provides "maximum extent" ground truth

### Body Mask Generation
- **Threshold**: -300 HU (separates body from air)
- **Connected components**: Extracts largest body region
- **Hole filling**: Creates continuous anatomical mask
- **Purpose**: Provides anatomical context for background labeling

### Segmentation Integration Strategy
1. Start with Vista3D multi-organ segmentation (baseline)
2. Override with nodule union masks (Label 23) - highest priority
3. Fill remaining body regions (Label 200) - intermediate priority
4. Preserve background air (Label 0) - lowest priority

---

## 🔗 Related Resources

- **Original LIDC-IDRI**: https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI
- **TCIA Collection**: The Cancer Imaging Archive
- **Vista3D Model**: NVIDIA MONAI Vista3D foundation model
- **Processing Code**: https://github.com/fitushar/HAID
- **Processed By**: Fakrul Islam Tushar

---

## 📝 Citation

If you use this pre-processed dataset, please cite:

1. **Original LIDC-IDRI Dataset**:
   ```
   Armato III, S. G., et al. (2011). 
   The Lung Image Database Consortium (LIDC) and Image Database Resource Initiative (IDRI): 
   A completed reference database of lung nodules on CT scans. 
   Medical Physics, 38(2), 915-931.
   ```

2. **TCIA**:
   ```
   Clark, K., et al. (2013). 
   The Cancer Imaging Archive (TCIA): Maintaining and operating a public information repository. 
   Journal of Digital Imaging, 26(6), 1045-1057.
   ```

3. **Pre-processed Dataset**:
   ```
   Fakrul Islam Tushar. (2026). 
   LIDC-IDRI Pre-processed with Multi-Radiologist Union and Organ Segmentation.
   GitHub: https://github.com/fitushar/HAID
   ```

---

## 📌 Notes

**Annotation Philosophy**: Multi-radiologist union approach prioritizes sensitivity over specificity  
**Clinical Context**: Comprehensive lung nodule detection and segmentation benchmark  
**Label Priority**: Nodule (23) > Body (200) > Organ (Vista3D) > Background (0)  
**Unique Features**: Integration of expert consensus with foundation model organ segmentation

---

**Document Version**: 1.0  
**Last Updated**: January 18, 2026  
**Processed By**: Fakrul Islam Tushar  
**Contact**: GitHub - https://github.com/fitushar/HAID
