---
source: arxiv
url: https://arxiv.org/abs/2605.28510v1
published_at: '2026-05-27T14:12:17'
authors:
- Andrea Gurioli
- Davide D'Ascenzo
- Federico Pennino
- Maurizio Gabbrielli
- Stefano Zacchiroli
topics:
- code-provenance
- llm-generated-code
- code-retrieval
- plagiarism-detection
- vector-search
- software-compliance
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Efficient and Scalable Provenance Tracking for LLM-Generated Code Snippets

## Summary
HybridSourceTracker traces LLM-generated code fragments back to likely source snippets at large-corpus scale. It combines a 300M-parameter code encoder with Winnowing fingerprint re-ranking to keep high match quality while avoiding full linear scans.

## Problem
- Code LLMs can reproduce training snippets or renamed variants, which creates plagiarism, attribution, and license-compliance risks for developers.
- Winnowing-based detectors are effective for code similarity, but comparing a query against billion-scale training corpora is too slow because search cost grows with corpus size.
- Exact-match tracing systems miss many adapted snippets when identifiers or local names change.

## Approach
- SourceTracker encodes a code fragment and full code snippets into 1024-dimensional vectors, then retrieves nearby snippets with Qdrant using HNSW vector search.
- The model uses the first 9 layers of ModularStarEncoder, totaling 300M parameters, and is trained with CLIP contrastive loss so matching fragment-snippet pairs sit close in vector space.
- Training uses 60-token fragments from a 10M-snippet subset of TheStackV2; 50% are verbatim clones and 50% have frequent identifiers replaced to simulate renamed code.
- HybridSourceTracker first retrieves the top 100 vector candidates, then applies Winnowing fingerprints and Jaccard similarity only to those candidates.
- This makes the expensive exact comparison run on a fixed-size set, so the claimed query complexity is logarithmic in corpus size.

## Results
- On an in vitro 100k-snippet search space with adapted queries, HST matches Winnowing MRR at 30-token windows and exceeds it for windows of 60 tokens or more.
- The paper reports HST beating Winnowing by up to 5.4% for windows of at least 60 tokens while keeping logarithmic-time retrieval through Qdrant.
- Against OLMoTrace on 100k snippets with type-2 clones, HST is much stronger for longer windows: OLMoTrace MRR is 44.3% at 60 tokens with a -45.3 point gap to HST, implying HST at 89.6%.
- The same OLMoTrace comparison implies HST MRR of 95.4% at 120 tokens, 98.2% at 240 tokens, and 99.3% at 480 tokens.
- OLMoTrace performs better only at 7 tokens: 26.1% MRR, +15.6 points over HST, implying HST at 10.5%.
- The system is trained and evaluated on a 10M-snippet TheStackV2 subset, with final reported search-space experiments ranging from 1,000 to 100,000 samples and windows from 7 to 480 tokens.

## Link
- [https://arxiv.org/abs/2605.28510v1](https://arxiv.org/abs/2605.28510v1)
