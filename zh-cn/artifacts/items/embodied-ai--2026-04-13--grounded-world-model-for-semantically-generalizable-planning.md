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
这篇论文把模型预测控制中的目标图像打分，换成了共享视觉-语言潜空间中的语言落地打分。得到的系统 **GWM-MPC** 保留了预训练语义知识，在未见过的指令和视觉信号上，比标准视觉-语言-动作策略有明显更强的泛化能力。

## 问题
- 标准视觉运动 MPC 通常需要一张目标图像，并用候选未来与该图像在潜空间中的距离来打分。这对新任务不方便，作为人机交互接口也较弱。
- 微调后的 VLA 策略常常记住训练指令和场景捷径，而不是使用预训练语义知识。在本文的 WISER 基准上，它们能完成训练任务，但在保留测试任务上失败了；这些测试任务需要相同的动作，只是换了新的表述和新的视觉线索。
- 目标问题是语义泛化：只要训练中展示过所需动作，系统就能遵循未见过的指代表达和基于世界知识的指令。

## 方法
- 论文在 **Qwen3-VL-Embedding** 的冻结潜空间中训练 **Grounded World Model (GWM)**。这是一个多模态检索模型，可将文本、图像和视频映射到同一个嵌入空间。
- 测试时，系统根据当前关节位置，通过对示范轨迹做最近邻检索，提出 **12** 个候选动作序列。对每个候选，GWM 预测执行后行为的未来潜嵌入。
- 系统在共享嵌入空间中，用与语言指令的 **cosine similarity** 给每个预测未来打分，然后执行得分最高的动作片段。这样就把 MPC 变成了语言条件规划器，不再需要目标图像。
- 为了在不学习单独动作 tokenizer 的情况下编码动作，该方法使用 **Rendering-based Action Tokenization (RAT)**：用机器人的 URDF 和相机参数，把未来的机器人关节配置渲染成图像，再将这些渲染结果送入预训练视觉编码器。
- 训练只使用潜空间中的未来观测监督，损失函数是预测未来特征与真实未来特征之间的 MSE loss。基础模型保持冻结，以保留其语义知识。

## 结果
- 在新的基准 **WISER** 上，该基准包含 **24** 个知识类别、**288** 个训练任务和 **288** 个测试任务，**GWM-MPC** 的测试成功率达到 **0.87**，而 VLA 基线平均只有 **0.22**。
- GWM-MPC 的训练成功率为 **0.92**，测试成功率为 **0.87**。基线平均分别是 **0.90** 和 **0.22**，说明 GWM 在已见任务上保持了表现，同时明显缩小了训练到测试的泛化差距。
- 各具名基线在测试集上的成功率要低得多：**InstructVLA 0.47**、**Wall-OSS 0.40**、**InternVLA-A1 0.26**、**π0.5 0.26**、**GR00T-N1.6 0.18**、**SmolVLA 0.08**、**π0 0.08**。
- GWM-MPC 在测试集上的 **grasp** 指标达到 **0.99**，**reach** 指标达到 **0.88**；基线平均分别是 **0.54** 和 **0.29**。
- 提出的动作 tokenizer 很关键：**GWM-MPC-AC** 的测试成功率降到 **0.24**，而完整的 GWM-MPC 保持在 **0.87**。
- 在这个基准中，跨机器人形态的零样本迁移表现也很强：**GWM-MPC-xArm6** 在动作空间、运动学和外观都不同的情况下，测试成功率仍有 **0.83**。检索上界 **GT-MPC** 达到 **0.93** 的测试成功率，这说明主要瓶颈是冻结基础模型空间中的打分质量。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11751v1](http://arxiv.org/abs/2604.11751v1)
