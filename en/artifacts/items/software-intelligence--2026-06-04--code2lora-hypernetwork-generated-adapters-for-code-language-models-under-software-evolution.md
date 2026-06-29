---
source: arxiv
url: https://arxiv.org/abs/2606.06492v1
published_at: '2026-06-04T17:59:46'
authors:
- Liliana Hotsko
- Yinxi Li
- Yuntian Deng
- Pengyu Nie
topics:
- code-intelligence
- repository-level-adaptation
- lora-adapters
- hypernetworks
- software-evolution
- code-language-models
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Code2LoRA: Hypernetwork-Generated Adapters for Code Language Models under Software Evolution

## Summary
Code2LoRA generates repository-specific LoRA adapters for frozen code LMs, so repository knowledge enters adapter weights with no extra input tokens at inference. It handles both fixed repository snapshots and commit-by-commit code changes.

## Problem
- Code LMs need repository context to resolve imports, APIs, helper functions, and project conventions.
- RAG and dependency-context methods add token and retrieval cost on every query. Per-repository fine-tuning and LoRA training are costly across many repositories and age poorly as commits change code.
- This matters for coding assistants because real projects are large, multi-file, and active.

## Approach
- A frozen Qwen3-Embedding-0.6B encoder embeds repository files in 4096-token chunks with 512-token overlap, mean-pools chunks into 1024-dimensional file vectors, then aggregates files with a weighted mean plus max pool.
- A trained hypernetwork maps the repository embedding to rank-16 LoRA matrices for Qwen2.5-Coder-1.5B. The base LM and repository encoder stay frozen.
- Code2LoRA-Static maps one repository snapshot to one adapter.
- Code2LoRA-Evo initializes a GRU state from the repository snapshot, updates it with commit diff embeddings, and generates a fresh adapter after each code change.
- The generated adapters cover seven projection types: q, k, v, o, gate, up, and down.

## Results
- The paper builds RepoPeftBench with 604 Python repositories: 512 in-distribution repositories and 92 temporal out-of-distribution repositories.
- Static track: Code2LoRA-Static reaches 63.8% exact match on cross-repo test, beating FFT + RAG at 53.9% by 9.9 percentage points. RAG scores 39.7%, dependency-resolved context scores 48.2%, and Single LoRA scores 47.4%.
- Static track in-repo: Code2LoRA-Static reaches 66.2% exact match, above the reported per-repository LoRA upper-bound baseline at 64.0%.
- Evolution track cross-repo: Code2LoRA-Evo reaches 60.3% exact match, compared with Single LoRA at 55.1% and Code2LoRA-Static at 55.7%.
- Evolution track in-repo: Code2LoRA-Evo reaches 64.5% exact match, compared with Single LoRA at 61.3%, Code2LoRA-Static at 60.6%, and per-repository LoRA at 64.2%.
- Evolution track also reports 0.810 EditSim and 0.763 CodeBLEU for Code2LoRA-Evo on cross-repo test, and 0.828 EditSim and 0.790 CodeBLEU on in-repo test.

## Link
- [https://arxiv.org/abs/2606.06492v1](https://arxiv.org/abs/2606.06492v1)
