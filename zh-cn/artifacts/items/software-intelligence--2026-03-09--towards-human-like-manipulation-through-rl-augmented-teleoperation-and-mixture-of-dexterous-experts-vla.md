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
- robotic-manipulation
- vision-language-action
- dexterous-manipulation
- multimodal-fusion
- reinforcement-learning
relevance_score: 0.26
run_id: materialize-outputs
language_code: zh-CN
---

# Towards Human-Like Manipulation through RL-Augmented Teleoperation and Mixture-of-Dexterous-Experts VLA

## Summary
本文提出一个面向类人双手灵巧操作的整体框架：用 RL 训练的 IMCopilot 辅助遥操作并作为低层技能，再用 MoDE-VLA 将力觉/触觉以残差专家方式接入预训练 VLA。它针对高自由度、接触丰富的手内操作数据难采、技能难统一、模态难融合三大瓶颈，宣称在四个任务上显著优于基线。

## Problem
- 现有 VLA 主要适用于低自由度夹爪和视觉主导的抓取放置，难以扩展到 63-DoF 的双手类人灵巧操作，尤其是接触丰富的手内操作。
- 这件事重要，因为像削苹果、插接、装配这类真实任务需要双手协作、连续接触调节、触觉/力觉反馈和分层技能控制，单靠视觉和单一策略往往不够。
- 关键难点是：高质量示教数据难采集、一个策略难同时覆盖粗动作与精细手内技能、直接把力觉/触觉拼接进预训练 VLA 还可能损害原有能力。

## Approach
- 提出 **IMCopilot**：一组用 PPO 在仿真中训练的原子手内技能，如稳定抓持和绕指定轴旋转物体。最简单地说，它像“自动驾驶副驾驶”：人负责大动作，困难的手指协调交给 RL 技能。
- IMCopilot 具有双重用途：采集数据时由操作者通过脚踏触发，帮助完成难以直接遥操作的手内阶段；自主执行时则由 VLA 输出一个触发信号来调用这些低层技能，形成分层控制。
- 提出 **MoDE-VLA**：不给预训练 VLA 粗暴追加传感器输入，而是单独为臂部力矩和指尖触觉建立 token 通路，经自注意力和稀疏 MoE 专家路由后，作为残差修正注入动作预测。
- 其核心机制可概括为：视觉/语言/本体信息负责“看懂任务和大方向”，力觉/触觉专家只负责“在接触瞬间小幅纠偏”，并按物理语义分开影响 arm 与 hand 动作，从而尽量不破坏原预训练知识。

## Results
- 在手内操作能力对比中，**IMCopilot 明显优于纯遥操作**：乒乓球 **25/30=83% vs 3/30=10%**，网球 **28/30=93% vs 20/30=67%**，苹果 **27/30=90% vs 8/30=27%**，总体 **80/90=89% vs 31/90=34%**。
- 论文摘要声称，在四个逐步增加复杂度的接触丰富灵巧任务上，其方法相对基线实现了**成功率翻倍（doubled success rate improvement）**，基线为预训练 **π0/OpenPI-0** 风格 VLA；但当前摘录未给出每个任务完整的逐项数值表。
- 评测覆盖 **4 个任务**：gear assembling、charger plugging、test tube rearranging、apple peeling；每个方法每任务 **20 次试验**，主指标是 **Success Rate (SR)**，削苹果还报告 **Peel Completion Ratio (PCR)**，按 **25%** 粒度离散。
- 系统在真实机器人上工作于 **63 DoF**，并使用 **10 个指尖触觉传感器（60 维触觉）** 与 **14 维双臂关节力矩** 作为额外模态；这支撑了其“首次实现自主双灵巧手削苹果”的强主张。
- 从训练/实现上，MoDE 使用 **8 个专家、top-k=1**，动作预测时域 **H=50**、推理去噪 **N=10**；这些不是性能指标，但体现了方法的具体工程配置。
- 摘录中没有完整给出所有任务相对各基线的详细定量结果和消融数值，因此最强的明确量化证据是上述 **IMCopilot 89% vs 34%** 手内操作成功率提升，以及摘要中的“**任务成功率翻倍**”总体声明。

## Link
- [http://arxiv.org/abs/2603.08122v1](http://arxiv.org/abs/2603.08122v1)
