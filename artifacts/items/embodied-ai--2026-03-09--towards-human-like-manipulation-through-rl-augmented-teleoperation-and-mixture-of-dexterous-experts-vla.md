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
- bimanual-robotics
- tactile-force-fusion
- hierarchical-policy
- shared-autonomy
relevance_score: 0.95
run_id: materialize-outputs
---

# Towards Human-Like Manipulation through RL-Augmented Teleoperation and Mixture-of-Dexterous-Experts VLA

## Summary
本文提出一个面向类人双手灵巧操作的整体框架：用RL训练的IMCopilot辅助遥操作并在执行时充当底层技能，再用MoDE-VLA把力觉/触觉稳健地接入预训练VLA。它针对高自由度、接触丰富的手内操作，宣称在4个任务上相对基线实现约2倍成功率提升。

## Problem
- 现有VLA多停留在低自由度夹爪和简单抓放，难以扩展到**63-DoF**双臂双手的类人手内操作与双手协同。
- 高质量演示数据难采：纯遥操作很难稳定完成多指协调和手内旋转，尤其是苹果削皮这类接触丰富任务。
- 单一策略难同时覆盖粗运动、插入/切削等力控阶段、以及触觉驱动的手内调整；同时，直接把力/触觉拼接进预训练VLA还可能损害原有能力。

## Approach
- 提出**IMCopilot**：一组RL训练的原子手内技能（如稳定抓握、绕指定轴旋转）。采集数据时由人通过脚踏板触发，帮助操作员完成最难的手内阶段；自主执行时同样由VLA输出触发信号调用，形成分层控制。
- 提出**MoDE-VLA**：在预训练OpenPI-0 / PaliGemma式VLA骨干外，单独建立力觉与触觉通道，而不是简单拼接输入。
- 将**臂关节力矩**作为force模态、**10个指尖6-DoF触觉/力扭矩读数**作为tactile模态，投影成token后与主干上下文、自回归/流匹配动作状态一起做自注意力交互。
- 使用**稀疏Mixture-of-Experts**按token/时间步选择专家，学习不同接触阶段（接近、接触初期、稳定抓持、动态旋转）的不同修正规律。
- 通过**residual injection**把force主要修正到臂动作、tactile主要修正到手动作；当触发IMCopilot时，手部动作可被RL技能直接接管。

## Results
- 在手内操作能力对比中，**IMCopilot显著优于纯遥操作**：乒乓球 **3/30→25/30（10%→83%）**，网球 **20/30→28/30（67%→93%）**，苹果 **8/30→27/30（27%→90%）**，总体 **31/90→80/90（34%→89%）**。
- 论文在**4个接触丰富任务**上评测：gear assembling、charger plugging、test tube rearranging、apple peeling；每种方法每任务**20次试验**，主指标为**Success Rate**，苹果削皮还报告**Peel Completion Ratio**。
- 摘要声称：在灵巧接触丰富任务上，相比基线取得**“doubled success rate improvement”**，即成功率约提升到**2倍**水平；显式基线为预训练**\(\pi_0\)**。
- 文中还宣称据其所知实现了**首个自主双灵巧手苹果削皮**，这是一个需要视觉、力觉、触觉、双手协同与手内旋转共同作用的综合任务。
- 受限于给定摘录，完整逐任务数值表和消融实验结果未全部提供；当前最强的定量证据主要来自**Table I**与摘要中的**约2倍成功率提升**声明。

## Link
- [http://arxiv.org/abs/2603.08122v1](http://arxiv.org/abs/2603.08122v1)
