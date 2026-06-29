---
source: arxiv
url: https://arxiv.org/abs/2605.13357v1
published_at: '2026-05-13T11:14:59'
authors:
- Hailin Zhong
- Shengxin Zhu
topics:
- software-agents
- code-intelligence
- agent-evaluation
- runtime-systems
- software-verification
- human-ai-interaction
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents

## Summary
AI Harness Engineering treats autonomous coding performance as a property of the model, runtime harness, and software environment together. The paper defines harness components and an evaluation protocol for making agent software work auditable.

## Problem
- Software agents often fail on full repository tasks even when they can write plausible local patches; failures include wrong file selection, weak testing, bad failure diagnosis, lost task state, and premature success claims.
- The problem matters because human developers currently supply missing runtime support: repository context, tool choices, feedback interpretation, verification, permission control, and cleanup.
- Standard pass/fail evaluation misses whether an agent actually verified the change, preserved prior behavior, or needed hidden human help.

## Approach
- The core mechanism is a runtime harness between the foundation model and the repository. It controls what the agent can see, what tools it can use, how it records state, and how it proves completion.
- The paper defines 11 harness responsibilities: task specification, context selection, tool access, project memory, task state, observability, failure attribution, verification, permissions, entropy auditing, and intervention recording.
- It proposes a 4-level ladder, H0 to H3, that adds runtime support in stages: minimal repository access, tool support, context and memory support, then observability and verification support.
- It defines a trace-based episode package with 8 trace classes: action, tool, context, verification, failure attribution, intervention, entropy, and outcome.
- Evaluation focuses on the full model-harness-environment system, with human intervention treated as a measurable signal through missing-harness human intervention rate, M-HIR.

## Results
- No task-success rate, pass@k score, benchmark win rate, or large-scale quantitative evaluation is reported in the excerpt.
- The paper claims a controlled validation task produced different episode evidence across the 4 harness levels, with higher levels producing richer audit records than lower levels.
- H0 produces mainly a final patch, while H3 adds reproduction logs, failure attributions, deterministic requirement checks, and structured verification reports.
- The method supplies 11 named runtime responsibilities and maps each one to a failure mode and an evidence artifact.
- The evaluation protocol records 8 evidence types per episode and classifies failures into 8 types: context, tool, feedback, verify, recovery, entropy, model, and unknown.

## Link
- [https://arxiv.org/abs/2605.13357v1](https://arxiv.org/abs/2605.13357v1)
