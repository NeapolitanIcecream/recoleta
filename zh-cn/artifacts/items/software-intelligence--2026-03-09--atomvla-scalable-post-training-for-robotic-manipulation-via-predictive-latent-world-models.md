---
source: arxiv
url: http://arxiv.org/abs/2603.08519v1
published_at: '2026-03-09T15:52:48'
authors:
- Xiaoquan Sun
- Zetian Xu
- Chen Cao
- Zonghe Liu
- Yihan Sun
- Jingrui Pang
- Ruijian Zhang
- Zhen Yang
- Kang Pang
- Dingxin He
- Mingqi Yuan
- Jiayu Chen
topics:
- robotic-manipulation
- vision-language-action
- world-models
- offline-rl
- long-horizon-control
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models

## Summary
AtomVLA 是一个面向机器人操作的两阶段后训练框架，目标是提升视觉-语言-动作模型在长时程、多步骤任务中的稳定性与泛化能力。其核心是把高层指令拆成原子子任务，并用潜在世界模型离线评估动作候选以进行RL后训练。

## Problem
- 现有 VLA 模型在监督微调时通常只使用粗粒度高层任务指令，缺少中间步骤指导，导致长时程任务中误差不断累积。
- 在线强化学习需要真实机器人交互或昂贵仿真，成本高、风险大，难以规模化用于策略改进。
- 像素级生成式世界模型在长序列预测中容易产生自回归误差和视觉幻觉，削弱离线后训练的可靠性。

## Approach
- 用 GPT-4o 将每条高层演示轨迹自动分解为 2-5 个原子子任务，并把这些子任务指令与原始高层指令一起输入模型做 SFT，增强指令落地与阶段性引导。
- 主体模型以 Qwen3-VL-4B-Instruct 为视觉语言骨干，配合 cross-attention Diffusion Transformer 动作头，直接预测一段 action chunk 而不是单步动作。
- 后训练阶段使用基于 V-JEPA2 的动作条件潜在世界模型：给定当前观测和候选动作段，预测未来潜在状态，并与“子任务边界帧”和“最终目标帧”的潜在表示做距离比较来打分。
- 奖励由三部分组成：子目标能量、最终目标能量、以及与专家动作的偏差惩罚，从而既鼓励朝目标推进，又避免奖励黑客和偏离示范太远。
- 用离线 GRPO 在同一离线演示数据上比较多个候选动作段，只更新动作头并加 KL 约束到 SFT 参考策略，以稳定提升长时程决策能力。

## Results
- 在 **LIBERO** 上，AtomVLA 达到 **97.0%** 平均成功率；分项为 **Spatial 96.4% / Object 99.6% / Goal 97.6% / Long 94.4%**。相较其 **SFT 基线 93.0%**，完整后训练提升 **4.0 个百分点**；在 **Long** 套件上提升 **4.4 个百分点**（**90.0% → 94.4%**）。
- 与已有方法对比，AtomVLA 的 **LIBERO 平均 97.0%** 高于 **π0 的 94.2%**、**NORA-1.5 的 94.5%**、**CoT-VLA 的 83.9%**、**OpenVLA 的 76.5%**，表明无需跨本体大规模预训练也能取得 SOTA 级结果。
- 在更难的 **LIBERO-PRO** 上，AtomVLA 平均成功率为 **0.48（48.0%）**，高于 **X-VLA 0.46**、**π0 0.45**、**MolmoAct 0.41**、**NORA 0.39**，说明其在扰动和分布偏移下更稳健。
- 子任务指令确实有效：在 **LIBERO-Long** 上，仅图像输入为 **80.4%**；加入高层任务指令后为 **90.0%**；再加入原子子任务指令后提升到 **92.2%**。
- 动作 chunk 大小为 **4** 时效果最好：在 LIBERO 上平均 **97.0%**，优于 chunk=**8/16** 的 **96.6%** 和 chunk=**32** 的 **96.3%**。
- 真实世界 Galaxea R1 Lite 六项任务中，标准设置下 AtomVLA 平均 **66.7%**，与 **π0 的 65.8%** 接近；但在泛化设置下 AtomVLA 达到 **47.5%**，显著高于 **π0 的 29.2%**，绝对提升 **18.3 个百分点**。其中折叠 T-shirt 为 **25% vs 5%**，折叠 towel 为 **35% vs 20%**。

## Link
- [http://arxiv.org/abs/2603.08519v1](http://arxiv.org/abs/2603.08519v1)
