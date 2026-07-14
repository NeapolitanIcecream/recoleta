---
kind: trend
trend_doc_id: 861
granularity: day
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-14T00:00:00'
topics:
- robot learning
- world models
- action representations
- spatial grounding
- data efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-861
tags:
- recoleta/trend
- topic/robot-learning
- topic/world-models
- topic/action-representations
- topic/spatial-grounding
- topic/data-efficiency
language_code: en
pass_output_id: 354
pass_kind: trend_synthesis
---

# Robot learning gains come from predicting consequences and aligning control coordinates

## Overview
The last populated daily window emphasized efficient use of scarce action signals. Today’s papers keep that concern and add a stronger signal around predictive supervision and explicit geometry. Generated futures, action-free video, and coordinate-aligned inputs all produce measurable policy gains. VIA also shows that a capable general agent can control robots through a carefully designed visual interface without robot-specific fine-tuning.

## Clusters

### Predictive supervision
Future scene changes are becoming direct training targets for control. Xiaomi-Robotics-U0 generates embodied observations and manipulation videos; adding its synthetic data raises out-of-distribution policy success from 36.9% to 63.2%. WALA learns semantic and geometric future deltas from action-free video, then connects those latent changes to executable actions. It reaches 75.2% average success on RoboCasa, versus 54.2% for its base policy. Lumo-2 follows the same design logic by predicting action-relevant latent dynamics before producing action chunks, though its excerpt does not provide numerical benchmark margins.

#### Evidence
- [Xiaomi-Robotics-U0: Unified Embodied Synthesis with World Foundation Model](../Inbox/2026-07-13--xiaomi-robotics-u0-unified-embodied-synthesis-with-world-foundation-model.md): Reports the downstream policy improvement obtained with generated embodied data.
- [WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos](../Inbox/2026-07-13--wala-learning-executable-latent-actions-from-action-labeled-demonstrations-and-action-free-videos.md): Describes learning semantic-geometric latent actions from action-free future observations.
- [Towards Predictive, Aligned, and Scalable Robot Learning](../Inbox/2026-07-13--towards-predictive-aligned-and-scalable-robot-learning.md): Defines latent world dynamics as the intermediate representation used before action generation.

### Coordinate-aligned perception and action
Two methods reduce the burden of learning camera-to-action geometry implicitly. Robot-centric pointmaps attach robot-frame XYZ coordinates to the image grid. They raise π₀.₅ success on 24 RoboCasa tasks from 55.3% to 62.9%, with larger gains under unseen camera placement. Pix2Act instead predicts continuous gripper-keypoint paths in two image planes and triangulates them into 3D actions. It achieves 75.2% mean success across ten MimicGen tasks, 12.1 points above the strongest reported baseline. Both results support explicit spatial grounding as a practical route to viewpoint tolerance.

#### Evidence
- [See like a Robot: Robot-Centric Pointmaps for Vision-Language-Action Models](../Inbox/2026-07-13--see-like-a-robot-robot-centric-pointmaps-for-vision-language-action-models.md): Defines the camera-frame versus robot-frame mismatch and the pointmap solution.
- [Pix2Act: Image-Space Manipulation Policies with Equivariant Augmentation](../Inbox/2026-07-13--pix2act-image-space-manipulation-policies-with-equivariant-augmentation.md): Describes continuous image-space keypoint prediction and triangulation into end-effector poses.

### Human data with minimal robot supervision
Human demonstrations are supplying useful structure before expensive robot data enters the loop. WALA extracts action-relevant scene evolution from videos that contain no motor labels; with only 10% of labeled demonstrations, it reaches 53.9% success versus 18.1% for its base policy. Regrind starts with one human demonstration, preserves hand-object contact relationships during retargeting, and uses residual reinforcement learning for physical refinement. Across two robot hands and two tool-use tasks, simulation success ranges from 98.7% to 99.8%, with zero-shot hardware transfer claimed but not numerically reported in the inspected excerpt.

#### Evidence
- [WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos](../Inbox/2026-07-13--wala-learning-executable-latent-actions-from-action-labeled-demonstrations-and-action-free-videos.md): Shows how unlabeled human video supplies semantic and geometric action targets.
- [A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation](../Inbox/2026-07-13--a-minimalist-retargeting-guided-reinforcement-learning-recipe-for-dexterous-manipulation.md): Describes learning contact-rich manipulation from a single human demonstration.
