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
- robot-manipulation
- flow-matching
- one-step-generation
- mean-flow
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# Mean-Flow based One-Step Vision-Language-Action

## Summary
This paper proposes a Mean-Flow one-step Vision-Language-Action framework for robotic manipulation, replacing traditional FlowMatching action generation that requires multi-step integration with mean vector field prediction that can be completed in a single step, thereby significantly reducing latency. Its core value is improving VLA control speed to a level better suited for real-time robotic applications while maintaining action quality and stability as much as possible.

## Problem
- Existing FlowMatching/diffusion-style VLAs can generate continuous, high-frequency actions, but inference typically depends on multi-step iterative sampling, resulting in high control latency for robots.
- When FlowMatching reduces the number of inference steps, Euler integration error is amplified, actions drift toward the data mean, and quality degrades significantly, creating a hard tradeoff between speed and accuracy.
- This is critical for dexterous manipulation and real-time control, because robots must respond quickly to new visual inputs while maintaining continuous, stable, and executable trajectories.

## Approach
- The core idea is to change the learning target from an **instantaneous denoising vector field** to an **average denoising vector field over an interval (mean vector field)**, i.e., directly learning the overall direction from noise to action rather than the local direction at each tiny time step.
- During training, the method introduces the MeanFlow Identity, uses the network to predict the mean vector field, and supervises it with a target constructed from the instantaneous field and a time-derivative correction term; in implementation, JVP is used to compute the derivative term, and stop-gradient is used to avoid instability from higher-order backpropagation.
- During inference, an action chunk can be generated directly in one step: starting from a noisy action $A_1$, compute $A_0 = A_1 - u_\theta(A_1,0,1)$, thus eliminating traditional multi-step numerical integration.
- In the VLA architecture, a pretrained VLM (SmolVLM-2) is frozen as the multimodal encoder, and only a Transformer-based Mean-Flow action expert is trained to output future action chunks.
- The paper also includes key training design choices: mixing learning of the instantaneous field and mean field (flow-ratio), and using adaptive loss instead of pure $L_2$ to improve convergence stability.

## Results
- Real-robot experiments claim that this method generates actions **8.7× faster than SmolVLA** and **83.9× faster than Diffusion Policy**.
- In hyperparameter experiments, **flow-ratio=0.2** and **NFE=5** achieved the best success rate at **84.5%**; by comparison, flow-ratio=0.5 achieved **80.5%**, and flow-ratio=1.0 achieved only **4.5%**.
- In loss-function experiments, adaptive loss with **$\gamma=0.5$** was best, with a success rate of **86.0%**; **$\gamma=0.3$** achieved **79.5%**, while pure **$L_2$** (**$\gamma=1.0$**) achieved only **9.5%**.
- The experimental platform was a 6-DoF SO-101 robotic arm, covering **3 real-world tasks** (pick-place, stacking, sorting), with **300 total trajectories** and **100 demonstrations per task**.
- The abstract and main text explicitly claim robust performance under **one-step or few-step generation**, but the provided excerpt does not include the full task-by-task success-rate tables relative to SmolVLA / Diffusion Policy, so a complete numerical accuracy comparison cannot be listed item by item.

## Link
- [http://arxiv.org/abs/2603.01469v1](http://arxiv.org/abs/2603.01469v1)
