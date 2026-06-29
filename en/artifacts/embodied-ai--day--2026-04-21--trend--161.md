---
kind: trend
trend_doc_id: 161
granularity: day
period_start: '2026-04-21T00:00:00'
period_end: '2026-04-22T00:00:00'
topics:
- robotics
- vision-language-action
- world-models
- humanoids
- training-data
run_id: materialize-outputs
aliases:
- recoleta-trend-161
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/humanoids
- topic/training-data
language_code: en
pass_output_id: 100
pass_kind: trend_synthesis
---

# Robotics papers judge models by how well training signals survive contact with execution

## Overview
This day is strongest on one point: robotics papers are tightening the link between pretraining, prediction, and real execution. EmbodiedMidtrain shows that VLA performance improves when the upstream data look more like robot experience. Mask World Model and RoboWM-Bench make the same demand on world models from opposite sides: preserve task-relevant structure, then judge success by executable behavior.

## Clusters

### Data curation for VLA pretraining
EmbodiedMidtrain makes data selection a first-class part of VLA training. The paper measures a real mismatch between generic vision-language model data and robot trajectories, then mid-trains on samples scored as closer to robot data. The gains are large for small backbones: InternVL3.5-1B rises from 36.5 to 56.3 success on SimplerEnv-Bridge and from 39.0 to 54.2 on Libero-10. Qwen3VL-2B also improves across Calvin, SimplerEnv-Bridge, and Libero-10. This gives the day a concrete message: better robot policies are coming from better pre-action data alignment, not only larger action heads or more robot fine-tuning.

#### Evidence
- [EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training](../Inbox/2026-04-21--embodiedmidtrain-bridging-the-gap-between-vision-language-models-and-vision-language-action-models-via-mid-training.md): Summary and benchmark gains for EmbodiedMidtrain across Calvin, SimplerEnv-Bridge, and Libero-10.

### Execution-grounded world models
World-model papers in this period care more about executable structure than photorealistic prediction. Mask World Model trains on future semantic masks, which keeps object layout and contact cues while dropping texture noise; it reports 98.3% average success on LIBERO and 68.3% on RLBench, ahead of several strong baselines. RoboWM-Bench tests the opposite side of the story: generated videos may look plausible yet still fail when converted to actions. Its robot evaluations stay low even for strong generators, and step-level analysis shows many systems can reach contact but fail to complete the task sequence. Taken together, the signal is clear: a useful world model for robotics is judged by execution fidelity.

#### Evidence
- [Mask World Model: Predicting What Matters for Robust Robot Policy Learning](../Inbox/2026-04-21--mask-world-model-predicting-what-matters-for-robust-robot-policy-learning.md): Summary and results for mask-based world modeling, including LIBERO and RLBench success rates.
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): Summary and results showing divergence between visual realism and executable manipulation behavior.

### Shared training interfaces across embodiments and stages
Two papers widen the training scope around robot control. UniT introduces a shared discrete action language for human and humanoid behavior, with policy and world-model training built on the same tokens. The paper uses 27,419 human trajectories, few-shot robot data, and real-humanoid tests, though the excerpt does not expose the main margins. VLA Foundry tackles a different bottleneck: it puts language pretraining, vision-language training, and action training in one stack, with support for distributed runs up to 128 GPUs and open model releases. The common theme is infrastructure for transfer. One line tries to reuse human motion across bodies; the other makes full-pipeline VLA experiments easier to reproduce and compare.

#### Evidence
- [UniT: Toward a Unified Physical Language for Human-to-Humanoid Policy Learning and World Modeling](../Inbox/2026-04-21--unit-toward-a-unified-physical-language-for-human-to-humanoid-policy-learning-and-world-modeling.md): Summary describes UniT's shared tokenization, human-to-humanoid transfer setting, and evaluation scope.
- [VLA Foundry: A Unified Framework for Training Vision-Language-Action Models](../Inbox/2026-04-21--vla-foundry-a-unified-framework-for-training-vision-language-action-models.md): Summary describes the unified LLM-VLM-VLA training stack and reported open training pipeline.
