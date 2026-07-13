---
source: arxiv
url: https://arxiv.org/abs/2607.09101v1
published_at: '2026-07-10T05:16:54'
authors:
- Quanjun Zhang
- Ye Shang
- Siqi Gu
- Jianyi Zhou
- Chunrong Fang
- Zhenyu Chen
- Liang Xiao
topics:
- unit-test-generation
- multi-agent-systems
- code-knowledge-graphs
- llm-software-engineering
- automated-testing
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Multi-Agent LLM Collaboration for Unit Test Generation via Human-Testing-Inspired Workflows

## Summary
TestAgent generates unit tests through three cooperating LLM agents and a test-focused repository knowledge graph. It reports higher coverage and mutation scores than LLM baselines on six Java projects, extends to Python, and finds 154 real-world bugs with 92.22% precision.

## Problem
- Manual unit-test development takes substantial effort, while conventional generators often produce tests with weak readability, maintainability, and fault-detection value.
- Existing LLM systems use fixed generation pipelines and coarse context extraction, which limits adaptation to execution feedback and misses dependencies needed to infer test requirements.

## Approach
- A requirement planner analyzes the focal method and creates test requirements for normal, boundary, and exceptional cases.
- A test generator retrieves repository context, writes tests, runs syntax and compilation checks, executes tests in a sandbox, analyzes failures, and revises the tests.
- A test reviewer evaluates correctness, coverage, and requirement alignment, then proposes additional test scenarios.
- Static analysis builds a repository-level knowledge graph containing code dependencies, test-specific entities, test links, summaries, test reports, and failure analyses.
- Agents invoke retrieval, graph-update, validation, coverage, and mutation-analysis tools on demand instead of following one fixed workflow.

## Results
- Across six Java projects, TestAgent achieved a 97.46% execution rate, 92.34% line coverage, 90.24% branch coverage, and 83.69% mutation score.
- Under the same GPT-4o backbone, it outperformed the LLM baselines ChatUniTest and HITS across all six reported metrics.
- Against the search-based tool EvoSuite, TestAgent produced a substantially higher mutation score, 83.69% versus 43.59%, with comparable correctness.
- Adding the knowledge graph improved line coverage by 22.31%, branch coverage by 24.52%, and mutation score by 26.83% in the ablation study.
- On Python projects, TestAgent reached 88.85% line coverage and 78.89% branch coverage, exceeding the reported results of CodaMosa and CoverUp.
- For non-regression testing, it detected 154 real-world bugs with 92.22% precision; industrial-project experiments and a user study also supported practical applicability.

## Link
- [https://arxiv.org/abs/2607.09101v1](https://arxiv.org/abs/2607.09101v1)
