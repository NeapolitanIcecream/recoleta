---
source: arxiv
url: http://arxiv.org/abs/2603.05185v1
published_at: '2026-03-05T13:55:33'
authors:
- Pengfei Yi
- Yingjie Ma
- Wenjiang Xu
- Yanan Hao
- Shuai Gan
- Wanting Li
- Shanlin Zhong
topics:
- vision-language-action
- long-horizon-manipulation
- hierarchical-control
- anomaly-detection
- ood-generalization
- robot-policy
relevance_score: 0.95
run_id: materialize-outputs
---

# Critic in the Loop: A Tri-System VLA Framework for Robust Long-Horizon Manipulation

## Summary
本文提出一种三系统视觉-语言-动作（VLA）框架，在高层VLM规划与低层VLA控制之间加入一个视觉Critic做动态调度，以提升长时程操作的实时性与鲁棒性。核心思想是只在需要时才唤醒慢速推理模块，从而在OOD干扰、停滞和失败恢复中取得更强表现。

## Problem
- 现有分层VLA常把**慢速但有语义理解的VLM**与**快速但语义较弱的VLA**硬性串联，导致切换僵硬、计算浪费、对扰动反应慢。
- 长时程操作中，机器人容易出现**停滞、抓错、掉落、无限重试**等问题；若靠为这些失败专门收集数据，扩展性很差。
- 这很重要，因为真实世界机器人需要同时具备**高层语义规划**与**低层实时闭环控制**，尤其在复杂、开放、OOD场景下。

## Approach
- 提出 **Tri-System**：System 2 是 VLM“Brain”负责生成语义子任务，System 1 是 flow-matching “Cerebellum”负责连续动作，System 3 是轻量视觉 **Critic** 负责监控执行并决定何时切换。
- Critic把子任务评估统一成VQA文本生成：输出要么是**进度值**（将完成度离散为101个bin，对应区间[-1,0]），要么是异常 token **`<aci>`**，从而同时做进度跟踪和失败检测。
- 调度是**事件驱动、异步**的：正常时由VLA持续20Hz左右执行；仅在**子任务完成、检测到事故、或长时间停滞**时，才触发VLM重规划并清空旧动作缓存。
- 为打破无限重试，系统加入**人类启发式规则**：若Critic发现进度长期不再提升（如最大停滞阈值 `N_stag=180` 帧），则重置机器人状态并让Brain根据短时记忆重新规划。
- 还提出自动子任务标注流水线：先用末端执行器轨迹与夹爪状态做关键帧提议，再用VLM检索语义标签，减少人工逐段标注成本。

## Results
- 在真实机器人 **Arrange the Tableware** 任务中，Tri-System 在 **Ordered / Scattered / Left cup / Fallen** 四种场景分别达到 **10/10、9/10、7/10、7/10**；优于 Single-System 的 **8/10、0/10、0/10、2/10** 和 Dual-System 的 **7/10、6/10、1/10、5/10**。
- 在更复杂的 **Tidy up the Desk** 长时程任务中，Tri-System 各阶段成功数为 **Open 9/10、Bottle1 8/10、Bottle2 5/10、Overall 4/10**；对应 Single-System 为 **7/10、5/10、2/10、0/10**，Dual-System 为 **6/10、5/10、1/10、0/10**。
- 论文声称该方法在所有评测场景上达到**state-of-the-art**，尤其在OOD左侧杯子场景中，因训练数据没有该任务的左臂样本，Tri-System 仍取得 **7/10**，显著高于 Dual-System **1/10** 和 Single-System **0/10**。
- 系统运行层面，作者给出关键机制数字：控制/观测循环约 **20 Hz**；成功阈值示例为 **`τ_succ ≈ -0.041`**；停滞阈值为 **`N_stag=180`**；Critic 采用约 **0.2B** 参数的 Florence-2-base，以支持实时异步评估。
- 训练数据方面，每个任务收集 **200** 条遥操作轨迹；餐具整理任务额外加入 **100** 条“杯子被打翻后恢复”的轨迹。尽管有这些数据，作者特别强调左侧杯子使用左臂仍是**未见分布**测试。

## Link
- [http://arxiv.org/abs/2603.05185v1](http://arxiv.org/abs/2603.05185v1)
