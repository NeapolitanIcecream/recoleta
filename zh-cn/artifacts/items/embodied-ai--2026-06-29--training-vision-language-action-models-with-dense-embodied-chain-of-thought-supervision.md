---
source: arxiv
url: https://arxiv.org/abs/2606.30552v1
published_at: '2026-06-29T16:48:48'
authors:
- Haoyang Li
- Guanlin Li
- Youhe Feng
- Chen Zhao
- Zhuoran Wang
- Yang Li
- Qizhe Wei
- Shifeng Bao
- Haitao Shen
- Yihan Zhao
- Tong Yang
- Jing Zhang
topics:
- vision-language-action
- embodied-chain-of-thought
- cross-embodiment-transfer
- robot-data-scaling
- diffusion-policy
- generalist-robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision

## Summary
## 摘要
ZR-0 是一个 26 亿参数的视觉-语言-动作模型，用于跨具身机器人操作。它用密集的具身思维链标签训练 VLM；在推理时跳过这类文本生成，由一个扩散动作专家输出连续动作块。

## 问题
- 跨具身 VLA 训练很难，因为机械臂、双臂系统和人形机器人使用不同的状态向量、动作空间、关节、传感器和控制接口。
- 填充、归一化和共享动作格式可以支持混合训练，但模型仍需要学习硬件特定模式，难以直接学习共享的操作概念。
- 这个问题很重要，因为有用的通用机器人策略需要共享的场景理解、对象定位、任务进度跟踪和子任务规划，同时还要生成面向具体机器人的控制。

## 方法
- ZR-0 结合了一个 21 亿参数的 Qwen3-VL-2B-Instruct VLM 和一个 5 亿参数的 Diffusion Transformer 动作专家。
- VLM 被训练为每一帧生成密集 ECoT 标签：场景描述、进度评估、未来计划、待执行动作、目标对象框和离散动作 token。
- 动作专家接收 VLM 特征、机器人状态、带噪动作块和 flow-matching 时间步，然后预测连续动作块。
- 交叉注意力掩码让动作专家只读取任务和图像提示特征，因此推理时可以跳过 ECoT 文本生成。
- 预训练使用 ProcCorpus-60M。该数据集汇总了来自 Open X-Embodiment、DROID、RH20T、Bridge 和 Fractal 等来源的机器人数据，并加入 CapsFusion 和 Pixmo 的通用视觉-语言数据，用于保持 VLM 能力。

## 结果
- ProcCorpus-60M 约有 6000 万帧、约 1000 小时、超过 40 万条轨迹，并为 96.8% 的帧提供 ECoT 标注。
- 在 LIBERO 上，ZR-0 报告的平均成功率为 97.8%；相比之下，MolmoAct2 为 97.2%，GR00T-N1.7 为 97.0%，π0.5 为 96.9%，π0 为 94.2%，CoT-VLA 为 83.9%，OpenVLA 为 76.5%。
- ZR-0 在 LIBERO 各套件上的得分为：Spatial 97.4%，Object 99.4%，Goal 98.0%，LIBERO-10 96.4%。
- LIBERO-10 是报告中最明确的提升：ZR-0 达到 96.4%，DeepThinkVLA 为 96.2%，GR00T-N1.7 为 94.4%，π0.5 为 92.4%，π0 为 85.2%，OpenVLA 为 53.7%。
- 摘录称评估覆盖 40 个 LIBERO 任务、50 个 RoboTwin 2.0 任务、24 个 RoboCasa GR-1 Tabletop 任务，以及真实 xArm 测试；真实测试包含 4 个任务、50 多个对象和 2000 多条轨迹，但摘录没有给出 RoboTwin、RoboCasa 或真实世界结果的完整定量表格。
- 在一块 NVIDIA A6000 GPU 上使用 bfloat16 精度时，推理生成一个动作块约需 90 ms；论文称推理时跳过 ECoT 生成不会造成性能损失。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30552v1](https://arxiv.org/abs/2606.30552v1)
