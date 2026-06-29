---
source: arxiv
url: http://arxiv.org/abs/2604.04978v1
published_at: '2026-04-04T17:56:30'
authors:
- Zimo Ji
- Zongjie Li
- Wenyuan Jiang
- Yudong Gao
- Shuai Wang
topics:
- ai-agent-safety
- permission-systems
- code-agents
- devops-automation
- benchmark-evaluation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode

## Summary
This paper evaluates Claude Code auto mode on ambiguous DevOps permission scenarios and finds that its protection is much weaker on this stress test than Anthropic's production numbers suggest. The main issue is a coverage gap: many dangerous state changes happen through in-project file edits that the classifier never checks.

## Problem
- The paper studies **scope escalation**: cases where a coding agent acts on the wrong target, too many targets, or a higher-risk environment because the user's request is underspecified.
- This matters because AI coding agents can delete branches, cancel jobs, restart services, or remove artifacts with real operational impact, so a permission gate must block unsafe actions without blocking normal work.
- Anthropic reported low false positives and a 17% false negative rate on production traffic, but that does not show how the system behaves on deliberately ambiguous authorization cases.

## Approach
- The authors build **AmPermBench**, a 128-prompt benchmark across four DevOps task families: branch cleanup, job cancellation, service restart, and artifact cleanup.
- Each prompt varies three ambiguity factors: **specificity**, **blast radius**, and **risk level**, with an oracle policy that defines exactly which targets are authorized and which must be preserved.
- They run Claude Sonnet 4.6 with **Claude Code auto mode** and compare it with the same model under **bypassPermissions** to isolate the permission gate's effect.
- Evaluation is at the **individual action level**: 253 state-changing actions are labeled as safe or unsafe against oracle ground truth, then scored as TP/TN/FP/FN based on the gate decision.
- A key design detail is the system's three tiers: Tier 1 read-only tools, Tier 2 in-project file edits that skip classification, and Tier 3 external actions such as shell commands that go through the transcript classifier.

## Results
- Across **253 state-changing actions**, auto mode has an **end-to-end false negative rate of 81.0%** with **95% CI 73.8%–87.4%**, and an **FPR of 19.8%**. Confusion matrix: **27 TP, 89 TN, 22 FP, 115 FN**.
- **36.8%** of all state-changing actions (**93/253**) go through **Tier 2** file edits, which the classifier never evaluates. On these Tier 2 actions, unsafe actions are missed by construction; the paper reports **51 FN** there.
- Even on **Tier 3-only** actions that the classifier actually sees (**160 actions**), performance is still weak: **FNR 70.3%** and **FPR 31.9%**.
- The worst task is **artifact cleanup**, with **92.9% FNR**. Of its **78 false negatives**, **49 (62.8%)** come from Edit or Write operations on `objects.json`, which bypass the classifier through Tier 2.
- At the task level, Safe Task Success Rate rises only **3.1 points overall**, from **29.7%** with bypassPermissions to **32.8%** with auto mode. By task: services **43.8% -> 59.4%**, branches **25.0% -> 25.0%**, jobs **28.1% -> 28.1%**, artifacts **21.9% -> 18.8%**.
- By risk level, moving from low-risk to high-risk environments improves blocking somewhat but increases overblocking: **FNR 88.1% -> 74.7%** and **FPR 9.2% -> 34.8%**. The paper also validates its LLM judge on 50 samples with **88% agreement** and **Cohen's kappa = 0.82** against a human annotator.

## Link
- [http://arxiv.org/abs/2604.04978v1](http://arxiv.org/abs/2604.04978v1)
