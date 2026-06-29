---
source: arxiv
url: https://arxiv.org/abs/2605.10990v1
published_at: '2026-05-09T11:41:53'
authors:
- Linfeng Fan
- Yuan Tian
- Ziwei Li
- Zhiwu Lu
topics:
- llm-agents
- skill-libraries
- software-maintenance
- code-intelligence
- agent-repair
- drift-detection
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries

## Summary
SkillGuard treats stale LLM-agent skills as failed environment contracts and checks only assumptions that affect execution. The paper claims this cuts false alarms while still finding real API, package, URL, config, and schema drift.

## Problem
- LLM agents reuse skill libraries for software tasks, but skills can break when external packages, APIs, URLs, configs, schemas, or auth flows change after the skill was written.
- Existing monitors often watch raw values, so they alert on harmless changes such as comment versions or documentation redirects.
- This matters because noisy alerts make long-lived agent skills hard to maintain, while missed drift can cause agents to run stale procedures.

## Approach
- SkillGuard extracts environment mentions from a skill document, including URLs, versions, imports, API paths, env vars, Docker images, GitHub Actions, CLI flags, and config files.
- It labels each mention as operational or incidental. Only operational mentions become contracts to validate.
- A contract records the type, role, value, and evidence span. Validation matches these contracts against known drift events or live sources such as registries and URL checks.
- Failed contracts give the repair model a local edit target: the stale value, its location, and the new condition when available.
- The paper also releases DriftBench, an 880-pair benchmark with controlled drifts, real-world drifts, identity pairs, formatting hard negatives, and semantic hard negatives.

## Results
- DriftBench contains 174 controlled drift pairs, 107 real-world drift pairs, and 599 negative controls; the controlled split reports 99.6% adjudicated validity, and the real-world split reports 100% validity.
- Contract-free CI probes produce 40% false positives, while SkillGuard reports 0 false positives over 599 no-drift and hard-negative cases, with Wilson 95% CI [0%, 0.6%].
- In known-drift verification, all five tested backbones reach 100% precision. Qwen3.6-Plus has the best recall at 76% with 95% CI [62%, 88%].
- Other reported known-drift recall values are DeepSeek-R1 62%, DeepSeek-V3.2 57%, GLM-5.1 54%, and Qwen3-235B-A22B 24%, all at 100% precision.
- Baselines report Grep/diff at 30% recall, Dependabot-style scanning at 11% recall with 10% FPR, NL2Contract-style extraction at 45% recall with 0% FPR, and contract-free CI probes at 30% recall with 40% FPR.
- In a pre-registered live scan of 49 real skills, SkillGuard flags 14 skills, with 12 true positives, 2 false positives, 10 false negatives, and 25 true negatives, giving 86% conservative precision, 55% recall, and 7% FPR. Contract-guided one-round repair reaches 78% success, compared with 10% without localization, 60% with plain drift text, 80% for three-round Self-refine, and 78% with full drift specifications.

## Link
- [https://arxiv.org/abs/2605.10990v1](https://arxiv.org/abs/2605.10990v1)
