---
source: arxiv
url: https://arxiv.org/abs/2606.24177v1
published_at: '2026-06-23T05:57:09'
authors:
- Youran Sun
- Xingyu Ren
- Chugang Yi
- Jiaxuan Guo
- Kejia Zhang
- Jianda Du
- Haizhao Yang
topics:
- autonomous-research
- multi-agent-systems
- prompt-orchestration
- research-automation
- human-ai-interaction
- software-agents
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Agon: An Autonomous Large-Scale Omnidisciplinary Research System Built on Prompt Economy

## Summary
Agon is a prompt-driven multi-agent system for running many research workflows in parallel, from topic selection to paper draft. It aims to scale artifact production while leaving claim judgment and scientific direction to humans.

## Problem
- Research agents can now generate code, experiments, reviews, and manuscripts, so the hard bottleneck shifts to checking claims, novelty, and evidence.
- Large autonomous workflows often grow many roles, long prompts, and brittle control code, which makes them hard to inspect, maintain, and move across fields.
- The system targets computational research settings where experiments, literature review, and paper drafting can be run through model calls and remote compute.

## Approach
- Agon uses reusable producer-critic loops called factories for ideas, proposals, experiments, and papers.
- Its core mechanism is Prompt Economy: keep a small set of role prompts and reuse them many times across many artifacts, instead of writing task-specific prompts for each project.
- A deep-literature loop searches, selects, reads, writes wiki entries, expands queries, and repeats, giving later agents a shared literature memory.
- The experiment factory separates scientist, coder, auditor, and reviewer roles; coders run jobs while auditors check plans, code, results, and handoff state.
- Dispatch is handled mainly by prompt-based dispatchers rather than workflow-specific state machines or parser-heavy control code.

## Results
- The paper reports 444 Prompt Economy loop iterations across domains.
- Agon uses 18 roles and 230.6 KiB of prompt text, compared with about 110 roles and 302.4 KiB for AI Scientist v2, 79 roles and 1157.4 KiB for ARIS, and 78 roles and 1297.5 KiB for AutoResearchClaw.
- The deep-literature process reads about 400-2000 papers per topic at the current operating scale.
- The authors report projects in more than 10 scientific domains and thousands of scientist-coder-auditor iterations, with no human writing experimental code.
- They report one month of continuous dispatcher operation without human intervention.
- The excerpt gives no quantitative benchmark for scientific correctness, paper acceptance, or claim validity; its strongest evidence is deployment scale, prompt-surface size, and the failure taxonomy.

## Link
- [https://arxiv.org/abs/2606.24177v1](https://arxiv.org/abs/2606.24177v1)
