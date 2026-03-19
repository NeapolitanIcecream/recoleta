---
source: arxiv
url: http://arxiv.org/abs/2603.04459v1
published_at: '2026-03-03T09:10:45'
authors:
- Junjie Chu
- Xinyue Shen
- Ye Leng
- Michael Backes
- Yun Shen
- Yang Zhang
topics:
- llm-safety
- benchmark-analysis
- research-metrics
- code-quality
- reproducibility
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Benchmark of Benchmarks: Unpacking Influence and Code Repository Quality in LLM Safety Benchmarks

## Summary
This paper systematically evaluates the **academic influence** and **code repository quality** of LLM safety benchmark papers, and analyzes whether the two are aligned. The core conclusion is: benchmark papers do not have significantly higher academic influence, but their code and maintenance are generally better, and a “well-known author/high-impact paper” does not equal “high-quality code.”

## Problem
- LLM safety research is growing extremely quickly, and benchmarks are widely used to track progress, but it is unclear **which benchmarks are more influential, and why they are more influential**.
- The community often assumes that “more famous papers/authors” means more reliable and more reproducible, but **code repository quality and usability** have lacked systematic review.
- This matters because if benchmark influence and code quality are decoupled, researchers may follow evaluation tools that are “more visible” rather than “more reproducible,” affecting the reliability of LLM safety research.

## Approach
- Collected and manually filtered **31 benchmark papers** and **382 non-benchmark papers**, covering three LLM safety topics: **prompt injection, jailbreak, hallucination**; the corresponding public repositories numbered **27** and **168**, respectively.
- Used **5 influence metrics** to evaluate paper impact: Citation Count, Citation Density, GitHub Star Count, GitHub Star Density, Scientific Field Count, and statistically compared benchmark and non-benchmark papers.
- Used **automated code analysis + manual execution-based evaluation** to assess code quality: the automated part included Pylint, Radon, static errors, maintenance frequency, etc.; the manual part checked whether the code could run, whether extra modifications were needed, installation instructions, data documentation, ethical statements, etc.
- Further analyzed the relationship between influence and 11 potential factors, including author prominence, institution, geography, publication status, and search visibility, and tested **whether paper influence is correlated with code quality**.

## Results
- In terms of academic influence, benchmark papers were **not significantly better than** non-benchmark papers: Citation Density **p=0.309**, Citation Count **p=0.237**, Scientific Field Count **p=0.632**, with negligible effect sizes.
- In terms of open-source community influence, benchmark papers were stronger: GitHub Star Density **p=0.012, Cliff's δ=-0.301 (small)**; GitHub Star Count **p=0.004, δ=-0.347 (medium)**.
- Author prominence was significantly correlated with paper influence: Author H-Index (Top-1) with Citation Count **ρ=0.73**, Citation Density **ρ=0.71**, Scientific Field Count **ρ=0.68**; Author Citation Count (Top-1) with GitHub Star Count **ρ=0.58**, Star Density **ρ=0.55**.
- Benchmark papers had higher repository openness: **87%** of benchmark papers provided accessible repositories, while only **44%** of non-benchmark papers did.
- In terms of code quality/maintenance, benchmark repositories performed better in Pylint Score and maintenance activity: Pylint Score **p=0.031, δ=-0.276**; Reply Time **p=0.044, δ=-0.239**; Number of Commits **p=0.001, δ=-0.389**; Commit Frequency **p=0.010, δ=-0.309**.
- But reproducibility remained poor: only **68%** of benchmark papers provided runnable scripts, and only **39%** of repositories could **run out of the box without modification**; only **16%** provided **flawless installation guides**, and only **6%** covered ethical considerations. The paper also claims that **neither author prominence nor paper influence is significantly correlated with code quality**, showing that “getting attention” does not mean “having usable code.”

## Link
- [http://arxiv.org/abs/2603.04459v1](http://arxiv.org/abs/2603.04459v1)
