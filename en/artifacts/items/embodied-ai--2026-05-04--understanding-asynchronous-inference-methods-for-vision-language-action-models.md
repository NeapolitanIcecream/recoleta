---
source: arxiv
url: https://arxiv.org/abs/2605.08168v1
published_at: '2026-05-04T18:01:15'
authors:
- Ayoub Agouzoul
topics:
- vision-language-action
- generalist-robot-policy
- asynchronous-inference
- robot-control-latency
- action-chunking
- libero-benchmark
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Understanding Asynchronous Inference Methods for Vision-Language-Action Models

## Summary
This paper finds that A2C2 is the strongest high-delay method for asynchronous VLA control, while TT-RTC has the lowest runtime cost when it works. The study is mainly a controlled benchmark of existing methods, with two unified codebases and matched evaluation settings.

## Problem
- VLA policies often predict action chunks, but inference takes enough time that the robot acts on an old observation by the time a chunk is ready.
- Synchronous execution avoids stale observations by pausing the robot, which lowers the control rate and can hurt fast manipulation or dynamic control.
- Prior methods for this delay problem were tested in separate codebases with different base policies, datasets, and protocols, so their trade-offs were hard to compare.

## Approach
- The paper compares four methods under shared implementations: IT-RTC, TT-RTC, VLASH, and A2C2.
- IT-RTC keeps the already-committed action prefix fixed and inpaints the rest of the action chunk during flow-matching inference.
- TT-RTC trains the policy with simulated delays, so it learns to condition on an action prefix and predict the remaining actions with no added inference cost.
- VLASH estimates the robot state at execution time by rolling the state forward, then conditions the policy on that future state.
- A2C2 runs a small correction model at every control step and adds a residual action to the stale base-policy action.

## Results
- On Kinetix with 10 environments and chunk size H=16, A2C2 stayed above 90% solve rate up to delay d=8, while the naive asynchronous baseline fell below 40%.
- On Kinetix with H=30 and delays up to d=15, A2C2 led overall; TT-RTC generalized well across d_max values of 4, 8, and 15; IT-RTC gave little gain over naive at high delay.
- On LIBERO with SmolVLA, 40 tasks, H=50, and delays d∈{0,1,2,4,8,15,20}, A2C2 led from d≥4 and reached about 58% success at d=20.
- At LIBERO d=20, the naive baseline was about 10-12%, IT-RTC about 20%, TT-RTC about 25% for d_max=8 and about 33% for d_max=4, while VLASH with d_max=8 or 16 stayed near 55-56%.
- LIBERO VLASH used ground-truth future states because the benchmark state and action dimensions do not match, so its high-delay results are an upper bound for a deployable version.
- On an RTX 3090 for LIBERO, naive SmolVLA inference took 405.2 ms per chunk, TT-RTC took 402.7 ms, IT-RTC took 469.7 ms, and A2C2 serial inference took 412.4 ms; the A2C2 residual head alone took 7.27 ms.

## Link
- [https://arxiv.org/abs/2605.08168v1](https://arxiv.org/abs/2605.08168v1)
