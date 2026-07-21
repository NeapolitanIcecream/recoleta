---
kind: ideas
granularity: day
period_start: '2026-07-20T00:00:00'
period_end: '2026-07-21T00:00:00'
run_id: 495fb6bb-c9d9-4405-bcdc-bf9c3b497896
status: succeeded
topics:
- embodied AI
- vision-language-action models
- robot memory
- 3D grounding
- world-model planning
- robustness
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vision-language-action-models
- topic/robot-memory
- topic/3d-grounding
- topic/world-model-planning
- topic/robustness
language_code: en
pass_output_id: 371
pass_kind: trend_ideas
upstream_pass_output_id: 370
upstream_pass_kind: trend_synthesis
---

# State representations and checks for embodied control

## Summary
Embodied-control teams should preserve different information at different rates: dense spatial detail for the current scene, compact physical records across time, and independently refreshed state for execution checks. The evidence also supports evaluating world models through action-sensitive interventions rather than plausible rollouts alone.

## Independent physical-state checks for robot action completion
Robot safety and deployment teams should check action completion against independently refreshed physical state rather than a policy’s reasoning trace. POT-VLA shows how the same role-indexed 3D object records can condition actions and then be refreshed after execution to test containment, support, alignment, or handover relations. This is a more concrete monitoring surface than text-plan consistency, which fell to chance under adaptive attack in the VLA robustness study.

The build change is to expose object relations—and contact events where force sensing is available—as a small execution contract after every action chunk. The monitor should receive new sensor measurements rather than hidden states or generated explanations, and it should trigger re-observation or recovery when evidence is uncertain. A useful first test would corrupt vision, force, and policy internals separately and compare this state-based check with plan–action and action-anomaly monitors at matched false-positive rates; the result would show whether physical grounding adds independent safety information rather than another view of the policy output.

### Sources
- [Closing the Loop in Humanoid VLA: Persistent 3D Object Tokens for Verifiable Loco-Manipulation](../Inbox/2026-07-20--closing-the-loop-in-humanoid-vla-persistent-3d-object-tokens-for-verifiable-loco-manipulation.md): POT-VLA refreshes shared 3D object records after action chunks and improves real-world success from 39/80 to 71/80.
- [Reasoning as a Double-Edged Sword: Architecture and Cross-Stage Robustness in Vision-Language-Action Models](../Inbox/2026-07-20--reasoning-as-a-double-edged-sword-architecture-and-cross-stage-robustness-in-vision-language-action-models.md): The plan–action consistency monitor’s AUC dropped from 0.996 to 0.493 under adaptive attack, and monitor fusion did not improve defended success.
- [FM-VLA: Force-based Memory for Vision-Language-Action Models in Contact-Rich Manipulation](../Inbox/2026-07-20--fm-vla-force-based-memory-for-vision-language-action-models-in-contact-rich-manipulation.md): Eight force-memory tokens captured visually ambiguous contact history and supported 83.3% average success across three tasks.

## Dense current-frame tokens with compressed physical history for edge robot control
Engineers fitting manipulation policies onto latency-constrained robots should allocate tokens asymmetrically: preserve dense patches for the current image, but compress history into object and contact records instead of retaining past frames. Patch Policy’s compression ablation indicates that reducing a current observation from 256 patches to 64 or fewer damages precise control, while FM-VLA shows that long force histories can be compressed into eight tokens with only 3.3 ms of added latency. POT-VLA adds a complementary form of compact history through persistent role-indexed 3D object slots.

A fixed-latency comparison should pit this design against uniform visual-token compression and sampled-frame memory on tasks that combine precise alignment, occlusion, and repeated contact. The decision-relevant measurement is not only task success but failure type: current-frame compression should increase localization errors, whereas missing physical history should increase wrong counts, premature completion, and failed recovery.

### Sources
- [Patch Policy: Efficient Embodied Control via Dense Visual Representations](../Inbox/2026-07-20--patch-policy-efficient-embodied-control-via-dense-visual-representations.md): On Push-T, 256 patches scored 0.69, while compression to 64, 16, 4, and 1 patch reduced scores to 0.52, 0.53, 0.51, and 0.48.
- [FM-VLA: Force-based Memory for Vision-Language-Action Models in Contact-Rich Manipulation](../Inbox/2026-07-20--fm-vla-force-based-memory-for-vision-language-action-models-in-contact-rich-manipulation.md): FM-VLA compressed force history into eight tokens, added 3.3 ms over the base policy, and outperformed sampled visual memory.
- [Closing the Loop in Humanoid VLA: Persistent 3D Object Tokens for Verifiable Loco-Manipulation](../Inbox/2026-07-20--closing-the-loop-in-humanoid-vla-persistent-3d-object-tokens-for-verifiable-loco-manipulation.md): POT uses eight role-indexed 3D object slots carrying position, extent, visibility, confidence, and spatial relations.

## Action-sensitive counterfactual tests for latent world-model planners
Teams selecting world models for robot or driving planners should test whether predicted futures change correctly under action and scene interventions, not whether rollouts merely look plausible. SAGE shows that planning performance depends heavily on which action sequences reach the frozen world model: removing its ranking and CEM refinement cuts horizon-150 PushT success from 64.7% to 16.0%. GeoWorldAD uses future geometry to guide trajectory refinement, but its reported excerpt does not isolate present geometry from predicted future geometry. Separately, Thinking in Video finds that generators can produce plausible continuations despite weak explicit causal perception.

The evaluation change is a matched counterfactual suite: hold the observation fixed, alter one candidate action or one causal scene variable, and score whether predicted object geometry, collisions, and candidate ranking change in the correct direction. Running this before a larger physical trial would distinguish a model that supplies action-relevant dynamics from one whose plausible futures contribute little beyond a strong proposal generator or current-scene geometry.

### Sources
- [SAGE: Subgoal-Conditioned Action Generation for Latent World Model Planning](../Inbox/2026-07-20--sage-subgoal-conditioned-action-generation-for-latent-world-model-planning.md): Without world-model ranking and CEM refinement, horizon-150 PushT success fell from 64.7% to 16.0%, showing that proposal generation alone was insufficient.
- [GeoWorldAD: Geometry World Action Model for Autonomous Driving](../Inbox/2026-07-20--geoworldad-geometry-world-action-model-for-autonomous-driving.md): GeoWorldAD predicts four future geometry chunks and reports 91.0 PDMS on NAVSIM v1, but the available excerpt lacks a full present-versus-future geometry ablation.
- [Thinking in Video: Can Video Generators Really Reason About the Real World?](../Inbox/2026-07-20--thinking-in-video-can-video-generators-really-reason-about-the-real-world.md): Open-source video generators produced moderately plausible continuations despite near-zero explicit causal perception under the paper’s protocol.
