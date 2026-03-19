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
- peft
- transformer-ensemble
- software-engineering
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# LoRA-MME: Multi-Model Ensemble of LoRA-Tuned Encoders for Code Comment Classification

## Summary
This paper proposes LoRA-MME, which uses a weighted ensemble of multiple code encoders fine-tuned efficiently with LoRA parameters for multilingual, multi-label code comment classification. Its main value is improving classification accuracy without full fine-tuning, but at the cost of higher inference overhead.

## Problem
- It addresses the **code comment classification** problem: automatically assigning comments in Java, Python, and Pharo to semantic categories such as summary, usage, parameters, and deprecation.
- This matters because high-quality comment classification can support automatic documentation generation, code retrieval, program comprehension, and developer assistance tools.
- The difficulty is that this is a **multilingual, multi-label, class-imbalanced** task that requires understanding both natural language and code-related terminology and structure, while also balancing accuracy and computational efficiency.

## Approach
- The core method is simple: independently fine-tune 4 code-specific Transformer encoders (UniXcoder, CodeBERT, GraphCodeBERT, and CodeBERTa) with **LoRA adapters**, then combine their predictions using a **learned weighted ensemble**.
- LoRA adds low-rank trainable matrices only to the query/key/value/dense components of the attention layers, freezing most of the original parameters, so that each model trains only about **4.5% of parameters (about 5.9M)** and can be trained on an **RTX 3090**.
- The ensemble is not a simple average; instead, it learns separate weights for each class, allowing different models to contribute more on the categories they handle best. For example, GraphCodeBERT, which carries structural information, can be more important for certain code-structure-related categories.
- To handle class imbalance, training uses **Focal Loss (γ=2.0)** and positive-class weighting; it also searches classification thresholds separately for each **language-class** pair rather than uniformly using 0.5.
- On the data side, the method also applies language-aware preprocessing, including repairing corrupted symbols, preserving JavaDoc/Sphinx/Pharo-specific syntax, and heuristically splitting Pharo comments.

## Results
- On the test set, LoRA-MME achieves **Weighted F1 = 0.7906** and **Macro F1 = 0.6867**.
- Compared with the official/in-paper baseline, overall **Macro F1 improves from 0.6508 to 0.6867 (+0.0359)**; the per-language gains are **Java 0.7306→0.7445 (+0.0139)**, **Python 0.5820→0.6296 (+0.0476)**, and **Pharo 0.6152→0.6668 (+0.0516)**.
- Threshold optimization brings clear gains: with a **fixed threshold of 0.5**, **Macro F1 = 0.6512** and **Weighted F1 = 0.7654**; after switching to **class-wise optimized thresholds**, performance improves to **0.6867 / 0.7906**, i.e. **+0.0355 Macro F1** and **+0.0252 Weighted F1**.
- Looking at specific categories, stronger results include **Java/Ownership F1 = 0.9333**, **Pharo/Example F1 = 0.8889**, **Java/Summary F1 = 0.8848**, **Java/Usage F1 = 0.8793**, and **Pharo/Intent F1 = 0.8511**; weaker categories include **Java/Rational F1 = 0.3696** and **Python/DevelopmentNotes F1 = 0.3929**.
- The paper also explicitly notes the efficiency cost: average inference time is **45.13 ms/sample**, total computation is about **235,759.28 GFLOPS**, and therefore the competition’s final submission score is only **41.20%**, showing that the accuracy gains come with a clear inference overhead.

## Link
- [http://arxiv.org/abs/2603.03959v2](http://arxiv.org/abs/2603.03959v2)
