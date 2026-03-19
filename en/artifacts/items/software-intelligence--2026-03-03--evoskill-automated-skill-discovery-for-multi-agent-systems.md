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
- coding-agents
- evolutionary-optimization
- agent-skills
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# EvoSkill: Automated Skill Discovery for Multi-Agent Systems

## Summary
EvoSkill proposes a framework that lets multi-agent systems automatically “grow skills”: instead of fine-tuning the model, it summarizes failures and generates reusable skill modules from them. The paper argues that this skill-level evolution is more transferable than directly modifying prompts or code, and brings consistent gains across multiple QA/search benchmarks.

## Problem
- Existing coding/agent systems are general-purpose, but lack the **domain skills** needed for specialized tasks, leading to unstable performance on tasks such as complex document reasoning and search verification.
- Most agent skills today rely on **manual hand-crafting**, which makes scaling to more tasks costly, hard to maintain, and difficult to iterate systematically.
- Existing evolutionary methods mostly optimize **low-level artifacts** (prompts, code), which are usually tightly bound to specific models and tasks, resulting in weaker reusability and cross-task transfer.

## Approach
- EvoSkill raises the optimization target from prompts/code to the **skill level**: skills are represented as structured skill folders containing trigger metadata, documentation (`SKILL.md`), and optional helper scripts.
- The system consists of three collaborating agents: **Executor** executes tasks, **Proposer** analyzes failure traces and proposes “add/modify skill” suggestions, and **Skill-Builder** turns those suggestions into concrete skills.
- The evolutionary process is **failure-driven**: in each round, it selects a parent program from the current best program set, collects low-scoring samples, proposes skill mutations based on failure analysis, and then evaluates them on a validation set.
- A fixed-capacity **Pareto/frontier** maintains high-scoring agent programs; only skills that truly improve performance on the held-out validation set are retained, while the underlying model remains frozen throughout.
- The system also maintains a **feedback history** that records past proposals, score changes, and successes/failures, avoiding repeated attempts and helping later proposals continue improving based on prior experience.

## Results
- **OfficeQA** (grounded reasoning over U.S. Treasury documents): baseline exact-match accuracy is **60.6%**, and EvoSkill’s best “merge-unique” configuration reaches **67.9%**, an improvement of **+7.3 percentage points**. Different training ratios in the same table also outperform the baseline: **5% training set 63.4% (+2.8)**, **10% 65.8% (+5.2)**, **15% 64.5% (+3.9)**.
- OfficeQA also improves under more lenient tolerances: for example, **0.10% tolerance** goes from **66.3% → 70.8%**, **1.00% tolerance** from **72.8% → 77.1%**, and **5.00% tolerance** from **77.2% → 80.5%**.
- **SealQA** (search-augmented QA with noisy retrieval): accuracy improves from **26.6%** to **38.7%**, an absolute gain of **+12.1 percentage points**.
- **Zero-shot transfer**: skills evolved on SealQA transfer to **BrowseComp** without modification, improving accuracy from **43.5%** to **48.8%**, a gain of **+5.3 percentage points**.
- The paper’s strongest claim is that with only a **small training subset** and a **frozen underlying model**, significant gains can be achieved by automatically discovering reusable skills, and some of those skills have cross-task transfer ability.
- As a limitation, the paper notes that some configurations were evaluated with only a **single run**; due to high computational cost, **variance analysis across multiple random seeds has not yet been provided**.

## Link
- [http://arxiv.org/abs/2603.02766v1](http://arxiv.org/abs/2603.02766v1)
