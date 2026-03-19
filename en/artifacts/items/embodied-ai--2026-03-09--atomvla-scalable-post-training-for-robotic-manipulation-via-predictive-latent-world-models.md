---
source: arxiv
url: http://arxiv.org/abs/2603.08519v1
published_at: '2026-03-09T15:52:48'
authors:
- Xiaoquan Sun
- Zetian Xu
- Chen Cao
- Zonghe Liu
- Yihan Sun
- Jingrui Pang
- Ruijian Zhang
- Zhen Yang
- Kang Pang
- Dingxin He
- Mingqi Yuan
- Jiayu Chen
topics:
- vision-language-action
- world-model
- offline-rl
- robot-manipulation
- long-horizon
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models

## Summary
AtomVLA proposes a two-stage post-training framework for robotic manipulation that uses atomic subtask instructions and latent world-model rewards to improve the stability and generalization of long-horizon tasks. It primarily addresses the problems of insufficient instruction grounding under pure imitation learning, severe error accumulation, and the high cost of online RL.

## Problem
- Existing VLA systems usually use only coarse-grained high-level instructions for supervised fine-tuning, lacking intermediate-step guidance, which leads to error accumulation in long-horizon multi-step manipulation.
- Online RL for robots is costly, risky, and hard to scale in real systems, making it difficult to continue optimizing policies through interaction.
- Pixel-level generative world models often suffer from long-sequence prediction errors and visual hallucinations, making them unreliable for providing stable rewards for offline policy optimization.

## Approach
- A two-stage training process is used: **Stage I** first uses GPT-4o to decompose a high-level task into 2–5 atomic subtasks, then uses both the high-level instruction and subtask instructions together for SFT to strengthen instruction grounding and stage-wise guidance.
- The backbone uses Qwen3-VL-4B-Instruct as the VLM, combined with a cross-attention Diffusion Transformer action head that directly generates action chunks rather than single-step actions.
- **Stage II** uses an action-conditioned latent world model based on V-JEPA2: given the current observation and a candidate action chunk, it predicts the future latent state and scores it by comparing distances to the latent representations of the current subtask boundary frame and the final goal frame.
- The reward consists of three parts: subgoal energy, final-goal energy, and a deviation constraint from expert actions; offline GRPO is then used to perform relative optimization within candidate action groups, with a KL constraint to stay close to the SFT reference policy.
- The core mechanism can be understood simply as: first break a complex task into small steps to teach the model “what it should do now,” then let the world model evaluate in latent space “whether this sequence of actions gets closer to the current subgoal and final goal,” and use that signal to reinforce better actions offline.

## Results
- On **LIBERO**, AtomVLA achieves an average success rate of **97.0%**; category results are Spatial **96.4%**, Object **99.6%**, Goal **97.6%**, and Long **94.4%**. For comparison, NORA-1.5 achieves an average of **94.5%**, π0 **94.2%**, and CoT-VLA **83.9%**.
- On the more difficult **LIBERO-PRO**, AtomVLA achieves an average success rate of **0.48 (48%)**, outperforming π0 at **0.45**, X-VLA at **0.46**, MolmoAct at **0.41**, and NORA at **0.39**.
- The authors state that **post-training consistently brings gains**: relative to the SFT baseline (LIBERO average **93.0%**), using only subgoal reward reaches **96.0%**, using only final-goal reward reaches **96.1%**, and the full reward reaches **97.0%**, for an overall improvement of about **4.0%**; on the Long subset, performance improves from **90.0%** to **94.4%**, a gain of **4.4%**.
- Subtask instructions are indeed important: on LIBERO-Long, image-only input achieves **80.4%**; image + high-level task instruction achieves **90.0%**; adding atomic subtask instructions further raises performance to **92.2%**.
- Action chunk size ablations show that **4 steps** works best: average **97.0%**, better than **96.6%** for 8 and 16 steps and **96.3%** for 32 steps; on the Long subset, 4 steps reaches **94.4%**, clearly higher than **91.2%** for 32 steps.
- On six real-world tasks with the Galaxea R1 Lite, AtomVLA averages **66.7%** under the standard setting, close to π0’s **65.8%**; but under the generalization setting, AtomVLA reaches **47.5%**, significantly higher than π0’s **29.2%**, an absolute improvement of **18.3%**. For example, Fold T-shirt improves from **5%** to **25%**, and Fold towel from **20%** to **35%**.

## Link
- [http://arxiv.org/abs/2603.08519v1](http://arxiv.org/abs/2603.08519v1)
