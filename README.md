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

| # | Dataset | Modality | Patients | #CT Scans | Condition | Demographics | Status |
|---|---------|----------|----------|-----------|-----------|--------------|--------|
| 1 | [**NSCLC-Radiomics (NSCLCR)**](#1️⃣-nsclc-radiomics-nsclcr) | CT | 421 | 421 | Lung Cancer | Netherlands | ✅ Available |
| 2 | [**UniToChest**](#2️⃣-unitochest) | CT | 623 | 715 | Lung Nodules | Italy | ✅ Available |
| 3 | [**IMDCT**](#3️⃣-imdct) | CT | 2,032 | 2,032 | Indeterminate Pulmonary Nodules | China (Multi-institutional) | ✅ Available |
| 4 | [**LNDb v4**](#4️⃣-lndb-v4) | CT | 294 | 294 | Pulmonary Nodules | Portugal | ✅ Available |
| 5 | [**BIMCV-R**](#5️⃣-bimcv-r) | CT | 5,340 | 8,069 | Multi-label Findings (COVID-19, Pneumonia, etc.) | Spain | ✅ Available |
| 6 | [**LUNGx**](#6️⃣-lungx) | CT | 83 | 83 | Lung Nodule Classification | USA | ✅ Available |
| 7 | [**LIDC-IDRI**](#7️⃣-lidc-idri) | CT | 875 | 875 | Lung Nodule Detection & Segmentation | USA (Multi-institutional) | ✅ Available |
| | More datasets coming soon... | - | - | - | - | - | 🔜 Planned |

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

### 4️⃣ LNDb v4
**Lung Nodule Database with Multi-Reader Expert Annotations and Text Report Extractions**

#### Dataset Status
- **Modality**: CT (Computed Tomography)
- **Patients**: 294 unique patients (237 after quality control)
- **Condition**: Pulmonary Nodules with multi-reader annotations
- **Source**: [LNDb Grand Challenge](https://lndb.grand-challenge.org/)
- **Original Publication**: Ferreira et al. (2024) - Scientific Data - DOI: [10.1038/s41597-024-03345-6](https://doi.org/10.1038/s41597-024-03345-6)
- **Institutions**: INESC TEC & São João Hospital Centre, Porto, Portugal

#### 🔬 Dataset Features
- **Chest CT scans**: 294 scans with comprehensive pulmonary nodule coverage
- **Multi-reader annotations**: Up to 4 expert radiologists per case (1,235 total nodule instances)
- **Dual annotation sources**: Radiological annotations + text report extractions
- **Rich clinical attributes**: 9 radiological characteristics rated on 1-6 scales:
  - Texture, Calcification, Malignancy, Subtlety, Lobulation, Margin, Sphericity, Spiculation, Internal Structure
- **Standardized preprocessing**: Resampled to uniform spacing [0.703125, 0.703125, 1.25] mm
- **Nodule size range**: 3-40 mm diameter (~85% sub-centimeter)
- **Train/Validation/Test splits**: 189/24/24 patients (~80%/10%/10%)
- **3D bounding box annotations** for nodule detection tasks
- **Fleischner score compatibility**: Suitable for patient follow-up recommendation systems

#### 📥 Data Access
- **Original Dataset**: [LNDb Grand Challenge Download](https://lndb.grand-challenge.org/Download/)
- **Preprocessed Dataset**: Available on Zenodo (DOI to be added)
- **Processing Documentation**: [LNDBV4_DATASET_DOCUMENTATION.md](LNDbv4/LNDBV4_DATASET_DOCUMENTATION.md)
- **Processing Notebook**: [LNDbv4-Datasetprocessing-HAID.ipynb](LNDbv4/LNDbv4-Datasetprocessing-HAID.ipynb)
- **Conversion Scripts**: 
  - [mhd_to_nifti.py](LNDbv4/mhd_to_nifti.py) - Convert CT scans
  - [mhd_to_nifti_masks.py](LNDbv4/mhd_to_nifti_masks.py) - Convert segmentation masks

#### 📖 Citation
If you use this dataset, please cite:

```bibtex
@article{ferreira2024lndb,
  title={LNDb v4: An open lung nodule database with multi-reader annotations and clinical attributes},
  author={Ferreira, Carlos and Pedrosa, João and Aresta, Guilherme and others},
  journal={Scientific Data},
  volume={11},
  year={2024},
  publisher={Nature Publishing Group},
  doi={10.1038/s41597-024-03345-6}
}

@misc{lndb_grandchallenge,
  title={LNDb Challenge - Lung Nodule Database},
  author={INESC TEC and São João Hospital Centre},
  year={2020},
  howpublished={\url{https://lndb.grand-challenge.org/}}
}
```

---

### 5️⃣ BIMCV-R
**Large-Scale Chest CT Dataset with Bilingual Radiology Reports and Multi-Label Findings**

#### Dataset Status
- **Modality**: CT (Computed Tomography)
- **Patients**: 5,340 unique patients (8,069 CT scans total)
- **Condition**: Multi-label radiological findings with comprehensive radiology reports
- **Source**: [BIMCV Database](https://bimcv.cipf.es/bimcv-projects/bimcv-covid19/) | [Hugging Face Dataset](https://huggingface.co/datasets/cyd0806/BIMCV-R)
- **Original Publication**: Chen et al. (2024) - MICCAI 2024 - DOI: [10.1007/978-3-031-72120-5_12](https://doi.org/10.1007/978-3-031-72120-5_12)
- **Institution**: Medical Imaging Databank of the Valencia Region (BIMCV), Spain

#### 🔬 Dataset Features
- **Large-scale chest CT dataset**: 8,069 CT volumes from 5,340 patients
- **Bilingual radiology reports**: Spanish (original) + English (machine translated)
- **Rich multi-label annotations**: 10+ major radiological findings including:
  - Ground Glass Pattern (34.4%), Pneumonia (30.6%), COVID-19 (26.7%)
  - Nodules (24.4%), Pleural Effusion (19.9%), Consolidation (12.5%)
  - Adenopathy, Calcified Densities, Vertebral Changes, and more
- **Real-world clinical data**: Hospital data from Valencia, Spain
- **COVID-19 cohort**: Significant representation (2,152 instances, 26.7%)
- **Text-image pairs**: Over 2 million 2D CT slices with associated reports
- **Proposed Train/Validation/Test splits**: 4,272/534/534 patients (~80%/10%/10%)
- **Patient-level stratification**: No patient overlap across splits

#### 📥 Data Access
- **Original Dataset**: [Hugging Face - BIMCV-R](https://huggingface.co/datasets/cyd0806/BIMCV-R)
- **BIMCV Database**: [BIMCV COVID-19 Projects](https://bimcv.cipf.es/bimcv-projects/bimcv-covid19/)
- **Processing Documentation**: [BIMCVR_DATASET_DOCUMENTATION.md](BIMCVR/BIMCVR_DATASET_DOCUMENTATION.md)
- **Analysis Notebook**: [BIMCV_DataAnalysis.ipynb](BIMCVR/BIMCV_DataAnalysis.ipynb)
- **Split Metadata**: Available in [metadata/](BIMCVR/metadata/) folder

#### 📖 Citation
If you use this dataset, please cite:

```bibtex
@inproceedings{chen2024bimcv,
  title={BIMCV-R: A landmark dataset for 3D CT text-image retrieval},
  author={Chen, Yinda and Liu, Che and Liu, Xiaoyu and Arcucci, Rossella and Xiong, Zhiwei},
  booktitle={International Conference on Medical Image Computing and Computer-Assisted Intervention},
  pages={124--134},
  year={2024},
  organization={Springer},
  doi={10.1007/978-3-031-72120-5_12}
}

@misc{bimcv_database,
  title={BIMCV-COVID19: Medical Imaging Databank of the Valencia Region},
  author={BIMCV},
  year={2020},
  howpublished={\url{https://bimcv.cipf.es/bimcv-projects/bimcv-covid19/}}
}
```

---

### 6️⃣ LUNGx
**SPIE-AAPM-NCI Lung Nodule Classification Challenge Dataset with Pathology-Confirmed Diagnoses**

#### Dataset Status
- **Modality**: CT (Computed Tomography)
- **Patients**: 73 test patients + 10 calibration patients = 83 total
- **Condition**: Lung nodule classification (benign vs. malignant)
- **Source**: [TCIA - The Cancer Imaging Archive](https://www.cancerimagingarchive.net/collection/spie-aapm-lung-ct-challenge/)
- **Original Publication**: Armato et al. (2016) - Journal of Medical Imaging - DOI: [10.1117/1.JMI.3.4.044506](https://doi.org/10.1117/1.JMI.3.4.044506)
- **Challenge Organization**: SPIE-AAPM-NCI (USA)
- **DOI**: [10.7937/K9/TCIA.2015.UZLSU3FL](https://doi.org/10.7937/K9/TCIA.2015.UZLSU3FL)

#### 🔬 Dataset Features
- **Diagnostic CT scans**: 83 chest CT volumes with nodule annotations
- **Pathology-confirmed labels**: 100% histologically confirmed diagnoses (gold standard)
- **Challenge dataset**: Real-world diagnostic performance evaluation
- **Nodule annotations**: 94 nodules with precise DICOM coordinates
- **Diagnosis distribution**: 57 benign (60.6%), 37 malignant (39.4%)
- **Multi-nodule cases**: 11 patients with 2 nodules each
- **Scanner**: Philips CT scanners (high-resolution protocols)
- **Processed features**:
  - World coordinate conversion from DICOM pixel space
  - Standardized resampling to [0.703125, 0.703125, 1.25] mm
  - 64×64×64 voxel diagnostic patches centered on nodules

#### 📥 Data Access
- **Original Dataset**: [TCIA - SPIE-AAPM Lung CT Challenge](https://doi.org/10.7937/K9/TCIA.2015.UZLSU3FL)
- **Nodule Annotations**: 
  - [TestSet_NoduleData_PublicRelease_wTruth.xlsx](https://www.cancerimagingarchive.net/wp-content/uploads/TestSet_NoduleData.xlsx)
  - [CalibrationSet_NoduleData.xlsx](https://www.cancerimagingarchive.net/wp-content/uploads/CalibrationSet_NoduleData.xlsx)
- **Processing Documentation**: [LUNGX_DATASET_DOCUMENTATION.md](LUNGx/LUNGX_DATASET_DOCUMENTATION.md)
- **Processing Notebook**: [LUNGx-Processing-HAID.ipynb](LUNGx/LUNGx-Processing-HAID.ipynb)

#### 📖 Citation
If you use this dataset, please cite:

```bibtex
@article{armato2016lungx,
  title={LUNGx Challenge for computerized lung nodule classification},
  author={Armato III, Samuel G and Drukker, Karen and Li, Feng and Hadjiiski, Lubomir and Tourassi, Georgia D and Engelmann, Roger M and Giger, Maryellen L and Redmond, George and Farahani, Keyvan and Kirby, Justin S and Clarke, Laurence P},
  journal={Journal of Medical Imaging},
  volume={3},
  number={4},
  pages={044506},
  year={2016},
  publisher={SPIE},
  doi={10.1117/1.JMI.3.4.044506}
}

@dataset{armato2015lungx,
  author={Armato III, Samuel G and Hadjiiski, Lubomir and Tourassi, Georgia D and Drukker, Karen and Giger, Maryellen L and Li, Feng and Redmond, George and Farahani, Keyvan and Kirby, Justin S and Clarke, Laurence P},
  title={SPIE-AAPM-NCI Lung Nodule Classification Challenge Dataset},
  year={2015},
  publisher={The Cancer Imaging Archive},
  doi={10.7937/K9/TCIA.2015.UZLSU3FL}
}
```

---

### 7️⃣ LIDC-IDRI
**Lung Image Database Consortium - Image Database Resource Initiative with Multi-Radiologist Consensus Annotations**

#### Dataset Status
- **Modality**: CT (Computed Tomography)
- **Patients**: 875 unique patients (processed from original 1,010)
- **Condition**: Lung nodule detection and segmentation
- **Source**: [TCIA - The Cancer Imaging Archive](https://www.cancerimagingarchive.net/collection/lidc-idri/)
- **Original Publication**: Armato et al. (2011) - Medical Physics - DOI: [10.1118/1.3528204](https://doi.org/10.1118/1.3528204)
- **Consortium**: LIDC-IDRI (7 academic centers, NCI/NIH/FDA partnership, USA)
- **DOI**: [10.7937/K9/TCIA.2015.LO9QL9SX](https://doi.org/10.7937/K9/TCIA.2015.LO9QL9SX)

#### 🔬 Dataset Features
- **Comprehensive lung nodule benchmark**: 875 diagnostic and screening chest CT scans
- **Multi-radiologist annotations**: Up to 4 expert thoracic radiologists per case
- **Two-phase annotation process**: Blinded read followed by unblinded review
- **Consensus approach**: Union of all radiologist annotations for complete nodule coverage
- **Rich nodule characterization**: Size, texture, calcification, malignancy, spiculation, lobulation ratings
- **Multi-class segmentation**: Nodule + organ (Vista3D) + body mask integration
- **Dataset splits**: 649 train / 163 validation / 63 test patients
- **Label scheme**:
  - Label 23: Pulmonary nodules (multi-radiologist union)
  - Label 200: Body/soft tissue regions
  - Other labels: Vista3D organ segmentations
- **Standardized format**: NIfTI with comprehensive metadata

#### 📥 Data Access
- **Original Dataset**: [TCIA - LIDC-IDRI Collection](https://doi.org/10.7937/K9/TCIA.2015.LO9QL9SX)
- **Radiologist Annotations**: [XML Files (8.62MB)](https://www.cancerimagingarchive.net/wp-content/uploads/LIDC-XML-only.zip)
- **pylidc Tool**: [GitHub - pylidc](https://github.com/pylidc/pylidc) (recommended for working with annotations)
- **Processing Documentation**: [LIDCIDRI_DATASET_DOCUMENTATION.md](LIDCIDRI/LIDCIDRI_DATASET_DOCUMENTATION.md)
- **Processing Notebook**: [LIDC-IDRI-Segmentation-Processing-HAID.ipynb](LIDCIDRI/LIDC-IDRI-Segmentation-Processing-HAID.ipynb)

#### 📖 Citation
If you use this dataset, please cite:

```bibtex
@article{armato2011lidc,
  title={The Lung Image Database Consortium (LIDC) and Image Database Resource Initiative (IDRI): a completed reference database of lung nodules on CT scans},
  author={Armato III, Samuel G and McLennan, Geoffrey and Bidaut, Luc and McNitt-Gray, Michael F and Meyer, Charles R and Reeves, Anthony P and Zhao, Binsheng and Aberle, Denise R and Henschke, Claudia I and Hoffman, Eric A and others},
  journal={Medical Physics},
  volume={38},
  number={2},
  pages={915--931},
  year={2011},
  publisher={Wiley Online Library},
  doi={10.1118/1.3528204}
}

@dataset{armato2015lidc,
  author={Armato III, Samuel G and McLennan, Geoffrey and Bidaut, Luc and McNitt-Gray, Michael F and Meyer, Charles R and Reeves, Anthony P and others},
  title={Data From LIDC-IDRI},
  year={2015},
  publisher={The Cancer Imaging Archive},
  doi={10.7937/K9/TCIA.2015.LO9QL9SX}
}
```

**Acknowledgement**: *The authors acknowledge the National Cancer Institute and the Foundation for the National Institutes of Health, and their critical role in the creation of the free publicly available LIDC/IDRI Database used in this study.*

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
- **LNDb v4**: Creative Commons Attribution 4.0 International License
- **BIMCV-R**: MIT License (academic research purposes only)
- **LUNGx**: Creative Commons Attribution 3.0 Unported License
- **LIDC-IDRI**: Creative Commons Attribution 3.0 Unported License

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

- **v1.0.0** (January 2026): Initial release with 7 curated datasets
  - NSCLC-Radiomics (Netherlands)
  - UniToChest (Italy)
  - IMDCT (China - Multi-institutional)
  - LNDb v4 (Portugal)
  - BIMCV-R (Spain)
  - LUNGx (USA)
  - LIDC-IDRI (USA - Multi-institutional)
- More updates coming soon...

---

**⭐ If you find this resource helpful, please consider starring this repository!**
