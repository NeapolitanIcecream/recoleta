---
source: arxiv
url: http://arxiv.org/abs/2604.06793v1
published_at: '2026-04-08T07:58:18'
authors:
- Xinchen Wang
- Ruida Hu
- Cuiyun Gao
- Pengfei Gao
- Chao Peng
topics:
- software-documentation
- repository-level-benchmark
- question-answering
- code-intelligence
- software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Evaluating Repository-level Software Documentation via Question Answering and Feature-Driven Development

## Summary
SWD-Bench is a benchmark for evaluating repository-level software documentation by testing whether an LLM can answer development questions from the documentation. It shifts evaluation away from vague judge scores and toward task performance on repository understanding and implementation details.

## Problem
- Existing documentation benchmarks usually score small code snippets, so they miss whether documentation explains functionality that spans multiple files and modules.
- Common evaluation methods, especially LLM-as-a-judge with Likert scales, use vague criteria and often lack enough repository knowledge to judge correctness.
- This matters because repository documentation is used for real work: finding whether a feature exists, locating the code, and understanding enough details to extend or fix it.

## Approach
- The paper builds **SWD-Bench**, a repository-level QA benchmark with 4,170 entries drawn from pull requests across 12 SWE-Bench repositories.
- Each entry is turned into three QA tasks tied to developer workflow: **Functionality Detection** (does this feature exist?), **Functionality Localization** (which files implement it?), and **Functionality Completion** (fill in missing technical details).
- The data pipeline starts from 177.4k GitHub pull requests, applies multi-step filtering for merged, reviewed, feature-related, persistent changes, and keeps 4,170 high-quality PRs.
- For each PR, the benchmark gathers repository context such as dependency analysis, linked issues, external pages, and commit history, then uses an LLM to write a functionality description along WHAT/WHY/HOW dimensions.
- Evaluation compares model answers against objective references extracted from PR metadata and code changes, instead of asking an LLM to score documentation quality directly.

## Results
- SWD-Bench contains **4,170** benchmark entries. Functionality descriptions average **771.45 characters**; positive detection cases are **50.65%** of entries.
- The localization task requires finding **2.01 files on average** per entry, with a range of **1 to 62** files.
- The completion task requires filling **7.48 details on average** per entry, with a range of **3 to 23** details.
- Manual validation on **100 sampled entries** reached **inter-annotator agreement above 90% Kappa**, which supports dataset quality.
- The paper claims current repository-level documentation generation methods still have clear limits, and methods with richer repository context perform better, but this excerpt does not include the full task metrics table.
- In downstream use, documentation from the best-performing method improves **SWE-Agent issue-solving rate by 20.00%** over its comparison setup, showing practical value for issue resolution.

## Link
- [http://arxiv.org/abs/2604.06793v1](http://arxiv.org/abs/2604.06793v1)
