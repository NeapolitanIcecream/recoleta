---
source: hn
url: https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments
published_at: '2026-03-05T23:54:26'
authors:
- hhs
topics:
- medical-foundation-model
- vision-language-model
- ct-analysis
- clinical-ai
- disease-risk-prediction
relevance_score: 0.23
run_id: materialize-outputs
language_code: en
---

# Automated CT scan analysis could fast-track clinical assessments

## Summary
Merlin is a vision-language foundation model for 3D abdominal CT, designed to extend a single general training run to a large number of clinical tasks such as diagnosis, prognosis, and quality control. Through joint training on large-scale CT scans, radiology reports, and diagnosis codes, it outperformed or matched specialized models across multiple task categories.

## Problem
- Traditional CT image interpretation depends on radiologists analyzing findings item by item, making the workflow time-consuming and harder to scale amid physician shortages.
- Existing automated tools are usually designed for a single task and struggle to simultaneously cover broad needs such as diagnosis, prognosis, organ segmentation, and report generation.
- If richer disease signals cannot be reliably extracted from routine CT scans, clinical care may miss opportunities to detect chronic disease risk and potential biomarkers earlier.

## Approach
- Build a CT foundation model called Merlin that learns general imaging representations from large-scale, weakly labeled / not specially annotated task-by-task data.
- The training data came from more than **15,000** 3D abdominal CT scans linked to corresponding radiology reports and nearly **1 million** diagnosis codes; the article describes this as the largest abdominal CT dataset to date.
- The core mechanism can be understood simply as having the model look at both **CT images** and **textual medical conclusions** at the same time, so it learns the mapping between “imaging features ↔ clinical meaning,” and then transfers this general capability to many tasks.
- During evaluation, the researchers tested the model on more than **50,000** previously unseen abdominal CT scans from **4 hospitals**, spanning **6** major categories and more than **750** tasks; some complex tasks then received additional training / fine-tuning, such as report generation and 3D organ delineation.
- State-of-the-art specialized models for each task were used as controls to verify whether a general model could truly replace or outperform expert systems.

## Results
- For prediction across **692** diagnosis codes, Merlin could on average determine with more than **81%** accuracy which of two CT scans was more likely to correspond to a given diagnosis code, outperforming multiple variants of two other models.
- On a subset containing **102** diagnosis codes, Merlin’s performance rose to **90%**.
- In chronic disease risk prediction, using CT alone, Merlin achieved **75%** accuracy when making pairwise comparisons of which patient was more likely to develop disease within the next **5 years**, higher than the control model’s **68%**; the diseases included diabetes, osteoporosis, and heart disease.
- The model also showed generalization across anatomical regions on chest CT: although no chest CT scans were used in training, the article says its performance was **comparable or better** than models trained only on chest CT, though the excerpt does not provide specific numbers.
- Overall, the authors claim that Merlin **outperformed or matched** specialized models on all tested tasks, covering scenarios such as diagnosis, prognosis, and quality control.
- The study also proposes an important clinical implication: the model may discover early disease features in CT scans that are difficult to perceive with the naked eye, providing clues for identifying new disease biomarkers.

## Link
- [https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments](https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments)
