---
source: arxiv
url: http://arxiv.org/abs/2603.14523v1
published_at: '2026-03-15T17:59:51'
authors:
- Chaoyang Wang
- Wenrui Bao
- Sicheng Gao
- Bingxin Xu
- Yu Tian
- Yogesh S. Rawat
- Yunhao Ge
- Yuzhang Shang
topics:
- vision-language-action
- embodied-ai
- multimodal-reasoning
- robot-manipulation
- tool-use
relevance_score: 0.36
run_id: materialize-outputs
---

# VLA-Thinker: Boosting Vision-Language-Action Models through Thinking-with-Image Reasoning

## Summary
本文提出 VLA-Thinker，把机器人视觉从一次性输入变成推理过程中可主动调用的部分，使模型能“边看边想边做”。它旨在提升视觉-语言-动作模型在长时程操作任务中的稳健性与成功率。

## Problem
- 现有带 CoT 的 VLA 方法大多仍是**文本主导推理**：图像只在开始编码一次，后续推理无法主动回看环境。
- 这种静态视觉上下文会限制模型处理**歧义、子目标跟踪、执行中纠错**的能力，尤其在长时程操作任务中更明显。
- 这很重要，因为直接学习“感知到动作”的整体映射通常需要大量高质量示范数据，而更强的推理与主动感知可提升数据效率和决策鲁棒性。

## Approach
- 核心机制是 **thinking-with-image**：模型在推理过程中不仅生成文字思考，还能把“请求新的视觉信息”当作一种显式动作来调用工具。
- 具体地，模型交替生成文本推理步骤、视觉工具调用和最终动作，形成**感知-推理-动作交错轨迹**，而不是只在开头看一眼图像。
- 当前实现的视觉工具是 **ZOOM-IN**，即对图像中指定区域放大查看细节，用于在中间推理阶段获取任务相关的局部视觉证据。
- 训练分两阶段：先用合成的视觉 CoT 数据做 **SFT 冷启动**，教会模型基本推理格式与何时调用工具；再用 **GRPO** 做轨迹级强化学习，用任务成功与格式奖励对完整推理-动作轨迹进行对齐。
- 为了构造训练数据，作者用 Qwen3-VL-30B-A3B-Instruct 为关键帧和中间帧生成结构化 CoT 与工具调用标注，并做 schema/时间一致性约束。

## Results
- 在 **LIBERO** 上，VLA-Thinker 达到 **97.5%** 平均成功率，相比骨干 **OpenVLA-OFT 的 91.0%** 提升 **+6.5 个百分点**。
- LIBERO 分项结果：**Spatial 98.7 vs 91.6 (+7.1)**，**Object 99.0 vs 95.3 (+3.7)**，**Goal 95.2 vs 90.6 (+4.6)**，**Long 96.9 vs 86.5 (+10.4)**；说明在长时程任务上提升尤为明显。
- 在 **RoboTwin 2.0** 上，作者报告分层平均成功率为 **62.3%（短时程）**、**70.7%（中时程）**、**64.6%（长/超长时程）**。
- 相比 **OpenVLA-OFT**，RoboTwin 2.0 上对应平均提升分别为 **+41.0**、**+23.6**、约 **+18.1** 个百分点（由 64.6 vs 46.5 计算）。
- RoboTwin 的若干单任务增益较大，例如短时程中 **Lift Pot 64.8 vs 10.1 (+54.7)**、**Beat Hammer Block 82.5 vs 28.1 (+54.4)**；中时程中 **Handover Mic 89.9 vs 45.3 (+44.6)**。
- 论文还声称该方法是**首个支持 thinking-with-image 的 VLA 模型**，并且只用单视角图像输入、在 **8×H100** 上约 **3 天**完成训练。

## Link
- [http://arxiv.org/abs/2603.14523v1](http://arxiv.org/abs/2603.14523v1)
