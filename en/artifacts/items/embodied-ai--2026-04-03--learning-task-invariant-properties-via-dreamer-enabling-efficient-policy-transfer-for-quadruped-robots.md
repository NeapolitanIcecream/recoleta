---
source: arxiv
url: http://arxiv.org/abs/2604.02911v1
published_at: '2026-04-03T09:27:36'
authors:
- Junyang Liang
- Yuxuan Liu
- Yabin Chang
- Junfan Lin
- Junkai Ji
- Hui Li
- Changxin Huang
- Jianqiang Li
topics:
- sim2real-transfer
- quadruped-locomotion
- world-models
- dreamer
- task-invariant-representation
- robot-adaptation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Learning Task-Invariant Properties via Dreamer: Enabling Efficient Policy Transfer for Quadruped Robots

## Summary
DreamTIP improves sim-to-real transfer for quadruped locomotion by teaching a Dreamer world model to predict task-invariant properties such as contact stability and terrain clearance. The paper claims this makes the latent state less tied to simulator-specific dynamics and improves transfer with little real-world adaptation data.

## Problem
- Quadruped policies trained in simulation often fail on real terrain because simulator dynamics, sensing, and contact behavior differ from the real robot.
- Existing transfer methods often depend on manual feature design, wide domain randomization, or expensive real-world fine-tuning.
- World-model policies can still overfit to the simulator's specific dynamics, which hurts transfer on harder or unseen terrain.

## Approach
- Build on Dreamer with an RSSM world model, then add an auxiliary head that predicts Task-Invariant Properties (TIPs) from the latent state.
- Use an LLM to generate a TIP extractor from task descriptions and privileged state inputs; in this paper, the main TIP examples are contact stability and terrain clearance.
- Train the world model with the standard Dreamer loss plus a likelihood term for predicting TIPs, so the latent representation keeps information that should transfer across tasks and dynamics changes.
- Adapt to the real robot with a mixed replay buffer that combines simulation and real trajectories, freeze the recurrent module, and keep the policy frozen.
- Stabilize adaptation by copying the pretrained world model as a frozen reference and adding a negative cosine similarity loss between current and reference stochastic states.

## Results
- The paper reports an average **28.1%** performance improvement across **8 simulated transfer tasks** over baselines.
- On a hard simulated **Crawl** task, baseline **WMP** drops from about **33.51** reward at the easiest level to **5.66** at the hardest, while **DreamTIP** drops from **36.58** to **25.35**.
- The same Crawl comparison is described as an **83.1%** drop for WMP versus **30.6%** for DreamTIP under increasing difficulty.
- In real-world tests on **Unitree Go2**, success rates on **10 trials per task** were: **Stair 16 cm**: WMP **100%**, Ours w/o Adapt **100%**, Ours **100%**; **Climb 52 cm**: WMP **10%**, Ours w/o Adapt **90%**, Ours **100%**; **Tilt 33 cm**: WMP **40%**, Ours w/o Adapt **50%**, Ours **80%**; **Crawl 25 cm**: WMP **70%**, Ours w/o Adapt **80%**, Ours **100%**.
- For TIP design variants in simulation, **DreamTIP-GPT5** beats the other listed TIP sources on several harder settings, including **Climb 61 cm: 22.40 ± 1.70** vs **20.74 ± 1.52** for DeepSeekV3 and **20.42 ± 1.23** for DWL-style supervision, and **Tilt 35 cm: 31.71 ± 1.11** vs **25.79 ± 1.29** and **20.92 ± 1.24**.
- The excerpt does not give full numeric tables for all eight tasks or all baselines, so some claims about state-of-the-art performance rely on summarized statements rather than complete reported comparisons in the provided text.

## Link
- [http://arxiv.org/abs/2604.02911v1](http://arxiv.org/abs/2604.02911v1)
