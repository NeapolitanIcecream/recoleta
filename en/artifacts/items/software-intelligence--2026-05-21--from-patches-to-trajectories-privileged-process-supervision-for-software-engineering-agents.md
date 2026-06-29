---
source: arxiv
url: https://arxiv.org/abs/2605.21996v1
published_at: '2026-05-21T04:54:55'
authors:
- Murong Ma
- Tianyu Chen
- Yun Lin
- Shuai Lu
- Qinglin Zhu
- Yeyun Gong
- Zhiyong Huang
- Peng Cheng
- Yan Lu
- Jin Song Dong
topics:
- software-engineering-agents
- code-intelligence
- sft-data-curation
- process-supervision
- swe-bench
- reference-patches
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# From Patches to Trajectories: Privileged Process Supervision for Software-Engineering Agents

## Summary
P2T uses developer reference patches to curate shorter and more useful training trajectories for software-engineering agents. It improves SFT data by scoring whether each step uncovers evidence needed for the fix while blocking leakage from the reference patch.

## Problem
- SFT on full teacher rollouts makes the student imitate every intermediate step, including unsupported reasoning, repeated file views, loops, and accidental test-passing behavior.
- Outcome-filtered training only checks whether the final patch passes tests, so it gives no direct signal for step quality or trajectory length.
- In the SWE-Gym pool cited by the paper, 70.2% of Qwen3-Coder-480B teacher instances and 64.7% of GLM-5-FP8 teacher instances provide no supervision because the teacher never reaches a passing patch.

## Approach
- P2T treats the developer reference patch as privileged curation data: the curator can inspect it, but the student never sees it.
- A reverse phase converts the reference patch into a process graph of facts and milestones needed to derive the fix, such as file locations, runtime behavior, root cause, edit plan, code edit, and validation.
- A forward phase samples blinded teacher continuations, mutates at most one step toward an available graph node, and keeps the shortest segment whose progress clears a threshold.
- A groundedness check blocks leakage by requiring mutated steps to mention only observed repository entities and to make claims supported by the visible trajectory prefix.
- Final trajectories are kept only if the submitted patch passes the task test suite.

## Results
- Training uses about 1.8k curated SWE-Gym instances from a pool of 2,438 real Python issues; rejection-sampling baselines run on 2,126 executable instances.
- The reverse phase builds 33,106 process-graph nodes, with a median of 18 nodes per instance.
- On SWE-bench Verified with 500 instances, P2T reports up to +10.8 Pass@1 points over outcome-filtered SFT.
- The paper reports about $15 lower average per-instance inference cost while raising Pass@1, using the same pricing basis across conditions.
- Gains are reported on SWE-bench Verified and SWE-bench Lite with 300 instances, across two teachers: Qwen3-Coder-480B-A35B-Instruct and GLM-5-FP8.
- Baselines include SWE-Gym-style test-pass rejection sampling and SWE-Lego tool-error masking; the paper says a size-matched ablation still beats both, which supports a data-quality claim beyond data scale.

## Link
- [https://arxiv.org/abs/2605.21996v1](https://arxiv.org/abs/2605.21996v1)
