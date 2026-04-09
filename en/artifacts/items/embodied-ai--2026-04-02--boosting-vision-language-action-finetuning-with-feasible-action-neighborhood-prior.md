---
source: arxiv
url: http://arxiv.org/abs/2604.01570v1
published_at: '2026-04-02T03:30:43'
authors:
- Haochen Niu
- Kanyu Zhang
- Shuyu Yin
- Qinghai Guo
- Peilin Liu
- Fei Wen
topics:
- vision-language-action
- robot-finetuning
- ood-generalization
- sample-efficiency
- manipulation-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior

## Summary
This paper adds a feasible action neighborhood prior to vision-language-action finetuning. The idea is to train robot policies to keep probability mass over a small region of similar good actions instead of collapsing onto one exact action.

## Problem
- Standard VLA finetuning uses language-model style objectives such as one-hot next-token prediction or PPO-style updates, which treat one action as the only correct target.
- In robot manipulation, many nearby actions can work equally well for the same state, so forcing a single sharp action distribution hurts generalization and wastes data.
- The paper targets two common failure modes: overfitting in supervised finetuning with small demonstration sets, and low sample efficiency in reinforced finetuning when the policy must discover action tolerance through exploration.

## Approach
- The paper defines a **feasible action neighborhood (FAN)**: for a state, a connected set of actions whose value is within a tolerance of the optimal action.
- It uses the policy distribution as a practical proxy for FAN size: a narrow spike means little tolerance, while a broader smooth peak means more robustness.
- The method adds a KL regularizer that pulls the action distribution toward a Gaussian centered at the policy's current best action. This encourages a smooth, unimodal distribution over nearby actions.
- For **FAN-SFT**, the regularizer is added to the supervised log-likelihood loss, with covariance taken from the policy's current variance.
- For **FAN-PPO**, the regularizer is added to PPO with a fixed covariance target, so policy updates trade off reward improvement, trust-region stability, and a Gaussian-shaped local action prior.

## Results
- On **ManiSkill** SFT with **OpenVLA**, **FAN-SFT** improves in-distribution success from **78.1 ± 3.1** to **89.8 ± 0.8** (**+11.7 points**).
- On ManiSkill OOD evaluation, **vision** success rises from **76.6 ± 1.9** to **81.7 ± 1.1** (**+5.1**), **semantic** from **57.4 ± 0.9** to **63.5 ± 1.5** (**+6.1**), and **execution** from **40.4 ± 0.8** to **44.8 ± 0.5** (**+4.4**).
- Average OOD success on ManiSkill improves from **58.1** to **63.3** (**+5.2 points**) against the OpenVLA + SFT baseline, and exceeds the reported **RL4VLA** OOD average of **60.7**.
- The paper also claims gains in **sample efficiency, convergence speed, and OOD robustness** across both **SFT and RFT**, using **OpenVLA** and **OpenVLA-OFT** on **ManiSkill** and **LIBERO**.
- The provided excerpt does not include the quantitative RFT tables or full LIBERO numbers, so those claims cannot be verified here with exact metrics.

## Link
- [http://arxiv.org/abs/2604.01570v1](http://arxiv.org/abs/2604.01570v1)
