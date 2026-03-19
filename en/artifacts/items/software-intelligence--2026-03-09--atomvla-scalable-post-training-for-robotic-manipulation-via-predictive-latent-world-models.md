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
- robotic-manipulation
- vision-language-action
- world-models
- offline-rl
- long-horizon-control
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models

## Summary
AtomVLA is a two-stage post-training framework for robotic manipulation, designed to improve the stability and generalization of vision-language-action models on long-horizon, multi-step tasks. Its core idea is to decompose high-level instructions into atomic subtasks and use a latent world model to evaluate action candidates offline for RL post-training.

## Problem
- Existing VLA models typically use only coarse-grained high-level task instructions during supervised fine-tuning, lacking intermediate step guidance, which leads to compounding errors in long-horizon tasks.
- Online reinforcement learning requires real robot interaction or expensive simulation, making it costly, risky, and difficult to scale for policy improvement.
- Pixel-level generative world models are prone to autoregressive errors and visual hallucinations in long-sequence prediction, undermining the reliability of offline post-training.

## Approach
- Use GPT-4o to automatically decompose each high-level demonstration trajectory into 2-5 atomic subtasks, and feed these subtask instructions together with the original high-level instruction into the model for SFT to enhance instruction grounding and stage-wise guidance.
- The main model uses Qwen3-VL-4B-Instruct as the vision-language backbone, paired with a cross-attention Diffusion Transformer action head that directly predicts an action chunk rather than a single-step action.
- In the post-training stage, it uses an action-conditioned latent world model based on V-JEPA2: given the current observation and a candidate action segment, it predicts future latent states and scores them by comparing distances to the latent representations of the "subtask boundary frame" and the "final goal frame."
- The reward consists of three components: subgoal energy, final-goal energy, and a deviation penalty from expert actions, thereby both encouraging progress toward the goal and avoiding reward hacking and drifting too far from demonstrations.
- Offline GRPO is used to compare multiple candidate action segments on the same offline demonstration data, updating only the action head and adding a KL constraint to the SFT reference policy to stably improve long-horizon decision-making.

## Results
- On **LIBERO**, AtomVLA achieves an average success rate of **97.0%**; the category breakdown is **Spatial 96.4% / Object 99.6% / Goal 97.6% / Long 94.4%**. Compared with its **SFT baseline of 93.0%**, full post-training improves performance by **4.0 percentage points**; on the **Long** suite, the improvement is **4.4 percentage points** (**90.0% → 94.4%**).
- Compared with prior methods, AtomVLA's **LIBERO average of 97.0%** exceeds **π0's 94.2%**, **NORA-1.5's 94.5%**, **CoT-VLA's 83.9%**, and **OpenVLA's 76.5%**, indicating that SOTA-level results can be achieved without large-scale cross-embodiment pretraining.
- On the more challenging **LIBERO-PRO**, AtomVLA achieves an average success rate of **0.48 (48.0%)**, higher than **X-VLA 0.46**, **π0 0.45**, **MolmoAct 0.41**, and **NORA 0.39**, indicating greater robustness under perturbations and distribution shift.
- Subtask instructions are indeed effective: on **LIBERO-Long**, image-only input achieves **80.4%**; adding high-level task instructions raises it to **90.0%**; adding atomic subtask instructions further improves it to **92.2%**.
- An action chunk size of **4** works best: on LIBERO it averages **97.0%**, outperforming chunk=**8/16** at **96.6%** and chunk=**32** at **96.3%**.
- On six real-world tasks with the Galaxea R1 Lite, under the standard setting AtomVLA averages **66.7%**, close to **π0's 65.8%**; but under the generalization setting, AtomVLA reaches **47.5%**, significantly higher than **π0's 29.2%**, an absolute gain of **18.3 percentage points**. Among these, folding a T-shirt is **25% vs 5%**, and folding a towel is **35% vs 20%**.

## Link
- [http://arxiv.org/abs/2603.08519v1](http://arxiv.org/abs/2603.08519v1)
