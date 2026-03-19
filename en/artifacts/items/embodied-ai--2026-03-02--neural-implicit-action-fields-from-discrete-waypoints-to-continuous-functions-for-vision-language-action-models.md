---
source: arxiv
url: http://arxiv.org/abs/2603.01766v1
published_at: '2026-03-02T11:48:24'
authors:
- Haoyun Liu
- Jianzhuang Zhao
- Xinyuan Chang
- Tianle Shi
- Chuanzhang Meng
- Jiayuan Tan
- Feng Xiong
- Tong Lin
- Dongjie Huo
- Mu Xu
- SongLin Dong
- Zhiheng Ma
- Yihong Gong
- Sheng Zhong
topics:
- vision-language-action
- continuous-action-representation
- implicit-neural-representation
- robot-manipulation
- impedance-control
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Neural Implicit Action Fields: From Discrete Waypoints to Continuous Functions for Vision-Language-Action Models

## Summary
NIAF changes the action output of vision-language-action models from discrete trajectory points to continuous-time functions, better matching the continuity of real robot motion. Its core value is that actions can be queried at arbitrary frequencies, while analytically providing velocity/acceleration/jerk directly, thereby improving long-horizon task performance and the smoothness of real-robot control.

## Problem
- Existing VLAs mostly predict discrete waypoints or fixed-length action chunks, but robot motion is inherently continuous; discretization ties the model to a fixed sampling rate and makes it hard to adapt to different control frequencies.
- Discrete representations usually lack consistent constraints on higher-order derivatives, so velocity/acceleration often rely on numerical differentiation, which easily introduces quantization noise, jitter, and control instability.
- This matters because fine-grained manipulation and impedance control require smooth, physically consistent reference trajectories, rather than coarse discrete point sequences suited only to rigid position control.

## Approach
- Represent an action chunk as a continuous function \(\mathcal{A}(\tau)=\Phi(\tau;\theta)\). Instead of directly outputting a discrete action sequence, the model predicts the function parameters \(\theta\) that define the entire trajectory.
- Use a multimodal large language model (MLLM) as a hypernetwork / hierarchical spectral modulator: based on images, state, and language instructions, it generates modulation vectors to reconfigure a shared SIREN action decoder.
- Use SIREN (sinusoidal implicit network) to represent the action field, because it naturally supports analytical differentiation and has \(C^{\infty}\) smoothness; therefore, position can be queried at any time point, and velocity, acceleration, and jerk can also be obtained analytically.
- Propose grouped hyper-modulation: assign different tokens to the frequency and phase modulation of each SIREN layer, so semantic information hierarchically controls trajectory geometry and kinematics.
- During training, in addition to position loss, analytical velocity loss, acceleration loss, and jerk regularization can also be added; on real robots, these analytical quantities can be directly used for feedforward/damping terms in impedance control.

## Results
- **CALVIN, ABCD→D**: NIAF (0.77B, **no large-scale robot pretraining**) achieves Avg. Len **4.66**, higher than BEAST **4.61**, FLOWER **4.62**, and UniVLA **4.63**; success rates for 1/2/3/4/5 consecutive tasks are **0.997/0.978/0.946/0.900/0.839**, respectively.
- **CALVIN, ABC→D**: NIAF achieves Avg. Len **4.47**, higher than BEAST **4.42**, FLOWER **4.44**, and UniVLA **4.41**; 4-task and 5-task success rates are **0.848** and **0.764**, outperforming BEAST's **0.827/0.744** and FLOWER's **0.823/0.755**.
- The paper claims **state-of-the-art** performance across multiple backbones on **CALVIN and LIBERO**, and mentions that it can scale from Florence-2 to Qwen3-VL; however, the LIBERO table in the provided excerpt is truncated, so its full numerical results cannot be completely listed.
- Real-robot experiments cover **4 tasks**: Item Placement, Cup Stacking, Shape Insertion, and Towel Folding. The excerpt does not provide quantitative metrics such as success rate or error, but the authors explicitly claim that continuous action representation can reduce control jitter found in discrete baselines and support more stable impedance control.
- Compared with discrete waypoint methods, the paper's strongest concrete claim is that NIAF can generate trajectories at **infinite resolution**, output a continuous action field in a **single forward pass**, and provide **analytical noise-free** velocity/acceleration/jerk for physically consistent control.

## Link
- [http://arxiv.org/abs/2603.01766v1](http://arxiv.org/abs/2603.01766v1)
