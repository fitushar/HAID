# BIMCV-R Dataset - Analysis and Proposed Splits

This document provides an overview of the **BIMCV-R** dataset - a large-scale chest CT dataset with radiological findings and Spanish/English radiology reports.

---

## 📂 Dataset Information

**Dataset Name**: BIMCV-R (BIMCV Radiological Reports)  
**Source**: BIMCV (Medical Imaging Databank of the Valencia Region)  
**Reference**: Chen et al., 2024  
**Paper**: "BIMCV-R: A landmark dataset for 3D CT volumes and radiology reports"  
**Original Dataset**: https://huggingface.co/datasets/cyd0806/BIMCV-R  
**Total Patients**: 5,340 unique patients  
**Total CT Scans**: 8,069 chest CT volumes  
**Radiology Reports**: Bilingual (Spanish + English translations)  
**Status**: Analysis and proposed splits completed (pre-processing not yet performed)  
**Processed By**: Fakrul Islam Tushar  
**GitHub Repository**: https://github.com/fitushar/HAID

### Dataset Characteristics
- **Multi-instance patients**: 1.5 CT scans per patient (mean)
- **Radiological findings**: 10+ major findings with co-occurrence patterns
- **Report language**: Spanish (original) + English (machine translated)
- **Clinical context**: Real-world hospital data from Valencia, Spain
- **COVID-19 cohort**: Significant COVID-19 cases included (2,152 instances)

---

## 📊 Dataset Statistics

### Top Radiological Findings
| Finding | Total Instances | Prevalence |
|---------|----------------|------------|
| Ground Glass Pattern | 2,776 | 34.4% |
| Pneumonia | 2,466 | 30.6% |
| COVID-19 | 2,152 | 26.7% |
| Nodule | 1,966 | 24.4% |
| Pleural Effusion | 1,605 | 19.9% |
| Unchanged | 1,492 | 18.5% |
| Adenopathy | 1,357 | 16.8% |
| Vertebral Degenerative Changes | 1,214 | 15.0% |
| Calcified Densities | 1,172 | 14.5% |
| Consolidation | 1,012 | 12.5% |

### Proposed Dataset Splits (Patient-Level)
| Split | Patients | CT Scans | Percentage |
|-------|----------|----------|------------|
| **Train** | 4,272 | 6,441 | 80% / 79.8% |
| **Validation** | 534 | 812 | 10% / 10.1% |
| **Test** | 534 | 816 | 10% / 10.1% |

**Split Strategy**: Patient-level stratification (no patient overlap across splits)

---

## 🔬 Analysis Performed

### 1️⃣ **Label Distribution Analysis**
- Parsed radiological finding labels from metadata
- Counted frequency of each finding across all 8,069 CT scans
- Identified top 20 most common findings
- Generated distribution bar plots

### 2️⃣ **Co-occurrence Analysis**
- Created co-occurrence matrix for top 20 findings
- Visualized finding combinations via heatmap
- Identified common finding patterns (e.g., COVID-19 + ground glass, pneumonia + consolidation)

### 3️⃣ **Split Proposal**
- Patient-level 80/10/10 train/validation/test split
- Ensured no patient appears in multiple splits
- Balanced finding distribution across splits
- Computed per-finding statistics for each split

### 4️⃣ **Report Text Search**
- Implemented keyword search functionality for radiology reports
- Example searches: "atelectasis", "pneumothorax", specific findings

---

## 🗂️ File Structure

```
BIMCVR/
├── BIMCV_DataAnalysis.ipynb                    # Analysis notebook
├── Chen-2024-Bimcv-r-a-landmark-dataset-for-d-ct.pdf  # Original paper
│
└── metadata/
    ├── bimcv_split_summary.csv                 # Patient/CT counts per split
    ├── bimcv_split_summary_table.csv           # Finding distribution across splits
    ├── bimcv_finding_distribution.csv          # Top findings statistics
    ├── bimcv_train.csv                         # Training split metadata
    ├── bimcv_val.csv                           # Validation split metadata
    ├── bimcv_test.csv                          # Test split metadata
    └── co_occurrence_heatmap_top20.png         # Finding co-occurrence visualization
```

---

## 🛠️ Analysis Code

**Notebook**: [BIMCV_DataAnalysis.ipynb](BIMCV_DataAnalysis.ipynb)

**Key Functions**:
- Label parsing from string lists
- Patient-level stratified splitting
- Finding frequency counting
- Co-occurrence matrix generation
- Report text search

**Libraries Used**:
- pandas, numpy (data manipulation)
- matplotlib, seaborn (visualization)
- sklearn.model_selection (train_test_split)
- ast (parsing stringified lists)

---

## 📋 Finding Distribution Across Splits

| Finding | Train | Validation | Test |
|---------|-------|------------|------|
| Ground Glass Pattern | 2,182 (78.6%) | 300 (10.8%) | 294 (10.6%) |
| Pneumonia | 1,975 (80.1%) | 234 (9.5%) | 257 (10.4%) |
| COVID-19 | 1,719 (79.9%) | 212 (9.9%) | 221 (10.3%) |
| Nodule | 1,574 (80.1%) | 207 (10.5%) | 185 (9.4%) |
| Pleural Effusion | 1,262 (78.6%) | 171 (10.7%) | 172 (10.7%) |
| Adenopathy | 1,040 (76.6%) | 141 (10.4%) | 176 (13.0%) |
| Consolidation | 790 (78.1%) | 93 (9.2%) | 129 (12.7%) |

**Balance**: Splits maintain approximately 80/10/10 distribution for most findings.

---

## 🔗 Related Resources

- **Original Publication**: Chen et al., 2024 - "BIMCV-R: A landmark dataset for 3D CT volumes and radiology reports"
- **Original Dataset**: https://huggingface.co/datasets/cyd0806/BIMCV-R
- **Analysis Code**: https://github.com/fitushar/HAID
- **Processed By**: Fakrul Islam Tushar

---

## 📝 Citation

If you use this split or analysis, please cite:

1. **Original BIMCV-R Dataset**:
   ```
   Chen et al. (2024). 
   BIMCV-R: A landmark dataset for 3D CT volumes and radiology reports.
   [Add full citation with DOI]
   ```

2. **Analysis and Splits**:
   ```
   Fakrul Islam Tushar. (2026). 
   BIMCV-R Dataset Analysis and Proposed Splits.
   GitHub: https://github.com/fitushar/HAID
   ```

---

## 📌 Notes

**Current Status**: Analysis phase - splits proposed but no pre-processing applied yet  
**Next Steps**: Image resampling, standardization, NIfTI conversion (if needed)  
**Intended Use**: Multi-label classification, report generation, vision-language models, COVID-19 detection

---

**Document Version**: 1.0  
**Last Updated**: January 17, 2026  
**Processed By**: Fakrul Islam Tushar  
**Contact**: GitHub - https://github.com/fitushar/HAID
