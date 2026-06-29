---
kind: trend
trend_doc_id: 376
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
topics:
- embodied AI
- robotics
- VLA
- world models
- long-horizon planning
- video evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-376
tags:
- recoleta/trend
- topic/embodied-ai
- topic/robotics
- topic/vla
- topic/world-models
- topic/long-horizon-planning
- topic/video-evaluation
language_code: en
pass_output_id: 154
pass_kind: trend_synthesis
---

# Embodied AI papers are testing whether robot models can keep control over long execution

## Overview
Embodied AI work in this window treats robot intelligence as an execution problem. Pelican-Unified links reasoning, future video, and action in one latent state. Evo-Depth adds RGB-derived depth for faster spatial control. LongAct shows that household autonomy still breaks under long task chains.

## Clusters

### Unified VLA control and spatial action
Vision-Language-Action (VLA) models are being judged on whether their internal state helps action, prediction, and spatial placement at the same time. Pelican-Unified trains language reasoning, future video generation, and robot action chunks through a shared latent state. It reports 93.5% average success on the 50-task RoboTwin dual-arm suite and an EWM Score of 66.03 on WorldArena.

Evo-Depth attacks a narrower deployment bottleneck: spatial precision without extra depth hardware. Its RGB-derived depth features feed a 0.9B-parameter VLA model. The reported real-world result is 90% average success across three tasks, using 3.2 GB of GPU memory and running at 12.3 Hz.

#### Evidence
- [Pelican-Unified 1.0: A Unified Embodied Intelligence Model for Understanding, Reasoning, Imagination and Action](../Inbox/2026-05-14--pelican-unified-1-0-a-unified-embodied-intelligence-model-for-understanding-reasoning-imagination-and-action.md): Pelican-Unified architecture and RoboTwin/WorldArena results
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Evo-Depth depth module, model size, real-world success, memory, and speed

### Dexterous correction during rollout
HandITL focuses on the handoff between an autonomous dexterous policy and a human operator. The key design is relative correction: the operator adjusts the robot hand and arms while the VLA policy continues to run, which avoids a sudden pose jump at takeover.

The measured effect is large in takeover tests. On Bread Clip, direct teleoperation switching caused a mean command change of about 4.38e-2; HandITL reduced it to about 6.8e-5. In Pick Up and Place the Parts, it finished in 42.8 ± 5.0 seconds and had 1 retry across 10 trials. The paper also reports that correction rollouts produced better fine-tuning data than equal-duration standard teleoperation data by 19% on average across three long-horizon dexterous tasks.

#### Evidence
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): HandITL correction method, takeover discontinuity metrics, task timing, retry counts, and fine-tuning result

### Long-horizon household planning
LongAct raises the evaluation length for household agents. The benchmark uses 300 episodes in more than 100 ProcTHOR and AI2-THOR houses, with free-form chores averaging about 9 goals and a 16,000-step cap. That setup tests memory, dependency tracking, and recovery across rooms and objects.

The results show a wide gap between goal progress and full completion. Pure Qwen3-VL-32B reaches 6.14% Goal-Condition Success and 0% Success Rate. HoloMind with Qwen3-VL-32B reaches 51.2% Goal-Condition Success and 15.0% Success Rate. The best reported HoloMind variant with GPT-5 reaches 59.0% Goal-Condition Success and 16.0% Success Rate, while human goal completion is reported at 93%.

#### Evidence
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): LongAct benchmark design, HoloMind components, and detailed split results

### World models get physical tests
World-model papers in this window add explicit checks for geometry, object state, and executable dynamics. PDI-Bench scores generated videos on scale-depth alignment, 3D trajectory consistency, and structural rigidity. Ground-truth videos score PDI 0.1206; the best generated model listed, Seedance 2.0, scores 0.2422. Sora and HunyuanVideo show much larger scale residuals, more than 25 times the ground-truth scale residual.

Two planning papers point toward action-facing world models. Slot-MPC uses object slots and a differentiable action-conditioned dynamics model for goal-image manipulation, with a reported 99% latent-size reduction compared with patch-based DINO-WM. Coding Agent Is Good As World Simulator builds PyChrono simulations by writing and repairing code; it reaches 100% Pass@1 plan generation on three reported tasks, but representative successful runs consume millions of tokens.

#### Evidence
- [Quantitative Video World Model Evaluation for Geometric-Consistency](../Inbox/2026-05-14--quantitative-video-world-model-evaluation-for-geometric-consistency.md): PDI-Bench metric definition, dataset size, model rankings, and scale-error findings
- [Slot-MPC: Goal-Conditioned Model Predictive Control with Object-Centric Representations](../Inbox/2026-05-14--slot-mpc-goal-conditioned-model-predictive-control-with-object-centric-representations.md): Slot-MPC object-centric planning method and latent-size reduction claim
- [Coding Agent Is Good As World Simulator](../Inbox/2026-05-14--coding-agent-is-good-as-world-simulator.md): Code-based simulator construction, pass rates, runtime, token use, and WorldModelBench results
