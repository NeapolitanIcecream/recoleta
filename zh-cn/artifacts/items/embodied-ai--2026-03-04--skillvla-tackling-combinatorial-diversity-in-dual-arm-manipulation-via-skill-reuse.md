---
source: arxiv
url: http://arxiv.org/abs/2603.03836v1
published_at: '2026-03-04T08:38:27'
authors:
- Xuanran Zhai
- Zekai Huang
- Longyan Wu
- Qianyou Zhao
- Qiaojun Yu
- Jieji Ren
- Ce Hao
- Harold Soh
topics:
- vision-language-action
- dual-arm-manipulation
- skill-reuse
- combinatorial-generalization
- robot-foundation-model
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse

## Summary
SkillVLA研究双臂机器人中的“组合多样性”问题：许多双臂任务其实是左右手单臂技能的不同组合，但现有VLA通常把两臂动作纠缠在一起，难以重组已学技能。论文提出一种分层、按技能自适应的双臂VLA，使机器人能复用单臂技能并在需要时再启用双臂协作。

## Problem
- 现有双臂VLA常直接预测拼接后的联合动作，导致左右臂技能**纠缠**，只能复现训练中见过的动作配对。
- 双臂任务存在明显的**组合爆炸**：若左右手各学到多种技能，可能组合数量近似二次增长，不可能逐一示教学习。
- 这很重要，因为通用双臂机器人若不能把已有单臂技能灵活重组，就难以扩展到新任务、长程任务和持续学习场景。

## Approach
- 提出**两级推理**框架：高层VLM先根据视觉/语言输入，为左臂和右臂分别生成子任务文本提示，把每个手臂该做什么显式拆开。
- 低层为左右臂分别建立动作生成流，各自根据对应提示和观测产生动作，从而支持把已学单臂技能在新左右配对中直接重组。
- 对真正需要紧密配合的任务，引入**自适应跨臂通信**：两个动作流之间通过cross-attention交换信息，但通信强度由合作估计器控制。
- 合作估计器输出标量 lpha∈[0,1]（文中记作alpha），通过比较“开/关通信”时的行为克隆误差，学习何时需要双臂耦合、何时应保持解耦。
- 进一步加入VLM先验、时间平滑和保守通信正则，并可将合作门离散化为0/1，以提高推理稳定性。

## Results
- 在**9个未见过的技能重组任务**上，SkillVLA平均成功率达到 **0.51**，而 **π0.5 = 0.0**、**π0-FAST = 0.0**、**TwinVLA = 0.04**，显示其对未见左右技能配对具有明显组合泛化能力。
- 具体重组任务中，SkillVLA在 **Cup×Cake 0.7、Cup×Stir 0.4、Cup×Smash 0.5、Box×Cake 0.6、Box×Stir 0.4、Box×Smash 0.5、Mug×Cake 0.6、Mug×Stir 0.3、Mug×Smash 0.6**；而主要基线几乎全为 **0.0**。
- 在**已学习技能**测试上，SkillVLA平均 **0.78**，与 **π0.5 的 0.77** 相当，优于 **π0-FAST 的 0.70** 和 **TwinVLA 的 0.67**，说明其提升重组能力的同时没有明显损害已知技能表现。
- 论文还声称在**三类高协作任务**上可与基线匹敌，说明自适应通信仍能表达紧密双臂协调，但摘录中未给出具体数值。
- 在**两个多阶段长程任务**中，SkillVLA可根据阶段自动判断合作需求，并通过并行化可重组技能使执行时间降低 **21%**；摘录中未提供对应基线的完整表格数值。
- 论文进一步声称在**有限示范的持续学习**中，技能复用能显著帮助新技能获取，但摘录未提供定量结果。

## Link
- [http://arxiv.org/abs/2603.03836v1](http://arxiv.org/abs/2603.03836v1)
