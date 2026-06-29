---
source: arxiv
url: http://arxiv.org/abs/2604.07341v1
published_at: '2026-04-08T17:54:08'
authors:
- Ali Reza Ibrahimzada
- Brandon Paulsen
- Daniel Kroening
- Reyhaneh Jabbarvand
topics:
- multi-agent-systems
- code-translation
- repository-level-analysis
- code-validation
- language-agnostic
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories

## Summary
ReCodeAgent is a multi-agent system for translating whole software repositories across programming languages without building a separate pipeline for each language pair. It targets large real-world projects and reports higher compilation and test success than prior neuro-symbolic and agentic baselines.

## Problem
- The paper tackles repository-level code translation and validation across multiple source-target language pairs, where prior systems usually support one pair because the engineering cost is high.
- This matters because codebase migration affects reliability, security, and technical debt, and large repositories include dependencies, tests, naming consistency, and long-range interactions that simple file-by-file translation misses.
- The paper also targets two failure modes in agentic translation: hallucinated code changes in long workflows and weak validation when test translation and code repair are mixed carelessly.

## Approach
- ReCodeAgent splits the job across four agents: Analyzer, Planning, Translator, and Validator.
- The Analyzer studies repository structure, dependencies, error handling, and library usage, then writes a target-project design with target-language library choices and structural mappings.
- The Planning agent identifies translation units, builds a name mapping and project skeleton, and creates a dependency-aware implementation plan.
- The Translator translates both source code and tests into the target repository, while the Validator runs translated tests, checks coverage gaps, generates extra tests for uncovered functions, and sends repair reports back to the Translator.
- To stay language-agnostic, the system uses general tooling exposed through MCP, especially Language Server Protocol tools and lightweight project-analysis tools, instead of hand-built program analysis for each language pair.

## Results
- Evaluation covers 118 real-world projects, 4,583 translation units, and more than 230K lines of code across 6 languages and 4 language pairs: C-Rust, Go-Rust, Java-Python, and Python-JavaScript.
- ReCodeAgent reaches 99.4% compilation success and 86.5% test pass rate on average. The paper says this is 2.5 percentage points higher in compilation and 60.8 percentage points higher in test pass rate than alternative approaches on ground-truth tests.
- Average project size is 1,975 lines of code and 43 translation units. Average runtime is 57 minutes and average cost is $15.3 per project.
- For translated tests, it reports 99.3% assertion equivalence, 0.91 cosine similarity, and 94.9% assertion type match.
- In ablations, removing the Analyzer, Planning, and Validator reduces test pass rate by 22.7, 25.3, and 30.3 percentage points, respectively, and increases trajectory complexity by 28%.
- Compared with two baseline agents, those baselines reach only 25.3% and 24.1% test pass rate, which the paper reports as 61.2 and 62.4 percentage points below ReCodeAgent. A single-agent design also drops test pass rate by 40.4 percentage points and produces trajectories 28% longer.

## Link
- [http://arxiv.org/abs/2604.07341v1](http://arxiv.org/abs/2604.07341v1)
