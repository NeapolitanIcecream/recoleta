---
source: arxiv
url: https://arxiv.org/abs/2605.12160v1
published_at: '2026-05-12T14:10:54'
authors:
- Joonha Park
- Jiseung Jeong
- Taesik Gong
topics:
- vision-language-action
- generalist-robot-policy
- streaming-instructions
- visual-grounding
- robot-latency
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Premover: Fast Vision-Language-Action Control by Acting Before Instructions Are Complete

## Summary
Premover lets a frozen VLA policy start useful work while a user is still typing or speaking an instruction. It adds a focus map and readiness gate so the robot can act early without the success collapse seen in naive early execution.

## Problem
- Standard VLA evaluation assumes the full instruction is available before control starts, so it ignores user input time.
- On LIBERO, instruction entry at 52.24 WPM accounts for an average 39% of total interaction time, with LIBERO-Spatial estimated at 17.69s of 31.05s.
- Acting too early can move toward the wrong object when the prefix has not identified the target.

## Approach
- The backbone is frozen π₀.₅; trainable parts are two 2-layer MLP projection heads and one scalar readiness threshold, under 1% of backbone parameters.
- The image and language heads map intermediate image-patch states and streaming-prefix token states into a shared normalized space.
- Patch-token cosine scores form a per-patch focus map, supervised with simulator target-object segmentation masks using class-balanced BCE.
- The focus map from step t reweights image tokens at step t+1 with floor scale α=0.2, so target patches get more weight without muting all context.
- A readiness score equals top-10 focus-map mean minus global mean; the policy executes once this score passes the learned threshold.

## Results
- On LIBERO, Premover cuts mean wall-clock time over all episodes from 34.0s to 29.4s, 86.4% of the full-prompt baseline, while success stays 95.1% versus 95.0% for full-prompt.
- Naive premoving on LIBERO gives 66.4% success and 34.5s mean wall-clock time, so early execution without the gate loses 28.6 percentage points of success versus full-prompt.
- LIBERO per-suite wall-clock time with Premover is 22.7s Spatial, 24.4s Object, 21.9s Goal, and 48.6s LIBERO-10, versus 31.0s, 30.7s, 23.8s, and 50.8s for full-prompt.
- On VLA-arena Level-1, Premover reduces all-episode wall-clock time from 85.4s to 76.6s, 89.7% of full-prompt, with mean success 30.9% versus 33.0% for full-prompt.
- VLA-arena success is weak across methods, including 0.0% on Long-horizon for full-prompt and Premover, so the main claimed gain is latency reduction with a small average success loss.

## Link
- [https://arxiv.org/abs/2605.12160v1](https://arxiv.org/abs/2605.12160v1)
