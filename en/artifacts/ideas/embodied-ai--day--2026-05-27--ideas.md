---
kind: ideas
granularity: day
period_start: '2026-05-27T00:00:00'
period_end: '2026-05-28T00:00:00'
run_id: 1c06e363-c98d-489c-b975-2263ff49b7ab
status: succeeded
topics:
- robot learning
- vision-language-action models
- manipulation
- tactile sensing
- model compression
- autonomous driving safety
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/manipulation
- topic/tactile-sensing
- topic/model-compression
- topic/autonomous-driving-safety
language_code: en
pass_output_id: 235
pass_kind: trend_ideas
upstream_pass_output_id: 234
upstream_pass_kind: trend_synthesis
---

# Robot policy deployment benchmarks

## Summary
Robot teams can test deployment barriers directly: 4-bit policy compression, force-aware manipulation scoring, and primitive-labeled long-horizon fine-tuning all have concrete evaluation recipes in the cited work.

## W4A4 acceptance tests for robot VLA policies
Robotics teams trying to run Pi 0.5 or GR00T-class policies close to the robot should add a 4-bit policy acceptance test before buying more inference hardware. The test is concrete: quantize the language backbone and diffusion action head to uniform W4A4, calibrate DiT activation scales on a small set of unlabeled trajectories, then compare against the FP16 policy on the team’s manipulation suite.

Ω-QVLA reports Pi 0.5 W4A4 at 98.0% average LIBERO success versus 97.1% FP16 and GR00T N1.5 W4A4 at 87.8% versus 87.0%, with a 71.3% static memory-footprint cut. The practical gate should include task success, action smoothness, memory use, and real robot progress, since the same paper reports ARX R5 dual-arm progress close to FP16 and a much larger gap over QuantVLA.

### Sources
- [Ω-QVLA: Robust Quantization for Vision-Language-Action Models via Composite Rotation and Per-step Scaling](../Inbox/2026-05-27--o-qvla-robust-quantization-for-vision-language-action-models-via-composite-rotation-and-per-step-scaling.md): Ω-QVLA reports uniform W4A4 quantization of both language backbone and DiT action head, near-FP16 LIBERO success, 71.3% static memory reduction, and real ARX R5 progress results.
- [Ω-QVLA: Robust Quantization for Vision-Language-Action Models via Composite Rotation and Per-step Scaling](../Inbox/2026-05-27--o-qvla-robust-quantization-for-vision-language-action-models-via-composite-rotation-and-per-step-scaling.md): The paper abstract reports 98.0% and 87.8% success rates while reducing static memory footprint by 71.3%.

## Contact-force metrics for gentle manipulation rollouts
Manipulation teams handling fragile, slippery, or deformable objects should add contact-force metrics to rollout evaluation. A useful scorecard records maximum transient grip force, average grip force, maximum transient applied force, and average applied force for each task attempt, with language-conditioned runs such as “gently” and “firmly.”

Tabero shows how to build the data path by replaying manipulation trajectories in Isaac Lab with tactile sensing, recording GelSight-style tactile images, marker displacement grids, and fingertip forces, then sending predicted pose and force targets to a hybrid controller. It reports over 70% lower average grip force under gentle instructions. CoP adds a complementary path for dexterous hands: represent touch as a 3D contact force and 3D contact location per tactile region, then train in simulation. On real peg-in-hole insertion, CoP reaches 0.78 success across six shapes, compared with 0.48 for raw taxels and 0.53 for binary contact. A rollout can pass task completion and still fail the contact-force limit.

### Sources
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): Tabero defines the force-control problem, simulated tactile data pipeline, hybrid controller, and four contact-quality metrics.
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): The abstract states that Tabero reduces average grip force by over 70% under gentle instructions while maintaining high task success.
- [Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation](../Inbox/2026-05-27--beyond-binary-sim-to-real-dexterous-manipulation-with-physics-grounded-contact-representation.md): CoP reports a compact tactile representation and real peg-in-hole success gains over raw taxels and binary contact.

## Primitive labels and switch rules for long-horizon VLA demonstrations
Robot data teams with task-level demonstrations can add an offline primitive-labeling pass before VLA fine-tuning. The workflow is specific: infer a sequence over primitives such as Grasp, Place, Lift, Move, Push, Pull, Insert, Press, Twist, Tilt, and Rotate; generate state-based boundary rules for those segments; track object masks with SAM and Cutie; train the VLA on canonical primitive instructions; then use a planner and state-history switch rules during execution.

PrimitiveVLA reports large gains where memorizing whole demonstrations hurts most. OpenVLA rises from 7.38% to 45.50% on LIBERO-90-Novel, OpenVLA-OFT reaches 66.50% on LIBERO-Long versus 3.75%, and pi0.5 reaches 80.25% on LIBERO-Long versus 30.50%. The cheap check is a held-out set of novel object-skill pairs and long-horizon tasks with the same demonstration budget.

### Sources
- [PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation](../Inbox/2026-05-27--primitivevla-learning-reusable-motion-primitives-for-efficient-and-generalizable-robotic-manipulation.md): PrimitiveVLA describes the 11 primitives, automated boundary detection, object-centric masks, test-time primitive planning, and LIBERO gains.
- [PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation](../Inbox/2026-05-27--primitivevla-learning-reusable-motion-primitives-for-efficient-and-generalizable-robotic-manipulation.md): The paper explains why task-level demonstrations are segmented into shared task-agnostic motion patterns such as Grasp and Pull.
