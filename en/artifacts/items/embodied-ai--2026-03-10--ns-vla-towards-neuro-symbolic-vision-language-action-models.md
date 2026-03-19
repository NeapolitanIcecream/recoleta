---
source: arxiv
url: http://arxiv.org/abs/2603.09542v1
published_at: '2026-03-10T11:51:54'
authors:
- Ziyue Zhu
- Shangyang Wu
- Shuai Zhao
- Zhiqiu Zhao
- Shengjie Li
- Yi Wang
- Fang Li
- Haoran Luo
topics:
- vision-language-action
- neuro-symbolic-ai
- robot-manipulation
- online-reinforcement-learning
- data-efficient-learning
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# NS-VLA: Towards Neuro-Symbolic Vision-Language-Action Models

## Summary
NS-VLA is a vision-language-action model for robotic manipulation that combines neural perception, symbolic action primitives, and online reinforcement learning. Its goal is to achieve stronger generalization, robustness, and exploration capability with less demonstration data.

## Problem
- Existing end-to-end VLA models often regress actions directly from images and instructions, lacking explicit structural modeling of reusable action primitives, which leads to weaker long-horizon and compositional generalization.
- Many methods rely on large models, complex architectures, and large amounts of demonstration data, but in real robotics it is impractical to collect massive numbers of demonstrations for every task.
- Pure supervised imitation usually only reproduces demonstration trajectories and struggles to actively explore in the environment, which limits both performance ceilings and robustness.

## Approach
- First, a frozen pretrained VLM encodes images and language, then generates a task plan composed of discrete primitives; afterward, a symbolic classifier predicts which primitive is currently being executed.
- Through a "plan constraint + monotonic pointer" mechanism, primitives are only allowed to stay at the current step or move forward according to the plan order. Intuitively, this makes execution proceed step by step more stably, reducing oscillation and erroneous switching.
- A symbolic solver converts the current primitive into actions: it first selects only the most relevant visual tokens for that primitive (Top-K sparsification), then combines them with the embodiment state and uses a Transformer to output an action chunk in one shot, rather than densely predicting at every step.
- In the online reinforcement learning stage, only lightweight modules are updated while the backbone VLM remains unchanged; the reward includes task success, primitive segment-switching milestones, and within-segment progress shaping, and KL regularization keeps the policy close to the behavior cloning policy to stabilize training.

## Results
- **LIBERO 1-shot (only 1 demonstration per task)**: NS-VLA achieves an average success rate of **69.1%** with 2B parameters, outperforming VLA-Adapter **65.3%**, EVOLVE-VLA **61.3%**, UniVLA **55.1%**, OpenVLA-OFT **48.9%**, and OpenVLA **35.7%**.
- On the same 1-shot LIBERO benchmark, NS-VLA scores **Spatial 85.7% / Object 75.3% / Goal 70.7% / Long 45.2%** across the subsets, clearly higher than 7B OpenVLA's **47.4 / 46.0 / 44.3 / 4.9** and 3B π0's **48.6 / 47.2 / 33.2 / 20.4**.
- **LIBERO-Plus generalization test (trained on full LIBERO, tested in perturbed environments)**: NS-VLA reaches an average success rate of **79.4%**, surpassing OpenVLA-OFT **69.6%**, RIPT-VLA **68.4%**, π0-Fast **61.6%**, VLA-Adapter **58.9%**, and OpenVLA **15.6%**.
- On LIBERO-Plus, NS-VLA scores **88.1 / 79.0 / 70.2 / 80.3** on the four task categories, with an average performance drop of only **19.2** points; compared with OpenVLA-OFT **27.5**, RIPT-VLA **25.2**, and π0-Fast **23.9**, this indicates stronger robustness under perturbations.
- **Ablation (LIBERO average SR)**: full NS-VLA reaches **98.6%**; removing plan constraints drops it to **79.7%**, removing the visual extractor gives **90.1%**, removing the action generator gives **85.2%**, and removing RL gives **91.6%**; this shows that both plan constraints and RL are key components.
- The paper also claims validated performance on CALVIN, stronger robustness in perturbed scenarios, and a larger exploration space, but the provided excerpt does not include specific CALVIN numbers.

## Link
- [http://arxiv.org/abs/2603.09542v1](http://arxiv.org/abs/2603.09542v1)
