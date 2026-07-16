---
source: arxiv
url: https://arxiv.org/abs/2607.13965v1
published_at: '2026-07-15T15:52:11'
authors:
- Yiheng Huang
- Zhijia Zhao
- Bihuan Chen
- Susheng Wu
- Zhuotong Zhou
- Yiheng Cao
- Kun Hu
- Xin Hu
- Xin Peng
topics:
- code-intelligence
- software-supply-chain-security
- malware-detection
- multi-agent-software-engineering
- static-dynamic-analysis
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# ProfMalPlus: Agent-Coordinated Detection of Malicious NPM Packages via Static-Dynamic Analysis Synergy

## Summary
ProfMalPlus detects malicious NPM packages by combining object-sensitive behavior graphs, source-level code slices, static and dynamic evidence, and coordinated LLM agents. The paper reports strong benchmark and real-world results, including a 98.1% F1-score and 597 previously unknown malicious packages identified during three months of monitoring.

## Problem
- Malicious NPM packages threaten software supply chains, while the registry's size makes manual inspection infeasible.
- Existing detectors may miss obfuscated or object-mediated JavaScript behavior, fail to combine static and dynamic evidence, and provide limited explanations or code localization.

## Approach
- A script analyzer inspects installation commands and identifies files executed during installation and import time.
- An object-sensitive static analyzer builds behavior graphs containing control flow, control dependencies, data dependencies, sensitive APIs, third-party calls, and unresolved calls; a code slicer converts suspicious graph regions into source-preserving, annotated slices.
- Local judge agents assess slices, a global judge combines slice results, and self-consistency verification reduces variation in repeated LLM judgments.
- When evidence is insufficient, a router selects registry-based third-party enrichment or sandboxed dynamic augmentation, then repeats the reasoning process.
- A localization agent maps confirmed malicious behavior to concrete code snippets and generates explanations.

## Results
- ProfMalPlus achieved a 98.1% F1-score, the highest result among the evaluated detectors, outperforming state-of-the-art systems by 3.5 to 52.6 percentage points.
- Its line-level malicious-code localization F1-score was 88.9%, and its explanations were judged high quality for 86.9% of sampled malicious packages.
- During three months of monitoring newly published NPM packages, it detected 597 previously unknown malicious packages; the paper states that all were confirmed and removed from NPM.
- The reported real-world false positive rate was 16.5%, the lowest among the compared detectors.
- The excerpt does not specify the benchmark dataset size or the exact experimental protocol behind the reported F1 comparisons, so those results cannot be independently contextualized from the supplied text alone.

## Link
- [https://arxiv.org/abs/2607.13965v1](https://arxiv.org/abs/2607.13965v1)
