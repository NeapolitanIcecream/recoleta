---
source: arxiv
url: http://arxiv.org/abs/2604.07993v1
published_at: '2026-04-09T09:01:43'
authors:
- Shuanghao Bai
- Meng Li
- Xinyuan Lv
- Jiawei Wang
- Xinhua Wang
- Fei Liao
- Chengkai Hou
- Langzhe Gu
- Wanqi Zhou
- Kun Wu
- Ziluo Ding
- Zhiyuan Xu
- Lei Sun
- Shanghang Zhang
- Zhengping Che
- Jian Tang
- Badong Chen
topics:
- humanoid-robotics
- vision-language-action
- whole-body-manipulation
- cross-embodiment-learning
- mixture-of-experts
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation

## Summary
HEX is a vision-language-action system for full-sized humanoid robots that targets whole-body manipulation, where arms, hands, legs, waist, and balance must work together. Its main claim is that modeling humanoid state in a shared body-part format and predicting short-term future proprioception improves coordination, generalization, and task success on real robots.

## Problem
- Existing VLA policies for robots often predict high-dimensional actions without modeling how body parts depend on each other through posture and balance, which hurts humanoid whole-body control.
- Whole-body manipulation needs locomotion, manipulation, and dynamic stability at the same time, especially in fast-reaction and long-horizon tasks.
- Cross-embodiment training is hard because different humanoids have different joints, sensors, and state dimensions.

## Approach
- HEX uses a **humanoid-aligned universal state representation**: it maps each robot's proprioception into fixed canonical body-part slots such as arms, hands, legs, head, and waist, with learned tokens for missing parts.
- It adds a **Unified Proprioceptive Predictor (UPP)** that takes these part tokens and predicts short-horizon future body states. UPP uses a shared transformer plus morphology-aware mixture-of-experts layers so different body parts and robot embodiments can route to different experts.
- For visual context, HEX stores compact **history query features** from past frames instead of re-encoding long image sequences. The paper sets the visual history window to **2** frames in experiments.
- Its **Action Expert** generates actions with dual conditioning: one branch attends to visual-language features, another attends to predicted future proprioceptive features, and a learned gate decides how much state prediction should influence the action.
- Training combines a **flow-matching action objective** with an auxiliary **future-state prediction loss**, and the full system runs hierarchically with a high-level VLA policy plus a low-level RL whole-body controller for balance-preserving execution.

## Results
- The paper claims **state-of-the-art real-world performance** on humanoid whole-body manipulation tasks, measured by **task success rate** and **generalization**, compared with **ACT, SwitchVLA, GR00T N1.5, and $\Pi_{0.5}$**.
- It reports the strongest gains in **fast-reaction** and **long-horizon** tasks, where temporal consistency and whole-body coordination matter most.
- Experiments are conducted on two real humanoid platforms: **Tienkung 2.0** and **Tienkung 3.0**.
- The excerpt does **not include the numerical tables or exact success-rate values**, so the claimed margins over baselines cannot be verified from the provided text alone.
- The paper also claims improved **cross-embodiment generalization** through shared body-part state encoding and MoE-based proprioceptive prediction, but this excerpt does not provide quantitative transfer metrics.

## Link
- [http://arxiv.org/abs/2604.07993v1](http://arxiv.org/abs/2604.07993v1)
