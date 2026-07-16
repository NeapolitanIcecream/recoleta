---
kind: trend
trend_doc_id: 536
granularity: day
period_start: '2026-06-04T00:00:00'
period_end: '2026-06-05T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- test-time compute
- affordance grounding
- policy evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-536
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/test-time-compute
- topic/affordance-grounding
- topic/policy-evaluation
language_code: en
pass_output_id: 256
pass_kind: trend_synthesis
---

# Robot policies are being scored by predicted futures and execution latency

## Overview
The day is dominated by robotics papers that treat Vision-Language-Action (VLA) policy quality as a closed-loop control problem. WLA, MPCoT, and PiL-World give the clearest evidence: future-state prediction, latent action selection, and imagined rollouts are tied directly to success rates and latency.

## Findings

### World models inside robot policies
Several papers use future-state prediction as a training signal or as part of action choice. WLA predicts a textual subtask, a compact physical transition, and an action chunk in one policy. Its world-modeling loss has a measurable effect: removing it lowers RoboTwin Clean success from 92.94% to 90.98% and LIBERO average success from 98.6% to 97.9%.

The same idea appears beyond tabletop manipulation. WorldFly couples future video latents with navigation actions for low-altitude UAV control. On its Urban Canyon Traversal benchmark, it reports 87% success on seen intersections and 31% on harder unseen intersections, beating OpenFly and Pi-0-UAV on the reported metrics. DexFuture uses predicted future hand-tool-object targets for bimanual tool use and runs at 60 Hz, avoiding slow online planning over high-dimensional hand actions.

#### Sources
- [World-Language-Action Model for Unified World Modeling, Language Reasoning, and Action Synthesis](../Inbox/2026-06-04--world-language-action-model-for-unified-world-modeling-language-reasoning-and-action-synthesis.md): WLA architecture, world-model ablation, LIBERO and RoboTwin results.
- [WorldFly: A World-Model-Based Vision-Language-Action Model for UAV Navigation](../Inbox/2026-06-04--worldfly-a-world-model-based-vision-language-action-model-for-uav-navigation.md): WorldFly future-view/action coupling and Urban Canyon Traversal results.
- [DexFuture: Hierarchical Future-State Visuomotor Targeting for Bimanual Dexterous Tool Use](../Inbox/2026-06-04--dexfuture-hierarchical-future-state-visuomotor-targeting-for-bimanual-dexterous-tool-use.md): DexFuture future-state targeting, success rates, and 60 Hz execution.

### Inference-time control budgets
The strongest control papers report compute as part of the result. MPCoT keeps OpenVLA-OFT’s 8-step action interface and adds latent multi-path refinement. Its best setting raises LIBERO Long success from 95.3% to 98.9%, while measured latency rises from 24 ms to 38 ms and no reasoning tokens are generated.

A second line cuts decoding cost. The one-step VLA paper shows that a high-noise-biased flow-matching schedule can make single-step action generation competitive with 10-step decoding. On LIBERO-Plus, all 18 comparable recipes place one-step decoding at or above 10-step decoding, with a mean margin of 5.4 success points. TempoVLA addresses execution speed at the policy level by conditioning one VLA policy on commanded speed, with similar LIBERO success across three speed-conditioning methods.

#### Sources
- [MPCoT: Reward-Guided Multi-Path Latent Reasoning for Test-Time Scalable Vision-Language-Action](../Inbox/2026-06-04--mpcot-reward-guided-multi-path-latent-reasoning-for-test-time-scalable-vision-language-action.md): MPCoT latent refinement, LIBERO/CALVIN gains, and latency numbers.
- [Let It Be Simple: One-Step Action Generation for Vision-Language-Action Models](../Inbox/2026-06-04--let-it-be-simple-one-step-action-generation-for-vision-language-action-models.md): One-step action generation method and LIBERO-family results.
- [TempoVLA: Learning Speed-Controllable Vision-Language-Action Policies](../Inbox/2026-06-04--tempovla-learning-speed-controllable-vision-language-action-policies.md): TempoVLA speed conditioning and reported LIBERO speed-control results.

### Spatial affordances as action inputs
AffordanceVLA makes contact cues explicit. It predicts the target object, a 2D interaction region, and 3D shape/layout cues before action generation. The paper does not provide numeric LIBERO or CALVIN tables in the available excerpt, but it does describe an automated pipeline that produces more than 100,000 affordance annotations.

DexFuture gives a more measured version of the same concern for dexterous tool use. It predicts sparse future targets for hand links, the tool, and the object, then lets a low-level policy track those targets. On OakInk2 bimanual tasks, it reports 59.69% average success, close to the privileged target baseline at 66.52%; the no-target policy is reported near 7% average success in the abstract.

#### Sources
- [AffordanceVLA: A Vision-Language-Action Model Empowering Action Generation through Affordance-Aware Understanding](../Inbox/2026-06-04--affordancevla-a-vision-language-action-model-empowering-action-generation-through-affordance-aware-understanding.md): AffordanceVLA object, contact-region, 3D shape cues, and annotation pipeline.
- [DexFuture: Hierarchical Future-State Visuomotor Targeting for Bimanual Dexterous Tool Use](../Inbox/2026-06-04--dexfuture-hierarchical-future-state-visuomotor-targeting-for-bimanual-dexterous-tool-use.md): DexFuture target representation and OakInk2 success comparisons.

### Closed-loop evaluation and recovery data
Evaluation work is using world models to reduce reliance on full robot rollouts. PiL-World alternates a frozen VLA policy with a world model, feeding generated terminal observations back into the policy. On three real dual-arm tasks, it cuts the average real-imagined success-rate gap from 63.2% with Ctrl-World to 12.0% and reports 0.94 Pearson correlation across task-checkpoint settings.

The logistics data-flywheel paper uses an action-conditioned world model for recovery data. WM-DAgger generates and filters synthetic recovery trajectories, then trains imitation policies with real demonstrations. In Soft Bag Pushing, 5 real demonstrations plus 1,500 generated trajectories reach 93.3% success, compared with 26.7% for behavioral cloning.

#### Sources
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): PiL-World closed-loop imagined evaluation and real-imagined gap results.
- [Towards a Data Flywheel for Embodied Intelligence in Logistics](../Inbox/2026-06-04--towards-a-data-flywheel-for-embodied-intelligence-in-logistics.md): WM-DAgger synthetic recovery data and logistics manipulation success rates.
