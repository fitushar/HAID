# HAID - Health AI Data Resource


<div align="center">
<p align="center">
  <img src="https://github.com/fitushar/HAID/blob/main/Documentations/HAID_logo/HAID_LogoCroped.png" alt="HAID_logo" width="500">
</p>

**HAID: A Comprehensive Health AI Data Resource Resource for Imaging/metadata**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Docker](https://img.shields.io/badge/Docker-ft42%2Fpins%3Alatest-2496ED?logo=docker)](https://hub.docker.com/r/ft42/pins)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Medical Imaging](https://img.shields.io/badge/Medical-Imaging-red.svg)](https://simpleitk.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.8.0-orange.svg)](https://pytorch.org)
[![MONAI](https://img.shields.io/badge/MONAI-1.4.0-blue.svg)](https://monai.io)
[![PiNS](https://img.shields.io/badge/PiNS-1.0.0-blue.svg)](https://github.com/fitushar/PiNS)
[![CaNA](https://img.shields.io/badge/CaNA-1.0.0-cyan.svg)](https://github.com/fitushar/CaNA)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)
</div>

The **HAID (Health AI Data Resource)** is an open-access repository hosted on GitHub that provides **standardized medical imaging datasets** to support the development of artificial intelligence and machine learning models. Curated by **Fakrul Islam Tushar**, the platform currently offers 13 distinct clinical collections covering conditions such as **lung cancer, COVID-19, and universal lesions**. Each resource includes **preprocessed imaging files**, expert-verified annotations, and consistent train-test splits to ensure research reproducibility. Beyond raw data, the repository serves as a functional toolkit by supplying **curated Jupyter notebooks** and reference workflows for data analysis. By unifying diverse international datasets with **comprehensive documentation**, HAID aims to democratize high-quality clinical data for the global medical imaging community.

🚀 **Interactive Research** : You can chat with the source materials for this project using our **NotebookLM Dashboard**:
👉 [Access the Interactive Notebook](https://notebooklm.google.com/notebook/65820f9a-15d7-412d-b466-a196fde2e2c9)

📊 **Slide Deck**
View the technical overview of the HAID project:
👉 [Download Slide Deck (PDF)](./Documentations/NotebookLLM_Contents/Health_AI_Data_Resource_HAID.pdf)




🎥 **HAID Intro Video**

[![HAID Introduction](https://img.youtube.com/vi/eJybx-j_ynI/maxresdefault.jpg)](https://youtu.be/eJybx-j_ynI)

*Click the image above to watch the introduction to HAID on YouTube*


## 🎯 Mission

To democratize access to high-quality, preprocessed medical imaging datasets by providing:
- ✅ **Standardized preprocessing** pipelines
- ✅ **Comprehensive documentation** 
- ✅ **Ready-to-use annotations** for detection, segmentation, and classification
- ✅ **Train/validation/test splits** for reproducible benchmarking
- ✅ **Reference implementations** in Jupyter notebooks


![HAID Dataset Overview](Documentations/NotebookLLM_Contents/Infographics_2.png)
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
| 8 | [**LUNA25**](#8️⃣-luna25) | CT | 2,020 | 4,069 | Lung Nodule Detection with AI Segmentations | Netherlands (Multi-institutional) | ✅ Available |
| 9 | [**MIDRC-RICORD**](#9️⃣-midrc-ricord) | CT | 227 | 328 | COVID-19 Detection & Classification | USA (Multi-institutional) | ✅ Available |
| 10 | [**U-10 (United-10)**](#🔟-u-10-united-10) | CT | 12,000+ | 12,000+ | COVID-19 Multi-Dataset Collection (10 datasets) | Multi-national | ✅ Available |
| 11 | [**NLST-3D**](#1️⃣1️⃣-nlst-3d) | CT | 900+ | 969 | Lung Cancer Screening with 3D Nodule Annotations | USA (Multi-institutional) | ✅ Available |
| 12 | [**DLCS 2024**](#1️⃣2️⃣-dlcs-2024) | CT (LDCT) | 2,061 | 2,061 | Lung Cancer Screening with Lung-RADS Scores | USA (Duke University) | ✅ Available |
| 13 | [**DeepLesion-1kTest3D**](#1️⃣3️⃣-deeplesion-1ktest3d) | CT | 10,594 | 1,000 | Universal Lesion Detection (8 Body Regions) | USA (NIH Clinical Center) | ✅ Available |
| | More datasets coming soon... | - | - | - | - | - | 🔜 Planned |

---



# 📚 Associated Open-Access Tools & Studies

🎯 SEGMENTATION
🧠 CLASSIFICATION
🔍 DETECTION
📊 BENCHMARK
🧬 GENERATION
✍️ ANNOTATION

| 🔗 Resource | 🧠 Type | 📝 Details | 🌐 Link |
|-----------|--------|-----------|--------|
| **VLST** (Virtual Lung Screening Trials) | 🧬 Simulation | In-silico lung screening trials | https://fitushar.github.io/VLST.github.io/ |
| **Lung Cancer Benchmarks** | 📊 Classification, 🔍Detection | CADe & CADx Benchmarking | https://zenodo.org/records/13799069 · https://shorturl.at/Xh2uO |
| **PiNS** | 🎯 Segmentation | Point-driven nodule masks | https://github.com/fitushar/PiNS |
| **CaNA** | 🧩 Augmentation | Context-aware nodule synthesis | https://github.com/fitushar/CaNA |
| **NoMAISI** | 🧬 Syntheis | Controlled synthetic lung nodules | https://github.com/fitushar/NoMAISI |
| **TriAnnot** | 🧠 Annotation-tool | Tri-stage annotation consensus | 🚧 In preparation |



## 🤝 Community & Collaborator Open-Source Resources

| 🔗 Resource | 👤 Contributor | 🧠 Type | 📝 Details | 🌐 Link |
|-----------|--------------|--------|-----------|--------|
| **3D-Segmentation** | Lavsen Dahal | 🎯 Segmentation | Curated collection of open-source 3D segmentation models | https://github.com/lavsendahal/3D-segmentation |



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
- **Clinical metadata**: Patient
