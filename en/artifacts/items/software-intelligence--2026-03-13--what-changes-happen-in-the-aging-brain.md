---
source: hn
url: https://www.salk.edu/news-release/what-changes-happen-in-the-aging-brain/
published_at: '2026-03-13T23:03:48'
authors:
- hhs
topics:
- brain-aging
- single-cell-omics
- spatial-transcriptomics
- epigenetics
- deep-learning
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# What changes happen in the aging brain?

## Summary
This work constructed a single-cell multi-omics and spatial transcriptomics atlas of the aging mouse brain to characterize epigenetic changes across different brain regions and cell types, and to help clarify the molecular basis of neurodegenerative diseases. Its core value lies in providing the most comprehensive cell type-specific reference resource for the aging brain to date, and in reporting deep-learning models that can be used to predict age-related changes in gene expression.

## Problem
- Aging is an important risk factor for neurodegenerative diseases such as Alzheimer’s disease, Parkinson’s disease, and ALS, but **how aging reshapes the brain’s molecular state across different brain regions and cell types** remains unclear.
- Traditional bulk analyses lose cell-type and spatial information, making it difficult to explain **why the same cell type shows different aging trajectories in different brain regions**.
- This matters because neurodegenerative diseases already affect **more than 57 million** people, and incidence is expected to **double every 20 years**, creating a need for more fine-grained mechanistic understanding to support diagnosis and intervention.

## Approach
- The researchers built an atlas of the aging mouse brain that is **single-cell, multi-omic, and spatially resolved**, jointly measuring DNA methylation, chromatin conformation, and gene expression.
- The dataset covers **8 brain regions and 36 major brain cell types**, enabling analysis of aging-related changes by cell type and brain region.
- Specifically, they collected **132,551** single-cell methylomes, **72,666** joint methylation-chromatin conformation profiles, and combined these with **nearly 900,000** spatial transcriptomics cells.
- The study further compared different age groups to identify aging-related features such as changes in methylation, TAD boundary strength, and accessibility of CTCF binding sites.
- On this basis, the authors developed **deep-learning models** that use epigenetic information to predict age-related changes in gene expression, laying the groundwork for a “virtual brain aging model.”

## Results
- The authors built what they describe as the **most comprehensive** single-cell epigenomic atlas of the aging brain to date, covering **8 brain regions, 36 cell types, and more than 200,000 single-cell multi-omic samples**, and including **nearly 900,000** spatial transcriptomics cells.
- Methylation analysis showed that age-related methylation changes are more pronounced in **non-neuronal cells**; at the same time, transposable elements exhibit **loss of DNA methylation** during aging, suggesting that these “jumping genes” may become more active and be linked to functional decline.
- Chromatin conformation analysis proposed a new biomarker of brain aging: **increased TAD boundary strength**, accompanied by greater accessibility at related **CTCF** binding sites.
- Spatial transcriptomics analysis indicated that **the same cell type can display different aging patterns depending on the brain region it occupies**; for example, the text notes that non-neuronal cells in posterior brain regions show stronger inflammatory features than those in anterior regions.
- The authors state that they have used these data to develop a deep-learning method for **predicting age-related changes in gene expression**, but **the excerpt does not provide specific quantitative metrics, baseline models, or numerical performance gains**.
- The data resource has been made publicly available on **AWS** and **GEO**, serving as a reference framework for subsequent interpretation of human brain data and research on neurodegenerative diseases.

## Link
- [https://www.salk.edu/news-release/what-changes-happen-in-the-aging-brain/](https://www.salk.edu/news-release/what-changes-happen-in-the-aging-brain/)
