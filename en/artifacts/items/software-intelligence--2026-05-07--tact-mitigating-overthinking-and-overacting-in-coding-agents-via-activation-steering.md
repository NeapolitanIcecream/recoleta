---
source: arxiv
url: https://arxiv.org/abs/2605.05980v1
published_at: '2026-05-07T10:24:27'
authors:
- Yuan Sui
- Yulin Chen
- Yibo Li
- Xue Jiang
- Yufei He
- Yihong Dong
- Xiaoxin He
- Tianyu Gao
- Bryan Hooi
topics:
- coding-agents
- activation-steering
- agent-drift
- code-intelligence
- software-engineering-benchmarks
- automated-debugging
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# TACT: Mitigating Overthinking and Overacting in Coding Agents via Activation Steering

## Summary
TACT steers coding agents away from two step-level failure modes: repeated reasoning over known facts and repeated tool use without using recent evidence. It claims higher solve rates on software-engineering benchmarks without fine-tuning or prompt changes.

## Problem
- Long coding-agent runs can drift over dozens or hundreds of steps, causing wasted reasoning, repeated searches, redundant file reads, and missed fixes.
- Final task success does not show whether a failed trajectory broke down through overthinking or overacting, so step-level diagnosis matters for reliable coding agents.
- These failures matter because they reduce resolve rate and increase steps, context use, and tool calls.

## Approach
- The paper labels each agent step as overthinking, overacting, or calibrated using an LLM judge with a rolling verified state of known facts, hypotheses, edits, test outcomes, and repeated actions.
- It extracts hidden states at the `</think>` token, the point where reasoning ends and action begins.
- It builds two mean-difference activation directions: overthinking vs. calibrated and overacting vs. calibrated.
- It orthogonalizes the overacting direction against the overthinking direction, then applies test-time residual-stream steering along both axes.
- The steering variants either cap out-of-band projections, apply a fixed additive shift, or apply a gated partial correction when an activation leaves the calibrated band.

## Results
- Hidden states for overthinking, overacting, and calibrated steps are linearly separable along the drift axes, with AUC about 0.9.
- Across SWE-bench Verified, Terminal-Bench 2.0, and CLAW-Eval, TACT raises average resolve rate by +5.8 percentage points on Qwen3.5-27B.
- On Gemma-4-26B-A4B-it, TACT raises average resolve rate by +4.8 percentage points across the same benchmark set.
- TACT cuts steps-to-resolve by up to 26 steps.
- The LLM judge reports recalls of 84% for overthinking, 82% for overacting, and 87% for calibrated against human consensus; Cohen's kappa against four references is 0.73 to 0.81.

## Link
- [https://arxiv.org/abs/2605.05980v1](https://arxiv.org/abs/2605.05980v1)
