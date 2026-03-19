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
- hierarchical-control
- cluttered-robotics
- diffusion-policy
relevance_score: 0.46
run_id: materialize-outputs
language_code: zh-CN
---

# HSC-VLA: Hierarchical Scene-Clearing for Robust Bimanual Manipulation in Dense Clutter

## Summary
HSC-VLA针对高密度杂乱场景中的双臂操作，提出把“高层语义规划”和“低层动作执行”分开的分层VLA框架。核心思想是先用视觉语言模型找出应忽略的干扰物并清理场景，再让扩散策略只基于过滤后的视觉和本体感觉执行动作。

## Problem
- 解决的问题：现有端到端VLA在高密度杂乱环境中容易被无关物体分散注意力，导致指令跟随、目标定位、抓取和放置失败。
- 为什么重要：真实超市货架等场景有遮挡、反光、复杂摆放和长时序任务，错误会逐步累积，影响机器人在物流/零售中的可用性。
- 现有方法缺陷：单体模型把规划、记忆、感知和控制都塞进一个表示里，难以稳定处理长时程、多子任务、失败恢复和视觉分布偏移。

## Approach
- 使用分层架构：高层“Brain”接收语言指令和观察历史，分解为子目标，并预测需要忽略的任务无关区域框。
- 用分割与掩码做“scene clearing”：先对这些无关区域做零样本分割，再用时序传播更新掩码，把原图中的干扰物抹掉，仅保留与当前子任务相关的几何信息。
- 低层“Cerebellum”是基于扩散的双臂操作策略，只看掩码过滤后的图像、14维本体状态和当前子目标，生成动作块而不是单步动作，以提高平滑性和稳定性。
- 训练/部署保持一致：离线数据也用同样的规划-分割-掩码流水线处理，减少训练和测试时视觉预处理不一致带来的分布差异。
- 加入验证与重规划：每个动作块后检查子目标是否完成，失败时允许重试、修改掩码约束或调整后续计划。

## Results
- 在真实高密度杂乱超市货架上，HSC-VLA总体成功率达到 **86.7%**，相比最佳单体基线 **π0-Full FT 的 34.3%** 提升 **52.4 个百分点**。
- 在高密度设置下，各原子技能成功率分别为：**抓取 85%**、**放置 78%**、**双臂操作 97%**；而 π0-Full FT 分别为 **75% / 13% / 15%**。
- 在低密度场景下，HSC-VLA总体成功率为 **90.7%**，高于 π0-Full FT 的 **87.7%**；分项为 **抓取 92%**、**放置 84%**、**双臂 96%**。
- 场景简化消融显示：高密度下 **无掩码 56%**、**静态掩码 69%**、**动态清理 80%**；长时程任务下分别为 **40% / 10% / 72%**，说明动态清理对长时序尤为关键。
- 论文摘要还报告长时程任务结果：**clutter sorting 72%**，**restocking 66%**，并声称具备更强鲁棒性与失败恢复能力。
- 数据与设置方面：作者在真实双臂平台上采集了 **2,100 条** 专家轨迹，在统一训练配置下与 ACT、DP、DP3、RDT、π0-LoRA、π0-Full FT 等方法比较。

## Link
- [http://arxiv.org/abs/2603.07484v1](http://arxiv.org/abs/2603.07484v1)
