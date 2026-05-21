---
source: arxiv
url: https://arxiv.org/abs/2605.13716v1
published_at: '2026-05-13T16:02:25'
authors:
- Hongji Pu
- Xinyuan Song
- Liang Zhao
topics:
- llm-agents
- skill-libraries
- code-intelligence
- agent-maintenance
- technical-debt
- software-agents
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# SkillOps: Managing LLM Agent Skill Libraries as Self-Maintaining Software Ecosystems

## Summary
SkillOps maintains LLM agent skill libraries before task execution by detecting stale, duplicate, unsafe, and incompatible skills. On ALFWorld, it reports higher task success than several retrieval, planning, graph, and self-repair baselines while adding near-zero library-time LLM cost.

## Problem
- LLM agents reuse skill libraries for multi-step tasks, but those libraries can collect persistent defects such as redundant skills, missing validators, stale implementations, and interface drift.
- Task-time repair can fix one failed episode while leaving the damaged skill in the library, so the same defect can affect later retrieval, composition, or execution.
- This matters for automated software production and code-oriented agents because a growing skill library behaves like maintained software: broken interfaces and unvalidated outputs can spread failures across workflows.

## Approach
- Each skill is stored as a typed contract `(P,O,A,V,F)`: preconditions, executable operation, produced artifact, validator, and known failure modes.
- SkillOps builds a Hierarchical Skill Ecosystem Graph that links skills with dependency, compatibility, redundancy, and alternative edges.
- A library-time pass scores health across utility, redundancy, compatibility, failure risk, and validation gaps, then applies typed actions such as `merge`, `repair`, `retire`, `add_validator`, and `add_adapter`.
- At task time, its optional planner retrieves skills with BM25 plus semantic scoring, filters by preconditions, stitches plans only through dependency and compatibility edges, inserts validators or adapters, and tries local repair after failures.
- The plug-in path is simple: `run_maintenance(raw_library)` returns a cleaned library that existing retrieval or planning agents can use without code changes.

## Results
- On ALFWorld with a 200-skill library, SkillOps_Full reaches 79.5% task success with Wilson 95% CI [75.9, 82.6], compared with LLM_Skill_Planner at 70.6%, GoS_Style at 61.1%, Hybrid_Retrieval at 58.2%, SkillWeaver at 50.3%, and ReAct at 12.8%.
- Against the strongest baseline in Table 1, LLM_Skill_Planner, SkillOps gains +8.9 percentage points in task success; the abstract reports +8.8 percentage points.
- As a drop-in maintenance layer at the 200-skill scale, it improves Hybrid Retrieval from 38.2% to 41.1% (+2.90pp), BM25 Only from 41.8% to 42.8% (+1.00pp), Dense Only from 32.3% to 33.4% (+1.12pp), GoS Style from 42.8% to 43.6% (+0.80pp), LLM Skill Planner from 49.8% to 50.3% (+0.50pp), and SkillWeaver from 41.3% to 43.8% (+2.46pp); ReAct stays at 11.9%.
- The paper reports near-zero library-time LLM calls across library sizes up to 2,000 skills.
- Task-time token use decreases in 24 of 35 measured cells, stays nearly unchanged in 4, and increases in 7; the largest reported decrease is -3.95% for Dense_Only at library size 1,000, while the largest increase is +5.56% for BM25_Only at library size 500.

## Link
- [https://arxiv.org/abs/2605.13716v1](https://arxiv.org/abs/2605.13716v1)
