---
source: arxiv
url: https://arxiv.org/abs/2605.26177v1
published_at: '2026-05-25T06:26:43'
authors:
- Hanyu Li
- Yichi Zhang
- Speed Zhu
- Hang Su
- Jun Zhu
- Yinpeng Dong
topics:
- code-agents
- repository-context
- swe-bench
- code-intelligence
- multi-file-reasoning
- agent-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations

## Summary
RepoMirage tests whether code agents that solve SWE-Bench Verified issues can reason over repository context across files. Its perturbation-based suite shows large score drops when direct local cues are removed, even though the underlying tasks keep the same behavior.

## Problem
- Existing repository-level benchmarks report end-to-end issue-resolution success, but they do not isolate whether an agent found and connected task-relevant information across files.
- This matters because real code fixes often require tracing imports, runtime targets, constants, and multi-file edits, while many successful SWE-Bench runs inspect only a few files.
- In the paper's file-access analysis, GPT-5 inspected 1 file in 53.8% of solved cases and no more than 3 files in 88.0%; DeepSeek-V3.2 stayed within 3 files in 55.7% of solved cases.

## Approach
- RepoMirage-Perturb starts from SWE-Bench Verified and applies behavior-preserving repository perturbations while keeping the original issue-resolution task and tests.
- The three perturbations are dependency-path indirection with a 4-layer proxy chain, runtime-target masking through renamed targets and re-export wrappers, and local-value externalization into JSON resources.
- RepoMirage-Extend turns these structural bottlenecks into explicit tasks: multi-file issue resolution, proxy-chain completion, runtime target identification, and missing-constant recovery.
- The paper evaluates 8 models through mini-swe-agent and records trajectories to measure file access and exploration/edit/test action shifts.
- RepoAnchor is a prototype workflow that first builds a task-related repository structure summary, then uses that summary to guide solving.

## Results
- On RepoMirage-Perturb, the average resolved rate across 8 models fell from 66.80% on SWE-Bench Verified to 49.78% after perturbation, while average accessed files rose from 4.77 to 13.24.
- Relative resolved-rate drops ranged from 15.96% for Claude-Sonnet-4.6 to 52.60% for GPT-4.1; GPT-5 fell from 65.00% to 49.00%.
- On RepoMirage-Extend, average success fell from 66.80% on the original setting to 25.25% across 8 models.
- Task-level averages on RepoMirage-Extend were 17.86% for multi-file issue resolution, 17.19% for proxy-chain recovery, 28.26% for runtime target identification, and 33.94% for missing-constant recovery.
- The best overall RepoMirage-Extend average in Table 2 was Gemini-3.1-Pro at 41.40%; GPT-4.1 was lowest at 3.40%.
- The excerpt reports that RepoAnchor improves performance with structural scaffolding, but it does not provide exact RepoAnchor gain numbers.

## Link
- [https://arxiv.org/abs/2605.26177v1](https://arxiv.org/abs/2605.26177v1)
