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

| Dataset | Modality | Patients | Condition | Demographics | Status |
|---------|----------|----------|-----------|--------------|--------|
| [**NSCLC-Radiomics (NSCLCR)**](#1️⃣-nsclc-radiomics-nsclcr) | CT | 421 | Lung Cancer | Netherlands | ✅ Available |
| [**UniToChest**](#2️⃣-unitochest) | CT | 623 | Lung Nodules | Italy | ✅ Available |
| [**IMDCT**](#3️⃣-imdct) | CT | 2,032 | Indeterminate Pulmonary Nodules | China (Multi-institutional) | ✅ Available |
| More datasets coming soon... | - | - | - | - | 🔜 Planned |

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

### 2️⃣ UniToChest
**Chest CT Imaging with Expert-Annotated Lung Nodule Segmentation**

#### Dataset Status
- **Modality**: CT (Computed Tomography)
- **Patients**: 623 unique patients (715 CT scans total)
- **Condition**: Lung Nodules (10,071 annotated nodules)
- **Source**: [Zenodo Repository](https://zenodo.org/records/5797912)
- **Original Publication**: Chaudhry et al. (2022) - ICIAP 2022 - DOI: [10.1007/978-3-031-06427-2_16](https://doi.org/10.1007/978-3-031-06427-2_16)
- **Institution**: Città della Salute e della Scienza di Torino & University of Turin, Italy

#### 🔬 Dataset Features
- **Chest CT scans**: 715 scans from 623 patients with varying slice thickness and spacing
- **Expert annotations**: 10,071 lung nodule segmentation masks by expert radiologists
- **Standardized preprocessing**: Resampled to uniform spacing [0.703125, 0.703125, 1.25] mm
- **3D bounding box annotations** for nodule detection tasks
- **Train/Validation/Test splits**: 579/66/70 scans from 501/62/63 patients (~80%/10%/10%)
- **Clinical metadata**: Patient demographics (age, sex), scanner parameters, acquisition details
- **Nodule characteristics**: Diameter statistics (mean 21.4 ± 20.2 mm)

#### 📥 Data Access
- **Original Dataset**: [Zenodo Repository - DOI: 10.5281/zenodo.5797912](https://zenodo.org/records/5797912)
- **Preprocessed Dataset**: [Zenodo Repository - DOI: 10.5281/zenodo.18285682](https://zenodo.org/uploads/18285682)
- **Processing Documentation**: [UNITOCHEST_PROCESSING_DOCUMENTATION.md](UniToChest/UNITOCHEST_PROCESSING_DOCUMENTATION.md)
- **Processing Notebook**: [Demo_Dicom_to_CT-HAID.ipynb](UniToChest/Demo_Dicom_to_CT-HAID.ipynb)
- **Data Analysis Notebook**: [DataAnalysis.ipynb](UniToChest/DataAnalysis.ipynb)

#### 📖 Citation
If you use this dataset, please cite:

```bibtex
@inproceedings{chaudhry2022unitochest,
  title={UniToChest: A Lung Image Dataset for Segmentation of Cancerous Nodules on CT Scans},
  author={Chaudhry, Aymen and Perlo, Daniele and Renzulli, Riccardo and Santinelli, Francesca and Tibaldi, Stefano and Cristiano, Carmen and Grosso, Marco and Limerutti, Giorgio and Grangetto, Marco and Fonio, Paolo},
  booktitle={International Conference on Image Analysis and Processing (ICIAP)},
  pages={189--200},
  year={2022},
  publisher={Springer},
  doi={10.1007/978-3-031-06427-2_16}
}

@dataset{perlo2021unitochest,
  author={Perlo, Daniele and Renzulli, Riccardo and Santinelli, Francesca and Tibaldi, Stefano and Cristiano, Carmen and Grosso, Marco and Limerutti, Giorgio and Grangetto, Marco and Fonio, Paolo},
  title={UniToChest},
  year={2021},
  publisher={Zenodo},
  doi={10.5281/zenodo.5797912}
}
```

---

### 3️⃣ IMDCT
**Indeterminate Pulmonary Nodules Multi-institutional CT Dataset with Histopathological Confirmation**

#### Dataset Status
- **Modality**: CT (Computed Tomography)
- **Patients**: 2,032 unique patients
- **Condition**: Indeterminate Pulmonary Nodules with histopathological confirmation
- **Source**: [Zenodo Repository](https://zenodo.org/records/13908015)
- **Original Publication**: Zhao et al. (2024) - Nature Communications - DOI: [10.1038/s41467-024-55594-4](https://doi.org/10.1038/s41467-024-55594-4)
- **Institutions**: Multi-institutional (5 clinical centers in China)

#### 🔬 Dataset Features
- **Chest CT scans**: 2,032 scans with indeterminate pulmonary nodules
- **Histopathological confirmation**: 100% pathology-confirmed diagnoses (gold standard)
- **One annotated nodule per patient**: Single target per scan for simplified analysis
- **High malignancy rate**: 78.6% malignant, 21.4% benign nodules
- **Clinically relevant sizes**: Predominantly intermediate to very large nodules (10-30+ mm)
- **3D bounding box annotations** for nodule detection and localization
- **Train/Validation/Test splits**: 1,625/203/204 patients (~80%/10%/10%)
- **Clinical metadata**: Patient age, nodule dimensions, malignancy labels
- **Nodule characteristics**: Mean diameter 30.0 ± 20.8 mm, solid component 15.7 ± 13.2 mm

#### 📥 Data Access
- **Original Dataset Part-I**: [Zenodo Repository - DOI: 10.5281/zenodo.13908015](https://zenodo.org/records/13908015)
- **Original Dataset Part-II**: [Zenodo Repository - DOI: 10.5281/zenodo.13913777](https://zenodo.org/records/13913777)
- **Processing Documentation**: [IMDCT_DATASET_DOCUMENTATION.md](IMDCT/IMDCT_DATASET_DOCUMENTATION.md)
- **Processing Notebooks**: 
  - [IMDCT-Segmentation_Processing-HAID.ipynb](IMDCT/IMDCT-Segmentation_Processing-HAID.ipynb)
  - [IMDCT-Annotation-HAID.ipynb](IMDCT/IMDCT-Annotation-HAID.ipynb)

#### 📖 Citation
If you use this dataset, please cite:

```bibtex
@article{zhao2024integrated,
  title={Integrated multiomics signatures to optimize the accurate diagnosis of lung cancer},
  author={Zhao, Mengmeng and She, Yunlang and others},
  journal={Nature Communications},
  volume={15},
  year={2024},
  publisher={Nature Publishing Group},
  doi={10.1038/s41467-024-55594-4}
}

@dataset{zhao2024imdct,
  author={Zhao, Mengmeng and She, Yunlang},
  title={CT dataset for "Integrated multiomics signatures to optimize the accurate diagnosis of lung cancer" Part-I},
  year={2024},
  publisher={Zenodo},
  doi={10.5281/zenodo.13908015}
}
```

---

## 🛠️ Installation & Requirements


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
- **UniToChest**: Creative Commons Attribution 4.0 International License
- **IMDCT**: Creative Commons Attribution 4.0 International License

Please review each dataset's specific license before use.

---

## 📧 Contact

**Maintainer**: Fakrul Islam Tushar, PhD  
**Email**: [fitushar.mi@gmail.com](mailto:fitushar.mi@gmail.com)  
**GitHub**: [@fitushar](https://github.com/fitushar)

For dataset-specific questions, please open an issue in this repository.

---

## 🙏 Acknowledgments

- **TCIA (The Cancer Imaging Archive)** for hosting and maintaining public medical imaging datasets
- Original dataset authors and contributors
- Open-source medical imaging community

---

## 🗂️ Version History

- **v1.2.0** (January 2026): Added IMDCT dataset with multi-institutional indeterminate pulmonary nodules
- **v1.1.0** (January 2026): Added UniToChest dataset with lung nodule segmentations
- **v1.0.0** (January 2026): Initial release with NSCLC-Radiomics dataset
- More updates coming soon...

---

**⭐ If you find this resource helpful, please consider starring this repository!**
