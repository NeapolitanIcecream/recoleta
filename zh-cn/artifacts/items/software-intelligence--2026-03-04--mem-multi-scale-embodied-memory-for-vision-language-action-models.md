---
source: arxiv
url: http://arxiv.org/abs/2603.03596v2
published_at: '2026-03-04T00:03:02'
authors:
- Marcel Torne
- Karl Pertsch
- Homer Walke
- Kyle Vedder
- Suraj Nair
- Brian Ichter
- Allen Z. Ren
- Haohuan Wang
- Jiaming Tang
- Kyle Stachowicz
- Karan Dhabalia
- Michael Equi
- Quan Vuong
- Jost Tobias Springenberg
- Sergey Levine
- Chelsea Finn
- Danny Driess
topics:
- vision-language-action
- robot-memory
- long-horizon-control
- video-encoder
- language-memory
relevance_score: 0.29
run_id: materialize-outputs
language_code: zh-CN
---

# MEM: Multi-Scale Embodied Memory for Vision Language Action Models

## Summary
MEM 为机器人视觉-语言-动作模型加入了分层、多模态记忆：用视频记住最近几秒的细节，用语言记住更久之前的语义事件。它旨在让机器人在最长约 15 分钟的真实长时任务中保持上下文，并在操作失败后进行就地调整。

## Problem
- 传统机器人策略通常只看当前观测，或把一小段历史直接塞进模型；对持续数分钟的任务，这在算力和延迟上都不可行。
- 长时机器人任务需要**不同粒度的记忆**：短期需要视觉细节来处理遮挡、失手重抓；长期需要语义摘要来记住哪些步骤已经完成。
- 单一记忆形式很难兼顾这两类需求，因此会限制真实场景中的长程操作、任务进度跟踪和鲁棒恢复能力。

## Approach
- 提出 **MEM (Multi-Scale Embodied Memory)**：把策略拆成高层与低层。高层根据当前观测、任务目标和已有语言记忆，生成下一步子任务指令并更新语言记忆；低层根据最近一段观测历史和子任务来输出动作。
- **长期记忆**用自然语言摘要表示：模型维护一个不断更新的语义记忆，只保留未来执行仍相关的信息，并压缩或丢弃冗余细节。
- 语言记忆的监督数据由外部 LLM 生成：根据子任务序列及成功/失败标记，生成“哪些过去事件仍然重要”的摘要，用来训练高层策略学习何时、如何更新记忆。
- **短期记忆**用高效视频编码器表示：在 ViT 中插入因果时间注意力，将多帧视觉历史压缩到当前时刻表示中，再送入 VLA 主干；复杂度从朴素时空注意力的 `O(n^2K^2)` 降到 `O(Kn^2 + nK^2)`。
- 该视频编码器**不增加新可学习参数**，可直接从预训练单图像 VLM/ViT 初始化；实验中预训练使用 6 帧输入，后训练/测试可扩展到 **18 帧、54 秒** 的观测记忆，并与语言记忆结合覆盖最长 **15 分钟**任务。

## Results
- 论文声称 MEM 让策略能够完成需要记忆长达 **15 分钟** 的任务，如 **kitchen cleanup** 和 **grilled cheese sandwich** 制作，以及 recipe setup 场景中的多阶段取放与收尾。
- 在 recipe setup 中，作者使用 **42 个训练食谱**，并在**未见厨房、未见物体**上的 **5 个测试食谱**评估；所有评估均为**每个策略/任务 10 次 rollout**，报告均值 ± 标准误。
- 与无记忆的 **π0.6** 相比，MEM 在长时任务上被描述为“显著提高成功率”；并且消融显示**短期视频记忆和长期语言记忆都不可或缺**。但给定摘录**未提供图中具体成功率数值**，无法逐项抄录精确百分比。
- 去掉视频记忆时，机器人会在洗盘子、擦台面等任务上因缺乏近期上下文而“卡住”；去掉语言记忆时，则难以记住配方步骤、哪些门柜已开合、哪些区域已完成清洁。
- 与“朴素语言记忆”（简单拼接全部过去子任务指令）相比，MEM 的**压缩式语言摘要**更强，作者将优势归因于减轻训练-推理分布偏移；同样，摘录未给出该对比的具体数字。
- 在短时任务上，MEM 还声称带来**in-context adaptation**：例如面对异常桌高导致的筷子误抓、或冰箱门开向不明确时，能根据近期失败历史调整抓取/开门策略；但本摘录没有给出对应定量指标。

## Link
- [http://arxiv.org/abs/2603.03596v2](http://arxiv.org/abs/2603.03596v2)
