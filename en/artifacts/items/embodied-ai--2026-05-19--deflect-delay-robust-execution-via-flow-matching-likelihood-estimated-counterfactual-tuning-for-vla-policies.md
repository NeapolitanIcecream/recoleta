---
source: arxiv
url: https://arxiv.org/abs/2605.19294v1
published_at: '2026-05-19T03:14:11'
authors:
- Yixiang Zhu
- Yonghao Chen
- Rui Meng
- Jingyu Guo
- Jiaxiang Zou
- Zijie Yang
- Taowen Wang
- Xinyu Chen
topics:
- vision-language-action
- asynchronous-inference
- flow-matching
- preference-optimization
- robot-manipulation
- delay-robust-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies

## Summary
DEFLECT is an offline post-training method for flow-matching VLA policies that improves asynchronous robot control under inference delay. It creates preference pairs from fresh and stale observations and trains the policy to prefer actions aligned with the execution-time state.

## Problem
- Asynchronous VLA deployment executes an old action chunk while the model computes the next one, so the new chunk can be conditioned on a scene that is several control steps out of date.
- This matters for moving or reactive tasks: on Kinetix, naive asynchronous rollover drops from 89% success to under 1% when inference delay reaches 7 control steps.
- Supervised fine-tuning does not rank fresh-consistent actions above stale-consistent actions, and flow-matching policies do not expose an analytic action likelihood for standard DPO.

## Approach
- DEFLECT uses offline trajectories and samples a delay d, with training delays up to d_max=4.
- A frozen VLASH reference policy generates two action chunks with shared sampling noise: A+ from a fresh context at t+d and A- from a stale context at t.
- Both chunks are scored under the deployment-time mixed context, which uses rolled-forward proprioception and stale vision, matching the async runtime input.
- The paper uses the negative flow-matching loss as an implicit log-likelihood surrogate, then applies a reference-calibrated DPO loss plus an SFT anchor on expert chunks.
- Deployment uses the same ODE inference as the base policy, with no extra runtime cost.

## Results
- Kinetix: DEFLECT reaches 83.3% average success over delays d=0-7 versus 79.4% for VLASH, 78.4% for PFM, 48.9% for RTC, 46.7% for BID, and 42.4% for naive async.
- Kinetix high-delay regime d=5-7, unseen during training: DEFLECT averages 73.5% success versus 67.1% for VLASH and 65.5% for PFM, gains of +6.4 and +8.0 points.
- Kinetix high-delay baselines collapse: naive async averages 1.5% success, RTC 2.0%, and BID 2.0% at d=5-7.
- LIBERO with a pi_0.5-scale VLA: DEFLECT improves over VLASH at every delay, with +4.6 points at d=7 after 200 fine-tuning steps.
- Real robots, N=30 per task: Conveyor-I gets 96.7% full-task success for pi_0.5 and DEFLECT, while VLASH gets 86.7%; Conveyor-II gets 90.0% for DEFLECT versus 83.3% for VLASH and 46.7% for pi_0.5.
- Real Whack-a-Mole, N=30: DEFLECT hits 13.6 moles per 30-second trial versus 10.4 for VLASH and 8.9 for pi_0.5.

## Link
- [https://arxiv.org/abs/2605.19294v1](https://arxiv.org/abs/2605.19294v1)
