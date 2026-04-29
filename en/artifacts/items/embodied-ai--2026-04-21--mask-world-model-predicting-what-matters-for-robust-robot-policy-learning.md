---
source: arxiv
url: http://arxiv.org/abs/2604.19683v2
published_at: '2026-04-21T17:05:37'
authors:
- Yunfan Lou
- Xiaowei Chi
- Xiaojie Zhang
- Zezhong Qian
- Chengxuan Li
- Rongyu Zhang
- Yaoxu Lyu
- Guoyu Song
- Chuyao Fu
- Haoxuan Xu
- Pengwei Wang
- Shanghang Zhang
topics:
- world-model
- robot-policy-learning
- vision-language-action
- semantic-masks
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Mask World Model: Predicting What Matters for Robust Robot Policy Learning

## Summary
Mask World Model replaces RGB video prediction with future semantic mask prediction so a robot world model learns object geometry and contact dynamics instead of texture and lighting. The paper claims this makes policy learning more robust and improves success rates in simulation and on a real robot while still using raw RGB at test time.

## Problem
- Standard robot world models often predict future RGB frames, which pushes capacity toward texture, lighting, reflections, and background changes that do not help action selection.
- Those appearance factors can cause predictive drift in closed-loop control, which hurts generalization and makes policies fragile under visual shifts.
- A useful robot policy needs features tied to object identity, spatial layout, and contact-relevant motion, especially for long-horizon manipulation.

## Approach
- MWM trains a world model to predict future **semantic masks** instead of future pixels. The masks cover task-relevant objects and the robot, creating a geometric bottleneck that drops photometric noise.
- Training has two stages. Stage 1 learns mask dynamics with a diffusion / flow-matching backbone conditioned on past multi-view RGB and language. Stage 2 trains a diffusion policy head that reads the backbone's predictive features and outputs actions.
- Semantic masks are used only as offline supervision during training. At inference, the system takes raw multi-view RGB plus language and does not require an external segmentation model.
- The model reuses a shared video VAE for both RGB frames and rendered mask images, then uses transformer features from the mask-prediction backbone as the policy context.

## Results
- On **LIBERO**, MWM reports **98.3% average success rate**, beating **GE-ACT at 96.5%**, **pi0 at 94.2%**, **CogACT at 93.6%**, **Cosmos w/ Latent IDM at 91.9%**, and **OpenVLA at 76.5%**.
- On the harder **LIBERO-10** subset, MWM reaches **96.0%**, compared with **94.4% for GE-ACT**, **85.2% for pi0**, **84.2% for Cosmos w/ Latent IDM**, and **48.8% for Cosmos w/ IDM**.
- The mask-based ablations support the main claim: **MWM-C1** improves over **Cosmos w/ IDM** from **67.5% to 81.0% average SR**; **MWM-C2** improves over **Cosmos w/ Latent IDM** to **91.8% average SR**.
- On **RLBench**, MWM reports **68.3% average success rate**, ahead of **FiS-VLA at 50.0%**, **CogACT at 42.5%**, **GE-ACT at 30.8%**, **pi0 at 33.3%**, and **OpenVLA at 23.3%**.
- The paper also states **67.5% average success** on a real **Franka** robot across four tasks and says MWM handles background, lighting, object-color shifts, and random token pruning better than RGB-based baselines.
- Quantitative robustness details for the real-world OOD tests are only partially visible in the provided excerpt, so the strongest complete claims are the benchmark success-rate gains above.

## Link
- [http://arxiv.org/abs/2604.19683v2](http://arxiv.org/abs/2604.19683v2)
