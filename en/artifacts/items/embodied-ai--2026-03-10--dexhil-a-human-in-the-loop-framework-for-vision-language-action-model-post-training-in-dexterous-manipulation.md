---
source: arxiv
url: http://arxiv.org/abs/2603.09121v1
published_at: '2026-03-10T02:55:27'
authors:
- Yifan Han
- Zhongxi Chen
- Yuxuan Zhao
- Congsheng Xu
- Yanming Shao
- Yichuan Peng
- Yao Mu
- Wenzhao Lian
topics:
- vision-language-action
- dexterous-manipulation
- human-in-the-loop
- robot-post-training
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# DexHiL: A Human-in-the-Loop Framework for Vision-Language-Action Model Post-Training in Dexterous Manipulation

## Summary
DexHiL proposes a human-in-the-loop post-training framework for dexterous manipulation vision-language-action models, integrating offline demonstrations, online human takeover, and intervention-aware reweighted training into a single arm-hand system. Its goal is to improve real-robot success rates and robustness on high-dimensional, contact-rich dexterous-hand tasks more efficiently than pure offline finetuning.

## Problem
- Existing VLAs show promise in general manipulation, but when transferred to downstream dexterous-hand tasks, **high-dimensional hand control, dense contact, and covariate shift** make pure offline post-training difficult to converge stably.
- Traditional HiL/DAgger-style correction mostly covers only robot arms or parallel grippers, and **cannot provide unified, continuous, fine-grained takeover for both the robot arm and the dexterous hand**, resulting in insufficient quality and coordination of corrective data.
- This matters because small errors in dexterous manipulation can accumulate rapidly and enter OOD states, directly affecting reliable deployment on real robots for complex tasks such as grasping and extraction.

## Approach
- Proposes an **integrated arm-hand HiL teleoperation system**: the robot arm uses an ArUco cube for 6D pose mapping, while the hand uses glove keypoints to drive learned joint retargeting, enabling instant online human takeover.
- Designs a **two-stage hand retargeting** process: first learning a stable motion manifold for the four fingers, then freezing the four fingers and optimizing thumb residuals plus inter-finger geometric constraints, preventing unified five-finger learning from degenerating into “pinch-style” grasping.
- Uses **asynchronous multithreaded control**: the policy executes autonomously at 20Hz, with human arm control at 30Hz and hand control at 90Hz; when imminent failure is detected, the human takes over and generates corrective trajectories.
- Applies **intervention-aware reweighting** during training: scarce but high-value human corrective segments are given higher weight in the loss, with the goal of increasing the intervention sample ratio to 0.5 so the model can learn recovery and error-avoidance behaviors more quickly.
- Combines an **offline warm-up + online iterative aggregation** data pipeline, and filters for recovery segments from “the last intervention to task completion,” reducing distribution conflict and policy oscillation caused by earlier erroneous actions.

## Results
- On the **Tissue Extraction** task, DexHiL reaches a **95%** success rate in round 3, outperforming **DAgger\*** at **80%** and the offline baseline at **75%**.
- On the **Plush Toy Grasping** task, DexHiL reaches a **65%** success rate in round 3, while **DAgger\*** achieves only **20%**, and the offline baseline is **35%**.
- The abstract states that, relative to the standard **offline-only finetuning** baseline, DexHiL delivers an **average 25%** improvement in success rate across different tasks.
- The introduction also states that after **3 rounds of online optimization**, compared with offline training baselines using the same amount of data, the two tasks achieve **20%** and **30%** success-rate improvements, respectively.
- The experimental setup shows: an initial **60 offline trajectories** are used for warm-up; afterward, **10 trajectories** per task are added each round, and compared against Offline-40/50/60 baselines with equal data budgets; each task is evaluated with **20** independent trials on a real robot.
- The paper also claims that ablation results show the **intervention-aware reweighting mechanism** is the key driver for breaking the sample-efficiency bottleneck, but the excerpt does not provide a more complete ablation table.

## Link
- [http://arxiv.org/abs/2603.09121v1](http://arxiv.org/abs/2603.09121v1)
