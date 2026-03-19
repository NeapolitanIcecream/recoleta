---
source: hn
url: https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments
published_at: '2026-03-05T23:54:26'
authors:
- hhs
topics:
- medical-imaging
- ct-foundation-model
- vision-language
- multitask-learning
- clinical-ai
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Automated CT scan analysis could fast-track clinical assessments

## Summary
This work introduces **Merlin**, a vision-language foundation model for 3D abdominal CT, aiming to expand a single medical imaging model into a generalizable multitask clinical analysis system. It demonstrates strong generality across more than 750 tasks in diagnosis, prognosis, quality control, and more, and outperforms specialized models on multiple tasks.

## Problem
- Existing CT analysis usually relies on radiologists interpreting scans one by one, and often requires additional tests, making the workflow time-consuming; physician shortages further increase the clinical burden.
- Previous automated models have mostly been single-task specialized tools, making it difficult to handle a broad range of tasks simultaneously, such as diagnosis, segmentation, report generation, and risk prediction.
- If richer disease signals could be extracted directly from CT scans, even before signs become visible to humans, it could accelerate diagnosis and treatment and help identify early biomarkers of chronic disease, which is important.

## Approach
- The core method is to train a **CT vision-language foundation model**: combining **15,000+** 3D abdominal CT scans, their corresponding radiology reports, and **nearly 1 million** diagnosis codes so the model learns the correspondence between imaging content and text/diagnostic labels.
- Put simply, Merlin first learns from large-scale clinical data what kinds of visual patterns in CT typically correspond to which medical descriptions and disease codes, and then transfers this general representation to different downstream tasks.
- The study evaluates Merlin on **6 major categories** and **750+** tasks, covering diagnosis, prognosis, and quality assessment; some tasks can be completed directly in zero-shot or with limited adaptation, while complex tasks such as report generation and 3D organ delineation require additional training.
- Evaluation used **50,000+** previously unseen abdominal CT scans from **4 hospitals**, and compared Merlin with multiple state-of-the-art specialized models designed for single tasks.
- Cross-anatomy generalization was also tested: although the training data did not include chest CT, Merlin was still used to interpret chest CT to examine whether it had learned generalizable disease features.

## Results
- On the average performance across **692** diagnosis codes, Merlin achieved over **81%** accuracy in predicting which of two scans was more likely to correspond to a given diagnosis code, outperforming multiple variants of two other model classes.
- On a subset of **102** diagnosis codes, Merlin's performance increased to **90%**.
- In tasks using CT to predict chronic disease risk over the next **5 years**, Merlin achieved **75%** accuracy in identifying which healthy subject was more likely to develop disease in the future, compared with **68%** for the comparison model; example diseases mentioned include diabetes, osteoporosis, and heart disease.
- On chest CT, an **anatomical region not seen during training**, Merlin matched or exceeded models trained only on chest scans, indicating cross-region generalization ability; however, the excerpt does not provide specific figures for this result.
- The authors claim that, as a general-purpose model, Merlin **matched or exceeded** specialized models across all evaluated tasks, with the key reasons being its 3D architecture and joint image-text training data; however, the excerpt does not provide a complete quantitative table for every task.

## Link
- [https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments](https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments)
