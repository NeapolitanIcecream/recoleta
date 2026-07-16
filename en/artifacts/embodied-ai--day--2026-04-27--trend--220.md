---
kind: trend
trend_doc_id: 220
granularity: day
period_start: '2026-04-27T00:00:00'
period_end: '2026-04-28T00:00:00'
topics:
- vision-language-action
- robot manipulation
- coarse-to-fine control
- robot deployment
- human demonstrations
- edge safety
run_id: materialize-outputs
aliases:
- recoleta-trend-220
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/coarse-to-fine-control
- topic/robot-deployment
- topic/human-demonstrations
- topic/edge-safety
language_code: en
pass_output_id: 116
pass_kind: trend_synthesis
---

# Robot VLA work is being judged by control latency, action structure, and data reuse

## Overview
The day’s strongest signal is practical robot execution under tight timing and data limits. Vision-Language-Action (VLA) work concentrates on action decomposition, efficient sampling, human-video priors, and edge safety. Libra-VLA, CF-VLA, and AsyncShield give the clearest evidence.

## Findings

### Coarse-to-fine action generation
Two manipulation papers treat action structure as a control problem. Libra-VLA splits prediction into discrete macro-direction intent and continuous fine control, then runs its heavier planner less often through an intent buffer. It reports 97.2% average success on LIBERO and 79.5% zero-shot success on LIBERO-Plus.

CF-VLA applies a similar coarse-then-fine idea to flow-based action sampling. It uses two function evaluations: one coarse action-aware start point and one local correction. The reported trade-off is concrete: 96.5 average LIBERO success at NFE=2, 75.4% lower action sampling latency, and 83.0 average success in real-robot experiments.

#### Sources
- [Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System](../Inbox/2026-04-27--libra-vla-achieving-learning-equilibrium-via-asynchronous-coarse-to-fine-dual-system.md): Libra-VLA summary, method split, LIBERO and LIBERO-Plus results.
- [CF-VLA: Efficient Coarse-to-Fine Action Generation for Vision-Language-Action Policies](../Inbox/2026-04-27--cf-vla-efficient-coarse-to-fine-action-generation-for-vision-language-action-policies.md): CF-VLA summary, two-stage sampling, latency and real-robot results.

### Data reuse for generalizable manipulation
The strongest data result comes from MoT-HRA. It builds HA-2.2M, a 2.2M-episode human manipulation dataset, then separates intent into a 3D trajectory expert, a MANO-style hand-motion expert, and a robot action expert. On SimplerEnv-WidowX, it reports 66.1% average success, ahead of ThinkACT, SpatialVLA, OpenVLA-OFT, RoboVLMs, and pi0 variants listed in the paper.

M²-VLA addresses generalization inside the model. It keeps the vision-language backbone frozen, selects useful layer features, and retrieves stored meta-skills to guide action prediction. The reported gains are clearest under instruction and object variation: 66.2% success on rephrased LIBERO Spatial instructions and 34.4% on a novel-object pick-and-place test, with smaller drops than OpenVLA and VLA-Adapter.

#### Sources
- [Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation](../Inbox/2026-04-27--learning-human-intention-priors-from-large-scale-human-demonstrations-for-robotic-manipulation.md): MoT-HRA dataset, factorized experts, and SimplerEnv-WidowX results.
- [$M^2$-VLA: Boosting Vision-Language Models for Generalizable Manipulation via Layer Mixture and Meta-Skills](../Inbox/2026-04-27--m-2-vla-boosting-vision-language-models-for-generalizable-manipulation-via-layer-mixture-and-meta-skills.md): M²-VLA frozen-backbone method and generalization results.

### On-robot latency and asynchronous safety
Deployment work is measuring the whole observe-infer-act loop. The cross-XPU VLA study profiles inference on RTX 4090, Jetson Thor, AGX Orin, Intel B60 Pro, and Ascend NPUs, then ranks hardware by cost, energy, and time. Its pi0 measurements show why peak speed is insufficient: RTX 4090 reaches 102.3 ms, Jetson Thor 246.0 ms, and AGX Orin 920.6 ms before compilation, with different energy costs.

AsyncShield handles another timing failure mode: stale cloud VLA waypoints. It realigns delayed waypoints with an SE(2) pose transform and uses a safety-constrained local policy with LiDAR input. Under mixed network degradation, it reports 76.7% success, while the no-temporal-alignment ablation falls to 36.7%.

#### Sources
- [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](../Inbox/2026-04-27--characterizing-vision-language-action-models-across-xpus-constraints-and-acceleration-for-on-robot-deployment.md): Cross-accelerator VLA profiling, CET ranking, latency and speedup results.
- [AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation](../Inbox/2026-04-27--asyncshield-a-plug-and-play-edge-adapter-for-asynchronous-cloud-based-vla-navigation.md): AsyncShield method and mixed-degradation results with ablations.
