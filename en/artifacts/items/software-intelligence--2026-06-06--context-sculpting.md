---
source: hn
url: https://perceptiontheory.bearblog.dev/context-sculpting/
published_at: '2026-06-06T23:20:01'
authors:
- perceptronblues
topics:
- agent-harnesses
- context-management
- software-agents
- code-intelligence
- multi-agent-systems
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Context Sculpting

## Summary
Context Sculpting tests a two-model agent harness where a stronger outer model can rewrite a weaker inner model's context between turns. The case study shows that active context rewriting works, but the runs also show high cost, latency, and control-policy risk.

## Problem
- Most chat and agent systems treat the context window as an append-only log. That can preserve stale files, failed paths, tool noise, and distractor evidence, which can waste tokens and steer long-running software agents poorly.
- The concrete question is whether one model can manage another model's working context by removing misleading state, compacting history, or steering the next step.
- This matters for code repair and corpus-grounded answers because the model's current context affects what it reads, edits, cites, verifies, and stops doing.

## Approach
- The prototype uses a Pi agent harness with an inner task agent and an outer control agent. The reported runs use `gpt-5.4-mini` as the inner model and `gpt-5.4` as the outer model.
- After each inner-agent turn, the outer agent reads the full inner context and chooses one action: `pass_through`, `rewrite_context`, `rollback`, or `terminate`.
- Demo 1 used two task types: a small file-backed task-manager CLI repair task and a local-corpus synthesis task with distractor documents. It ran 2 inner-only and 2 outer-harness runs per task, for 8 runs total.
- Demo 2 changed the outer prompt to an `intervention_targeted` profile, added noisier tasks, and weakened the inner model setting by using low thinking effort.

## Results
- Demo 1 completed 8 of 8 runs successfully, passed 8 of 8 verification checks, triggered 0 guardrails, and cost an estimated $0.7079.
- Demo 1 did not produce context rewriting. Across 4 harnessed runs, the outer agent made 16 calls: 12 `pass_through`, 4 `terminate`, 0 `rewrite_context`, and 0 `rollback`. The full harness cost 14x more than inner-only runs without improving pass rate.
- Demo 2 cost about $1.26 for 4 runs. Across 2 harnessed runs, the outer agent made 15 calls: 14 `rewrite_context`, 1 `terminate`, and 0 `rollback`, which demonstrates active context rewriting.
- In the noisy synthesis task, the outer agent used an early `inject` rewrite, later used a `compact` rewrite, and the inner agent wrote the final answer on the next turn. The excerpt does not report an accuracy delta against a baseline for this task.
- In the coding repair task, the control run passed in 7 turns, 42.7 seconds, and about $0.015. The harnessed run also passed, but used 12 turns, 566.9 seconds, about $1.06, 12 outer calls, and 12 rewrites, then hit the `maxInnerTurns` guardrail.
- The strongest claim is feasibility, not a benchmark breakthrough. The case study shows that prompt policy can change the outer agent from passive supervision to aggressive context editing, and that aggressive editing can make a successful run much more expensive.

## Link
- [https://perceptiontheory.bearblog.dev/context-sculpting/](https://perceptiontheory.bearblog.dev/context-sculpting/)
