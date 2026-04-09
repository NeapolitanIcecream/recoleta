---
source: arxiv
url: http://arxiv.org/abs/2603.28740v1
published_at: '2026-03-30T17:50:54'
authors:
- Yichi Zhang
- Weihao Yuan
- Yizhuo Zhang
- Xidong Zhang
- Jia Wan
topics:
- vision-language-action
- robot-manipulation
- attention-mechanism
- dexterous-manipulation
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# FocusVLA: Focused Visual Utilization for Vision-Language-Action Models

## Summary
FocusVLA is a vision-language-action model for robotic manipulation that improves how the policy uses visual tokens during action generation. It targets fine-grained manipulation failures in auto-regressive VLA policies by forcing attention onto task-relevant image regions and filtering irrelevant visual content.

## Problem
- Existing auto-regressive VLA policies often miss fine visual details needed for precise manipulation because their attention structure lets the policy rely on action-query shortcuts instead of image evidence.
- Large numbers of visual tokens spread attention too thin, and background content adds noise, which reduces action accuracy.
- The paper argues that performance is limited more by visual utilization than by the raw quality of the visual representation itself, which matters for building stronger robot foundation models without only scaling encoders.

## Approach
- FocusVLA replaces mixed attention with **Modality Cascaded Attention**. The action latent attends to self state, action-query features, and visual features separately, then fuses them. This removes the shortcut where the model can ignore visual details.
- It adds **Patch-level Focus**: keep only top-K visual patches selected by action-to-vision attention scores, so the policy uses the most task-relevant image regions.
- It adds **Channel-level Focus**: apply an element-wise gate on visual attention outputs to suppress noisy feature channels while keeping useful ones.
- For vision values, it uses shallow visual backbone features for fine spatial detail, while deeper VLM features guide which regions matter.
- The paper also runs controlled comparisons across attention structures and visual representations to show that regulating visual use matters more than swapping encoders.

## Results
- On **LIBERO, multi-weight setting**, FocusVLA reaches **98.7% average success rate** with **0.5B parameters**, compared with **98.5%** for **VLA-Adapter-Pro (0.5B)**, **98.5%** for **Spatial Forcing (7B)**, **98.1%** for **X-VLA (0.9B)**, and **97.1%** for **OpenVLA-OFT (7B)**.
- On **LIBERO, single-weight setting**, FocusVLA gets **97.0% average success rate**, beating **VLA-Adapter-Pro: 95.6%**, **EVO-1: 94.8%**, **NORA-1.5: 95.0%**, and **Pi0.5: 96.9%**.
- In the LIBERO multi-weight breakdown, FocusVLA reports **99.6 Spatial**, **100.0 Object**, **98.8 Goal**, and **96.2 Long**. Against VLA-Adapter-Pro, that is **+0.0**, **+0.4**, **+0.6**, and **-0.2** points respectively.
- In an ablation on LIBERO, switching from **mixed attention** to **cascaded attention** with VLM features and no gate improves average success from **93.6%** to **97.0%**; suite scores move from **94.4/95.6/93.2/91.0** to **98.0/98.6/96.2/95.0** on Spatial/Object/Goal/Long.
- The paper claims training converges faster: **1.5x overall speedup** versus VLA-Adapter on LIBERO, and **5x speedup** on **LIBERO-Spatial**.
- For **RoboTwin**, the excerpt gives qualitative claims that FocusVLA outperforms Diffusion Policy, pi0, and VLA-Adapter, especially on fine-grained tasks such as **Hugging Mug**, but the provided text does not include task-by-task numbers.

## Link
- [http://arxiv.org/abs/2603.28740v1](http://arxiv.org/abs/2603.28740v1)
