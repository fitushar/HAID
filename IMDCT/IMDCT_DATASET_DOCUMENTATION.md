# IMDCT Dataset Processing Pipeline - Complete Documentation

This document provides comprehensive documentation for the **IMDCT (Indeterminate Pulmonary Nodules Multi-institutional CT Dataset)**, a multi-institutional dataset comprising 2,032 patients with indeterminate pulmonary nodules (IPNs) with histopathological confirmation, as described in Zhao et al. [1].

---

## 📂 Dataset Information

**Dataset Name**: IMDCT (Indeterminate Pulmonary Nodules Multi-institutional CT Dataset)  
**Source**: Multi-institutional collection  
**Reference**: Zhao et al. [1]  
**Original Dataset**: https://zenodo.org/records/13908015  
**Total Patients**: 2,032 unique patients  
**Total CT Scans**: 2,032  
**Total Nodule Annotations**: 2,032 (one per patient)  
**Histopathological Confirmation**: All nodules confirmed by pathology  
**Pre-processed Data Repository**: Available on Zenodo at **[xxx]** (replace with your DOI)  
**Metadata & Annotations**: All generated CSV files saved in local directory  
**Processed By**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID

### Dataset Characteristics
- **One annotated nodule per patient**
- **Malignancy rate**: 78.6% malignant, 21.4% benign
- **Patient age**: 55.9 ± 12.3 years (mean ± SD)
- **Solid component size**: 15.7 ± 13.2 mm (mean ± SD)
- **Nodule diameter**: 30.0 ± 20.8 mm (mean ± SD)
- **Nodule size distribution**: No sub-centimeter nodules; predominantly intermediate (37.9%), large (26.8%), and very large (33.8%)

### Dataset Splits
- **Training Set**: 1,625 patients (80%)
- **Validation Set**: 203 patients (10%)
- **Test Set**: 204 patients (10%)
- **Split Strategy**: Random split ensuring balanced cancer label distribution

---

## 🔄 Complete Processing Pipeline

### 1️⃣ **Data Collection & Multi-institutional Aggregation**
**Purpose**: Compile CT scans and annotations from multiple clinical institutions

**Process**:
- Collected from multiple medical institutions for diverse scanner representation
- Each patient contributes one CT scan with one annotated indeterminate pulmonary nodule
- Nodules identified and annotated by expert radiologists
- Histopathological confirmation obtained for all nodules (benign vs malignant)
- Quality control performed to ensure annotation accuracy

**Inclusion Criteria**:
- Indeterminate pulmonary nodules requiring diagnostic workup
- Histopathological confirmation available
- Complete CT imaging available
- Nodule size ≥6 mm (no sub-centimeter nodules included)

---

### 2️⃣ **Histopathological Confirmation & Labeling**
**Purpose**: Establish ground truth malignancy labels through pathology

**Malignancy Distribution**:
- **Benign (Label 0)**: 434 nodules (21.4%)
  - Histologically confirmed benign lesions
  - Includes granulomas, hamartomas, and other benign pathologies
- **Malignant (Label 1)**: 1,598 nodules (78.6%)
  - Histologically confirmed malignancies
  - Includes primary lung cancers and metastatic lesions

**Label Validation**:
- Gold standard pathology reports
- No ambiguous or unconfirmed cases included
- Binary classification task (benign vs malignant)

---

### 3️⃣ **Nodule Annotation & Size Measurement**
**Purpose**: Characterize nodule dimensions and solid component

**Measurements Collected**:
- **Solid Component Size**: Maximum diameter of solid portion (mm)
  - Mean: 15.7 ± 13.2 mm
  - Important for Lung-RADS and risk stratification
- **Total Nodule Diameter**: Maximum 3D diameter (mm)
  - Mean: 30.0 ± 20.8 mm
  - Includes solid and ground-glass components

**Nodule Size Categories**:
- **Sub-centimeter (<6 mm)**: 0 nodules (0.0%)
- **Small (6–10 mm)**: 30 nodules (1.5%)
- **Intermediate (10–20 mm)**: 771 nodules (37.9%)
- **Large (20–30 mm)**: 545 nodules (26.8%)
- **Very Large (>30 mm)**: 686 nodules (33.8%)

**Annotation Protocol**:
- Expert radiologist review
- Consistent measurement methodology across institutions
- Maximum axial diameter recorded
- Solid component separately measured

---

### 4️⃣ **Dataset Splitting & Stratification**
**Purpose**: Create reproducible train/validation/test splits with balanced characteristics

**Splitting Strategy**:
- **Random split**: 80% training, 10% validation, 10% test
- **Stratification criteria**:
  - Balanced cancer label distribution across splits
  - Similar patient age distributions
  - Comparable nodule size distributions
- **Reproducibility**: Fixed random seed for consistent splits

**Split Validation**:
- Chi-square tests for categorical balance (malignancy rate)
- T-tests for continuous variable balance (age, size)
- Visual inspection of distribution plots (Figure S8)

**Results**:
- Training: 1,625 patients (78.6% malignant rate)
- Validation: 203 patients (78.8% malignant rate)
- Test: 204 patients (78.4% malignant rate)
- No significant differences in patient characteristics across splits

---

### 5️⃣ **3D Bounding Box Annotation Extraction** (if applicable)
**Purpose**: Derive 3D bounding boxes from nodule annotations for detection tasks

**Process**:
- Extract bounding box from segmentation masks or radiologist annotations
- Convert to world coordinates (mm)
- Calculate center point and dimensions (width, height, depth)
- Store with corresponding malignancy label

**Outputs**:
- `IMDCT_bounding_boxes_annotations.csv`
- Columns: PatientID, coordX, coordY, coordZ, w, h, d, cancer_label

---

### 6️⃣ **Image Preprocessing & Resampling** (if performed)
**Purpose**: Standardize CT spacing for consistent model training

**Target Spacing** (if applicable): `[0.703125, 0.703125, 1.25]` mm or institution-specific

**Process**:
- Resample CT images to uniform spacing
- B-spline interpolation for CT images
- Preserve Hounsfield Unit intensity values
- Maintain spatial metadata

---

### 7️⃣ **Metadata Integration & Summary Statistics**
**Purpose**: Compile comprehensive clinical and imaging metadata

**Metadata Fields**:
- **Patient Information**:
  - Patient ID (anonymized)
  - Age (years)
- **Nodule Characteristics**:
  - Solid component size (mm)
  - Total diameter (mm)
  - Size category (small/intermediate/large/very large)
  - Cancer label (0=benign, 1=malignant)
- **Dataset Assignment**:
  - Split (train/validation/test)

**Statistical Summaries**:
- Generated for publication (Table S6)
- Stratified by dataset split
- Both categorical (counts, percentages) and continuous (mean ± SD) variables

---

## 📊 Complete Output Summary

| Output Type | File Name | Location | Description |
|------------|-----------|----------|-------------|
| **CT Images** | `{PatientID}_0000.nii.gz` | `IMDCT_nifti_ct/` | CT scans in NIfTI format |
| **Segmentation Masks** | `{PatientID}_mask.nii.gz` | `IMDCT_nifti_mask/` | Nodule segmentation masks |
| **Metadata CSV** | `IMDCT_dataset_metadata.csv` | Working directory | Complete patient and nodule metadata |
| **Train Split** | `IMDCT_train_split.csv` | Working directory | Training set (1,625 patients) |
| **Validation Split** | `IMDCT_validation_split.csv` | Working directory | Validation set (203 patients) |
| **Test Split** | `IMDCT_test_split.csv` | Working directory | Test set (204 patients) |
| **Bounding Boxes** | `IMDCT_bounding_boxes_annotations.csv` | Working directory | 3D bounding box annotations |
| **Summary Statistics** | `IMDCT_summary_statistics.csv` | Working directory | Table S6 data |

---

## 🔬 Final Dataset Characteristics

### Cohort Summary
- **Total Patients**: 2,032
- **Total CT Scans**: 2,032 (one per patient)
- **Total Nodule Annotations**: 2,032 (one per patient)
- **Image Modality**: CT (Computed Tomography)
- **Annotation Type**: Expert-annotated indeterminate pulmonary nodules
- **Pathological Confirmation**: 100% histopathologically confirmed

### Clinical Characteristics
- **Patient Age**: 55.9 ± 12.3 years (mean ± SD)
  - Training: 55.8 ± 12.6 years
  - Validation: 57.2 ± 11.0 years
  - Test: 55.6 ± 11.6 years

### Malignancy Distribution
- **Overall Malignancy Rate**: 78.6%
- **Benign (Label 0)**: 434 nodules (21.4%)
- **Malignant (Label 1)**: 1,598 nodules (78.6%)
- **Balanced across splits**: ~78% malignant in all subsets

### Nodule Size Characteristics
- **Solid Component Size**: 15.7 ± 13.2 mm (mean ± SD)
  - Training: 15.4 ± 12.9 mm
  - Validation: 18.3 ± 15.4 mm
  - Test: 15.6 ± 13.2 mm
- **Total Nodule Diameter**: 30.0 ± 20.8 mm (mean ± SD)
  - Training: 29.6 ± 20.3 mm
  - Validation: 33.8 ± 24.2 mm
  - Test: 29.2 ± 20.3 mm

### Nodule Size Categories
- **Sub-centimeter (<6 mm)**: 0 (0.0%) - Excluded from dataset
- **Small (6–10 mm)**: 30 (1.5%)
- **Intermediate (10–20 mm)**: 771 (37.9%)
- **Large (20–30 mm)**: 545 (26.8%)
- **Very Large (>30 mm)**: 686 (33.8%)

### Dataset Split Distribution
- **Training**: 1,625 patients (80.0%), 1,278 malignant (78.6%)
- **Validation**: 203 patients (10.0%), 160 malignant (78.8%)
- **Test**: 204 patients (10.0%), 160 malignant (78.4%)

---

## ⚙️ Software Dependencies

### Core Libraries
```python
# Medical Image I/O
SimpleITK >= 2.0.0          # Medical image reading/writing/processing
pydicom >= 2.0.0            # DICOM file handling
nibabel >= 3.2.0            # NIfTI file handling

# Data Processing
pandas >= 1.3.0             # DataFrame operations
numpy >= 1.20.0             # Numerical operations

# Visualization
matplotlib >= 3.4.0         # Plotting
seaborn >= 0.11.0           # Statistical visualizations

# Machine Learning
scikit-learn >= 0.24.0      # Dataset splitting

# Statistics
scipy >= 1.7.0              # Statistical tests
tabulate                    # Table formatting
```

### Installation
```bash
pip install SimpleITK pydicom nibabel pandas numpy matplotlib seaborn scikit-learn scipy tabulate
```

---

## 📖 Citation & License

### Dataset Citation
If you use this dataset or processing pipeline, please cite:

**Primary Reference**:
> Zhao et al. [1] - [Add full citation details]

**Original Dataset**:
> Available at: https://zenodo.org/records/13908015

### Pre-processed Data
Pre-processed CT images with annotations and metadata are available at:
**Zenodo Repository**: [xxx] (replace with your DOI after upload)

---

## 📝 Processing Notes & Recommendations

### Key Features of IMDCT Dataset
1. **Histopathological Confirmation**: 100% pathology-confirmed diagnoses (gold standard)
2. **High Malignancy Rate**: 78.6% malignant nodules - enriched for cancer cases
3. **Clinically Relevant Sizes**: Predominantly intermediate to very large nodules (10-30+ mm)
4. **Multi-institutional**: Diverse scanner manufacturers and protocols
5. **One Nodule Per Patient**: Simplified task with single target per scan
6. **Balanced Splits**: Consistent malignancy rates across train/val/test sets

---

## 👨‍💻 Processing Information

**Dataset Compiled**: As described in Zhao et al. [1]  
**Processing Date**: January 2026  
**Dataset Version**: 1.0  
**Number of Institutions**: Multi-institutional (specific number TBD)  
**Hardware Requirements**: Minimum 16GB RAM, sufficient storage for 2,032 CT scans

---

## 🔗 Related Resources

- **Original Publication**: Zhao et al. [1] [Add DOI/link]
- **Original Dataset**: https://zenodo.org/records/13908015
- **Pre-processed Data**: [Zenodo - xxx]
- **Processing Code & Documentation**: https://github.com/fitushar/HAID
- **Processed By**: Fakrul Islam Tushar
- **Processing Notebooks**: [GitHub repository link]

---

## 📂 Repository Structure

```
IMDCT/
├── IMDCT_dataset_metadata.csv                    # Complete metadata
├── IMDCT_train_split.csv                         # Training set (1,625 patients)
├── IMDCT_validation_split.csv                    # Validation set (203 patients)
├── IMDCT_test_split.csv                          # Test set (204 patients)
├── IMDCT_bounding_boxes_annotations.csv          # 3D bounding boxes
├── IMDCT_summary_statistics.csv                  # Table S6 data
├── IMDCT_nifti_ct/                               # CT images
│   ├── patient_0001_0000.nii.gz
│   ├── patient_0002_0000.nii.gz
│   └── ...
├── IMDCT_nifti_mask/                             # Segmentation masks
│   ├── patient_0001_mask.nii.gz
│   ├── patient_0002_mask.nii.gz
│   └── ...
└── IMDCT_DATASET_DOCUMENTATION.md                # This documentation
```

---

## 📊 Summary Tables & Figures

### Table S6: Patient, CT Scan, and Lesion Characteristics
Comprehensive summary of patient demographics, nodule characteristics, and malignancy distribution across training, validation, and test splits. Shows balanced distribution with ~80% training, 10% validation, 10% test, and consistent 78% malignancy rate across all subsets.

### Figure S8: Nodule Diameter Distribution
- **(a) Violin Plots**: Distribution and spread of nodule diameters across splits, showing similar patterns in all three subsets with median values and interquartile ranges clearly visible
- **(b) Kernel Density Estimates**: Close alignment of KDE curves demonstrates consistent size distributions between training, validation, and test sets, validating effective stratification

---

## 📦 Zenodo Upload Description Template

**Copy and paste this text into your Zenodo upload description:**

---

### IMDCT Dataset: Multi-institutional CT Scans of Indeterminate Pulmonary Nodules with Histopathological Confirmation

**Description:**

This dataset contains 2,032 chest CT scans with indeterminate pulmonary nodules (IPNs) from multiple clinical institutions, all with histopathological confirmation of malignancy status. Each patient has one annotated nodule with expert delineation and gold-standard pathology diagnosis. This dataset is ideal for developing and validating computer-aided diagnosis systems for lung nodule malignancy prediction.

**What's Included:**

1. **CT Images** (2,032 scans)
   - One CT scan per patient
   - Format: NIfTI (.nii.gz)
   - Hounsfield Unit intensity values
   - Multi-institutional acquisition (diverse scanner types)

2. **Nodule Annotations** (2,032 nodules)
   - One indeterminate pulmonary nodule per patient
   - Expert radiologist delineation
   - Segmentation masks available
   - 3D bounding box coordinates

3. **Histopathological Labels**
   - **Benign (Label 0)**: 434 nodules (21.4%)
   - **Malignant (Label 1)**: 1,598 nodules (78.6%)
   - 100% pathology-confirmed (gold standard)
   - No ambiguous or unconfirmed cases

4. **Clinical Metadata**
   - Patient age: 55.9 ± 12.3 years (mean ± SD)
   - Solid component size: 15.7 ± 13.2 mm
   - Total nodule diameter: 30.0 ± 20.8 mm
   - Nodule size categories (small/intermediate/large/very large)

5. **Pre-defined Dataset Splits**
   - Training: 1,625 patients (80%)
   - Validation: 203 patients (10%)
   - Test: 204 patients (10%)
   - Balanced malignancy rates across all splits (~78% malignant)

**Dataset Characteristics:**

- **Total Patients**: 2,032 unique patients
- **Pathology Confirmation**: 100% histologically confirmed
- **Malignancy Rate**: 78.6% malignant, 21.4% benign
- **Patient Age**: Mean 55.9 ± 12.3 years
- **Nodule Sizes**: Predominantly intermediate (37.9%), large (26.8%), and very large (33.8%)
- **No Sub-centimeter Nodules**: All nodules ≥6mm (clinically significant)
- **One Nodule Per Patient**: Simplified annotation structure

**Intended Use:**

- Lung nodule malignancy classification (benign vs malignant)
- Computer-aided diagnosis (CAD) system development
- Risk stratification models for indeterminate pulmonary nodules
- Radiomics and deep learning research
- Clinical decision support tools
- Comparison benchmarks for lung cancer prediction algorithms
- Multi-task learning (detection + classification)

**Clinical Relevance:**

This dataset addresses a critical clinical challenge: determining malignancy status of indeterminate pulmonary nodules detected on CT scans. Accurate prediction can:
- Reduce unnecessary invasive procedures for benign nodules
- Enable early intervention for malignant nodules
- Improve patient outcomes through timely diagnosis
- Reduce healthcare costs and patient anxiety

**File Structure:**

```
imdct_dataset.zip
├── IMDCT_nifti_ct/                               # 2,032 CT scans
├── IMDCT_nifti_mask/                             # 2,032 segmentation masks
├── IMDCT_dataset_metadata.csv                    # Complete metadata
├── IMDCT_train_split.csv                         # Training set
├── IMDCT_validation_split.csv                    # Validation set
├── IMDCT_test_split.csv                          # Test set
├── IMDCT_bounding_boxes_annotations.csv          # 3D bounding boxes
└── README.txt                                     # Quick start guide
```

**Quality Assurance:**

- Multi-institutional data collection for diversity
- Expert radiologist annotations
- Histopathological confirmation for all nodules
- Quality control for annotation accuracy
- Balanced dataset splits with stratification
- Validated consistent distributions across splits (see Figure S8)

**Citation:**

If you use this dataset, please cite:

1. **Original Dataset Reference:**
   Zhao et al. [1] [Add full citation]
   Original dataset: https://zenodo.org/records/13908015

2. **This Dataset Release:**
   [Your Name/Lab] (2026). IMDCT Dataset: Multi-institutional CT Scans of Indeterminate Pulmonary Nodules with Histopathological Confirmation. Zenodo. DOI: [Your Zenodo DOI]

**Related Links:**

- Original dataset: https://zenodo.org/records/13908015
- Original publication: Zhao et al. [1] [Add DOI/link]
- Processing code & documentation: https://github.com/fitushar/HAID
- Processed by: Fakrul Islam Tushar

**License:**

[Specify license - e.g., CC BY 4.0, MIT, etc.]  
All data is de-identified according to HIPAA standards.

**Keywords:** lung nodules, indeterminate pulmonary nodules, malignancy classification, histopathology, multi-institutional, CT imaging, computer-aided diagnosis, deep learning, lung cancer, pathology confirmation

---

**Note:** Remember to replace `[Your Zenodo DOI]`, `[Your GitHub repository]`, and other placeholders with actual values.

---

**End of Documentation**

For questions or issues with this dataset, please contact the maintainer or open an issue in the repository.

---

**Last Updated**: January 17, 2026
