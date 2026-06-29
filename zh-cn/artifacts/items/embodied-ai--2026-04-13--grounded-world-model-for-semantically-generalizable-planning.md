---
source: arxiv
url: http://arxiv.org/abs/2604.11751v1
published_at: '2026-04-13T17:25:41'
authors:
- Quanyi Li
- Lan Feng
- Haonan Zhang
- Wuyang Li
- Letian Wang
- Alexandre Alahi
- Harold Soh
topics:
- world-model
- vision-language-action
- semantic-generalization
- model-predictive-control
- robot-planning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Grounded World Model for Semantically Generalizable Planning

## Summary
## 摘要
本文把模型预测控制中的目标图像评分，改成了共享的视觉-语言潜空间里的语言对齐评分。由此得到的规划系统 GWM-MPC 保留了预训练语义知识，在未见过的指令和视觉信号上，比标准视觉-语言-动作策略的泛化能力强得多。

## 问题
- 标准的视觉运动 MPC 通常需要目标图像，并用候选未来与该图像在潜空间中的距离来打分。这对新任务来说很不方便，也不适合作为人与系统交互的接口。
- 经过微调的 VLA 策略常常记住训练中的指令和场景捷径，而不是使用预训练的语义知识。在本文的 WISER 基准上，它们能解决训练任务，但在需要相同动作、但换了措辞和新的视觉线索的留出任务上会失败。
- 目标问题是语义泛化：只要所需动作在训练中见过，就要能跟随未见过的指代表达和基于世界知识的指令。

## 方法
- 论文在 **Qwen3-VL-Embedding** 的冻结潜空间中训练了一个 **Grounded World Model (GWM)**。它是一个多模态检索模型，把文本、图像和视频映射到同一个嵌入空间。
- 测试时，系统用当前关节位置通过对示范轨迹做最近邻检索，提出 **12** 条候选动作序列。对每个候选序列，GWM 预测其行为对应的未来潜在嵌入。
- 系统在共享嵌入空间里，用 **余弦相似度** 把每个预测未来和语言指令对比打分，然后执行得分最高的动作块。这把 MPC 变成了一个语言条件规划器，不需要目标图像。
- 为了在不单独学习动作分词器的情况下编码动作，方法使用 **Rendering-based Action Tokenization (RAT)**：先用机器人 URDF 和相机参数把未来的机器人关节配置渲染成图像，再把这些渲染结果送入预训练视觉编码器。
- 训练只使用潜空间里的未来观测监督，用 MSE 损失来约束预测的未来特征和真实未来特征。基础模型保持冻结，这样做是为了保留它的语义知识。

## 结果
- 在 **WISER** 上，这个新基准包含 **24** 个知识类别、**288** 个训练任务和 **288** 个测试任务，**GWM-MPC** 的测试成功率达到 **0.87**，而 VLA 基线的平均值是 **0.22**。
- GWM-MPC 的训练成功率是 **0.92**，测试成功率是 **0.87**。基线的平均训练成功率是 **0.90**，测试成功率是 **0.22**，说明 GWM 在见过的任务上保持了表现，同时明显缩小了训练和测试之间的泛化差距。
- 各个命名基线在测试集上的成功率低得多：**InstructVLA 0.47**、**Wall-OSS 0.40**、**InternVLA-A1 0.26**、**π0.5 0.26**、**GR00T-N1.6 0.18**、**SmolVLA 0.08**、**π0 0.08**。
- GWM-MPC 在测试集上的 **抓取** 成功率是 **0.99**，**到达** 成功率是 **0.88**；基线平均值分别是 **0.54** 和 **0.29**。
- 提出的动作分词器很关键：**GWM-MPC-AC** 的测试成功率降到 **0.24**，而完整的 GWM-MPC 仍然保持在 **0.87**。
- 在这个基准上，跨机器人本体的零样本迁移表现很强：**GWM-MPC-xArm6** 在动作空间、运动学和外观都不同的情况下，测试成功率仍有 **0.83**。一个检索上限 **GT-MPC** 的测试成功率达到 **0.93**，这说明主要瓶颈是冻结基础模型空间里的评分质量。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11751v1](http://arxiv.org/abs/2604.11751v1)
