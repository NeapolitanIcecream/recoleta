---
source: arxiv
url: http://arxiv.org/abs/2603.02766v1
published_at: '2026-03-03T09:07:22'
authors:
- Salaheddin Alzubi
- Noah Provenzano
- Jaydon Bingham
- Weiyuan Chen
- Tu Vu
topics:
- multi-agent-systems
- skill-discovery
- llm-agents
- evolutionary-search
- transfer-learning
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# EvoSkill: Automated Skill Discovery for Multi-Agent Systems

## Summary
EvoSkill proposes a framework for automatically discovering and improving agent “skills.” Instead of directly tuning prompts or code, it turns failure cases into reusable skill modules. With the underlying model frozen, it improves the performance of multi-agent/coding agents on question answering and retrieval tasks through iterative error analysis, and demonstrates cross-task transfer ability.

## Problem
- Most existing agent skills rely on manual authoring, which is costly and scales poorly, making it hard to cover a growing number of specialized tasks.
- Existing evolutionary methods usually optimize low-level artifacts (prompts, code), which are often tightly bound to specific models and tasks, resulting in weak reusability and transferability.
- The authors aim to solve: **how to automatically discover, filter, and accumulate reusable, transferable agent skills without fine-tuning the underlying model**; this matters because it can improve the reliability and capability of general-purpose coding agents on specialized tasks in a more sustainable way.

## Approach
- EvoSkill uses three collaborating agents: an execution agent that attempts the task, a proposal agent that analyzes failure trajectories and proposes textual plans for “new skills / skill edits,” and a skill-construction agent that materializes those plans into structured skill folders.
- A skill is not just a single prompt, but a reusable module containing trigger metadata, `SKILL.md` operating instructions, and optional Python/TypeScript helper scripts.
- The overall process is driven by a failure-driven iterative loop: first collect low-scoring samples, then perform root-cause analysis, generate candidate skills, and finally retain only those skills that improve validation-set performance.
- The method maintains a fixed-capacity Pareto/frontier set of programs. A candidate program enters the frontier only if it outperforms a currently weaker member on the validation set; it also records historical feedback to avoid repeating mistakes and to support further refinement of partially effective skills.
- The underlying model remains frozen throughout; only the skill library and agent metadata change, so performance gains mainly come from accumulation and selection at the skill level rather than model-parameter updates.

## Results
- **OfficeQA** (grounded reasoning over U.S. Treasury documents): baseline exact-match accuracy is **60.6%**, and EvoSkill’s best “merge-unique” configuration reaches **67.9%**, an improvement of **+7.3 percentage points**.
- Under different OfficeQA training-set sizes, exact match improves from **60.6%** to **63.4% (5% training set, +2.8)**, **65.8% (10%, +5.2)**, and **64.5% (15%, +3.9)** respectively; this suggests performance is best around 10%, and more data does not necessarily keep improving results.
- OfficeQA also shows consistent gains under different tolerances: for example, **0.10% tolerance** improves from **66.3%** to **70.8%**, **1.00% tolerance** from **72.8%** to **77.1%**, and **5.00% tolerance** from **77.2%** to **80.5%**.
- **SealQA** (search-augmented QA with noisy retrieval): accuracy improves from **26.6%** to **38.7%**, an absolute gain of **+12.1 percentage points**.
- **Zero-shot transfer**: skills evolved on SealQA transfer directly to **BrowseComp**, improving accuracy from **43.5%** to **48.8%** on **128** stratified samples, i.e. **+5.3 percentage points**, without any skill modification.
- The paper also provides a strong qualitative conclusion: automatically discovered skills are interpretable and composable, such as a “table numeric extraction verification protocol” and a “search persistence protocol”; however, the authors also note that some experiments were run only once and **do not include variance analysis across multiple random seeds**.

## Link
- [http://arxiv.org/abs/2603.02766v1](http://arxiv.org/abs/2603.02766v1)
