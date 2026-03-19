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
- robot-learning
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse

## Summary
SkillVLA研究双臂机器人中的“组合多样性”问题：已有VLA常把双臂动作绑在一起学，导致无法把左右臂已学技能自由重组到新任务中。论文提出一种分层、按技能自适应的双臂VLA框架，在保持协作能力的同时显著提升未见技能组合的成功率。

## Problem
- 现有双臂VLA通常直接预测拼接后的双臂联合动作，容易产生**skill entanglement**，即左右臂技能被绑定，难以重组。
- 双臂任务存在**combinatorial diversity**：若左右臂各自有多种技能，可能组合数会快速增长，逐一学习每种组合既低效也不具扩展性。
- 这很重要，因为真实双臂操作既包含独立并行的单臂技能组合，也包含必须紧密协作的双臂技能；若不能复用技能，泛化和持续学习都会受限。

## Approach
- 提出**SkillVLA**：用两级推理把“选什么技能”和“怎么出动作”分开，高层先为左右臂分别生成自然语言子任务描述，作为可重组的技能表示。
- 低层为左右臂分别用独立VLM流和动作专家生成动作；当任务需要协作时，再通过**自适应 cross-attention**在双臂间传递信息。
- 引入**collaboration estimator**输出合作强度 \(\alpha\in[0,1]\)，决定何时让双臂解耦、何时启用耦合通信，从而在单臂技能复用和双臂协作之间切换。
- 用“开启通信 vs 关闭通信”的行为克隆误差差值来训练合作估计器：若通信能降低BC损失，就增大 \(\alpha\)；否则减小。
- 再配合VLM先验、时序平滑与保守通信正则，以及可选的离散门控，提高合作级别判断的稳定性。

## Results
- 在**9个未见技能重组任务**上，SkillVLA平均成功率达到 **0.51**，而 **\(\pi_{0.5}\)=0.0**、**\(\pi_{0}\)-FAST=0.0**、**TwinVLA=0.04**；论文称这是从接近 **0%** 提升到 **51%** 的组合泛化突破。
- 具体重组任务中，SkillVLA在 **Cup×Cake 0.7、Cup×Stir 0.4、Cup×Smash 0.5、Box×Cake 0.6、Box×Stir 0.4、Box×Smash 0.5、Mug×Cake 0.6、Mug×Stir 0.3、Mug×Smash 0.6**，整体显著优于基线几乎全零的表现。
- 在**已学习技能**上，SkillVLA平均成功率 **0.78**，与 **\(\pi_{0.5}\) 的 0.77** 相当，并高于 **\(\pi_{0}\)-FAST 的 0.70** 和 **TwinVLA 的 0.67**，说明它没有靠牺牲基础技能执行来换取重组能力。
- 论文还声称在**3个高协作任务**上可与基线匹敌，说明自适应通信仍能表达紧密双臂协调；但摘录中未给出具体数值表。
- 在**2个长时程多阶段任务**中，SkillVLA通过在可并行阶段重组技能来加速执行，**执行时间降低 21%**；摘录未提供更细的任务级数字。
- 论文还声称在**持续学习/少样本新技能获取**场景下显著更好，但摘录中没有给出定量结果。

## Link
- [http://arxiv.org/abs/2603.03836v1](http://arxiv.org/abs/2603.03836v1)
