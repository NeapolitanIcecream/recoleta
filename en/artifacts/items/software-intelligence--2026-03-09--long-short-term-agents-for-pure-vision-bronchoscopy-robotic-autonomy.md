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
- medical-robotics
relevance_score: 0.29
run_id: materialize-outputs
language_code: en
---

# Long-Short Term Agents for Pure-Vision Bronchoscopy Robotic Autonomy

## Summary
This paper proposes a **pure-vision** autonomous robotic bronchoscopy navigation system that relies only on preoperative CT-generated virtual target images and intraoperative endoscopic video, without requiring electromagnetic localization or shape sensors. Its core consists of hierarchical long-short agents plus a world-model arbiter, demonstrating long-horizon navigation capability in a phantom, ex vivo porcine lungs, and a live porcine model.

## Problem
- Target problem: achieving **long-range, intraoperative autonomous navigation** in robotic bronchoscopy, while traditional methods often depend on external localization hardware, increasing complexity and cost and being affected by CT-to-body mismatch, respiratory motion, and metal interference.
- Pure-vision control is attractive because the endoscope itself already provides real-time images; however, the bronchial tree has a narrow field of view, repetitive structures, deformable tissue, and artifacts such as fluid occlusion and blur, making long-horizon closed-loop control very difficult.
- This matters because eliminating external sensors could make robots simpler, cheaper, and closer to autonomous endoluminal navigation in real clinical settings.

## Approach
- Uses **hierarchical long-short agents**: the short-term agent handles high-frequency, low-latency continuous motion control; the long-term agent intervenes only at key decision points such as bifurcations or abnormal situations, providing strategic guidance.
- The short-term agent uses a lightweight vision Transformer: it takes the current endoscopic frame and current virtual target frame as input, and outputs actions including forward, backward, four-direction bending, and “switch to the next subgoal”; it is trained through imitation learning from expert demonstrations.
- The long-term agent combines two information sources: one is **preplanned guidance** from the preoperative CT centerline, and the other is **semantic-level guidance** from a large multimodal model, used in visually ambiguous or anatomically uncertain scenarios.
- If the two agents agree, the action is executed directly; if they conflict, a **world-model critic** predicts short-term future images for candidate actions and uses LPIPS to compare the similarity between the “predicted future view” and the “target virtual view,” selecting the best-matching action.
- Overall navigation is decomposed into a sequence of image subgoals, and the robot gradually advances to the distal target segment by continuously aligning the current view with the virtual target view.

## Results
- **High-fidelity airway phantom (17 trajectories covering 17 lung segments)**: the authors’ method reached **all planned segmental targets** and, like the expert, was one of the only approaches able to go beyond the **8th-generation bronchi**; mean reached generation was **5.53±1.55**, better than **GNM 4.24±1.60** and **ViNT 3.65±1.62**.
- In the phantom, compared with the expert, the authors’ method was **slower but used fewer actions**: total time **450.7±69.5 s** vs. expert **273.5±77.5 s**; number of actions **275.8±31.9** vs. expert **346.8±45.9**, with a statistically significant reduction in actions (**P<0.001**). The paper explains that the main slowdown comes from a mandatory **3-second safety window** at each step rather than inference, since model inference takes only **6 ms**.
- Compared with ViNT, which shares a similar low-level network backbone, the authors’ method achieved higher end-view similarity: **SSIM 0.841±0.066** vs. **0.776±0.044**, indicating that the improvement mainly comes from the hierarchical multi-agent mechanism rather than just the network backbone.
- **Robustness test under visual contamination**: succeeded on **4/5** trajectories with glycerol-contaminated lenses; under contamination, the number of actions increased to **419.4±72.9** (vs. **270.0±40.4** for autonomous navigation in clean conditions), and time was **385.5±73.6 s**; however, endpoint quality remained stable, with **SSIM 0.874±0.051** under contamination versus **0.878±0.033** in clean conditions, with no statistically significant difference.
- **Ex vivo porcine lungs (3 lungs, 59 trajectories)**: the system maintained **over 80% success rate within the 8th-generation bronchi**; mean time was **323.82±123.92 s**, and mean number of actions was **198.12±79.34**. Failures mainly came from persistent mucus or bubbles adhering to the lens and completely occluding the target lumen.
- **Live porcine model (7 tasks)**: the system succeeded in **7/7 (100%)** reaching the targets; relative to the expert physician, endpoint CBCT spatial deviation was **4.90±2.64 mm**, on the same order as the expert–novice physician difference of **3.92±2.42 mm**; endpoint view similarity was **SSIM 0.7701±0.0564**, close to the inter-physician value of **0.7847±0.0401**. In 4 nodule tasks, the system’s minimum distance to the nodules was **6.77–20.55 mm**, with some trajectories outperforming the expert physician (e.g., **Traj 1: 6.77 mm vs. 10.08 mm**). In terms of time, the system took **417.1±74.9 s**, slower than the expert physician’s **176.7±52.5 s (P=0.016)**, but close to the novice physician’s **334.3±34.7 s (P=0.109)**; the number of actions, **240.6±28.2**, showed no significant difference from the expert’s **228.6±24.5** or the novice’s **233.3±31.9**.

## Link
- [http://arxiv.org/abs/2603.07909v1](http://arxiv.org/abs/2603.07909v1)
