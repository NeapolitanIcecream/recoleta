---
source: arxiv
url: http://arxiv.org/abs/2603.02944v1
published_at: '2026-03-03T12:51:54'
authors:
- Edi Sutoyo
- Paris Avgeriou
- Andrea Capiluppi
topics:
- architecture-technical-debt
- active-learning
- explainable-ai
- issue-tracking
- satd-detection
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Reducing Labeling Effort in Architecture Technical Debt Detection through Active Learning and Explainable AI

## Summary
This paper studies how to detect Architecture Technical Debt (ATD) in Jira issues with lower manual annotation cost, while also making model predictions more interpretable. The core idea is to combine keyword filtering, active learning, and explainable AI to build an ATD detection pipeline for large-scale open-source projects.

## Problem
- ATD is one of the hardest types of technical debt to detect and also one of the most impactful, because it involves abstract architectural decisions and context rather than simple code smells.
- Existing SATD/TD research mostly focuses on general technical debt, and there is little high-quality labeled data for ATD in issue trackers; expert annotation is also expensive, time-consuming, and difficult to scale.
- Even if a model can classify ATD, a lack of interpretability can weaken engineers' trust in and adoption of the results, so ATD identification methods need to be traceable and understandable.

## Approach
- First, the authors further refined an existing dataset of 116 Jira issues related to ATD, obtaining 57 expert-validated samples and extracting representative ATD keywords from them.
- These keywords were used for initial filtering across 10 large open-source projects, identifying more than 103,000 candidate issues in order to narrow the scope of manual inspection and assess the cross-project reusability of the keywords.
- Pool-based active learning was then applied to the filtered data, comparing multiple query strategies (such as Breaking Ties, Prediction Entropy, Least Confidence, Embedding K-Means, Contrastive Active Learning, Random) to prioritize the samples “most worth labeling.”
- A classification model was used to automatically identify ATD, and LIME and SHAP were used to provide local explanations highlighting which words/features drove the model’s decisions; experts then evaluated explanation quality using multiple criteria.

## Results
- Dataset construction: from an existing set of **116** ATD-related issues, the authors refined **57** expert-validated samples, and based on these screened **103,000+** candidate issues across **10** open-source projects.
- Active learning: the **Breaking Ties** strategy was the most consistently strong performer, achieving the highest **F1 = 0.72** while reducing manual annotation effort by **49%**.
- Interpretability: expert evaluation found that both **LIME** and **SHAP** could provide “reasonable” classification explanations; whether an explanation was useful depended largely on whether the highlighted features were semantically related to architectural debt.
- Preference: experts generally preferred **LIME** because its explanations were clearer and easier to use.
- The paper also claims to be among the first to systematically incorporate domain experts into explanation evaluation for SATD/ATD detection; however, the provided excerpt does not include more detailed numerical results (such as full precision/recall for each strategy, false positive/false negative rates for keyword filtering, or mean expert scores).

## Link
- [http://arxiv.org/abs/2603.02944v1](http://arxiv.org/abs/2603.02944v1)
