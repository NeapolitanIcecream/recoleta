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
- robot-manipulation
- implicit-neural-representation
- continuous-control
- siren
- impedance-control
relevance_score: 0.38
run_id: materialize-outputs
language_code: en
---

# Neural Implicit Action Fields: From Discrete Waypoints to Continuous Functions for Vision-Language-Action Models

## Summary
This paper proposes NIAF, which changes robot action modeling from “predicting a sequence of discrete waypoints” to “predicting a continuous-time function,” making it better aligned with real physical motion. Its core value is the simultaneous improvement of trajectory resolution independence, differentiability, and control smoothness, making vision-language-action models better suited for fine manipulation and impedance control.

## Problem
- Existing VLAs often represent actions as discrete waypoints or compressed control points at a fixed sampling rate, but real robot motion is inherently continuous.
- Discrete representations introduce quantization error, fixed-frequency constraints, and difficulties in consistently supervising higher-order dynamics such as velocity, acceleration, and jerk, leading to jitter and unstable control.
- This matters because fine contact, compliant control, and dynamic execution all rely on smooth and physically consistent continuous trajectories, not just sequences of position points.

## Approach
- Represent an action chunk as a continuous function \(\mathcal{A}(\tau)=\Phi(\tau;\theta)\), so the model no longer directly outputs waypoints, but instead regresses the function parameters that define the entire trajectory segment.
- Use a multimodal large language model as a hypernetwork / hierarchical spectral modulator to generate modulation vectors from image, language, and state context, which modulate a shared SIREN motion prior.
- Use a SIREN implicit neural representation to ensure analytical differentiability and theoretically infinite smoothness of the trajectory, enabling action queries at arbitrary control frequencies.
- Use analytical derivatives to directly supervise velocity, acceleration, and jerk, and feed analytical velocity into the impedance control law, avoiding the noise introduced by numerical differentiation in discrete methods.

## Results
- **CALVIN, ABCD→D**: Under **0.77B, no large-scale robot pretraining**, NIAF achieves **Avg. Len 4.66**, outperforming **BEAST 4.61** and **FLOWER 4.62**, and also exceeding **UniVLA 4.63 (9B, with pretraining)**.
- **CALVIN, ABCD→D**: Success rates for completing **1/2/3** consecutive tasks are **0.997/0.978/0.946**, higher than **BEAST 0.981/0.962/0.930**; however, **5-task** is **0.839**, lower than **FLOWER 0.855** and **BEAST 0.848**.
- **CALVIN, ABC→D**: NIAF reaches **Avg. Len 4.47**, outperforming **FLOWER 4.44**, **BEAST 4.42**, and **UniVLA 4.41**. Its **4-task/5-task** success rates are **0.848/0.764**, higher than **BEAST 0.827/0.744** and **FLOWER 0.823/0.755**.
- The paper claims SOTA on **CALVIN and LIBERO**, and that it scales across different backbones from **Florence-2 to Qwen3-VL**, but the **LIBERO table is truncated** in the provided excerpt, so it is not possible to fully verify all values.
- Real-robot experiments claim that NIAF reduces control jitter in discrete baselines, supports stable impedance control, and improves performance on fine-grained dynamic tasks; however, the excerpt **does not provide real-world quantitative metrics**, only these specific qualitative claims."

## Link
- [http://arxiv.org/abs/2603.01766v1](http://arxiv.org/abs/2603.01766v1)
