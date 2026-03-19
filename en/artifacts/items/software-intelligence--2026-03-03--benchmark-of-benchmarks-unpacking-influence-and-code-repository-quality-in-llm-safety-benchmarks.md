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
- benchmark-evaluation
- repository-quality
- research-metrics
- reproducibility
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Benchmark of Benchmarks: Unpacking Influence and Code Repository Quality in LLM Safety Benchmarks

## Summary
This paper systematically evaluates whether the “influence” of LLM safety benchmark papers aligns with the “quality” of their accompanying code repositories, covering three topics: prompt injection, jailbreak, and hallucination. The conclusion is: benchmark papers are not significantly more influential academically than non-benchmark papers, but their code usability and maintainability are overall better, and “famous authors/high-impact papers” do not imply higher code quality.

## Problem
- LLM safety research is growing extremely fast, and researchers increasingly rely on benchmarks to track progress, but it is unclear which benchmarks become more influential and why they attract more attention.
- Existing work rarely examines systematically whether the code repository quality, reproducibility, and supplementary materials of benchmark papers are actually usable, which directly affects research reproduction and practical adoption.
- If paper influence and code quality are disconnected, the community may pay more attention to work with “greater name recognition” rather than work that is “more reproducible and more responsible.”

## Approach
- The authors constructed a cross-topic dataset of **31 benchmark papers** and **382 non-benchmark papers**, spanning **2022-11-30 to 2024-11-01** and covering **prompt injection, jailbreak, hallucination**.
- They evaluated paper/project influence using five categories of influence metrics, including **Citation Count, Citation Density, GitHub Star Count, GitHub Star Density, Scientific Field Count**, and compared them against non-benchmarks.
- They assessed code quality using both automated and manual methods: the automated evaluation used **Pylint, Radon** and GitHub maintenance metrics; the manual evaluation checked whether the code could run, whether additional modifications were needed, and whether installation guides, data guides, and ethical statements were complete.
- They further analyzed the relationship between influence and 11 potential factors, such as **author h-index, author citation count, institution, region, publication status, search appearance frequency**, and tested whether influence is correlated with code quality.

## Results
- Dataset size: a total of **31 benchmark papers** were analyzed (including **27 public repositories**) and **382 non-benchmark papers** (including **168 public repositories**).
- In terms of academic influence, there was **no significant difference** between benchmarks and non-benchmarks: Citation Density **p=0.309, Cliff's δ=-0.112**; Citation Count **p=0.237, δ=-0.130**; Scientific Field Count **p=0.632, δ=-0.052**.
- In terms of open-source community influence, benchmarks were stronger: GitHub Star Density **p=0.012, δ=-0.301（small）**; GitHub Star Count **p=0.004, δ=-0.347（medium）**.
- There was a correlation between author prestige and influence: Author H-Index (Top-1) with Citation Count **ρ=0.73**, Citation Density **ρ=0.71**, Scientific Field Count **ρ=0.68**; Author Citation Count (Top-1) with GitHub Star Count **ρ=0.58**, Star Density **ρ=0.55**.
- On code openness and tool-based evaluation, benchmarks performed better: public repository rate **87% vs 44%**; Pylint Score **p=0.031, δ=-0.276**; Reply Time **p=0.044, δ=-0.239**; Number of Commits **p=0.001, δ=-0.389**; Commit Frequency **p=0.010, δ=-0.309**.
- Manual reproduction still showed clear shortcomings: only **68%** of benchmarks provided runnable scripts, only **39%** of repositories were “ready to run without modification,” only **16%** provided **flawless** installation guides, and only **6%** included ethical considerations; moreover, **no significant correlation** was found between paper influence and intrinsic code quality/maintenance frequency.

## Link
- [http://arxiv.org/abs/2603.04459v1](http://arxiv.org/abs/2603.04459v1)
