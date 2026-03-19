---
source: arxiv
url: http://arxiv.org/abs/2603.01581v1
published_at: '2026-03-02T08:12:03'
authors:
- Zihao Zheng
- Zhihao Mao
- Maoliang Li
- Jiayu Chen
- Xinhao Sun
- Zhaobo Zhang
- Donggang Cao
- Hong Mei
- Xiang Chen
topics:
- vision-language-action
- speculative-decoding
- robot-kinematics
- kalman-filter
- embodied-ai
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# KERV: Kinematic-Rectified Speculative Decoding for Embodied VLA Models

## Summary
This paper proposes KERV, which introduces robotic kinematics into speculative decoding for embodied VLA, using lightweight kinematic prediction to replace part of the re-inference and dynamically adjust thresholds, thereby accelerating inference while minimizing loss in task success rate. Its core value is to simultaneously leverage token generation capability and short-horizon kinematic prediction capability in robot control.

## Problem
- The paper addresses the problem that **VLA robot policy inference is too slow**; although speculative decoding can accelerate inference, once a draft token is wrong in VLA, it usually requires costly re-inference, which limits the speedup.
- Another key issue is that the **acceptance threshold is hard to set**: if the threshold is too loose, action errors accumulate and success rate drops; if it is too strict, the speed benefit disappears. A fixed threshold cannot adapt to different tasks and environments.
- This matters because VLA is the mainstream paradigm for embodied foundation model / vision-language-action robots, but real robot control requires faster and more stable closed-loop inference.

## Approach
- The core idea of KERV is simple: **when a token error occurs during speculative decoding, instead of always having the large model recompute, it directly uses a kinematics-based Kalman Filter to complete the remaining part of the current action segment**.
- The method first maps VLA output tokens into 7-DoF actions (position, orientation, gripper), and builds an action cache for each DoF; the KF uses short action context for one-step prediction. The paper sets **Predict Length = 1, Action Context = 10** to control kinematic prediction error.
- To avoid accumulation of long-term KF prediction error, the compensation mechanism is not enabled at every step: after each compensation, KF is disabled for the next **n=4** steps, then the system returns to standard SD.
- The second mechanism is **dynamic acceptance-threshold adjustment based on kinematic fluctuation K_var**: instead of only checking whether token ID error is below a fixed threshold, it maps the error into action space and dynamically tightens or relaxes the threshold according to kinematic variation. Most tasks in the paper use **r_max=15, r_min=5**.
- In system implementation, large-model draft/verify runs on GPU, while KF compensation and threshold adjustment run on CPU; because these two components have small FLOPs but many logical decisions, CPU+GPU collaboration is more suitable. The paper reports the compute cost as: draft **0.07 GFLOPs/inf**, verify **3.92 TFLOPs/inf**; memory usage is about **700MB vs 15GB**.

## Results
- On the four **LIBERO** task suites (Goal/Object/Spatial/Long), KERV reportedly achieves **1.48×–1.57×** end-to-end speedup over naive VLA+SD, with "**without SR loss / nearly no Success Rate loss**".
- Compared with existing **SpecVLA**, the paper claims KERV achieves an additional **27%–37%** speedup while almost not sacrificing success rate; the abstract directly gives this as the main conclusion.
- **Goal**: naive VLA+SD has **76.2% SR, 1.00×, 159.2 steps**; SpecVLA reaches about **1.23×** at fastest (**r=15**) but SR drops to **71.0%**; **KERV achieves 75.6% SR, 1.54×, 153.5 steps**. Relative to naive, this is a **54%** speedup; relative to SpecVLA(r=15), about **25%** faster, with SR only **0.6pt** below naive but higher than SpecVLA under the faster threshold.
- **Object**: naive has **68.6% SR, 1.00×, 195.9 steps**; SpecVLA reaches **1.09×–1.10×**, with SR between **58.0%–70.0%**; **KERV achieves 72.3% SR, 1.49×, 186.8 steps**. Relative to naive, this is a **49%** speedup, and SR also improves by **3.7pt**.
- **Spatial**: naive has **82.8% SR, 1.00×, 127.3 steps**; SpecVLA reaches **1.24×–1.26×**, with SR between **77.8%–85.2%**; **KERV achieves 83.7% SR, 1.57×**, the highest speed in the table. The excerpt does not fully provide its steps, but the paper claims KERV has the fewest average inference steps across the four environments.
- The paper also provides a negative control: when naive SD is directly attached to VLA, speed in the four environments is only **0.86×–0.98×** (actually slower than **1×** AR), and per-step latency rises from **0.188–0.198s** to **0.200–0.217s**, showing that if error re-inference and threshold issues are not solved, SD may not be effective for VLA.

## Link
- [http://arxiv.org/abs/2603.01581v1](http://arxiv.org/abs/2603.01581v1)
