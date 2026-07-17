---
source: arxiv
url: https://arxiv.org/abs/2607.15205v1
published_at: '2026-07-16T17:02:25'
authors:
- Shaoxiong Zhan
- Shi Hu
- Boyu Feng
- Hai Lin
- Andrew Gong
- Zhengda Zhou
- Jiaying Zhou
- Yunyun Hou
- Hao Su
- Hai-Tao Zheng
topics:
- code-intelligence
- automated-software-production
- multimodal-reasoning
- repository-search
- software-engineering-benchmarks
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# MM-IssueLoc: A Controlled Benchmark for Evaluating Visual Evidence in Multimodal Repository-Level Issue Localization

## Summary
MM-IssueLoc introduces a controlled benchmark that measures whether visual evidence helps systems locate responsible files and functions in real software repositories. It separates localization from patch generation through paired text-only and image-conditioned evaluations.

## Problem
- Existing repository-level software-engineering benchmarks are mainly text-only, while real issues often include screenshots, error dialogs, rendered states, and logs.
- Multimodal repair benchmarks combine localization with patch synthesis, so they cannot show whether images improved localization or were ignored.
- This matters because localization errors propagate into automated patch generation and issue resolution.

## Approach
- Construct a benchmark from linked GitHub issues and fixing pull requests, using pre-fix repository snapshots, file-level gold labels for 652 instances, and function-level labels for 343 instances.
- Annotate 1,050 images by seven evidence categories and four relevance levels, including a human-reviewed harmful-image stress test with 55 instances.
- Compare text-only, raw-image, Visual Content Evidence (VCE), and VCE-plus-image modes. VCE converts images into structured text containing fields such as OCR, error signals, UI elements, and code hints.
- Evaluate LLM agents and retrievers with strict Acc@K metrics; the MM-IssueLoc-VL-Embedding retriever uses contrastive learning, hard negatives, and a file-to-function training curriculum.

## Results
- On 652 file-level instances, the strongest overall result is OpenHands with GPT-5.2 at 38.96 File Acc@5; its File Acc@1 and Acc@3 scores are 23.93 and 36.35.
- On 343 function-level instances, MM-IssueLoc-VL-Embedding-8B achieves the best retrieval result, with 33.86 Function Acc@10; the strongest agent reaches 22.45.
- Removing images reduces File Acc@5 by 4.91 points for the 2B controlled retriever and 4.44 points for the 8B version, while image effects on agents are smaller and inconsistent.
- Performance declines sharply on difficult multi-edit issues: OpenHands GPT-5.2 falls from 83.10 Acc@10 on easy instances to 2.84 on hard instances, and the 8B retriever falls from 74.18 to 3.98.
- Text-dominant benchmark performance does not transfer directly: OpenHands reaches 94.53 File@5 on SWE-bench-Lite and 90.20 on SWE-bench-Verified, compared with 43.14 for the best system on SWE-bench-MM.
- The provided text reports both 23 and 24 programming languages, and both 608 repositories and 650 repository snapshots; this accounting discrepancy does not change the core benchmark size but limits precise dataset-scope interpretation.

## Link
- [https://arxiv.org/abs/2607.15205v1](https://arxiv.org/abs/2607.15205v1)
