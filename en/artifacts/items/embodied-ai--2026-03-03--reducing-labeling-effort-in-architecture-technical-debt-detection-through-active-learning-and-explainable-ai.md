---
source: arxiv
url: http://arxiv.org/abs/2603.02944v1
published_at: '2026-03-03T12:51:54'
authors:
- Edi Sutoyo
- Paris Avgeriou
- Andrea Capiluppi
topics:
- technical-debt-detection
- architecture-technical-debt
- active-learning
- explainable-ai
- issue-tracking
- satd
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Reducing Labeling Effort in Architecture Technical Debt Detection through Active Learning and Explainable AI

## Summary
This paper studies how to reduce costly expert labeling effort when detecting Architecture Technical Debt (ATD) in Jira issues, while also making model outputs easier to understand. The authors combine keyword filtering, active learning, and explainable AI to build a more efficient and transparent ATD detection process.

## Problem
- Architecture technical debt is more abstract and more context-dependent than general technical debt, making it difficult to automatically identify from issue text.
- High-quality ATD-labeled data is scarce, and expert manual annotation is costly and time-consuming, limiting scalability.
- Existing SATD/TD detection research mostly focuses on classification performance, pays less attention to the ATD subcategory, and also lacks expert validation of explanation quality.

## Approach
- First, they refined 116 existing ATD-related Jira issues into 57 expert-validated samples as more reliable seed data.
- They extracted representative ATD keywords from these seed samples and used them to filter more than 103,000 candidate issues across 10 open-source projects, narrowing the scope requiring manual inspection.
- On the filtered data, they applied active learning and compared multiple query strategies (such as Breaking Ties, Prediction Entropy, Least Confidence, Embedding K-Means, Contrastive Active Learning, Random), prioritizing samples that were “most informative” for annotation.
- They used LIME and SHAP to explain automated classification results, highlighting words/features that influenced predictions, and asked experts to evaluate the usefulness of these explanations.

## Results
- In dataset construction: the authors refined the previous 116 ATD issues into 57 expert-validated instances, and used them to expand to over 103,000 candidate issues across 10 projects.
- In active learning: the **Breaking Ties** strategy performed most consistently, achieving the highest **F1 = 0.72** while **reducing labeling effort by 49%**.
- In interpretability: expert evaluation found that **both LIME and SHAP can provide reasonable explanations**, but whether an explanation is useful depends on whether the highlighted features are truly relevant.
- In preference: experts **generally preferred LIME** because its explanations were clearer and easier to use.
- The abstract does not provide more complete quantitative results (such as precision/recall, itemized comparisons across strategies, or specific false-positive/false-negative values for keyword filtering), so further numerical comparison is not possible.

## Link
- [http://arxiv.org/abs/2603.02944v1](http://arxiv.org/abs/2603.02944v1)
