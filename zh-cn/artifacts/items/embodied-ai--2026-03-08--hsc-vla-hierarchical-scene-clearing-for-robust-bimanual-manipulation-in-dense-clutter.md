---
source: arxiv
url: http://arxiv.org/abs/2603.07484v1
published_at: '2026-03-08T05:58:36'
authors:
- Zhen Liu
- Xinyu Ning
- Zhe Hu
- XinXin Xie
- Yitong Liu
- Zhongzhu Pu
topics:
- vision-language-action
- bimanual-manipulation
- hierarchical-policy
- cluttered-scene-robotics
- diffusion-policy
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# HSC-VLA: Hierarchical Scene-Clearing for Robust Bimanual Manipulation in Dense Clutter

## Summary
HSC-VLA针对高密度杂乱场景中的双臂操作，提出把“高层理解与规划”和“低层动作执行”分开的分层VLA框架。核心是先用视觉语言模型清除与任务无关的场景干扰，再让扩散策略只在被过滤的视觉输入上执行动作，从而显著提升鲁棒性与长时程表现。

## Problem
- 现有端到端单体VLA在高密度杂乱环境中容易**指令跟随失败**，因为无关物体和背景会分散注意力、破坏目标定位与几何感知。
- 在超市货架这类场景里，遮挡、反光、拥挤摆放和大量SKU会让双臂抓取、放置和协同操作变得不稳定，长时程任务还会累积错误。
- 这很重要，因为真实物流/零售环境需要机器人在复杂货架中稳定完成拣选、整理、补货等任务，而现有单体策略对视觉分布变化和复杂子任务序列不够稳健。

## Approach
- 采用分层框架：高层“Brain”负责根据语言指令和视觉历史做任务分解，决定当前子目标，以及哪些区域/物体是当前应忽略的干扰项。
- 高层输出的是**任务无关区域的边框**，再交给零样本分割模型生成像素级mask，并通过时序传播持续更新，得到动态“场景清理”结果。
- 低层“Cerebellum”是**基于扩散的双臂策略**，输入仅包括mask过滤后的图像、14维本体状态和当前子目标，从而专注于任务相关几何结构，而不是原始杂乱像素。
- 方法强调**训练-测试感知一致性**：离线数据也用同样的规划+分割+mask传播流程做预处理，减少部署时的分布差异。
- 执行中加入验证与重规划：若子目标失败，系统可重试、更新mask约束或调整后续计划，以支持失败恢复和长时程执行。

## Results
- 在真实高密度杂乱超市货架中，HSC-VLA的**聚合成功率为86.7%**，显著超过最佳单体基线 **pi0-Full FT 的34.3%**，提升**52.4个百分点**。
- 在高密度场景的分项结果中，HSC-VLA达到：**抓取85%**、**放置78%**、**双臂操作97%**；相比 **pi0-Full FT** 的 **75% / 13% / 15%**，尤其在放置与双臂操作上优势很大。
- 在低密度场景下，HSC-VLA也达到**90.7%聚合成功率**，对应分项为**抓取92% / 放置84% / 双臂96%**，相比 **pi0-Full FT 的87.7%** 仍有提升。
- 消融实验表明，**dynamic clearing** 优于不加mask或静态mask：低密度 **98%**，高密度 **80%**，长时程 **72%**；而 **base VLA, no mask** 为 **90% / 56% / 40%**，**static mask** 为 **98% / 69% / 10%**。这说明动态场景清理对高杂乱和长时程任务都关键。
- 论文摘要还报告了长时程任务结果：**clutter sorting 72%**、**restocking 66%**，并宣称具备更强的鲁棒性与失败恢复能力。
- 数据方面，作者在真实双臂平台上通过示教收集了**2,100条完整专家轨迹**，覆盖单臂抓稳、单臂放置和双臂协作抓取三类技能。虽然这不是直接性能指标，但支撑了其低层策略训练。

## Link
- [http://arxiv.org/abs/2603.07484v1](http://arxiv.org/abs/2603.07484v1)
