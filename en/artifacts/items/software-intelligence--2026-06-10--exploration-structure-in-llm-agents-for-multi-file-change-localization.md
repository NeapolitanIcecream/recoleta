---
source: arxiv
url: https://arxiv.org/abs/2606.11976v1
published_at: '2026-06-10T11:54:14'
authors:
- Akeela Darryl Fattha
- Kia Ying Chua
- Lingxiao Jiang
- Laura Wynter
topics:
- software-agents
- code-localization
- multi-agent-systems
- swe-bench
- repository-analysis
- llm-code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Exploration Structure in LLM Agents for Multi-File Change Localization

## Summary
The paper claims that parallel exploration by repository subsystem improves multi-file change localization for LLM software agents, especially for small models with limited search budget. It evaluates Ansible issues from SWE-bench Pro and compares no-tool LLMs, sequential REPL agents, domain-scoped agents, BM25, and Codex 5.5 High.

## Problem
- The task is to predict which repository files must change for a GitHub issue before patch generation begins; this matters because SWE-bench Pro has an 80% multi-file rate, so missing one subsystem can block a correct fix.
- Most LLM agents inspect one file, directory, or grep result per step, which can waste the budget in one part of the repository when the true fix spans code, plugins, CLI paths, tests, or docs.
- Raw file-system access can add false positives, especially test files and changelog files that may be present in resolving PRs but absent from the curated SWE-bench Pro gold set.

## Approach
- The method builds persistent domain agents for coherent Ansible repository areas such as `lib/ansible/cli/`, `lib/ansible/module_utils/`, `lib/ansible/galaxy/`, plugins, and `docs/docsite/rst/`.
- At query time, a root coordinator reads the issue, selects relevant domain agents, runs them in parallel, and merges their candidate file lists.
- Each domain agent searches only its assigned repository region and returns candidate files with a short rationale.
- A bounded I/O layer keeps large files and directories outside the prompt by using previews, line-range reads, search results, compact directory listings, and handles in a persistent Python environment.
- The evaluation uses a persistent-session Ansible slice: 19 SWE-bench Pro instances at base commit `01e7915b0a97`, with 15 hard multi-file cases, 4 easy cases, 63 curated gold files, and 9 cases with docs files.

## Results
- The excerpt reports that Haiku-class domain agents achieve the highest micro-F1 among Haiku-class methods by a large margin; exact micro-F1 values are not provided in the excerpt.
- On the authors' expanded PR-based benchmark with 2025 and 2026 PRs, domain agents rank second behind Codex 5.5 High; exact scores are not provided in the excerpt.
- On the original curated 2020 SWE-bench Pro slice, a larger Sonnet plain-LLM baseline gets higher micro-F1 by predicting fewer files, which raises precision but lowers all-gold recall; exact precision, recall, and F1 values are not provided in the excerpt.
- The benchmark slice contains 19 Ansible issues, 63 curated gold files, and a PR-based reference set of 171 touched files; the 108 PR-touched files missing from curated gold include 52 integration-test files, 27 unit-test files, 10 other test files, and 16 changelog fragments.
- Bounded I/O cuts prompt cost sharply: a large source file drops from 29,895 tokens to 719 tokens for bounded context, a 97.6% reduction; a large docs file drops from 14,366 tokens to 121 tokens, a 99.2% reduction.
- Compact directory listings keep path reconstruction accuracy at 50/50 while reducing average input tokens from 1,540 to 910, a 40.8% reduction.

## Link
- [https://arxiv.org/abs/2606.11976v1](https://arxiv.org/abs/2606.11976v1)
