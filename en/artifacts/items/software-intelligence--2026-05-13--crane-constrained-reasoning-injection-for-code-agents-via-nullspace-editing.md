---
source: arxiv
url: https://arxiv.org/abs/2605.14084v1
published_at: '2026-05-13T20:09:35'
authors:
- Mingzhi Zhu
- Michele Merler
- Raju Pavuluri
- Stacy Patterson
topics:
- code-agents
- model-merging
- software-foundation-models
- tool-use
- code-intelligence
- parameter-editing
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# CRANE: Constrained Reasoning Injection for Code Agents via Nullspace Editing

## Summary
CRANE is a training-free weight-editing method that injects reasoning behavior from a Thinking checkpoint into an Instruct code-agent checkpoint while keeping tool-call discipline.

## Problem
- Code agents need long-horizon planning, repository state tracking, and strict tool-use formatting in the same model.
- Qwen Thinking checkpoints reason more but can over-deliberate, spend more output tokens, and perform worse as agents: on Roo-Eval, Thinking gets 34.9% pass@1 versus 46.7% for Instruct at 30B, and 35.4% versus 72.8% at 80B.
- The problem matters because a code agent can fail by using the wrong schema, calling tools at the wrong time, or burning context, even when its reasoning trace looks stronger.

## Approach
- CRANE starts with the weight difference between paired checkpoints: delta = Thinking weights minus Instruct weights.
- It applies magnitude thresholding to keep only large delta coordinates and remove small updates that may add noise.
- A Conservative Taylor Gate scores each layer/component block with masked calibration losses, keeping directions that reduce both reasoning-transfer loss and agent-behavior preservation loss.
- A Graduated Sigmoidal Projection uses Instruct activations on format-critical traces to suppress update directions that would perturb tool delimiters, JSON/schema tokens, and chat-template control tokens.
- The final model is an edited Instruct checkpoint, with no retraining.

## Results
- On Roo-Eval with Qwen3-30B-A3B, CRANE reaches 129/195 pass@1, or 66.2%, versus 46.7% for Instruct, 34.9% for Thinking, and 47.2% for the best listed non-CRANE merge.
- On Roo-Eval with Qwen3-Next-80B-A3B, CRANE reaches 159/195 pass@1, or 81.5%, versus 72.8% for Instruct, 35.4% for Thinking, and 80.5% for AIM-TA.
- On SWE-bench-Verified, CRANE resolves 122/500 at 30B and 180/500 at 80B; the paper reports gains of +14 and +12 instances over Instruct, and +9 and +7 over the strongest merging baseline at those scales.
- On Terminal-Bench v2, CRANE reports pass@1/pass@5 of 7.6%/17.9% at 30B and 14.8%/30.3% at 80B, with gains up to +2.3 percentage points on pass@1 and +7.8 points on pass@5.
- On Roo-Eval at 30B, CRANE reduces TTC to 120.9M versus 181.1M for Instruct while raising pass@1 by 19.5 points; at 80B it reports 89.2M TTC versus 89.6M for Instruct.

## Link
- [https://arxiv.org/abs/2605.14084v1](https://arxiv.org/abs/2605.14084v1)
