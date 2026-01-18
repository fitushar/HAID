# HAID - Health AI Data Resource

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

**HAID (Health AI Data)** is a curated public resource providing standardized, research-ready clinical imaging datasets with comprehensive preprocessing pipelines, documentation, and reference implementations for AI/ML model development in medical imaging.

---

## 🎯 Mission

To democratize access to high-quality, preprocessed medical imaging datasets by providing:
- ✅ **Standardized preprocessing** pipelines
- ✅ **Comprehensive documentation** 
- ✅ **Ready-to-use annotations** for detection, segmentation, and classification
- ✅ **Train/validation/test splits** for reproducible benchmarking
- ✅ **Reference implementations** in Jupyter notebooks

---

## 📂 Available Datasets

| Dataset | Modality | Patients | Condition | Status |
|---------|----------|----------|-----------|--------|
| [**NSCLC-Radiomics (NSCLCR)**](#1️⃣-nsclc-radiomics-nsclcr) | CT | 421 | Lung Cancer | ✅ Available |
| More datasets coming soon... | - | - | - | 🔜 Planned |

---

## 📚 Dataset Details

### 1️⃣ NSCLC-Radiomics (NSCLCR)
**Non-Small Cell Lung Cancer CT Imaging with Radiomics Analysis**

#### Dataset Status
- **Modality**: CT (Computed Tomography)
- **Patients**: 421 (1 excluded due to segmentation issues)
- **Condition**: Non-Small Cell Lung Cancer (NSCLC)
- **Source**: [TCIA - The Cancer Imaging Archive](https://www.cancerimagingarchive.net/collection/nsclc-radiomics/)
- **Original Publication**: Aerts et al. (2015) - DOI: [10.7937/K9/TCIA.2015.PF0M9REI](https://doi.org/10.7937/K9/TCIA.2015.PF0M9REI)

#### 🔬 Dataset Features
- **Pre-treatment CT scans**: 512×512×[88-176] voxels, ~0.977mm in-plane, 3mm slice thickness
- **Multi-label segmentations**:
  - Gross Tumor Volume (GTV-1)
  - Esophagus, Heart, Spinal Cord
  - Left & Right Lungs
- **Clinical metadata**: TNM staging, histology, survival time, demographics
- **Bounding box annotations** for tumor detection tasks
- **Train/Validation/Test splits**: 334/41/46 patients (stratified by histology)

#### 📥 Data Access
- **Preprocessed Dataset**: [Zenodo Repository - DOI: 10.5281/zenodo.18284366](https://zenodo.org/records/18284366)
- **Processing Documentation**: [DATASET_PROCESSING_DOCUMENTATION.md](NSCLCR/DATASET_PROCESSING_DOCUMENTATION.md)
- **Processing Notebook**: [NSCLCR_HAID_processing.ipynb](NSCLCR/NSCLCR_HAID_processing.ipynb)

#### 🗂️ File Structure
```
NSCLCR/
├── NSCLCR_HAID_processing.ipynb          # Full preprocessing pipeline
├── DATASET_PROCESSING_DOCUMENTATION.md   # Detailed processing documentation
├── metadata/                             # Annotations and splits
│   ├── NSCLC_bounding_boxes_annotations.csv
│   ├── NSCLCRadiomics_train_split.csv
│   ├── NSCLCRadiomics_validation_split.csv
│   ├── NSCLCRadiomics_test_split.csv
│   ├── NSCLCRadiomics_merged_with_fitSplit.csv
│   ├── NSCLCRadiomics_clinical_summary_table.csv
│   ├── NSCLCRadiomics_fold1.json         # Detection format
│   └── Experiments_NSCLCRadiomics_*.json # Generative format
└── [Download from Zenodo for NIfTI files]
```

#### 🚀 Quick Start
```python
import pandas as pd
import SimpleITK as sitk

# Load training split
train_df = pd.read_csv('NSCLCR/metadata/NSCLCRadiomics_train_split.csv')

# Load a CT scan
ct_image = sitk.ReadImage(train_df.iloc[0]['ct_path'])

# Load corresponding segmentation
seg_mask = sitk.ReadImage(train_df.iloc[0]['seg_path'])

# Access bounding box annotation
bbox = train_df.iloc[0][['coordx', 'coordy', 'coordz', 'w', 'h', 'd']].values
```

#### 🎯 Use Cases
- **Tumor Detection**: 3D bounding box annotations for object detection models
- **Segmentation**: Multi-organ segmentation (tumor, lungs, heart, esophagus, spinal cord)
- **Classification**: Histology prediction (adenocarcinoma, squamous cell, large cell)
- **Survival Prediction**: Clinical outcome modeling with survival time labels
- **Radiomics**: Feature extraction and biomarker discovery

#### 📊 Clinical Metadata
- **Age**: Mean 68.0 ± 10.1 years (range: 38.8 - 91.7)
- **Gender**: 131 female (31%), 290 male (69%)
- **Histology**:
  - Adenocarcinoma: 165 patients
  - Squamous cell carcinoma: 144 patients
  - Large cell carcinoma: 49 patients
  - NOS/Unknown: 63 patients
- **TNM Staging**: Complete T, N, M, and overall stage information
- **Survival Data**: Event status and survival time (days)

#### 📖 Citation
If you use this dataset, please cite:

```bibtex
@article{aerts2014decoding,
  title={Decoding tumour phenotype by noninvasive imaging using a quantitative radiomics approach},
  author={Aerts, Hugo JWL and Velazquez, Emmanuel Rios and Leijenaar, Ralph TH and others},
  journal={Nature Communications},
  volume={5},
  pages={4006},
  year={2014},
  doi={10.1038/ncomms5006}
}

@misc{aerts2015nsclc,
  author={Aerts, Hugo JWL and Wee, Leonard and Rios Velazquez, Emmanuel and others},
  title={Data From NSCLC-Radiomics},
  year={2015},
  publisher={The Cancer Imaging Archive},
  doi={10.7937/K9/TCIA.2015.PF0M9REI}
}
```

---

## 🛠️ Installation & Requirements

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: Minimum 16GB recommended
- **Storage**: ~100GB for full NSCLCR dataset

### Python Dependencies
```bash
pip install SimpleITK pydicom pandas numpy matplotlib seaborn scikit-learn
```

### Optional Dependencies
```bash
pip install pydicom-seg opencv-python tqdm tabulate
```

---

## 📖 How to Use This Repository

1. **Browse available datasets** in the table above
2. **Download preprocessed data** from the provided Zenodo links
3. **Review processing documentation** in each dataset folder
4. **Load data splits** using the provided CSV/JSON files
5. **Run reference notebooks** to understand preprocessing pipelines

---

## 🤝 Contributing

We welcome contributions! If you'd like to add a new dataset or improve existing documentation:
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/new-dataset`)
3. Follow our [contribution guidelines](CONTRIBUTING.md)
4. Submit a pull request

---

## 📜 License

This repository and preprocessing code are licensed under the **Apache License 2.0**.

Individual datasets retain their original licenses:
- **NSCLC-Radiomics**: Creative Commons Attribution 3.0 Unported License

Please review each dataset's specific license before use.

---

## 📧 Contact

**Maintainer**: Fakrul Islam Tushar, PhD  
**Email**: [fitushar@uhnresearch.ca](mailto:fitushar@uhnresearch.ca)  
**GitHub**: [@fitushar](https://github.com/fitushar)

For dataset-specific questions, please open an issue in this repository.

---

## 🙏 Acknowledgments

- **TCIA (The Cancer Imaging Archive)** for hosting and maintaining public medical imaging datasets
- Original dataset authors and contributors
- Open-source medical imaging community

---

## 🗂️ Version History

- **v1.0.0** (January 2026): Initial release with NSCLC-Radiomics dataset
- More updates coming soon...

---

**⭐ If you find this resource helpful, please consider starring this repository!**
