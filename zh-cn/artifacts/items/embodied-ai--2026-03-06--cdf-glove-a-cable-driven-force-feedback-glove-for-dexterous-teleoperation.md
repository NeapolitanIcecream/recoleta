---
source: arxiv
url: http://arxiv.org/abs/2603.05804v1
published_at: '2026-03-06T01:31:23'
authors:
- Huayue Liang
- Ruochong Li
- Yaodong Yang
- Long Zeng
- Yuanpei Chen
- Xueqian Wang
topics:
- dexterous-teleoperation
- haptic-feedback
- force-feedback-glove
- imitation-learning
- diffusion-policy
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# CDF-Glove: A Cable-Driven Force Feedback Glove for Dexterous Teleoperation

## Summary
这篇论文提出了 CDF-Glove，一种用于灵巧手遥操作的低成本、轻量级、缆驱力反馈手套，目标是提升示教数据质量并支持模仿学习。其核心价值在于把高维手部跟踪与触觉/力反馈结合起来，同时把成本压到约 230 美元并开源设计。

## Problem
- 灵巧操作中的模仿学习高度依赖高质量遥操作示教，但现有手套常缺少触觉反馈，导致操作者难以根据接触状态实时修正手指姿态。
- 现有高 DoF 触觉手套通常在**价格高、体积大、反馈弱、可穿戴性差**之间做妥协，不利于长时间数据采集。
- 如果示教质量低，训练出的策略成功率和效率都会受限，因此更好的遥操作接口对 dexterous manipulation 数据收集很重要。

## Approach
- 设计了一个**cable-driven force-feedback glove**：手背集成部件、手指用钢索/PTFE 套管传动，兼顾轻量、安全和易复制。
- 手套提供 **20 个手部 DoF 状态**：其中 **16 个直接测量**，**4 个通过运动学耦合推断**；并结合 HTC Vive 进行腕部 6D 跟踪。
- 提出从**编码器位移到手指关节角**的运动学模型：直接测 MCP/DIP，利用 DIP-PIP 耦合关系推算 PIP，再映射到不同灵巧手。
- 提出力反馈跟随模型：根据手指关节角实时计算钢索长度变化，由伺服收放线维持张力；同时加入双模态反馈策略，低力区用 LRA 振动，高力区用缆驱阻力反馈。
- 用该系统采集双手遥操作数据集，并训练 **Diffusion Policy** 基线，与 kinesthetic teaching 数据训练的策略做对比。

## Results
- 硬件指标：手套重量 **0.49 kg**，最大采样频率约 **100 Hz**，可测 **16 DoF**、耦合推断 **4 DoF**，力反馈到手的延迟约 **200 ms**。
- 精度指标：食指 DIP 重复定位实验的平均接触角为 **63.15°**，标准差 **0.29°**；作者声称远端关节重复性 **< 0.4° / 约 0.4°**，其他 MCP/PIP 测试也保持在 **0.4° 以下**。
- 成本指标：总成本约 **$230.51**，对比文中列举的 **DOGlove $600** 和 **GEX Series $600**，更低成本。
- 力反馈有效性：抓水瓶实验中，在遮眼+降噪条件下，成功率从 **1/10 (10%)** 提升到 **5/10 (50%)**，是 **4×** 提升，平均完成时间从 **18.30 s** 降到 **8.52 s**；在无感官遮挡条件下，成功率从 **7/10 (70%)** 提升到 **9/10 (90%)**，完成时间从 **3.11 s** 降到 **2.51 s**。
- 模仿学习结果：基于 CDF-Glove 遥操作示教训练的策略，相比 kinesthetic teaching，作者报告**平均成功率提高 55%**，平均完成时间减少约 **15.2 s**，即 **47.2% 相对下降**。
- 泛化主张：作者称其运动学与控制栈已在多种不同运动学/DoF 的灵巧手上验证，并且代码与硬件设计已开源；但摘录中未给出更细的跨平台定量表格。

## Link
- [http://arxiv.org/abs/2603.05804v1](http://arxiv.org/abs/2603.05804v1)
