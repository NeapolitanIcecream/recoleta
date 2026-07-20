---
source: arxiv
url: https://arxiv.org/abs/2607.15621v1
published_at: '2026-07-17T04:40:02'
authors:
- Yun Li
- Jiachen Gong
- Simon Thompson
- Ehsan Javanmardi
- Qunli Zhang
- Zifan Zeng
- Shiming Liu
- Peng Wang
- Zixuan Guo
- Manabu Tsukada
topics:
- vision-language-action
- robot-foundation-model
- embodied-foundation-model
- real-time-inference
- closed-loop-driving
- sim2real
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Think at 5 Hz, Act at 20 Hz: Asynchronous Fast-Slow Vision-Language-Action Inference for Closed-Loop Driving

## Summary
The paper presents an asynchronous fast-slow vision-language-action system for closed-loop driving: a frozen 7B backbone updates a cached scene representation slowly, while a 337M action expert predicts waypoints at every control tick. In CARLA, this removes stale-command replay and raises route completion from 37.0 to 94.0, although long-route safety remains weak.

## Problem
- Large vision-language backbones cannot recompute visual history within a vehicle's control budget, so LMDrive produces fresh decisions at 10 Hz and replays commands on intervening 20 Hz ticks.
- Acting on observations that are 50–100 ms old can cause route deviations, timeouts, and missed traffic events, making latency a closed-loop control problem rather than only an inference-speed problem.
- The study matters because it tests whether a language-conditioned driving agent can preserve scene reasoning while issuing fresh control on consumer hardware.

## Approach
- The frozen LLaMA-7B vision-language backbone processes instructions and visual history every four 20 Hz ticks, exposing its per-layer key-value cache as a persistent scene representation.
- A 337M-parameter transformer action expert cross-attends to that cache and the current camera frame at every tick, then predicts five waypoints in one forward pass.
- Randomized staleness training hides a randomly delayed portion of the backbone history, teaching the expert to combine stale context with current visual evidence and its previous prediction.
- Incremental cache updates keep per-tick model cost nearly independent of history length; the system runs on an RTX 3090 Ti with a reported 32.4 ms model cost per tick.

## Results
- On 32 LangAuto-Short routes in CARLA town05, route completion increased from 37.0 ± 0.4 for replayed-tick LMDrive at 10 Hz to 94.0 ± 2.6 for the proposed 20 Hz system; driving score increased from 28.8 ± 0.8 to 32.9 ± 0.7.
- The same expert at the baseline's 10 Hz cadence achieved 82.1 route completion, isolating per-tick freshness as the source of the further increase to 94.0; route deviations fell from 11.3 to 4.3 per kilometer and red-light violations from 10.4 to 6.9.
- Open-loop waypoint L1 error was 0.031 m with randomized staleness, versus 0.037 m for a no-staleness expert and 0.123 m for the frozen backbone action head.
- Zero-shot transfer from town05 to unseen towns produced 84.3% and 94.4% route completion in towns 01 and 02, compared with 40.5% and 30.7% for LMDrive.
- On eight long routes in unseen town03, the system completed 85.4% of the route but achieved only a 2.96 driving score because collisions and red-light violations reduced its penalty factor to 0.04; the authors therefore do not establish long-horizon safety or road readiness.

## Link
- [https://arxiv.org/abs/2607.15621v1](https://arxiv.org/abs/2607.15621v1)
