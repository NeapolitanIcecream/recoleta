---
source: arxiv
url: http://arxiv.org/abs/2603.14327v1
published_at: '2026-03-15T11:13:04'
authors:
- Yixuan Li
- Le Ma
- Yutang Lin
- Yushi Du
- Mengya Liu
- Kaizhe Hu
- Jieming Cui
- Yixin Zhu
- Wei Liang
- Baoxiong Jia
- Siyuan Huang
topics:
- humanoid-teleoperation
- robot-learning
- benchmarking
- transformer-policy
- motion-retargeting
relevance_score: 0.58
run_id: materialize-outputs
language_code: zh-CN
---

# OmniClone: Engineering a Robust, All-Rounder Whole-Body Humanoid Teleoperation System

## Summary
OmniClone 是一个面向人形机器人全身遥操作的工程化系统，目标是在真实部署中同时实现鲁棒性、通用性和低成本。论文同时提出 OmniBench 细粒度诊断基准，用来揭示现有方法在不同动作类型上的失衡，并据此优化训练数据与系统设计。

## Problem
- 现有人形全身遥操作通常只报告汇总指标，混合了操控、下蹲、奔跑、跳跃等不同运动模式，导致关键失败模式被掩盖。
- 现有系统往往与特定硬件/软件配置强耦合，跨操作者、跨 MoCap 设置时需要繁琐校准，难以稳定落地。
- 这很重要，因为全身遥操作既是实时远程控制工具，也是收集高质量示范、训练自主机器人/VLA 策略的数据引擎。

## Approach
- 提出 **OmniBench**：一个针对未见动作的诊断式基准，覆盖 6 类功能动作（loco-manipulation、manipulation、squatting、walking、running、jumping），并按难度/动态强度细分为 18 个评测类别。
- 提出 **OmniClone**：使用基于 Transformer 的统一全身跟踪策略，替代较弱的 MLP，以更好建模时序依赖；通过 teacher-student 蒸馏训练部署版 student policy。
- 用 OmniBench 反向指导训练数据配方：最终采用约 60% manipulation、其余 40% 在动态动作与稳定运动之间平衡的数据组成，以获得更均衡的技能覆盖。
- 在系统层面加入 **subject-agnostic refined retargeting**，根据初始校准帧动态缩放人体 MoCap 数据，减少不同身高/不同设备带来的形态失配，无需逐人手工校准。
- 加入基于 FIFO 队列的稳健通信与零阶保持，使用 UDP 降低传输开销，在信号波动/延迟下保持平滑控制，并实现约 80 ms 端到端延迟；同一策略还兼容实时遥操作、生成动作回放和 VLA 控制源。

## Results
- 论文声称系统级改进后 **MPJPE 降低超过 66%**，同时只需 **30 小时动作数据** 和 **单张消费级 GPU**；训练总成本约 **80 GPU 小时**（RTX 4090，上文细分为 teacher 约 60 小时、student 蒸馏约 22 小时），相比同类方法“低若干数量级”。
- 在 OmniBench 的 18 个分层类别上，OmniClone 相比 GMT / Twist2 显著更均衡：例如 **Loco-Manip Low** 上 OmniClone **SR 100%, MPJPE 51.3 mm**，GMT 为 **95%, 180.5 mm**，Twist2 为 **65%, 210.5 mm**。
- 在操控相关任务上也明显领先：如 **Manip Medium** 上 OmniClone **SR 100%, MPJPE 20.4 mm**，GMT **100%, 54.7 mm**，Twist2 **100%, 156.3 mm**。
- 在敏捷运动上保持强性能：如 **Run Medium** 上 OmniClone **SR 100%, MPJPE 42.0 mm**，GMT **100%, 120.8 mm**，Twist2 **100%, 176.9 mm**；**Jump Medium** 上 OmniClone **SR 100%, MPJPE 34.5 mm**，GMT **90%, 105.3 mm**，Twist2 **85%, 177.2 mm**。
- 消融表明 Transformer 明显优于 MLP：例如 **Walk Fast** 上 OmniClone MLP 仅 **SR 20%, MPJPE 111.7 mm**，而 OmniClone 为 **SR 100%, MPJPE 63.5 mm**。
- 系统可跨不同体型操作者泛化：在 **1.47 m–1.94 m** 共 **6 名**参与者上完成复合 loco-manipulation 任务；论文称所有新手操作者均能在 **5–7 次练习**内完成任务。另一个下游结果是基于 OmniClone 数据训练的 VLA 策略在 **Pick-and-Place** 与 **Squat to Pick-and-Place** 上分别达到 **85.71%** 和 **80.00%** 成功率。

## Link
- [http://arxiv.org/abs/2603.14327v1](http://arxiv.org/abs/2603.14327v1)
