---
source: arxiv
url: http://arxiv.org/abs/2603.01469v1
published_at: '2026-03-02T05:30:30'
authors:
- Yang Chen
- Xiaoguang Ma
- Bin Zhao
topics:
- vision-language-action
- flow-matching
- one-step-generation
- robot-manipulation
- mean-flow
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Mean-Flow based One-Step Vision-Language-Action

## Summary
This paper proposes a MeanFlow-based one-step Vision-Language-Action framework that changes traditional FlowMatching action generation, which requires multi-step integration, into directly predicting the “mean denoising direction,” thereby significantly reducing robot action generation latency. It targets real-world robotic manipulation and focuses on addressing the efficiency bottleneck of high-frequency continuous action generation in real-time deployment.

## Problem
- Existing FlowMatching-based VLA methods, although more efficient than diffusion policies, still rely on multi-step numerical integration; when the number of steps is reduced, action quality degrades significantly.
- This creates a **latency–accuracy trade-off in real-time control**: making it faster causes distortion, while making it more accurate requires multi-step inference, making it difficult to use for dexterous manipulation.
- This matters for robots because high-frequency, continuous, low-latency action generation directly affects the success rate and stability of real-world tasks such as grasping, stacking, and sorting.

## Approach
- The core idea is to change the learning target from the **instantaneous vector field** in traditional FlowMatching to the **interval-averaged denoising vector field** in MeanFlow; intuitively, instead of moving “step by step along the path,” the model directly predicts the average direction from a noisy action to the target action.
- The model uses a pretrained and frozen VLM backbone to fuse multi-view images, language instructions, and proprioceptive states; the action expert is Transformer-based and conditionally generates future action chunks.
- During training, time pairs \(r,t\) are randomly sampled, and the model learns both local instantaneous information and cross-interval mean flow; the authors introduce `flow-ratio` to control the proportion of the two sample types, balancing local precision and global stability.
- To mitigate training instability caused by the high variance in the MeanFlow objective and multimodal action data, the authors replace the standard \(L_2\) loss with an adaptive loss, improving convergence stability without distillation, pretraining, or consistency regularization.
- During inference, the model can generate in a single step directly: starting from a Gaussian noise action, one forward pass produces the entire continuous action chunk; it also supports few-step generation as a compromise.

## Results
- In real-world robot experiments, the authors claim that this method generates actions **8.7× faster than SmolVLA** and **83.9× faster than Diffusion Policy**.
- Data and platform: 3 real manipulation tasks (pick-place, stacking, sorting), with a total of **300 trajectories**; **100 demonstrations** per task; the robot is an SO-101 with **6-DoF + gripper**; inputs include stereo RGB, language, and proprioceptive states; the action space is **7-dimensional**.
- Hyperparameter experiments (pick-place, **NFE=5**) show that when `flow-ratio=0.2`, the success rate is **84.5%**, better than **80.5%** for `0.5`, and far higher than **4.5%** for `1.0`.
- Loss experiments (`flow-ratio=0.2`, **NFE=5**) show that adaptive loss with `gamma=0.5` achieves a success rate of **86.0%**, better than **79.5%** for `gamma=0.3`, and significantly higher than pure \(L_2\) (`gamma=1.0`) at **9.5%**.
- The abstract explicitly claims robust performance under both **one-step and multi-step generation modes**, but the provided excerpt does not include a complete task success-rate table or more fine-grained quantitative comparisons against SmolVLA / Diffusion Policy for each real-world task.

## Link
- [http://arxiv.org/abs/2603.01469v1](http://arxiv.org/abs/2603.01469v1)
