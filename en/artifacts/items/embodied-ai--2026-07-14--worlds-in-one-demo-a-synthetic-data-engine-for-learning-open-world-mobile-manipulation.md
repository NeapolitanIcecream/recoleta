---
source: arxiv
url: https://arxiv.org/abs/2607.13154v1
published_at: '2026-07-14T18:04:58'
authors:
- Lingxiao Guo
- Huanyu Li
- Guanya Shi
topics:
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- sim2real
- mobile-manipulation
- vision-language-action
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Worlds in One Demo: A Synthetic Data Engine for Learning Open-World Mobile Manipulation

## Summary
WANDA turns one real RGBD mobile-manipulation demonstration into synthetic trajectories across reconstructed and generated 3D scenes. The paper reports improved data efficiency, spatial generalization, and long-horizon robustness, including real-world deployment on five tasks and zero-shot transfer to a different robot embodiment.

## Problem
- Open-world mobile manipulation needs many demonstrations because robots must coordinate navigation and manipulation across varied object locations, scenes, and long task horizons.
- Teleoperation and UMI data collection require substantial human effort, hardware, and accurate localization, making large-scale data collection expensive.
- This matters because policies trained from limited demonstrations often suffer from spatial generalization failures and compounding state errors during long-horizon execution.

## Approach
- WANDA reconstructs the background from mobile RGBD views using Gaussian splatting and reconstructs object geometry and 6D motion with BundleSDF, creating a renderable planning workspace from one demonstration.
- It relocates contact-rich interaction segments to new object and robot configurations, then uses whole-body inverse kinematics and RRT-Connect planning to chain navigation and manipulation into complete trajectories.
- Corrective State Expansion perturbs object and robot states to expose the policy to navigation and manipulation drift rather than only nominal demonstrations.
- It generates additional 3D scenes from single everyday photos with Marble and creates visual training data by combining splatted backgrounds with rendered robot and object meshes.

## Results
- In Bigym simulation, WANDA generated data from one source demonstration and achieved an average success rate of 75.6% across three tasks, compared with 78.0% for ACT trained on roughly 40–60 source demonstrations; the reported data-efficiency gain is approximately 50x over teleoperation baselines in the single-scene setting.
- On the BEHAVIOR Challenge task, WANDA reached a Q-score of 16.67 from one demonstration and 1,360 generated demonstrations, versus 3.33, 11.11, and 62.22 for policies trained on 20, 50, and 200 official demonstrations, respectively.
- On Agibot G1, one demonstration produced an average real-world progress score of 54.8% across five long-horizon tasks and 10 trials per task: Lunch Box 55.0%, Utensil 52.5%, Drop Trash 75.0%, Fridge 46.7%, and Pour 45.0%, as reported in the excerpt.
- Removing Corrective State Expansion reduced the reported average real-world progress to 15.7%, compared with 54.8% for full WANDA.
- The paper reports deployment on 16 environments and zero-shot transfer to a Linearbot mobile manipulator with a different morphology using synthetic data generated from a single Agibot G1 demonstration; the excerpt provides no separate transfer success metric.

## Link
- [https://arxiv.org/abs/2607.13154v1](https://arxiv.org/abs/2607.13154v1)
