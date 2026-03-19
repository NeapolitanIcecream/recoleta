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
- robotic-manipulation
- reinforcement-learning
- data-efficient-learning
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# NS-VLA: Towards Neuro-Symbolic Vision-Language-Action Models

## Summary
NS-VLA提出一种把神经感知、符号原语推理和在线强化学习结合起来的视觉-语言-动作框架，用于机器人操作。核心目标是在更少演示数据下获得更强的泛化、鲁棒性和探索能力。

## Problem
- 现有VLA常用端到端方式直接从图像和指令回归动作，难以显式学习可复用的操作原语，因此长程任务和跨任务泛化较弱。
- 许多方法依赖大模型和大规模示范数据，但为每个机器人任务收集高质量演示代价很高，限制实际落地。
- 纯模仿学习主要复现演示轨迹，缺少在线探索能力，难以在扰动环境或未见情形下持续改进。

## Approach
- 用预训练VLM先编码视觉与语言，再生成一条由离散符号原语组成的计划；执行时用带单调约束的符号分类器判断当前处于哪个原语阶段。
- 用符号求解器把“当前原语”转成动作：先根据原语对视觉token做Top-K稀疏选择，只保留相关区域，再用因果Transformer输出一段连续动作chunk，而不是逐步密集回归。
- 在线训练阶段冻结VLM主干，只更新轻量模块，通过分段奖励、进度塑形和KL约束下的GRPO进行强化学习，鼓励超越示范的探索同时减少策略漂移。
- 整体上，方法可以简单理解为：先把任务拆成“拿、放、开、关”等可复用小步骤，再只关注当前相关视觉区域，并用RL让这些步骤在真实交互中变得更稳更强。

## Results
- 在LIBERO 1-shot训练（每任务仅1条演示）下，NS-VLA以**69.1% Avg. SR**领先：高于VLA-Adapter的**65.3%**、EVOLVE-VLA的**61.3%**、UniVLA的**55.1%**、OpenVLA-OFT的**48.9%**、OpenVLA的**35.7%**；模型规模为**2B**，小于多种**7B**基线。
- 在同一1-shot设置下，NS-VLA各子集SR分别为**85.7 / 75.3 / 70.7 / 45.2**（Spatial/Object/Goal/Long），对应优于VLA-Adapter的**80.6 / 71.6 / 69.8 / 39.2**，尤其长程任务提升约**6.0**个百分点。
- 相比其全量数据训练版本，NS-VLA在1-shot下平均仅下降**29.5**个百分点，优于VLA-Adapter的**33.2**、EVOLVE-VLA的**34.5**、UniVLA的**40.1**、OpenVLA-OFT的**48.2**、π0的**56.8**，支撑其“高数据效率”主张。
- 在LIBERO-Plus泛化测试（全LIBERO训练）上，NS-VLA达到**79.4% Avg. SR**，显著高于OpenVLA-OFT的**69.6%**、RIPT-VLA的**68.4%**、π0-Fast的**61.6%**、VLA-Adapter的**58.9%**、π0的**53.6%**。
- 在LIBERO-Plus上，NS-VLA各子集SR为**88.1 / 79.0 / 70.2 / 80.3**，其中Long任务**80.3%**明显超过RIPT-VLA的**67.5%**和OpenVLA-OFT的**66.4%**。
- 消融实验显示完整NS-VLA在LIBERO平均SR为**98.6%**；去掉计划约束后降到**79.7%**，去掉视觉提取器为**90.1%**，去掉动作生成器为**85.2%**，去掉RL为**91.6%**，说明计划约束和整体神经-符号+RL设计贡献明显。

## Link
- [http://arxiv.org/abs/2603.09542v1](http://arxiv.org/abs/2603.09542v1)
