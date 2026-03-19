---
source: arxiv
url: http://arxiv.org/abs/2603.07909v1
published_at: '2026-03-09T03:09:51'
authors:
- Junyang Wu
- Mingyi Luo
- Fangfang Xie
- Minghui Zhang
- Hanxiao Zhang
- Chunxi Zhang
- Junhao Wang
- Jiayuan Sun
- Yun Gu
- Guang-Zhong Yang
topics:
- robotic-bronchoscopy
- vision-only-navigation
- hierarchical-agents
- world-model
- imitation-learning
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# Long-Short Term Agents for Pure-Vision Bronchoscopy Robotic Autonomy

## Summary
This paper presents a pure-vision hierarchical agent system for autonomous robotic bronchoscopy navigation, relying only on preoperative CT-generated virtual targets and intraoperative endoscopic video, without external localization such as electromagnetic tracking or shape sensing. Its core contribution is combining short-term reactive control, long-term strategic decision-making, and world-model arbitration for long-horizon navigation, and demonstrating near-expert performance in a phantom, ex vivo porcine lungs, and live pigs.

## Problem
- In deep airways with many bifurcations, narrow fields of view, and blur/secretions causing occlusion, robotic bronchoscopy finds it difficult to achieve stable long-horizon navigation using endoscopic images alone.
- Existing systems often rely on electromagnetic tracking or shape sensing, but these external sensors increase hardware complexity and cost, and are affected by CT-to-in vivo anatomical mismatch, respiratory motion, and metal interference.
- The key question is: how can near-human-expert long-distance autonomous bronchoscopy navigation be achieved using vision alone under **no external localization**, which is important for both clinical adoption and robustness?

## Approach
- Segment the airway tree and target lesions from the preoperative CT, plan a path, and render it into a sequence of virtual bronchoscopic views; navigation is converted into a process of stepwise matching to these image subgoals.
- Use a **short-term reactive agent** for high-frequency, low-latency control: it takes the current endoscopic image and current virtual target image as input, encodes them with EfficientNet-B0, and uses a decoder-only Transformer to output discrete actions, including forward, backward, four-direction bending, and “switch to the next target.”
- Use a **long-term strategic agent** that intervenes only at anatomically ambiguous points or during anomalies, combining two forms of guidance: preplanned actions based on the preoperative CT centerline, and high-level semantic suggestions provided by a large multimodal model.
- When the long- and short-term agents produce conflicting actions, introduce a **world-model critic**: it predicts short-term future endoscopic frames for candidate actions, compares the predicted frames with the target virtual view using LPIPS, and selects the action closest to the target.
- Overall training is primarily based on imitation learning, with the goal of learning local manipulation, target switching, and bifurcation decisions in long-sequence navigation from expert demonstrations.

## Results
- **High-fidelity phantom (17 paths covering 17 lung segments)**: the system reached all planned segmental targets, with a mean reached generation of **5.53±1.55**, outperforming **GNM 4.24±1.60** and **ViNT 3.65±1.62**; only the authors’ method and experts could reach airways **beyond the eighth generation**. For endpoint view similarity, the authors’ method achieved **SSIM=0.841±0.066**, higher than **ViNT 0.776±0.044**.
- **Phantom efficiency**: the autonomous system took **450.7±69.5 s**, longer than expert teleoperation at **273.5±77.5 s**, but used fewer actions, at **275.8±31.9 vs. 346.8±45.9** (**P<0.001**). The authors explain that the longer time mainly came from a **3-second safety execution window** per step rather than model inference, which took only **6 ms**.
- **Visual contamination robustness test (5 paths)**: lens contamination reduced the baseline **SSIM between clean and contaminated images to 0.59**; the system still successfully completed **4/5** paths, failing only on the complex **RB2**. Under contamination, the **SSIM** between the endpoint and expert view was **0.874±0.051**, with no significant difference from the clean condition at **0.878±0.033**, but the action count increased to **419.4±72.9** (vs. **270.0±40.4** for clean autonomy).
- **Ex vivo porcine lungs (3 lungs, 59 paths)**: the system maintained a success rate of **>80%** for airways **up to the eighth generation**, with mean time **323.82±123.92 s** and mean action count **198.12±79.34**. Failures mainly resulted from the lens being persistently covered by mucus or bubbles fully obscuring the target lumen.
- **Live pigs (7 targets)**: the system successfully reached **7/7** targets. CBCT measured the mean deviation between its endpoint and that of a senior expert as **4.90±2.64 mm**, on the same scale as the difference between a junior physician and the senior expert at **3.92±2.42 mm**. Endpoint view similarity was **SSIM=0.7701±0.0564**, close to the inter-physician difference of **0.7847±0.0401**.
- **Live pig nodule tasks and efficiency**: in 4 nodule navigation tasks, the system’s minimum distance to the nodules was **6.77–20.55 mm**, with some trajectories outperforming the senior expert (e.g., **Traj 1: 6.77 mm vs. 10.08 mm**). Mean time was **417.1±74.9 s**, longer than the senior expert’s **176.7±52.5 s** (**P=0.016**), but similar to the junior physician’s **334.3±34.7 s**; mean action count was **240.6±28.2**, with no significant difference from the senior expert’s **228.6±24.5** or the junior physician’s **233.3±31.9**.

## Link
- [http://arxiv.org/abs/2603.07909v1](http://arxiv.org/abs/2603.07909v1)
