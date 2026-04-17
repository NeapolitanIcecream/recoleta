---
source: arxiv
url: http://arxiv.org/abs/2604.05672v3
published_at: '2026-04-07T10:18:40'
authors:
- Kaidong Zhang
- Jian Zhang
- Rongtao Xu
- Yu Sun
- Shuoshuo Xue
- Youpeng Wen
- Xiaoyu Guo
- Minghao Guo
- Weijia Liufu
- Liu Zihou
- Kangyi Ji
- Yangsong Zhang
- Jiarun Zhu
- Jingzhi Liu
- Zihang Li
- Ruiyi Chen
- Meng Cao
- Jingming Zhang
- Shen Zhao
- Xiaojun Chang
- Feng Zheng
- Ivan Laptev
- Xiaodan Liang
topics:
- vision-language-action
- generalist-robot-policy
- adaptive-inference
- flow-matching
- robot-data-scaling
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# A1: A Fully Transparent Open-Source, Adaptive and Efficient Truncated Vision-Language-Action Model

## Summary
A1 is an open-source vision-language-action model for robot manipulation that targets lower inference cost without giving up much task success. Its main idea is to stop the backbone early when actions have stabilized and to cut flow-matching denoising work by reusing the previous layer's partial action.

## Problem
- Vision-language-action models for robot control often use large vision-language backbones plus diffusion or flow-based action heads, which makes real-time deployment slow and expensive.
- Speedups that only shorten the backbone leave the action head as a bottleneck, especially when action generation needs 10 to 20 denoising steps.
- This matters for robot manipulation because control loops need low latency on practical hardware, not only high benchmark accuracy.

## Approach
- A1 combines a pretrained Molmo-based VLM backbone with either a flow-matching action head (`A1-FM`) or a simpler MLP action head (`A1-MLP`).
- During training, it supervises actions from intermediate backbone layers, so the model can produce usable actions before the full stack runs.
- At inference, it compares the action predicted at the current layer with the previous layer. If the difference is below a calibrated threshold, it exits early.
- For flow matching, it introduces **Inter-Layer Truncated Flow Matching**: run only a small number of denoising steps per layer, such as 2, and warm-start the next layer from the current layer's predicted action instead of restarting from random noise.
- It is pretrained on several open robot datasets including DROID, AgiBot, RoboCOIN, RoboMind, GM-100, and RoboChallenge, plus 15,951 in-house trajectories across multiple robots.

## Results
- On **RoboChallenge**, A1 reports **29.00%** average success, above **pi_0: 28.33%**, **X-VLA: 21.33%**, and **RDT-1B: 15.00%**.
- On real robots across **Franka, AgiBot, OpenArm, and Dobot-Arm**, A1 reports **56.7%** mean success rate. The excerpt says this is above baselines, but it does not include the baseline numbers in the shown text.
- On **LIBERO**, A1 reports **96.6%** average success. In the shown table, this is above **pi_0: 94.2%**, below **OpenVLA-OFT: 97.1%**, and near **pi_0.5: 96.9%**.
- On **VLABench**, A1 reports **53.5%** average success. In the shown table, this is above **pi_0: 42.0%** and **pi_0.5: 49.5%**.
- For efficiency, the paper claims **up to 72% lower per-episode latency** for flow-matching inference and **up to 76.6% backbone computation reduction** with minor performance loss.
- A concrete latency example in the text is **37.8s to 10.5s per episode on LIBERO** for flow-matching inference under their setup.

## Link
- [http://arxiv.org/abs/2604.05672v3](http://arxiv.org/abs/2604.05672v3)
