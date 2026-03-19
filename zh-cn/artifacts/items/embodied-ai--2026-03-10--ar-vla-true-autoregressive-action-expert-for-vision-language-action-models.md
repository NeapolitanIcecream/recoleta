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
- robot-control
- generalist-robot-policy
- long-horizon-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# AR-VLA: True Autoregressive Action Expert for Vision-Language-Action Models

## Summary
AR-VLA提出了一种真正跨时间自回归的动作专家，把机器人控制视为连续动作序列生成，而不是每次看一帧就重新预测一段动作。它的目标是在保留或提升任务成功率的同时，显著增强历史感知、轨迹平滑性和长时程控制稳定性。

## Problem
- 现有VLA、扩散策略和动作分块方法大多是**反应式**的：每次新观测到来时都会重置上下文，缺少持续的动作/状态记忆。
- 这种“Markovian amnesia”会让机器人难以利用长期运动历史，导致控制抖动、时序不连贯，并在长时程或部分可观测任务中失败。
- 机器人中还存在**慢感知/快控制**的频率错配：重型视觉语言骨干更新慢，但电机控制需要高频连续输出，因此需要一种能在视觉延迟下仍稳定工作的动作生成机制。

## Approach
- 提出一个独立的**autoregressive action expert**：像语言模型逐token生成文本一样，模型逐时刻生成连续动作，并显式条件于过去动作与本体状态历史，以及最近可用的视觉语言前缀。
- 设计**Hybrid Key-Value Cache (HKV)**：把记忆拆成两路，动作/本体流使用长寿命滚动FIFO缓存，视觉语言流使用低频刷新、单槽替换的语义前缀缓存，从而解耦快控制与慢感知。
- 提出**Dynamic Temporal Re-anchoring (DTR)**：给视觉语言token打上“采样时刻”锚点，利用RoPE相对位置特性让模型显式理解图像有多“旧”，从而在训练和推理时处理异步、多延迟输入。
- 采用两阶段训练：先做**仅动作预训练**，学习运动学“语法”；再做视觉-动作对齐，并通过历史dropout迫使模型在历史不完整时仍利用视觉前缀。

## Results
- 在**BridgeV2训练、SimplerEnv评测**的通才VLA设置中，AR-VLA平均成功率达到 **61.5%**，高于第二名 **CogACT 52.1%**，领先 **+9.4%**。
- 与相同 **Paligemma-3B + 300M** 规模、共享同一VLM骨干的基线相比，AR-VLA优于 **Pi-0-Fast 49.0%** 和 **Pi-0.5 51.0%**。
- 分任务结果中，AR-VLA在 **spoon** 任务上达到 **75.0%**，高于 **Pi-0-Fast 62.5%** 和 **Pi-0.5 58.3%**。
- 在需要更精细操作的 **carrot** 任务上，AR-VLA达到 **54.2%**，明显优于 **Pi-0-Fast 29.2%** 和 **Pi-0.5 33.3%**。
- 论文还声称其在**真实机器人操作、专家策略替换、轨迹平滑性、长时程任务**上优于或不差于SOTA反应式VLA/扩散基线，但给定摘录未提供这些部分的完整定量表格数字。
- 定性上，作者声称AR-VLA生成的关节轨迹更平滑、更符合运动学一致性，并且在 **PushT2**、**Stack3** 等强调历史依赖的长时程任务中能成功，而 **DP** 和 **FM** 等基线会因缺乏时序上下文而失败。

## Link
- [http://arxiv.org/abs/2603.10126v1](http://arxiv.org/abs/2603.10126v1)
