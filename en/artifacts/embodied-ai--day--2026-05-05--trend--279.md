---
kind: trend
trend_doc_id: 279
granularity: day
period_start: '2026-05-05T00:00:00'
period_end: '2026-05-06T00:00:00'
topics:
- robotics
- VLA
- world models
- spatial reasoning
- benchmarks
- multimodal models
run_id: materialize-outputs
aliases:
- recoleta-trend-279
tags:
- recoleta/trend
- topic/robotics
- topic/vla
- topic/world-models
- topic/spatial-reasoning
- topic/benchmarks
- topic/multimodal-models
language_code: en
pass_output_id: 132
pass_kind: trend_synthesis
---

# Robot policies and world models are being judged by memory, contact, and action fidelity

## Overview
The day’s clearest signal is evaluation pressure on embodied AI. After several days of Vision-Language-Action (VLA) deployment work, the current papers make success depend on memory, contact sensing, action-conditioned prediction, and spatial consistency. RLDX-1, RoboAlign-R1, and iWorld-Bench give the strongest evidence.

## Findings

### Dexterous VLA policies
RLDX-1 treats dexterous manipulation as a multi-signal control problem. The policy adds video motion, a small memory store, and tactile or torque inputs to a Qwen3-VL-based VLA. Its Multi-Stream Action Transformer keeps cognition, proprioception, and physics streams separate before cross-stream attention combines them for action prediction.

The reported gains are largest on tasks where current-image policies struggle. RLDX-1 reports 86.8% success on ALLEX humanoid tasks, while π₀.₅ and GR00T N1.6 are around 40%. On ALLEX Object-in-Box Selection, a memory-heavy task, it reports 91.7% success while the two baselines are in the 30% range. The report also ties deployment to latency: inference optimization cuts per-step latency on an RTX 5090 from 71.2 ms to 43.7 ms.

#### Sources
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): Summary details RLDX-1 architecture, training stages, success rates, memory task results, and latency reduction.

### Robot video world models
RoboAlign-R1 makes robot video prediction answer to task-level behavior, not only pixel loss. It fine-tunes an 8B multimodal judge, distills it into a 98M reward model, and uses that reward for post-training. The judge scores instruction following, manipulation success, action-outcome consistency, temporal consistency, contact realism, and physics adherence.

The paper reports a RobotWorldBench score of 8.52±0.15, compared with 7.74±0.62 for iVideoGPT. Its Sliding Window Re-encoding method refreshes rollout context during long predictions and reports better SSIM, PSNR, LPIPS, and ROI-LPIPS with about 1% added latency. The practical point is clear: long-horizon robot video models need both behavioral rewards and rollout maintenance.

#### Sources
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): Summary gives the distilled reward setup, six judge dimensions, benchmark results, and sliding-window rollout metrics.

### Interactive world-model benchmarks
iWorld-Bench targets a measurement gap for interactive world models: whether generated futures follow actions and preserve memory. It standardizes action inputs across text commands, one-hot controls, and camera parameters, allowing models with different control formats to face comparable tasks.

The benchmark is substantial in coverage. It contains 330,000 video clips, selects 2,100 evaluation videos, and defines 4,900 test tasks across action-control difficulty, memory, and camera following. Its data spans four viewpoints, nine outdoor weather types, five indoor lighting types, and 18 simulator environments. The supplied text does not give a model leaderboard, so the grounded contribution is the benchmark scale and action mapping.

#### Sources
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): Summary provides dataset scale, task counts, action standardization, coverage, and the limitation on missing leaderboard values.

### Spatial reasoning for unified visual models
JoyAI-Image connects image understanding, generation, and editing around spatial supervision. The system uses Qwen3-VL-8B-Instruct for multimodal understanding and instruction parsing, then conditions a 16B diffusion transformer for generation and editing. Its OpenSpatial data engine builds spatial QA and editing data from 3D boxes, masks, visibility checks, and multi-view consistency checks.

The reported result is strongest on spatial understanding. JoyAI-Image-Und reaches a 64.4 average across nine spatial benchmarks, up 5.3 points over Qwen3-VL-8B-Instruct and matching Gemini-2.5-Pro in the supplied summary. General benchmark scores stay close to the base model, which matters because the added spatial training does not erase broad visual skills in the reported tests.

#### Sources
- [Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation](../Inbox/2026-05-05--awaking-spatial-intelligence-in-unified-multimodal-understanding-and-generation.md): Summary gives JoyAI-Image architecture, OpenSpatial data construction, training mix, and spatial benchmark results.
