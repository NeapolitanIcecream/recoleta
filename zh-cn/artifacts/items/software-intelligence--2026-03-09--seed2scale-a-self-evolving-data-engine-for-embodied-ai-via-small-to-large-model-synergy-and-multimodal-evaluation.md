---
source: arxiv
url: http://arxiv.org/abs/2603.08260v1
published_at: '2026-03-09T11:30:45'
authors:
- Cong Tai
- Zhaoyu Zheng
- Haixu Long
- Hansheng Wu
- Zhengbin Long
- Haodong Xiang
- Rong Shi
- Zhuo Cui
- Shizhuang Zhang
- Gang Qiu
- He Wang
- Ruifeng Li
- Biao Liu
- Zhenzhe Sun
- Tao Shen
topics:
- embodied-ai
- data-engine
- self-evolution
- vision-language-action
- multimodal-evaluation
relevance_score: 0.27
run_id: materialize-outputs
language_code: zh-CN
---

# Seed2Scale: A Self-Evolving Data Engine for Embodied AI via Small to Large Model Synergy and Multimodal Evaluation

## Summary
本文提出 Seed2Scale，一种面向具身智能的自进化数据引擎，用少量种子演示启动，再通过“小模型采集 + 大模型验证 + 目标模型学习”的协同闭环持续扩展高质量训练数据。它试图解决具身 AI 中高质量示教数据稀缺、自动生成数据噪声高且易导致自训练崩溃的问题。

## Problem
- 具身智能的 VLA 模型高度依赖大量高质量专家示范，但人工采集昂贵且难扩展，形成数据瓶颈。
- 现有自动数据生成方法要么只做局部扰动、缺乏真实探索能力，要么存在“embodiment gap”，难把视频知识转成可执行机器人动作。
- 自动收集的轨迹信噪比低，若没有可靠筛选机制，失败轨迹会污染后续训练并在迭代中造成性能退化甚至模型崩塌。

## Approach
- 核心机制很简单：先用一个小型 VLA 模型 **SuperTiny** 从仅 4 条种子示范出发，在并行环境里大量尝试动作、收集候选轨迹。
- 再用冻结的大型视觉语言模型 **Qwen3-VL-32B** 充当验证器，输入任务指令、当前 rollout 视频和参考成功视频，对每条轨迹打 0–10 分，只保留高于阈值的高质量样本。
- 这些筛过的“silver”数据被不断加入训练集，形成自进化闭环；最终目标模型 **SmolVLA** 在该高质量数据上训练，而不是直接依赖未经筛选的自生成数据。
- SuperTiny 采用轻量视觉/语言/状态编码、Transformer 解码和时间集成动作块，以较低推理成本实现稳定控制和大规模探索；SmolVLA 则用 conditional flow matching 学习更复杂的动作分布。

## Results
- 在 4 个 Agibot A2 任务上，仅用每任务 **4 条种子示范**，目标模型平均成功率从 **22.18%** 提升到 **68.57%**，相对提升 **209.15%**。
- 分任务结果：Kitchen Cleanup **24.63% → 71.43%**（**+190.01%**）；Cup-to-Cup Transfer **23.50% → 64.14%**（**+172.94%**）；Can Stacking **7.50% → 65.90%**（**+778.67%**）；Air Fryer Manipulation **33.08% → 72.82%**（**+120.13%**）。
- 与 MimicGen 在 GR-1 任务上比较，Policy Success 平均 **36.00% vs 79.63%**；Replay Success 平均 **34.75% vs 77.41%**，其中 Cylinder Grasp replay 成功率 **21.00% → 86.96%**。
- 论文声称相对 MimicGen，下游策略性能提升为：Cylinder Grasp **+77.18%**，Wheel Manipulation **+168.35%**；说明主动探索 + 多模态验证优于仅做轨迹增强。
- 轨迹质量上，Seed2Scale 更接近人工示范：Total Variation **1.34**（专家 **1.32**，MimicGen **3.68**），Mean Absolute Jerk **0.0047**（专家 **0.0063**，MimicGen **0.0261**），HF Ratio **0.30%**（专家 **0.22%**，MimicGen **2.07%**）。
- SuperTiny 作为采集器具有较高效率：**48M** 参数，推理时间 **38.08ms**，控制频率 **26.3 Hz**；对比 ACT 为 **45.67ms / 21.9 Hz**，Diffusion Policy 为 **135.83ms / 7.4 Hz**。

## Link
- [http://arxiv.org/abs/2603.08260v1](http://arxiv.org/abs/2603.08260v1)
