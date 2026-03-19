---
source: arxiv
url: http://arxiv.org/abs/2603.14373v1
published_at: '2026-03-15T13:25:52'
authors:
- Wu Ji
topics:
- ai-agents
- prompt-engineering
- debugging
- code-intelligence
- trust-framing
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Trust Over Fear: How Motivation Framing in System Prompts Affects AI Agent Debugging Depth

## Summary
This paper studies whether the “motivational framing” in system prompts changes the debugging depth of AI coding agents. The conclusion is: trust-based NoPUA prompts lead agents to investigate more deeply and discover more hidden issues, while the popular fear-based PUA prompts are not significantly better than a normal baseline.

## Problem
- The paper aims to answer whether the **incentive style in system prompts** (no framing, trust-based, fear-based) affects the depth of AI agent debugging investigations, rather than merely changing the tone of the output.
- This matters because AI coding agents are increasingly entering real software development workflows, and many practitioners are using threatening “PUA prompting” to pursue greater rigor, but its actual effectiveness lacks empirical validation.
- If different prompts systematically change the agent’s exploration, stopping, and self-correction strategies, that directly affects code quality, defect discovery capability, and the reliability of automated software production.

## Approach
- The authors conducted two controlled studies using **the same Claude Sonnet 4 model**, the same tool access, and the same real codebase/debugging tasks, changing only the motivational framing in the system prompt.
- Study 1: across 9 debugging/review scenarios from a real production AI pipeline, they compare a **standard baseline** with **NoPUA trust-based prompting**; they focus on metrics such as hidden issues, investigation steps, self-correction, and whether the agent went beyond the task scope.
- Study 2: on the same 9 scenarios, they performed **5 independent repeated runs**, adding a third condition, **PUA fear-based prompting**, for a total of 135 data points, to test reproducibility and directly compare trust vs. fear.
- The core mechanism of NoPUA, in the simplest terms, is: **treat the agent as a trusted collaborator rather than an employee who might be replaced**, while also asking it to exhaust options, verify hypotheses, and dig deeply to the root cause; the authors observe that this shifts strategy from “broad but shallow surface scanning” to “fewer but deeper root-cause investigation.”

## Results
- **Study 1 (9 scenarios)**: NoPUA actually found fewer total issues, **33 vs 39 (-15%)**, but discovered **more hidden issues: 51 vs 32 (+59%)**; investigation steps were **42 vs 23 (+83%)**; going beyond the task scope was **9/9 vs 2/9 (100% vs 22%)**; self-corrections were **6 vs 0**; root-cause documentation was **9/9 vs 0/9**.
- The key differences in Study 1 are statistically significant: both hidden issues and investigation steps are **Wilcoxon W=45.0, p=0.002**; effect sizes are very large, at **Cohen’s d=2.28** and **3.51**, respectively.
- **Study 2 (5 independent runs, 135 data points)**: relative to baseline, NoPUA had investigation steps of **48.0±11.8 vs 27.6±9.5 (+74%)**, hidden issues of **48.2±3.4 vs 38.6±4.9 (+25%)**, and total issues of **83.0±6.5 vs 69.0±6.8 (+20%)**.
- In Study 2, NoPUA significantly outperformed baseline: overall three-group difference for investigation steps was **Kruskal–Wallis H=9.57, p=0.008**; hidden issues were **Mann–Whitney U=24.0, p=0.016, d=2.26**; total issues were **U=24.0, p=0.016, d=2.10**.
- **PUA fear-based prompting showed no significant gains**: relative to baseline, investigation steps were only **+12%**, hidden issues only **+10%**, and both were **not significant** (e.g. steps **W=4.0, p=1.000**; hidden **W=3.0, p=0.313**; summarized in the paper as all p>0.3).
- The paper’s central breakthrough claim is that **trust rather than fear** shifts AI debugging agents from breadth-first surface scanning to depth-first investigation, thereby improving hidden bug discovery and root-cause analysis; the popular fear-based PUA prompting is basically no better than using no method at all.

## Link
- [http://arxiv.org/abs/2603.14373v1](http://arxiv.org/abs/2603.14373v1)
