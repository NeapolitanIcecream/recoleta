---
source: arxiv
url: http://arxiv.org/abs/2603.03959v2
published_at: '2026-03-04T11:36:32'
authors:
- Md Akib Haider
- Ahsan Bulbul
- Nafis Fuad Shahid
- Aimaan Ahmed
- Mohammad Ishrak Abedin
topics:
- code-comment-classification
- lora
- model-ensemble
- code-language-models
- parameter-efficient-fine-tuning
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# LoRA-MME: Multi-Model Ensemble of LoRA-Tuned Encoders for Code Comment Classification

## Summary
LoRA-MME is an ensemble method for multi-label code comment classification. It low-cost fine-tunes multiple code-specific Transformers with LoRA and then performs weighted fusion. Its primary goal is higher semantic classification accuracy, but it also clearly exposes the inference-efficiency cost introduced by ensembling.

## Problem
- It addresses the code comment classification problem: automatically assigning comment sentences in Java, Python, and Pharo to semantic categories such as summary, usage, parameters, and deprecation.
- This matters because identifying comment types can support automated documentation generation, code search, maintenance analysis, and developer assistance tools.
- The challenge is that this is a **multilingual, multi-label, imbalanced-class** task that must both leverage code semantics and control fine-tuning and inference costs.

## Approach
- It uses 4 code-specific encoders: UniXcoder, CodeBERT, GraphCodeBERT, and CodeBERTa, each trained independently rather than relying on a single model.
- It applies LoRA for parameter-efficient fine-tuning to each model: low-rank adapters are inserted only into the attention query/key/value/dense layers while most original parameters are frozen; each model trains only about **4.5% of parameters (about 5.9M)** and can be trained on an **RTX 3090**.
- The outputs of the 4 models are combined using a **class-wise learned weighted ensemble**: different comment categories can favor different models rather than simply averaging probabilities.
- It searches classification thresholds separately for each “language-category” pair rather than using a uniform 0.5; thresholds are grid-searched on the validation set from **0.1 to 0.9**, with a final range of about **0.28–0.85** and mean **0.65**.
- Training uses **focal loss (γ=2.0)** and positive-class weighting to mitigate class imbalance.

## Results
- On the test set, LoRA-MME achieves **Weighted F1 = 0.7906** and **Macro F1 = 0.6867**.
- Compared with the baseline reported in the paper, overall **Macro F1 improves from 0.6508 to 0.6867 (+0.0359)**; by language, the gains are **Java 0.7306→0.7445 (+0.0139)**, **Python 0.5820→0.6296 (+0.0476)**, and **Pharo 0.6152→0.6668 (+0.0516)**.
- Threshold optimization brings a clear gain: **Macro F1 0.6512→0.6867 (+0.0355)** and **Weighted F1 0.7654→0.7906 (+0.0252)**, outperforming the fixed threshold of 0.5.
- At the single-category level, stronger results include: **Java/Ownership F1 = 0.9333**, **Pharo/Example F1 = 0.8889**, **Java/Summary F1 = 0.8848**, **Java/Usage F1 = 0.8793**, and **Pharo/Intent F1 = 0.8511**.
- But efficiency is poor: average inference time is **45.13 ms/sample**, total computation is about **235,759.28 GFLOPS**, and this leads to a final competition submission score of only **41.20%**.
- The paper’s claimed core contribution is not a novel single-model architecture, but rather the combination of **LoRA + multi-model code-encoder ensemble + class-wise threshold optimization**, which achieves stronger classification performance while retaining parameter-efficient fine-tuning, at the cost of significantly higher inference overhead.

## Link
- [http://arxiv.org/abs/2603.03959v2](http://arxiv.org/abs/2603.03959v2)
