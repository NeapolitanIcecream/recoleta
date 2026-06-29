---
source: arxiv
url: https://arxiv.org/abs/2605.10865v2
published_at: '2026-05-11T17:13:36'
authors:
- Haozhe Zhang
- Kaichen Liu
- Miaomiao Chen
- Lei Li
- Shaojie Yang
- Cheng Peng
- Hanjie Chen
topics:
- programmatic-cad
- code-generation
- cad-benchmark
- multimodal-models
- engineering-automation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# BenchCAD: A Comprehensive, Industry-Standard Benchmark for Programmatic CAD

## Summary
BenchCAD tests whether multimodal models can turn images, code, and edit instructions into executable, editable industrial CAD programs. The benchmark shows that current models can often match rough shape but still miss engineering details, parameters, and CAD operations.

## Problem
- Industrial CAD automation needs parametric programs that engineers can edit, manufacture, and check, not just rendered shapes that look close.
- Existing CAD benchmarks often score end-to-end geometry similarity, which can hide wrong operations, weak parameter recovery, and poor edit behavior.
- The gap matters because parts such as gears, springs, drills, and fasteners depend on standard dimensions, local features, and operation choices.

## Approach
- BenchCAD contains 17,900 execution-verified CadQuery programs across 106 named industrial part families.
- The dataset includes 52 standard-anchored families out of 106, tied to 47 ISO, DIN, EN, ASME, or IEC codes.
- It tests four tasks: image-to-CadQuery generation, image QA, code QA, and instruction-guided code editing.
- It uses multi-view renders, paired image/code numeric QA items, and curated edit pairs to separate visual recognition, CAD operation understanding, parametric abstraction, and code synthesis.
- Its CadQuery coverage includes 49 operations, including helical sweeps, lofts, twistExtrude, polarArray, and parametric gear construction.

## Results
- BenchCAD-QA has 2,400 paired image/code numeric QA items; BenchCAD-Edit has 748 verified edit pairs.
- On Vision QA, the best reported total score is 0.587 for Gemini 3.1 Pro, compared with 0.375 for the blank-image baseline. GPT-4o scores 0.464, GPT-5.3 thinking scores 0.514, and Claude Opus 4.7 thinking scores 0.530.
- Code QA reaches about 0.838 for the best models, while Vision QA peaks at 0.587, showing a large gap between reading CAD code and inferring the same information from renders.
- On BenchCAD-Edit, GPT-5.3 thinking scores 0.865 normalized accuracy, Claude Opus 4.7 thinking scores 0.853, Gemini 3.1 Pro thinking scores 0.837, GPT-4o scores 0.615, and the no-change baseline scores 0.000.
- On Vision2Code, the strongest reported proprietary model score in the excerpt is Gemini 3.1 Pro thinking at 0.318 total; CAD-specialist models get good IoU but miss non-extrude operations.
- Fine-tuning and reinforcement learning on BenchCAD improve in-distribution generation and operation coverage, but the excerpt reports limited generalization to held-out part families rather than a single headline number.

## Link
- [https://arxiv.org/abs/2605.10865v2](https://arxiv.org/abs/2605.10865v2)
