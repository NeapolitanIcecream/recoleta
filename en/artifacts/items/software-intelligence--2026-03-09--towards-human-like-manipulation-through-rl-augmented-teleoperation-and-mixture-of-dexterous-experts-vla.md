---
source: arxiv
url: http://arxiv.org/abs/2603.08122v1
published_at: '2026-03-09T09:02:30'
authors:
- Tutian Tang
- Xingyu Ji
- Wanli Xing
- Ce Hao
- Wenqiang Xu
- Lin Shao
- Cewu Lu
- Qiaojun Yu
- Jiangmiao Pang
- Kaifeng Zhang
topics:
- robotic-manipulation
- vision-language-action
- dexterous-manipulation
- multimodal-fusion
- reinforcement-learning
relevance_score: 0.26
run_id: materialize-outputs
language_code: en
---

# Towards Human-Like Manipulation through RL-Augmented Teleoperation and Mixture-of-Dexterous-Experts VLA

## Summary
This paper proposes an integrated framework for human-like bimanual dexterous manipulation: it uses RL-trained IMCopilot to assist teleoperation and serve as low-level skills, and then uses MoDE-VLA to integrate force/tactile sensing into a pretrained VLA through residual experts. Targeting three major bottlenecks in high-DoF, contact-rich in-hand manipulation—difficulty of data collection, difficulty of unifying skills, and difficulty of multimodal fusion—it claims significant improvements over the baseline across four tasks.

## Problem
- Existing VLA models are mainly suited to low-DoF grippers and vision-dominant pick-and-place, and are difficult to extend to 63-DoF human-like bimanual dexterous manipulation, especially contact-rich in-hand manipulation.
- This matters because real tasks such as apple peeling, insertion, and assembly require bimanual coordination, continuous contact regulation, tactile/force feedback, and hierarchical skill control; vision alone and a single policy are often insufficient.
- The key challenges are: high-quality demonstration data is hard to collect, a single policy struggles to cover both coarse motion and fine in-hand skills, and directly concatenating force/tactile inputs into a pretrained VLA may damage its existing capabilities.

## Approach
- Proposes **IMCopilot**: a set of atomic in-hand skills trained with PPO in simulation, such as stable grasping and rotating an object around a specified axis. In the simplest terms, it acts like an “autopilot copilot”: the human handles large motions, while difficult finger coordination is delegated to RL skills.
- IMCopilot has a dual purpose: during data collection, the operator triggers it with a foot pedal to help complete in-hand phases that are hard to teleoperate directly; during autonomous execution, the VLA outputs a trigger signal to call these low-level skills, forming hierarchical control.
- Proposes **MoDE-VLA**: instead of crudely appending sensor inputs to the pretrained VLA, it builds separate token pathways for arm torques and fingertip tactile signals, then injects them as residual corrections into action prediction after self-attention and sparse MoE expert routing.
- Its core mechanism can be summarized as: vision/language/proprioception are responsible for “understanding the task and overall direction,” while force/tactile experts are responsible only for “making small corrections at moments of contact,” and they separately affect arm and hand actions according to physical semantics, thereby minimizing disruption to pretrained knowledge.

## Results
- In the comparison of in-hand manipulation ability, **IMCopilot clearly outperforms pure teleoperation**: ping-pong ball **25/30=83% vs 3/30=10%**, tennis ball **28/30=93% vs 20/30=67%**, apple **27/30=90% vs 8/30=27%**, overall **80/90=89% vs 31/90=34%**.
- The abstract claims that on four contact-rich dexterous tasks of increasing complexity, the method achieves a **doubled success rate improvement** relative to the baseline, where the baseline is a pretrained **π0/OpenPI-0**-style VLA; however, the current excerpt does not provide a complete per-task numerical table.
- The evaluation covers **4 tasks**: gear assembling, charger plugging, test tube rearranging, and apple peeling; each method is tested for **20 trials per task**, with the main metric being **Success Rate (SR)**, and apple peeling also reporting **Peel Completion Ratio (PCR)** discretized at **25%** granularity.
- The system operates on a real robot with **63 DoF**, and uses **10 fingertip tactile sensors (60-dimensional tactile input)** and **14-dimensional dual-arm joint torques** as additional modalities; this supports its strong claim of “the first autonomous dual-dexterous-hand apple peeling.”
- In terms of training/implementation, MoDE uses **8 experts, top-k=1**, with action prediction horizon **H=50** and inference denoising **N=10**; these are not performance metrics, but they reflect the method’s specific engineering configuration.
- The excerpt does not provide full detailed quantitative results or ablation values for all tasks against all baselines, so the strongest explicit quantitative evidence is the above **IMCopilot 89% vs 34%** in-hand manipulation success-rate gain, together with the abstract’s overall statement of a “**doubled task success rate**.”

## Link
- [http://arxiv.org/abs/2603.08122v1](http://arxiv.org/abs/2603.08122v1)
