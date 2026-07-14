---
kind: ideas
granularity: day
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-14T00:00:00'
run_id: 731c840e-d1dc-4e4a-977c-5a9fcc99c5cb
status: succeeded
topics:
- robot learning
- world models
- action representations
- spatial grounding
- data efficiency
tags:
- recoleta/ideas
- topic/robot-learning
- topic/world-models
- topic/action-representations
- topic/spatial-grounding
- topic/data-efficiency
language_code: en
pass_output_id: 355
pass_kind: trend_ideas
upstream_pass_output_id: 354
upstream_pass_kind: trend_synthesis
---

# Coordinate-aligned supervision for robot policy training

## Summary
Robot-learning teams can make predictive supervision more useful by expressing future changes in control-aligned coordinates, checking synthetic trajectories with explicit multi-view geometry, and using action-free video to shape dexterous residual RL.

## Robot-frame future-delta training for viewpoint-robust VLAs
VLA teams pooling demonstrations across camera setups need policies that predict physical consequences without relearning camera-to-robot transforms. WALA gained 21 points on RoboCasa by supervising semantic and geometric future deltas; robot-centric pointmaps improved π₀.₅ by 7.6 points and widened their advantage at unseen camera placements. Together, these results suggest expressing future geometry in the robot frame before latent-action training.

Add a decoder that predicts future robot-centric pointmaps or their deltas, centered on the current end effector. Keep WALA’s semantic target, and train the action head against the same coordinate system. This directly couples predicted scene evolution to executable motion.

Run a low-data test with fixed-camera training and unseen-camera evaluation. Compare depth-delta, camera-frame pointmap-delta, and robot-frame pointmap-delta targets. Use a pilot decision threshold: stop if the robot-frame target improves unseen-camera success by under 5 percentage points or lowers fixed-camera success by more than 3 points.

### Evidence
- [WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos](../Inbox/2026-07-13--wala-learning-executable-latent-actions-from-action-labeled-demonstrations-and-action-free-videos.md): WALA learns executable latent actions from semantic and geometric future changes and reports large policy gains.
- [See like a Robot: Robot-Centric Pointmaps for Vision-Language-Action Models](../Inbox/2026-07-13--see-like-a-robot-robot-centric-pointmaps-for-vision-language-action-models.md): Robot-centric pointmaps align dense scene geometry with the robot action frame and improve viewpoint generalization.

## Multi-view geometric acceptance tests for synthetic manipulation videos
Teams generating robot training videos need a cheap way to reject visually plausible trajectories that violate camera calibration or gripper kinematics. Xiaomi-Robotics-U0 reports a real-policy OOD gain from 36.9% to 63.2% with generated data, while Pix2Act shows that continuous gripper-keypoint paths in two image planes can be triangulated into precise 3D actions.

Attach projected gripper keypoints to each generated view, triangulate them frame by frame, and reject clips whose recovered pose disagrees across views, exceeds joint limits, or breaks temporal continuity. The same paths can condition generation, giving the model an explicit geometric control signal and yielding an audit score for every synthetic clip.

Generate matched batches with and without this check, then train equal-size policies and evaluate unseen scenes and camera poses. Use a pilot decision threshold: drop the check if it rejects fewer than 10% of clips while improving OOD success by under 3 percentage points, or if accepted clips still exceed the calibration error of real demonstrations by more than 25%.

### Evidence
- [Xiaomi-Robotics-U0: Unified Embodied Synthesis with World Foundation Model](../Inbox/2026-07-13--xiaomi-robotics-u0-unified-embodied-synthesis-with-world-foundation-model.md): Xiaomi-Robotics-U0 uses generated embodied data to raise downstream out-of-distribution manipulation success.
- [Pix2Act: Image-Space Manipulation Policies with Equivariant Augmentation](../Inbox/2026-07-13--pix2act-image-space-manipulation-policies-with-equivariant-augmentation.md): Pix2Act represents gripper motion as continuous multi-view keypoint paths and recovers 3D actions through triangulation.

## Video-derived residual rewards for one-demonstration dexterous learning
Dexterous robotics teams adapting a tool skill to a new hand need reward signals beyond one retargeted trajectory. Regrind preserves hand-object relationships from one human demonstration and refines the motion with residual RL. WALA shows that action-free videos can supply semantic and depth-based future-change supervision, including a large gain when labeled robot data are scarce.

Pretrain a future-delta encoder on ordinary videos of the same tool interaction. During Regrind simulation, score rollouts by agreement with the predicted object-motion and contact-region changes, alongside its object-centric keypoint tracking reward. This could widen the useful restart distribution without requiring motor labels for every human example.

Test one scissors or screwdriver skill with identical retargeting and simulation budgets. Measure success under perturbed object pose, tracking error, and hardware completion. Use a pilot decision threshold: stop if video-derived rewards add under 5 percentage points of perturbed-pose success, increase object-tracking error by over 2 mm, or reduce hardware completion relative to keypoint rewards alone.

### Evidence
- [A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation](../Inbox/2026-07-13--a-minimalist-retargeting-guided-reinforcement-learning-recipe-for-dexterous-manipulation.md): Regrind combines interaction-preserving retargeting from one human demonstration with residual RL for dexterous tool use.
- [WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos](../Inbox/2026-07-13--wala-learning-executable-latent-actions-from-action-labeled-demonstrations-and-action-free-videos.md): WALA extracts semantic and geometric future changes from action-free videos for executable policy learning.
