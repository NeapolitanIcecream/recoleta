---
source: arxiv
url: http://arxiv.org/abs/2604.03622v1
published_at: '2026-04-04T07:37:55'
authors:
- Ruwei Pan
- Junlei Shen
- Linhao Wu
- Yueheng Zhu
- Zixiong Yang
- Yakun Zhang
- Lu Zhang
- Hongyu Zhang
topics:
- repository-level-code-generation
- environment-alignment
- code-execution
- dependency-resolution
- multi-file-generation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Toward Executable Repository-Level Code Generation via Environment Alignment

## Summary
EnvGraph targets repository-level code generation where success depends on whether a generated multi-file project can actually install, run, and pass validation. It treats execution failures as an environment alignment problem across both external dependencies and internal repository references, then revises the repository in a targeted loop.

## Problem
- Repository-level code generation often fails under real execution because the generated project cannot install dependencies, resolve imports and symbols across files, or launch cleanly.
- The same runtime symptom, such as `ModuleNotFoundError`, can come from two different causes: missing external packages or broken internal references. A revise loop that follows only the visible error can edit the wrong part of the repository.
- This matters because executable validation is stricter than code plausibility: a repository must work as a whole, not just look correct file by file.

## Approach
- EnvGraph builds two graphs for the current repository: an external environment graph for package usage and declarations, and a repository dependency graph for files, modules, imports, symbols, unresolved references, and parse errors.
- It executes the repository and collects evidence such as install failures, runtime errors, stack traces, and test outcomes.
- It normalizes that evidence, then applies an explicit attribution policy to pick the dominant failure source in priority order: external dependency failure, internal reference resolution failure, then residual logic fault.
- Based on that diagnosis, it performs a single targeted revision step that focuses on dependency fixes, internal link repairs, or logic fixes, then rebuilds the graphs and repeats until success or budget exhaustion.
- The paper frames this as environment alignment rather than generic generate-execute-revise, because the revision direction depends on which execution precondition is currently broken.

## Results
- Across three backbone LLMs, EnvGraph beats the strongest non-EnvGraph baseline by **5.72 to 5.87 percentage points** in **Functional Correctness**.
- It also beats the strongest non-EnvGraph baseline by **4.58 to 8.66 percentage points** in **Non-Functional Quality**.
- The evaluation uses two repository-level benchmarks: **RAL-Bench** with **38 tasks** across **7 categories**, and **NL2Repo-Bench** with **104 tasks** across **9 categories**.
- NL2Repo-Bench inputs average about **18.8k tokens** and are split into **26 easy / 46 medium / 32 hard** tasks.
- In a motivating error study on failed direct generations from **GPT-5**, **DeepSeek-V3**, and **Gemini-3-Pro-Preview** on NL2Repo-Bench, environment-related failures account for **34.7%**, **68.9%**, and **30.9%** of failures, respectively.
- The excerpt does not provide full per-model score tables, exact baseline names with values, or ablation numbers, but it claims consistent gains over representative environment-aware and repository-level methods.

## Link
- [http://arxiv.org/abs/2604.03622v1](http://arxiv.org/abs/2604.03622v1)
