---
source: arxiv
url: https://arxiv.org/abs/2607.17937v1
published_at: '2026-07-20T13:34:53'
authors:
- Yue Xue
topics:
- code-intelligence
- software-foundation-models
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# How Agent Skills Fail under Long Contexts: A White-Box Study in Code Auditing

## Summary
This white-box study finds that long context can sharply reduce coding-agent reliability on a fixed code-auditing task, but the effect is task- and run-dependent. An explicit checklist improves completion more reliably than a generic self-check, while infrastructure failures create a separate source of missing data.

## Problem
- Agent Skills contain procedural requirements, but coding agents may omit or stop applying individual requirements during long tool-using trajectories.
- This matters because a nearly complete audit artifact can still fail when one mandatory field, preservation rule, or validation condition is missed.
- Final pass rates alone do not show whether a failure came from a lost requirement, editing drift, failed checking, or evaluator/runtime infrastructure.

## Approach
- The authors study a production-derived white-box code-audit workflow with a fixed task, starting artifact, tools, and frozen verifier containing 24 observable checks across four audit tasks.
- They compare Codex with gpt-5.4-mini in a 10,991-character clean context against 299,140-character relevant and irrelevant contexts, using 10 valid runs per condition.
- Saved instructions, artifacts, tool logs, and checker outputs support a four-class failure taxonomy: lost requirements, editing drift, failed checking, and non-agent failures.
- A mitigation experiment compares a generic instruction to validate all constraints with a detailed checklist that explicitly restates all 24 checks.
- Exploratory probes test other models, tasks, and coding-agent scaffolds, but these comparisons are not fully matched or inferentially powered.

## Results
- On the main task, clean context passes 8/10 runs, while both relevant-long and irrelevant-long contexts pass 3/10. The observed failure rate increases from 20% to 70%, a 50-percentage-point or 3.5-fold increase.
- The main contrasts are uncertain: two-sided Fisher exact tests give p=0.0698, below neither the prespecified alpha=0.05 threshold nor a definitive claim of a universal long-context effect.
- Requirement coverage remains high despite low task success: 237/240 checks pass in clean runs (98.8%), 221/240 in relevant-long runs (92.1%), and 225/240 in irrelevant-long runs (93.8%).
- Relevant and irrelevant long contexts have identical binary outcomes, 3/10 passes each, with Fisher p=1.0; the study finds no reliable evidence that same-domain material is more harmful than unrelated material of equal character length.
- The detailed external checklist passes 10/10 runs versus 5/10 for the generic self-check, with Fisher p=0.0325.
- A second task passes all clean and long-context runs, so the evidence supports a high-variance reliability loss for one model-task pair rather than a universal context-length threshold. In the extension, only 29 of 57 attempts produce scoreable outputs, separating infrastructure reliability from agent-task success.

## Link
- [https://arxiv.org/abs/2607.17937v1](https://arxiv.org/abs/2607.17937v1)
