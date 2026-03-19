---
source: arxiv
url: http://arxiv.org/abs/2603.10126v1
published_at: '2026-03-10T18:03:29'
authors:
- Yutong Hu
- Jan-Nico Zaech
- Nikolay Nikolov
- Yuanqi Yao
- Sombit Dey
- Giuliano Albanese
- Renaud Detry
- Luc Van Gool
- Danda Paudel
topics:
- vision-language-action
- autoregressive-policy
- robot-manipulation
- temporal-memory
- transformer-decoder
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# AR-VLA: True Autoregressive Action Expert for Vision-Language-Action Models

## Summary
AR-VLA提出了一种真正跨时间自回归的动作专家，用持续动作记忆而不是每步重置上下文来驱动机器人控制。它试图解决现有VLA/扩散策略“只在单步内自回归、跨步却是反应式”的结构问题，从而提升长时程一致性、平滑性和历史感知。

## Problem
- 现有Vision-Language-Action模型和扩散策略通常按“动作块”或单步反应式预测，每次新观察到来都会重置时序上下文，缺少持续内部状态。
- 这种“Markovian amnesia（马尔可夫失忆）”会让机器人难以利用过去动作与速度信息，导致轨迹抖动、时序不连贯，并在长时程/部分可观测任务上失效。
- 机器人控制还面临“慢感知/慢推理”与“快控制”之间的频率错配，因此需要一种能在视觉更新稀疏或延迟时仍稳定输出动作的结构。

## Approach
- 将动作生成建模为**真正跨时间的自回归序列预测**：当前动作依赖过去动作与本体状态历史，同时条件于最近一次可用的视觉-语言前缀，而不是只看当前快照。
- 设计**Hybrid Key-Value Cache (HKV)**：一条是高频、滚动FIFO的动作/本体历史缓存；另一条是低频、可刷新的视觉-语言缓存。这样动作专家可独立持续运行，视觉只负责异步“指导”。
- 提出**Dynamic Temporal Re-anchoring (DTR)**：给视觉token赋予其采样时刻的时间锚点，借助RoPE让模型显式理解视觉信息“过时了多久”，从而缩小短上下文训练与长时程推理之间的分布差异。
- 训练分两阶段：先做**仅动作预训练**学习运动学“语法”（动态、约束、常见运动模式），再进行**视觉-动作对齐**；并加入历史dropout，避免模型过度依赖完美历史、提升对延迟和噪声的鲁棒性。

## Results
- 在**BridgeV2训练、SimplerEnv评测**的通才VLA设置中，AR-VLA平均成功率达到**61.5%**，高于第二名**CogACT 52.1%**，提升**+9.4个百分点**。
- 在与相同Paligemma-3B骨干的模型对比中，AR-VLA优于**Pi-0-Fast 49.0%**和**Pi-0.5 51.0%**，说明改进主要来自动作专家结构而非更强感知骨干。
- 单任务上，AR-VLA在**spoon**任务达到**75.0%**，优于**Pi-0-Fast 62.5%**和**Pi-0.5 58.3%**；在更精细的**carrot**任务达到**54.2%**，优于**29.2%**和**33.3%**。
- 论文还声称在**模拟和真实机器人操作**中可替代传统chunk-based action heads，并在**轨迹平滑性、运动学一致性、历史感知、长时程任务完成能力**上明显优于反应式基线。
- 图文定性结果显示：AR-VLA生成的关节轨迹更平滑，且在需要持续历史意识的长时程任务中成功，而**DP**与**FM**等缺乏时序上下文的基线会失败。
- 该摘录未给出更多完整表格数值（如真实机器人、专才任务、消融、推理频率）的详细定量结果，因此这些部分只能依据作者的定性与摘要性描述概括。

## Link
- [http://arxiv.org/abs/2603.10126v1](http://arxiv.org/abs/2603.10126v1)
