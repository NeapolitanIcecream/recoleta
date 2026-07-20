---
kind: trend
trend_doc_id: 916
granularity: week
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-20T00:00:00'
topics:
- robot learning
- vision-language-action models
- closed-loop control
- predictive supervision
- deployment efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-916
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/closed-loop-control
- topic/predictive-supervision
- topic/deployment-efficiency
language_code: en
pass_output_id: 368
pass_kind: trend_synthesis
---

# Prediction enters the control loop, while execution remains the hard test

## Overview
The execution focus seen across recent weeks continues, but the evidence is now more integrated. Vision-language-action (VLA) policies use predicted futures, long histories, and asynchronous components while containing runtime cost. RoboTTT and Jetson-PI show practical gains from this design. IMBench tempers the signal: recognizing physical constraints still rarely translates into successful closed-loop action. Results span simulation and limited robot trials, so broad deployment readiness remains unproven.

## Findings

### Predictive and long-context control
Prediction is becoming part of the policy state rather than a separate planning output. RoboTTT compresses up to 8K timesteps into fast weights without latency growing with context length. It reports 79% average completion on three bimanual assembly tasks, versus 42% for its single-step baseline. FoMoVLA instead predicts a future feature state and sparse point trajectories; it reaches 97.6% on LIBERO-Long with 9.4 ms median overhead. Lumo-2 provides a third formulation by aligning latent world dynamics with action, vision, and language, though its available evidence does not include numerical task margins.

#### Sources
- [RoboTTT: Context Scaling for Robot Policies](../Inbox/2026-07-16--robottt-context-scaling-for-robot-policies.md): Reports the 8K-context mechanism, real-robot completion results, and fixed-trial limitations.
- [FoMoVLA: Bridging Visual Foresight and Motion Guidance for Vision-Language-Action Models](../Inbox/2026-07-16--fomovla-bridging-visual-foresight-and-motion-guidance-for-vision-language-action-models.md): Reports future-feature and point-trajectory supervision, LIBERO-Long success, and inference overhead.
- [Towards Predictive, Aligned, and Scalable Robot Learning](../Inbox/2026-07-13--towards-predictive-aligned-and-scalable-robot-learning.md): Describes latent future-dynamics prediction and notes the absence of numerical benchmark margins.

### Latency is treated as a control error
Deployment work increasingly models stale observations and discontinuous actions as policy failures, not just systems overhead. Jetson-PI predicts the future representation corresponding to already committed actions and reaches 6.06 Hz on Jetson Orin, versus 0.70 Hz for naive π₀.₅. ChunkFlow trains overlapping action chunks to agree at their seams and reports 93.4% success on LIBERO-Long with 4.43 ms average reasoning latency. In driving, a slow 7B scene model paired with a fast action expert raises short-route completion from 37.0% to 94.0% by issuing fresh control every tick. Its long-route driving score remains only 2.96, showing that higher control frequency does not establish safety.

#### Sources
- [Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference](../Inbox/2026-07-14--jetson-pi-towards-onboard-real-time-robot-control-via-foresight-aligned-asynchronous-inference.md): Provides the foresight-aligned asynchronous design and Jetson Orin frequency and latency measurements.
- [ChunkFlow: Towards Continuity-Consistent Chunked Policy Learning](../Inbox/2026-07-14--chunkflow-towards-continuity-consistent-chunked-policy-learning.md): Provides seam-aware training, LIBERO-Long success, continuity metrics, and reasoning latency.
- [Think at 5 Hz, Act at 20 Hz: Asynchronous Fast-Slow Vision-Language-Action Inference for Closed-Loop Driving](../Inbox/2026-07-17--think-at-5-hz-act-at-20-hz-asynchronous-fast-slow-vision-language-action-inference-for-closed-loop-driving.md): Reports the fast-slow architecture, route-completion gain, and poor long-route safety score.

### Generalization is measured through executable behavior
Two training studies target shortcuts that remain hidden by strong in-distribution scores. Semantic anchoring preserves pretrained task structure during robot fine-tuning; on a bimanual robot, it raises out-of-distribution success from 49.5% to 71.0%. AC-VLA decomposes demonstrations into reusable sub-tasks and suppresses wrist-view shortcuts during placement, improving real-world out-of-distribution success from 35.0% to 82.5%. IMBench shows why these interventions matter: leading vision-language models recognize constraints about 74% of the time, yet closed-loop GPT-5.5 succeeds on only 11.3% of tasks with vision-only input. The benchmark is simulation-only, so it establishes an evaluation gap rather than a universal capability ceiling.

#### Sources
- [Semantic Anchoring for Robotic Action Representations](../Inbox/2026-07-15--semantic-anchoring-for-robotic-action-representations.md): Links semantic erosion to out-of-distribution performance and reports real-robot gains from anchoring.
- [AC-VLA: Robust Out-of-Distribution Action Execution via Compositional Learning](../Inbox/2026-07-17--ac-vla-robust-out-of-distribution-action-execution-via-compositional-learning.md): Reports compositional supervision, state-conditioned masking, and real-world out-of-distribution results.
- [IMBench: A Benchmark for Intuitive Robotic Manipulation](../Inbox/2026-07-17--imbench-a-benchmark-for-intuitive-robotic-manipulation.md): Quantifies the gap between constraint recognition and closed-loop execution and states the simulation limitation.
