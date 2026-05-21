---
kind: trend
trend_doc_id: 318
granularity: day
period_start: '2026-05-09T00:00:00'
period_end: '2026-05-10T00:00:00'
topics:
- Vision-Language-Action
- robot manipulation
- long-horizon memory
- fine-tuning retention
- inference-time action selection
- world models
- robot security
- model ownership
- hardware agents
run_id: materialize-outputs
aliases:
- recoleta-trend-318
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/long-horizon-memory
- topic/fine-tuning-retention
- topic/inference-time-action-selection
- topic/world-models
- topic/robot-security
- topic/model-ownership
- topic/hardware-agents
language_code: en
pass_output_id: 140
pass_kind: trend_synthesis
---

# Robot VLA reliability is being tested at memory, action, and release points

## Overview
The day’s robotics work treats Vision-Language-Action (VLA) models as deployable control systems. ECHO extends long-horizon memory, KeyStone improves stochastic action choice at inference, and ATAAT shows that visual backdoors can survive tuning. The common test is whether robot policies keep useful behavior under longer tasks, new data, uncertain samples, and released-model risk.

## Clusters

### VLA memory and skill retention
ECHO and ConSFT focus on a basic deployment problem: a robot policy must remember useful experience and keep old skills after task adaptation. ECHO stores successful subgoal segments in a hierarchical hyperbolic memory and retrieves them during control. On LIBERO-Long, it reports 93.5% success against 80.7% for vanilla π0, with cross-suite generalization at 89.31% using no LIBERO-Long target memories.

ConSFT attacks forgetting during supervised fine-tuning. It down-weights high-loss transitions through a stop-gradient confidence weight, reducing large parameter updates on samples the model handles poorly. On LIBERO with π0, it keeps target success at 0.90 and raises average prior-task retention to 0.34, compared with 0.09 for standard supervised fine-tuning.

#### Evidence
- [ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models](../Inbox/2026-05-09--echo-continuous-hierarchical-memory-for-vision-language-action-models.md): ECHO summary, method, LIBERO-Long results, and cross-suite generalization.
- [Preserving Foundational Capabilities in Flow-Matching VLAs through Conservative SFT](../Inbox/2026-05-09--preserving-foundational-capabilities-in-flow-matching-vlas-through-conservative-sft.md): ConSFT summary, loss design, and retention results across VLA policies.

### Test-time action choice and low-cost planning
Two papers reduce control cost without retraining the full robot policy. KeyStone samples several diffusion or flow-matching action chunks, clusters them in action space, and executes the medoid of the largest cluster. On SimplerEnv-WidowX with GR00T N1.6, success increases to 63.3% from 50.0% at K=4. On LIBERO with SmolVLA, it reaches 57.2% from 50.4% at K=16.

GC-IDM takes a related efficiency stance for world-model control. It freezes a pretrained LeWorldModel and trains a 1.5M-parameter goal-conditioned inverse dynamics model. The controller predicts the next action in one forward pass and performs no rollout search. Across four benchmark families, it matches or beats the Cross-Entropy Method (CEM) in 7 of 8 settings and cuts per-decision planning cost by about 100 to 130 times.

#### Evidence
- [Geometry Guided Self-Consistency for Physical AI](../Inbox/2026-05-09--geometry-guided-self-consistency-for-physical-ai.md): KeyStone method and success-rate gains across VLA and WAM benchmarks.
- [Latent Geometry Beyond Search: Amortizing Planning in World Models](../Inbox/2026-05-09--latent-geometry-beyond-search-amortizing-planning-in-world-models.md): GC-IDM method, benchmark results, and planning speedup figures.

### Backdoors and ownership checks for released robot policies
Security work in this period treats VLA release and adaptation as an attack surface. ATAAT shows that an attacker can plant visual triggers into OpenVLA-style policies by separating benign-task and backdoor gradients. With a 5% poisoning rate, it reports 88.8% benign success and 83.5% targeted attack success on LIBERO-Spatial data poisoning with OpenVLA-7B. The triggers include visual objects and semantic conditions such as an open drawer or a person wearing a watch.

GuardVLA uses a related backdoor idea for ownership verification. It embeds a fixed 6-bit secret message into visual observations during training, then swaps in a trigger projector and classifier head at audit time. On LIBERO with OpenVLA-OFT, watermark identification confidence is near 100% across Spatial, Goal, Object, and LIBERO-10, with clean models near zero. Reported benign success rates stay close to clean baselines.

#### Evidence
- [ATAAT: Adaptive Threat-Aware Adversarial Tuning Framework against Backdoor Attacks on Vision-Language-Action Models](../Inbox/2026-05-09--ataat-adaptive-threat-aware-adversarial-tuning-framework-against-backdoor-attacks-on-vision-language-action-models.md): ATAAT threat model, gradient separation approach, triggers, and attack results.
- [Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models](../Inbox/2026-05-09--towards-backdoor-based-ownership-verification-for-vision-language-action-models.md): GuardVLA watermarking method, audit mechanism, WIC results, and benign success rates.

### Agent hardware bring-up as a robot bottleneck
Octopus Protocol targets the work that comes before a robot policy can act: device discovery, driver code, tool exposure, and repair. A coding agent probes operating-system devices, identifies capabilities, generates typed Model Context Protocol (MCP) tools, writes a FastMCP server, and deploys an HTTP/SSE endpoint.

The paper reports one-command hardware onboarding in about 10 to 15 minutes, with up to 30 generated MCP tools. The same markdown specification runs on Windows/WSL, Apple Silicon macOS, and Raspberry Pi 4. On a SO-ARM101 6-DOF arm with USB camera feedback, an MCP client performs closed-loop visual-motor control by capturing an image, moving a joint, and checking the result with another image.

#### Evidence
- [Octopus Protocol: One-Shot Hardware Discovery and Control for AI Agents via Infrastructure-as-Prompts](../Inbox/2026-05-09--octopus-protocol-one-shot-hardware-discovery-and-control-for-ai-agents-via-infrastructure-as-prompts.md): Octopus Protocol pipeline, platform coverage, hardware control demo, and integration results.
