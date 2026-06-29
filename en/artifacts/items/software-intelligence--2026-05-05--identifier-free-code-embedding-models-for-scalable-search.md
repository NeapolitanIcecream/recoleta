---
source: arxiv
url: https://arxiv.org/abs/2605.05251v1
published_at: '2026-05-05T17:53:51'
authors:
- Eric Wolos
- Michael Doyle
topics:
- code-embeddings
- binary-reverse-engineering
- function-search
- contrastive-learning
- decompiled-code
- code-intelligence
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Identifier-Free Code Embedding Models for Scalable Search

## Summary
The paper trains mitRE-embed-Qwen-0.6B, a Qwen3-Embedding-0.6B model tuned to match source functions with stripped Ghidra decompiled functions. It targets scalable binary reverse-engineering search when symbol names are missing.

## Problem
- Reverse engineers often see stripped binaries where function, variable, and parameter names are gone, so matching decompiled code to known source code is hard.
- Existing tools such as BSim and FLIRT help with function association, but open text embedding models have not covered bidirectional source-to-decompiled and decompiled-to-source search with simple text inputs.
- This matters because better retrieval can help analysts identify known functions in large binaries without custom AST or graph preprocessing.

## Approach
- The authors build paired data from the permissively licensed Assemblage WinPE split: nearly 500,000 source/decompiled function pairs, over 1M functions total, a 95/5 train/test split, and headless Ghidra decompilation.
- They fine-tune Qwen3-Embedding-0.6B with contrastive InfoNCE loss: a decompiled function is the anchor, its matching source function is the positive, and other source functions in the batch are negatives.
- Training uses 1 epoch, 964 steps, effective batch size 512, temperature 0.05, AdamW, learning rate 2e-5 with cosine schedule, bf16, and 4 NVIDIA H100 GPUs.
- Evaluation uses cosine-similarity retrieval in both directions with filtered candidate pools of 29,499 functions and combined source-plus-decompiled pools of 58,999 functions.
- The paper compares 11 embedding models, tests an FP8 quantized variant, and checks transfer on Signsrch constant association.

## Results
- On Decompiled-to-Source search with both representations in the pool, mitRE-embed-Qwen-0.6B reaches MRR 0.4104, Recall@1 0.3065, and Recall@10 0.6427; BinSeek-Embedding scores MRR 0.0802, Recall@1 0.0594, and Recall@10 0.1221.
- On Source-to-Decompiled search with both representations in the pool, the model reaches MRR 0.4104 and Recall@10 0.6337; the strongest non-MITRE baseline in MRR is SFR-Embedding-Mistral at 0.1429.
- With filtered pools, it reaches MRR 0.6207 and Recall@10 0.8353 for Decompiled-to-Source, and MRR 0.5962 and Recall@10 0.8094 for Source-to-Decompiled.
- The FP8 quantized model keeps close retrieval quality: Decompiled-to-Source combined-pool MRR is 0.4083 versus 0.4104 for full precision, and Source-to-Decompiled filtered-pool MRR is 0.5950 versus 0.5962.
- On Signsrch Constant-to-Other-Constants, the model has MAP 0.062765, ahead of Qwen3-Embedding-0.6B at 0.038412 and BinSeek-Embedding at 0.037864; on Group-to-Constants, embeddinggemma-300m leads with average precision 0.022182 while mitRE-embed-Qwen-0.6B scores 0.019732.
- FP8 quantization uses 0.72 GB of VRAM for weights versus 1.12 GB in full precision, and takes 88.6% of the full-precision inference time across five trials embedding 10,000 function pairs.

## Link
- [https://arxiv.org/abs/2605.05251v1](https://arxiv.org/abs/2605.05251v1)
