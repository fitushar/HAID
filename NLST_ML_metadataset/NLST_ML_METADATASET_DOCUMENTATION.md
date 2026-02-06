# NLST ML Metadataset Processing Pipeline - Documentation

This document provides documentation for the **NLST ML Metadataset** - a comprehensive nodule-level analysis dataset derived from the National Lung Screening Trial (NLST) with cleaned and engineered features for machine learning applications.

---

## 📂 Dataset Information

**Dataset Name**: NLST ML Metadataset (National Lung Screening Trial - Machine Learning Ready)  
**Source**: National Lung Screening Trial (NLST)  
**Original Dataset**: https://cdas.cancer.gov/nlst/  
**Total Participants**: CT screening arm participants  
**Focus**: Non-calcified nodules ≥ 4 mm (abnormality code 51)  
**Clinical Task**: Lung cancer risk prediction and nodule characterization  
**Processed By**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID

### Dataset Characteristics
- **Nodule-level analysis**: Each row represents a single CT-detected nodule
- **Comprehensive metadata**: Demographics, nodule features, cancer outcomes
- **Feature engineering**: Clinical risk factors derived from raw NLST data
- **Split by CT Set**: Set-1 and Set-2 for temporal validation
- **Inclusion criteria**: Non-calcified nodules ≥ 4 mm with complete metadata
- **Machine learning ready**: Cleaned, decoded, and structured for ML pipelines

### Dataset Splits
- **Set-1**: NLST CT Set-1 participants (temporal cohort 1)
- **Set-2**: NLST CT Set-2 participants (temporal cohort 2)

### Clinical Context
- **NLST Study**: Landmark randomized controlled trial comparing CT vs. chest X-ray screening
- **Outcome**: 20% reduction in lung cancer mortality with CT screening
- **Target population**: High-risk smokers (age 55-74, ≥30 pack-years smoking history)

---

## 🔄 Complete Processing Pipeline

### 1️⃣ **Data Extraction and Merging**
**Purpose**: Combine participant metadata with CT abnormality records to create comprehensive nodule-level dataset

**Input Files**:
- `participant_d040722.csv` (participant demographics and outcomes)
- `Spiral CT Abnormalities/sct_abnormalities_d040722.csv` (CT nodule detections)

**Process**:
```python
# Step 1: Load participant table
participants = pd.read_csv('participant_d040722.csv')

# Step 2: Load CT abnormalities table
ct_abnormalities = pd.read_csv('sct_abnormalities_d040722.csv')

# Step 3: Merge on participant ID
nodule_df = ct_abnormalities.merge(participants, on='pid', how='left')
```

**Output**:
- Merged nodule-level dataset with participant metadata
- Each row = one detected nodule with full participant context

---

### 2️⃣ **Categorical Variable Decoding**
**Purpose**: Convert numerical codes to human-readable labels for interpretation

**Decoded Variables**:

**Gender Decoder**:
```python
GENDER_DECODER = {1: 'Male', 2: 'Female'}
```

**Race Decoder**:
```python
RACE_DECODER = {
    1: 'White/Caucasian',
    2: 'Black/African American', 
    3: 'Hispanic',
    4: 'Asian',
    5: 'American Indian/Alaskan Native',
    6: 'Native Hawaiian/Pacific Islander',
    7: 'More than one race',
    99: 'Unknown/Not reported'
}
```

**Screening Group Decoder**:
```python
screening_group_decoder = {
    1: 'CT Screening',
    2: 'Chest X-ray Screening'
}
```

**Cancer Screening Outcome Decoder**:
```python
can_scr_decoder = {
    1: 'No Cancer',
    2: 'Lung Cancer - Screening Detected',
    3: 'Lung Cancer - Clinical Detection',
    4: 'Other Cancer'
}
```

**Nodule Location Decoder** (Lobe):
```python
LOBE_DECODER = {
    1: 'Right Upper Lobe',
    2: 'Right Middle Lobe',
    3: 'Right Lower Lobe',
    4: 'Left Upper Lobe',
    5: 'Left Lower Lobe',
    6: 'Multiple Lobes',
    99: 'Unknown'
}
```

**Nodule Attenuation/Type Decoder**:
```python
ATTENUATION_DECODER = {
    1: 'Solid',
    2: 'Part-solid',
    3: 'Ground-glass',
    4: 'Other/Unknown'
}
```

**Nodule Margin Decoder**:
```python
MARGIN_DECODER = {
    1: 'Smooth',
    2: 'Lobulated',
    3: 'Spiculated',
    4: 'Irregular',
    99: 'Unknown'
}
```

**Process**:
- Apply decoders to convert numerical codes to text labels
- Facilitate human interpretation and clinical relevance

---

### 3️⃣ **Cohort Filtering and Inclusion Criteria**
**Purpose**: Apply clinical criteria to create a well-defined analysis cohort

**Inclusion Criteria**:
1. **Study arm**: CT screening arm only (`rndgroup == 1`)
2. **Abnormality type**: Non-calcified nodule/mass ≥ 4 mm (`sct_ab_desc == 51`)
3. **Complete nodule size**: Non-missing `sct_long_dia` (longest diameter)
4. **Complete nodule type**: Non-missing `sct_pre_att` (attenuation)
5. **CT Set assignment**: Non-missing `all_sct_set` (Set-1 or Set-2)
6. **Complete demographics**: Non-missing Family History and emphysema diagnosis
7. **Valid nodule types**: Solid, part-solid, or ground-glass only (exclude "others/unknown")

**Exclusion Criteria**:
- Calcified nodules
- Nodules < 4 mm
- Missing critical metadata
- Chest X-ray screening arm participants

**Process**:
```python
# Filter to CT arm only
df = df[df['rndgroup'] == 1]

# Filter to non-calcified nodules ≥ 4mm
df = df[df['sct_ab_desc'] == 51]

# Drop missing values
df = df.dropna(subset=['sct_long_dia', 'sct_pre_att', 'all_sct_set', 
                       'Family_History', 'diagemph'])

# Keep only valid nodule types
df = df[df['Nodule_Type'].isin(['solid', 'part-solid', 'ground-glass'])]
```

---

### 4️⃣ **Feature Engineering**
**Purpose**: Derive clinically meaningful features for machine learning models

**Engineered Features**:

**1. Family History** (Binary):
```python
# Aggregate family history across all relatives
Family_History = max(fambrother, famchild, famfather, fammother, famsister)
# Output: 0 = No family history, 1 = Positive family history
```

**2. Nodule Type** (Categorical):
```python
# Map attenuation to standardized nodule type
Nodule_Type = map(sct_pre_att, {
    'solid': 1,
    'part-solid': 2,
    'ground-glass': 3
})
```

**3. Spiculation** (Binary):
```python
# Extract spiculation as key malignancy risk factor
Spiculation = 1 if sct_margins == 'spiculated' else 0
```

**4. Upper Lobe Location** (Binary):
```python
# Upper lobe nodules have higher malignancy risk
Upper_Lobe = 1 if sct_epi_loc in ['RUL', 'LUL', 'RML'] else 0
```

**5. Cancer Label** (Binary):
```python
# Binary outcome for supervised learning
Cancer_lbl = 0 if can_scr == 'No Cancer' else 1
```

**6. Primary Cancer Locations** (Text):
```python
# Comma-separated list of lung cancer locations
primary_cancer_locations = ', '.join([loc for loc in lung_locations if loc == 'Yes'])
```

**7. Time-indexed Cancer Flags**:
```python
# Cancer diagnosis at different screening years
lung_cancer_t0 = 1 if cancyr == 0 else 0  # Baseline
lung_cancer_t1 = 1 if cancyr == 1 else 0  # Year 1
lung_cancer_t2 = 1 if cancyr == 2 else 0  # Year 2
```

**8. Match Primary Cancer Location** (Optional):
```python
# Does nodule location match diagnosed cancer location?
match_primary = 1 if nodule_lobe matches primary_cancer_location else 0
```

---

### 5️⃣ **Dataset Splitting by CT Set**
**Purpose**: Separate data by NLST CT Set assignment for temporal validation

**Process**:
```python
# Split by CT Set
set1_df = df[df['all_sct_set'] == 1]
set2_df = df[df['all_sct_set'] == 2]

# Export to CSV
set1_df.to_csv('output_dir/nlst_ct_nodule_df_set1.csv', index=False)
set2_df.to_csv('output_dir/nlst_ct_nodule_df_set2.csv', index=False)
```

**Output Files**:
- `nlst_ct_nodule_df_set1.csv`: Set-1 nodule-level dataset
- `nlst_ct_nodule_df_set2.csv`: Set-2 nodule-level dataset

---

## 📊 Final Dataset Schema

### Core Columns

| Column | Type | Description |
|--------|------|-------------|
| `pid` | Integer | Participant ID (unique patient identifier) |
| `study_yr` | Integer | Screening year (0, 1, 2) |
| `age` | Integer | Participant age at screening |
| `gender` | Categorical | Male / Female |
| `race` | Categorical | Decoded race/ethnicity |
| `all_sct_set` | Integer | CT Set assignment (1 or 2) |
| `sct_long_dia` | Float | Nodule longest diameter (mm) |
| `sct_margins` | Categorical | Nodule margin characteristics |
| `sct_pre_att` | Categorical | Nodule attenuation type |
| `sct_epi_loc` | Categorical | Anatomical lobe location |
| `can_scr` | Categorical | Cancer screening outcome |
| `diagemph` | Binary | Emphysema diagnosis (0/1) |
| `Family_History` | Binary | Family history of lung cancer (0/1) |

### Engineered Features

| Column | Type | Description |
|--------|------|-------------|
| `Nodule_Type` | Categorical | solid / part-solid / ground-glass |
| `Spiculation` | Binary | Spiculated margins (0/1) |
| `Upper_Lobe` | Binary | Upper lobe location (0/1) |
| `Cancer_lbl` | Binary | Cancer outcome label (0 = No Cancer, 1 = Cancer) |
| `primary_cancer_locations` | Text | Comma-separated lung cancer locations |
| `lung_cancer_t0` | Binary | Cancer at baseline (0/1) |
| `lung_cancer_t1` | Binary | Cancer at year 1 (0/1) |
| `lung_cancer_t2` | Binary | Cancer at year 2 (0/1) |

---

## 🔬 Use Cases and Applications

### 1. **Lung Cancer Risk Prediction**
- Train machine learning models to predict malignancy risk
- Features: nodule size, type, margins, location, demographics
- Target: `Cancer_lbl` (binary classification)

### 2. **Nodule Characterization**
- Analyze relationships between nodule features and outcomes
- Compare solid vs. subsolid nodule cancer risk
- Evaluate spiculation as predictive biomarker

### 3. **Temporal Validation**
- Train on Set-1, validate on Set-2 (or vice versa)
- Assess model generalization across temporal cohorts

### 4. **Risk Stratification**
- Combine clinical factors (age, smoking, family history, emphysema)
- Nodule imaging features (size, type, location, margins)
- Develop composite risk scores

### 5. **Feature Importance Analysis**
- Identify strongest predictors of malignancy
- Compare demographic vs. imaging feature contributions
- Guide clinical decision support tool development

---

## 📁 Directory Structure

```
NLST_ML_metadataset/
├── NLST_ML_METADATASET_DOCUMENTATION.md  # This file
├── NLST_ML_Metadataset_prep.ipynb        # Processing notebook
├── scr_dir/                               # Source data directory
│   ├── participant_d040722.csv           # Participant metadata
│   └── Spiral CT Abnormalities/          # CT abnormality tables
│       └── sct_abnormalities_d040722.csv
└── output_dir/                            # Processed output directory
    ├── nlst_ct_nodule_df_set1.csv        # Set-1 nodule dataset
    └── nlst_ct_nodule_df_set2.csv        # Set-2 nodule dataset
```

---

## 🧪 Quality Control

### Data Validation Checks
- ✅ No missing values in critical columns
- ✅ Valid range checks (age, nodule size)
- ✅ Categorical consistency (valid codes only)
- ✅ Unique participant ID integrity
- ✅ Temporal consistency (screening year progression)

### Summary Statistics (Printed During Processing)
- Total participants in CT arm
- Nodule count by abnormality type
- Distribution after each filtering step
- Cancer positive vs. negative counts
- Set-1 vs. Set-2 cohort sizes

---

## 📖 References

1. **National Lung Screening Trial Research Team**. *Reduced Lung-Cancer Mortality with Low-Dose Computed Tomographic Screening*. N Engl J Med. 2011;365(5):395-409.

2. **NLST Data Portal**: https://cdas.cancer.gov/nlst/

3. **TCIA NLST Collection**: https://wiki.cancerimagingarchive.net/display/NLST

---

## 🛠️ Preprocessing Script

**Notebook**: `NLST_ML_Metadataset_prep.ipynb`

**Key Functions**:
- `percentage_and_count(df, column)`: Generate summary statistics with counts and percentages
- Decoder dictionaries: Convert numerical codes to human-readable labels
- Feature engineering functions: Derive clinical risk factors

**Configuration Flags** (in notebook):
```python
FILTER_BY_YEAR = False            # Filter by screening year
FILTER_BY_GENDER = False          # Filter by gender
FILTER_BY_ABNORMALITIES = False   # Filter by abnormality types
PLOT = True                       # Generate visualizations
```

---

## 📞 Contact & Citation

**Processed by**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID  

If you use this processed dataset, please cite:
- Original NLST study publications
- This preprocessing pipeline (GitHub repository)

---

## ⚠️ Data Usage Notes

1. **Access**: NLST data requires approved access through CDAS (Cancer Data Access System)
2. **Privacy**: Patient identifiers are retained only for linking purposes
3. **Clinical validation**: Feature engineering reflects clinical guidelines but should be validated
4. **Temporal bias**: Set-1 and Set-2 may have systematic differences; use appropriate validation strategies
5. **Missing data**: Cases with incomplete metadata are excluded; consider selection bias

---

## 🔄 Version History

**Version 1.0** (February 2026)
- Initial release
- Non-calcified nodules ≥ 4 mm
- Set-1 and Set-2 splits
- Core feature engineering complete

---

*Last Updated: February 6, 2026*
