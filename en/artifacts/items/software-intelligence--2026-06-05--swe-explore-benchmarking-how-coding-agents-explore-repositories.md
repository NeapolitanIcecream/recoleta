---
source: arxiv
url: https://arxiv.org/abs/2606.07297v1
published_at: '2026-06-05T14:08:27'
authors:
- Shaoqiu Zhang
- Yuhang Wang
- Jialiang Liang
- Yuling Shi
- Wenhao Zeng
- Maoquan Wang
- Shilin He
- Ningyuan Xu
- Siyu Ye
- Kai Cai
- Xiaodong Gu
topics:
- coding-agents
- repository-exploration
- code-localization
- software-benchmarks
- context-retrieval
- swe-bench
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# SWE-Explore: Benchmarking How Coding Agents Explore Repositories

## Summary
SWE-Explore is a benchmark for measuring how well coding agents find the code needed to fix repository issues. It separates repository exploration from patch generation and scores ranked line ranges against trajectory-derived ground truth.

## Problem
- Repository-level benchmarks such as SWE-bench usually report only pass or fail, so they hide whether an agent failed because it missed the relevant code or because it could not write the patch.
- File-level localization can look good while the agent still misses the exact lines needed for a fix, which matters in repositories with hundreds or thousands of files.
- The paper targets a shared evaluation task for lexical retrievers, dense retrievers, long-context selectors, and agentic code explorers.

## Approach
- Given an issue and a repository snapshot, an explorer returns a ranked list of code regions, each defined by file path and line range.
- SWE-Explore builds line-level ground truth from successful repair trajectories by strong coding agents, keeping instances with at least 2 successful trajectories.
- It extracts explicit read actions such as editor views, `cat`, `head`, `tail`, `sed -n`, and `grep -n`, then maps them to file-line intervals.
- It forms core target regions from line-level overlap across successful trajectories, promotes a small number of load-bearing optional reads with an LLM step, and manually audits the final regions.
- It scores outputs with line-level precision and recall, file and region hit rates, nDCG under a line budget, first useful hit, context efficiency, and noise rate; a restricted-context repair test checks whether these scores predict actual fixes.

## Results
- The benchmark contains 848 issues across 10 programming languages and 203 open-source repositories, drawn from SWE-bench Verified, SWE-bench-Pro, and SWE-bench Multilingual.
- Each instance averages 4.3 ground-truth files, 4.7 regions, and 1,578 target lines inside repositories averaging 759 non-test files and 179.6K non-test lines.
- In restricted-context repair on a 150-instance subset with K=5 regions, Oracle reaches 59.7% resolve rate and Random reaches 4.7%; CoSIL reaches 59.3%, Mini-SWE-Agent 50.0%, Codex 50.3%, Claude Code 48.0%, and OpenHands 47.7%.
- Classical retrieval is lower in the same repair test: TF-IDF reaches 26.0%, RAG 23.3%, and BM25 12.7% resolve rate.
- Upstream exploration metrics strongly track downstream repair: Context Efficiency has Pearson r=0.950, FUH r=0.928, Rec@100 r=0.926, HitFile r=0.925, and nDCG@500 r=0.921 against resolve rate.
- With the same Mini-SWE-Agent scaffold, GPT-5.4-mini has the best reported nDCG@500 at 0.924 and FUH at 0.956; GPT-5.4 has the best precision at 0.542 and context efficiency at 0.771.

## Link
- [https://arxiv.org/abs/2606.07297v1](https://arxiv.org/abs/2606.07297v1)
