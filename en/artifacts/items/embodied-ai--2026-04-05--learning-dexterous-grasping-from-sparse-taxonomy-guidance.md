---
source: arxiv
url: http://arxiv.org/abs/2604.04138v1
published_at: '2026-04-05T14:53:43'
authors:
- Juhan Park
- Taerim Yoon
- Seungmin Kim
- Joonggil Kim
- Wontae Ye
- Jeongeun Park
- Yoonbyung Chai
- Geonwoo Cho
- Geunwoo Cho
- Dohyeong Kim
- Kyungjae Lee
- Yongjae Kim
- Sungjoon Choi
topics:
- dexterous-manipulation
- grasp-taxonomy
- vision-language-planning
- reinforcement-learning
- sim-to-real
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Learning Dexterous Grasping from Sparse Taxonomy Guidance

## Summary
GRIT learns dexterous grasping from sparse high-level grasp taxonomy labels instead of dense pose demonstrations. It splits the problem into grasp-type selection and low-level finger control, aiming to improve generalization and user control.

## Problem
- Dexterous grasping needs both a suitable grasp plan and coordinated multi-finger execution, but dense grasp pose or contact labels for every object-task pair are expensive to specify.
- End-to-end reinforcement learning from task reward alone can learn grasping, but it gives little control over which grasp strategy the robot uses when it fails.
- The paper targets grasping on novel objects while keeping a human-adjustable high-level interface through grasp taxonomies.

## Approach
- GRIT is a two-stage system: first pick a grasp configuration, then execute it with a taxonomy-conditioned control policy.
- The grasp configuration is a discrete human-inspired taxonomy plus a target wrist orientation. The taxonomy library contains 30 grasp types based on Feix et al.
- At inference time, a vision-language model uses the scene image and task text to choose the taxonomy. To help with spatial reasoning, the method overlays candidate wrist directions on the image.
- The low-level policy takes the selected taxonomy, wrist target, proprioception, and object geometry features such as partial point cloud, hand-object distances, table distance, and Basis Point Set features.
- The controller is trained with reinforcement learning using a multiplicative reward that combines approach quality, object interaction, taxonomy adherence, object stability, and penalties for unintended contacts. A teacher-student distillation stage transfers the policy to a student that uses partial observations and an LSTM contact reconstructor for real deployment.

## Results
- The paper reports an overall success rate of **87.9%** for GRIT.
- Training uses **30 YCB objects** and evaluation on novel objects uses **373 Objaverse/RoboCasa objects** after filtering, split into **135 fruit_vegetable**, **82 household_utensil_tool**, and **156 packed_goods/drink/bread_food** instances.
- The universal GRIT policy is trained over **30 taxonomies** sampled during training.
- The evaluation protocol samples **8 wrist directions** around each object and runs **30 trials** per direction.
- The paper claims GRIT improves generalization to novel objects over **RDG** and **GraspXL**, but the excerpt does not include the per-baseline numeric comparison table.
- Real-world experiments claim controllability: users can adjust grasp strategy through taxonomy selection based on object geometry and task intent, but the excerpt does not provide real-world success numbers.

## Link
- [http://arxiv.org/abs/2604.04138v1](http://arxiv.org/abs/2604.04138v1)
