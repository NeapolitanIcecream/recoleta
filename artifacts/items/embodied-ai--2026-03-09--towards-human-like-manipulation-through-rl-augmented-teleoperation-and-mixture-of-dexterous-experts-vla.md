---
source: arxiv
url: http://arxiv.org/abs/2603.08122v1
published_at: '2026-03-09T09:02:30'
authors:
- Tutian Tang
- Xingyu Ji
- Wanli Xing
- Ce Hao
- Wenqiang Xu
- Lin Shao
- Cewu Lu
- Qiaojun Yu
- Jiangmiao Pang
- Kaifeng Zhang
topics:
- vision-language-action
- dexterous-manipulation
- force-tactile-fusion
- mixture-of-experts
- shared-autonomy-teleoperation
- hierarchical-robot-policy
relevance_score: 0.94
run_id: 47596b38-ed69-4aa2-a335-ff14a81186ef
---

# Towards Human-Like Manipulation through RL-Augmented Teleoperation and Mixture-of-Dexterous-Experts VLA

## Summary
## TL;DR: 通过“RL 训练的手内原子技能 + 可调用的分层VLA + 力/触觉MoE残差融合”，把VLA从低自由度抓取推进到更像人类的双手、接触丰富的手内操作，并在复杂任务上报告约2倍成功率提升。

## Problem:
- 现有VLA多停留在低自由度夹爪的视觉引导抓放，难以扩展到**双手高自由度（63 DoF）**、**接触丰富**的手内操作（如旋转、稳定握持、削苹果）。
- **数据采集瓶颈**：63 DoF 双臂双手纯人工遥操作很难产出稳定、高质量示范，尤其是持续手内旋转等精细阶段。
- **多技能学习与模态异质性**：同一任务包含视觉主导的粗动作、力反馈主导的插入/切削、触觉主导的防滑与手内重定位；把力/触觉“直接拼接到预训练VLA”会破坏预训练能力并降低表现。

## Approach:
- **IMCopilot（手内操作副驾驶）**：用PPO在IsaacLab中训练一组可组合的手内原子技能（如稳定抓取、按轴旋转），并通过域随机化实现零样本sim2real倾向。
- **RL增强遥操作采集**：人在外骨骼遥操作中负责手臂粗运动，遇到难的手内阶段用脚踏板触发IMCopilot代劳，从而提升示范质量与一致性。
- **分层执行**：推理时VLA除输出动作外还输出触发标量`c`；当`c>0.5`时由IMCopilot接管手部动作，而手臂仍由VLA控制，缓解“一把策略学全技能”的难题。
- **MoDE-VLA（Mixture-of-Dexterous-Experts）力/触觉融合**：为力（14维双臂关节力矩）与触觉（60维十指6DoF力/力矩）建立专用token通路；经自注意力与稀疏MoE（E=8, top-1路由）处理后，以**残差注入**方式分别修正手臂/手部动作（避免覆盖预训练VLA知识）。

## Results:
- **手内操作能力（Table I）**：与纯遥操作相比，IMCopilot显著提升手内操作成功率：
  - 乒乓球：10%（3/30）→ 83%（25/30）
  - 网球：67%（20/30）→ 93%（28/30）
  - 苹果：27%（8/30）→ 90%（27/30）
  - 总体：34%（31/90）→ 89%（80/90）
- **端到端任务评测设置**：4个接触丰富任务（齿轮装配、充电器插入、试管重排、削苹果），每任务20次试验；指标为成功率SR，削苹果额外报告PCR（25%粒度）。
- **总体性能主张（摘录中未给出逐任务数表）**：作者声称在“灵巧接触丰富任务”上相对基线VLA（π0/OpenPI-0骨干）实现**约2倍成功率提升**，并宣称“首次实现自主双灵巧手削苹果”。（注：除Table I外，摘录未提供逐任务SR/PCR的具体数值与对比表。）

## Links
- Canonical: http://arxiv.org/abs/2603.08122v1
