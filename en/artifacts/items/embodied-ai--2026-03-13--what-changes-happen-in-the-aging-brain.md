---
source: hn
url: https://www.salk.edu/news-release/what-changes-happen-in-the-aging-brain/
published_at: '2026-03-13T23:03:48'
authors:
- hhs
topics:
- brain-aging
- single-cell-omics
- epigenetics
- spatial-transcriptomics
- neurodegeneration
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# What changes happen in the aging brain?

## Summary
This work constructs the most comprehensive single-cell epigenetic atlas to date of the aging mouse brain, systematically mapping age-related changes in methylation, chromatin structure, and gene expression across different brain regions and cell types. Its goal is to provide a publicly accessible reference resource for understanding the mechanisms of brain aging and neurodegenerative disease.

## Problem
- Brain aging is a major risk factor for neurodegenerative diseases such as Alzheimer’s disease, Parkinson’s disease, and ALS, but its cell type-specific molecular mechanisms remain unclear.
- Traditional bulk analyses lose regional and cell type differences, making it difficult to explain why different cells and locations age at different rates.
- Without linking DNA methylation, chromatin conformation, and spatial gene expression, it is difficult to identify actionable aging biomarkers and pathogenic mechanisms.

## Approach
- In an aging mouse model, the researchers built a single-cell multi-omics atlas covering **8 brain regions** and **36 major brain cell types**.
- They collected single-cell methylation data from **132,551** cells, along with **72,666** joint methylation-chromatin conformation profiles, for a total of more than **200,000** single-cell multi-omics samples.
- They integrated spatial transcriptomics data from nearly **900,000** cells to analyze gene expression changes while preserving tissue spatial location.
- Using these data, they trained new deep learning models to predict age-related gene expression changes from epigenetic information, laying the groundwork for a “virtual brain aging model.”
- The complete atlas was made publicly available on **AWS** and **GEO** as a reference framework for future studies of human brain aging and neurodegenerative disease.

## Results
- In terms of scale, the paper describes this as one of the **most comprehensive** single-cell epigenetic atlases of brain aging: covering **8 brain regions, 36 cell types, >200,000 single-cell multi-omics profiles, and nearly 900,000 spatial transcriptomics cells**.
- Methylation analysis shows that **age-related methylation changes are more pronounced in non-neuronal cells**; at the same time, transposable elements **lose DNA methylation** with age, suggesting that these “jumping genes” may be more likely to become activated in the aging brain.
- Chromatin conformation analysis proposes new biomarkers of brain aging: **increased TAD boundary strength** and increased accessibility of related **CTCF binding sites**.
- Spatial transcriptomics results indicate that **the same cell type can show different aging trajectories depending on the brain region where it resides**; the article gives the example that non-neuronal cells in posterior brain regions show stronger inflammatory features than those in anterior regions.
- Methodologically, the authors say they developed **deep learning models** to predict age-related gene expression changes, but the summary text **does not provide specific accuracy, AUC, R^2, or quantitative comparisons with baseline methods**.
- At the resource level, the authors emphasize that the dataset was fully released in **December 2025** and can be accessed directly through the cloud, lowering the barrier to using large-scale brain aging data.

## Link
- [https://www.salk.edu/news-release/what-changes-happen-in-the-aging-brain/](https://www.salk.edu/news-release/what-changes-happen-in-the-aging-brain/)
