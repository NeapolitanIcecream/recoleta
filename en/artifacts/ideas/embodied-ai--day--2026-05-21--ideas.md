---
kind: ideas
granularity: day
period_start: '2026-05-21T00:00:00'
period_end: '2026-05-22T00:00:00'
run_id: bfdb3bae-77e6-44b1-88f2-6274001cf2f7
status: succeeded
topics:
- vision-language-action
- robot manipulation
- spatial grounding
- runtime verification
- world models
- autonomous driving
tags:
- recoleta/ideas
- topic/vision-language-action
- topic/robot-manipulation
- topic/spatial-grounding
- topic/runtime-verification
- topic/world-models
- topic/autonomous-driving
language_code: en
pass_output_id: 191
pass_kind: trend_ideas
upstream_pass_output_id: 190
upstream_pass_kind: trend_synthesis
---

# Robot control loop evaluation

## Summary
VLA deployment work now has enough concrete evidence to move evaluation closer to the robot control loop. The clearest changes are an action-chunk verifier before execution, explicit target tokens for dense manipulation scenes, and reachability-based terminal costs for latent world-model planning.

## Action-chunk verification before robot execution
Robot teams testing VLA policies should add a pre-execution verifier that scores each proposed action chunk for validity and expected value before the robot moves. The practical target is low-quality chunks under distribution shift: collisions, dropped objects, kinematic violations, and long-horizon failures that appear after a policy has already committed to a bad segment.

Pre-VLA gives a concrete design: encode the instruction, visual observation, proprioceptive state, and candidate action chunk, then use a small dual head to predict binary safety confidence and critic-derived advantage. Its runtime scheduler filters rejected chunks, resamples within a compute budget, and falls back to the highest predicted advantage. On LIBERO, it reports 0.9542 validity accuracy, a 0.0200 false pass rate for invalid actions, and a closed-loop gain for RynnVLA-002 from 30.79% to 37.62%, with 183.9 ms average verification time per chunk.

The cheap adoption test is to run the verifier offline on failed rollout logs, then replay the same task set with filtering enabled. The key measurements are false passes on invalid chunks, closed-loop success, rejected-chunk rate, and added wall-clock time. CrossVLA’s latency breakdown also points to the right optimization target for flow-matching policies: π₀.₅ spends about 220 ms of a 280 ms sample_actions call in the denoising loop, so verifier cost has to be judged against action generation and resampling cost, not only prefix computation.

### Evidence
- [Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts](../Inbox/2026-05-21--pre-vla-preemptive-runtime-verification-for-reliable-vision-language-action-and-world-model-rollouts.md): Pre-VLA provides the verifier design, LIBERO validity metrics, closed-loop success gain, and per-chunk verification latency.
- [CrossVLA: Cross-Paradigm Post-Training and Inference Optimization for Vision-Language-Action Models](../Inbox/2026-05-21--crossvla-cross-paradigm-post-training-and-inference-optimization-for-vision-language-action-models.md): CrossVLA provides the flow-matching latency breakdown and evidence that prefix caching is a weak speed target for π₀.₅.

## Visual target tokens for dense pick-and-place and pointing instructions
Manipulation cells with dense objects should expose an intermediate target representation before action decoding: points, boxes, masks, memory primitives, or gesture tokens tied to the intended object. This is most relevant when operators say “pick this up” or when many visually similar objects sit close together, since a text-only policy can choose the wrong target before motor control begins.

AVP is the clearest build pattern. The VLM predicts visual primitives for the next execution stage, projects those primitives into token space, and conditions a flow-matching action expert. The labels come from end-effector kinematics through camera calibration, so teams can generate supervision from robot traces. On Chinese chess manipulation, AVP reports 90.28% average success versus 62.67% for π₀.₅, and runs at 0.27 seconds per instruction without an external detector, segmenter, or online VLM API.

GesVLA covers the human-interface side. It extracts wrist and index-finger keypoints with MediaPipe, turns them into latent gesture tokens, and trains intent grounding with semi-synthetic pointing data rendered on real RGB-D scenes. Across three real-robot tasks, it reports 83.3% average success versus 31.7% for a text-only VLA. A practical pilot would add target-token logging to a pick-and-place workcell, then compare wrong-object grasps, placement errors, and instruction latency on cluttered scenes with at least several similar objects.

### Evidence
- [Action with Visual Primitives](../Inbox/2026-05-21--action-with-visual-primitives.md): AVP provides the visual-primitive interface, calibration-derived labels, latency, and real-robot pick-and-place gains.
- [GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations](../Inbox/2026-05-21--gesvla-gesture-aware-vision-language-action-model-embedded-representations.md): GesVLA provides the gesture-token design, semi-synthetic pointing data method, and real-robot gains over text-only VLA.

## Reachability-ranked terminal costs for latent world-model planners
Teams using latent world-model MPC should audit how the planner ranks candidate endpoints, then train a small reachability metric when raw latent distance misorders feasible routes. The failure mode is concrete: the latent state can contain the needed control variable while Euclidean terminal cost gives it too little weight.

TRM tests this directly. It trains a pairwise head on encoded state pairs from logged trajectories, using same-episode temporal separation as a reachability proxy. At planning time, the encoder, dynamics model, CEM sampler, optimizer, and evaluation manifest stay fixed; only the terminal cost changes. On hard TwoRoom with LeWM, raw latent MSE reaches 7.0% mean success while full-horizon TRM reaches 97.0%. With PLDM, the same recipe improves mean success from 32.7% to 84.0%.

The near pilot is an offline candidate-ranking audit. For each planning call, score the same sampled candidates with raw latent MSE and with a learned reachability head, then compare geodesic ranking or task-state progress for the selected endpoint. TRM’s same-candidate audit reports geodesic Spearman rising from 0.018 to 0.729 and the oracle-best candidate moving from rank percentile 31.71 to 3.86, which gives a concrete diagnostic before changing the closed-loop controller.

### Evidence
- [Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics](../Inbox/2026-05-21--beyond-euclidean-proximity-repairing-latent-world-models-with-horizon-matched-trajectory-reachability-metrics.md): TRM provides the reachability metric design, fixed-planner intervention, TwoRoom success gains, and same-candidate ranking audit.
