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
- embodied-foundation-model
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# MEM: Multi-Scale Embodied Memory for Vision Language Action Models

## Summary
MEM 提出一种给机器人视觉-语言-动作模型加入**多尺度记忆**的方法：用视频记住最近几秒的细节，用语言压缩记住长达十几分钟的语义事件。它面向真实长时程操作任务，尤其是厨房整理、做饭等需要持续跟踪进度与应对遮挡/失败重试的场景。

## Problem
- 现有端到端机器人策略通常只看当前观测，或直接拼接少量过去观测；这对**长时程、多阶段**任务不够，因为计算/延迟会迅速失控。
- 机器人需要两类不同记忆：**短期细粒度记忆**用于遮挡恢复、动态估计、重抓取；**长期语义记忆**用于记住任务进度，如哪些步骤已完成、哪些柜门还没关。
- 如果只用单一记忆形式（仅图像、仅语言、仅关键帧等），往往会在空间精度、时间覆盖范围或推理效率之间做出不理想折中，这会限制真实机器人在复杂任务中的表现。

## Approach
- 将策略拆成两层：**高层策略**根据当前观测、任务目标和已有语言记忆，输出下一步子任务指令并更新语言记忆；**低层策略**根据最近一段观测序列和子任务执行动作。
- **长期记忆**用自然语言摘要表示：模型不保存全部历史，而是持续维护一个简短的“已发生什么且仍然重要”的语义摘要；训练标签由外部LLM根据子任务序列和成功/失败标记自动生成，并显式做压缩与遗忘。
- **短期记忆**用高效视频编码器表示：在ViT中交替做空间注意力和因果时间注意力，把多帧视觉历史压缩进当前时刻表示，只把当前时刻token送入VLA主干，从而控制延迟。
- 视频编码器**不增加新可学习参数**，主要通过改注意力模式和时间位置编码实现，因此可直接继承预训练视觉语言模型权重。
- 该方法被集成到 **\(\pi_{0.6}\)** VLA 中：预训练时使用6帧输入（5个过去帧+当前帧，1秒步长），后训练/推理中可扩展到**18帧、54秒**的观测记忆；整体还能支持需要**最长15分钟**语义记忆的任务。

## Results
- 论文声称 MEM 让策略能够完成需要**最长15分钟**记忆的真实机器人任务，包括**kitchen clean-up** 和 **grilled cheese sandwich**，以及 recipe setup 等长时程操作。
- 在实现层面，MEM 支持的记忆尺度包括：短期视频记忆可扩展到**18帧 / 54秒**，长期语言记忆覆盖**最多15分钟**的任务过程。
- 实验设置上，长时程任务中 recipe setup 训练使用了**42个食谱**，并在**5个未见食谱**、未见厨房和未见物体上评估；每个策略/任务使用**10次rollouts**，报告均值±标准误。
- 论文明确宣称：与无记忆的 **\(\pi_{0.6}\)** 相比，MEM 在长时程任务上**显著提高成功率**，且在多种复杂操作任务上达到**state-of-the-art performance**；但给定摘录中**未提供具体成功率/分数数值**，无法逐项列出精确提升幅度。
- 消融结论：**短期视频记忆**和**长期语言记忆**都必不可少；去掉任一组件都会明显削弱长时程任务表现。作者还声称“朴素语言记忆”（直接拼接历史指令、不做压缩）明显弱于 MEM 的压缩式语言记忆，原因是训练-推理分布偏移更严重。
- 在较短任务上，MEM 还声称带来**in-context adaptation**：例如抓取失败后调整抓取高度、根据反馈改变开门方向等；摘录中未给出这部分的定量数字，但这是其核心能力主张之一。

## Link
- [http://arxiv.org/abs/2603.03596v2](http://arxiv.org/abs/2603.03596v2)
