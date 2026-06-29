---
source: arxiv
url: http://arxiv.org/abs/2604.17896v1
published_at: '2026-04-20T07:15:12'
authors:
- Yubai Wei
- Chen Wu
- Hashem Haghbayan
topics:
- vision-language-action
- diffusion-policy
- physical-feasibility
- obstacle-avoidance
- robot-manipulation
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Can Explicit Physical Feasibility Benefit VLA Learning? An Empirical Study

## Summary
This paper tests whether adding explicit physical-feasibility supervision helps train vision-language-action policies. In a controlled obstacle-aware reaching task, the added geometric loss improves clearance, task success, and low-data learning relative to standard imitation loss alone.

## Problem
- Standard VLA training matches demonstrated actions but does not directly supervise hard physical constraints such as obstacle avoidance and kinematic feasibility.
- That gap matters because a robot can imitate successful trajectories without learning the geometric regularities that keep motion safe and reliable under changed obstacle layouts.
- The paper studies this issue in close-obstacle reaching, where success depends on both reaching the target and maintaining clearance from a nearby obstacle.

## Approach
- The base policy is a diffusion VLA model, fine-tuned from RDT-1B, that predicts action chunks from RGB observations and language.
- During training, the predicted future joint states are mapped through forward kinematics, and selected robot link points are checked against the obstacle with an analytic signed-distance function to an oriented bounding box.
- A hinge-style geometric loss penalizes predicted link positions whose clearance falls below a safety margin: the total loss is MSE imitation loss plus a weighted feasibility loss.
- The geometric signal uses obstacle geometry and kinematics only during training. At inference, the policy still uses only RGB observations and language.
- The experiments use a simulated Franka close-obstacle reaching dataset generated in Isaac Sim with OMPL-planned expert trajectories and obstacle perturbations at test time.

## Results
- The training dataset has 120 episodes, 3 RGB views per episode, 80 steps per episode, and 15 Hz sampling. Mean minimum obstacle clearance is 6.57 ± 3.11 cm, and mean final target distance is 8.14 ± 6.60 cm.
- The paper claims that MSE+Feasibility improves both physical reliability and overall task performance over the MSE-only baseline under obstacle perturbations.
- It also claims better learning efficiency in low-data settings, with experiments on 40, 80, and 120 training episodes.
- The excerpt does not include the main result tables or exact gains for Safe Success Rate, clearance, or target accuracy, so the quantitative improvement over the baseline cannot be extracted here.
- Qualitative figures show a shift toward higher clearance and lower target error under large perturbations, and an example where the feasibility-trained policy keeps more distance from the obstacle while reaching closer to the target.

## Link
- [http://arxiv.org/abs/2604.17896v1](http://arxiv.org/abs/2604.17896v1)
