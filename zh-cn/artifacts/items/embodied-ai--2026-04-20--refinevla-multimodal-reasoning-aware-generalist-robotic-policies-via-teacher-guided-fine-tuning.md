---
source: arxiv
url: http://arxiv.org/abs/2604.17800v1
published_at: '2026-04-20T04:46:20'
authors:
- Tuan Van Vo
- Tan Q. Nguyen
- Khang Nguyen
- Nhat Xuan Tran
- Duy H. M. Nguyen
- An T. Le
- Ngo Anh Vien
- Minh Nhat Vu
topics:
- vision-language-action
- generalist-robot-policy
- multimodal-reasoning
- teacher-guided-finetuning
- sim2real
- robot-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# ReFineVLA: Multimodal Reasoning-Aware Generalist Robotic Policies via Teacher-Guided Fine-Tuning

## Summary
## 摘要
ReFineVLA 在视觉-语言-动作策略微调中加入教师生成的自然语言推理说明，让机器人模型同时学习动作和这些动作背后的理由。论文声称，这样可以提升模拟操作基准上的泛化能力和任务成功率，覆盖 Google Robot 和 WidowX 设置。

## 问题
- 标准 VLA 策略通常只学习从图像和指令到动作的直接映射，没有显式的逐步推理。
- 在长时程、组合式或分布外的操作任务中，这会影响可解释性和泛化，因为机器人需要处理物体关系、任务上下文和动作顺序。
- 论文认为，这对通用机器人策略很关键，因为跨环境和跨本体的成功不只取决于反应式动作预测。

## 方法
- 该方法为机器人示范补充教师撰写的推理说明。对每个观测-动作对，像 Gemini 这样的专家教师模型会生成文本，解释观测、情境分析、空间推理和任务规划。
- 它在一个带推理增强的数据集上微调预训练 VLA 主干，这个数据集大约有 125,000 条轨迹，来自 BridgeData-v2 和 Google RT-1 机器人数据。
- 训练使用联合损失：标准动作预测损失加上一个由调节系数加权的推理生成损失，这样模型可以同时学习预测动作和生成理由。
- 为了保留基础模型的预训练能力，它冻结了大部分参数，只更新较后面的 transformer 块和策略头，而不是对整个模型进行微调。
- 实例化模型从 SpatialVLA 开始，这是一个基于 PaliGemma 2 的 35 亿参数 VLA，预训练数据来自 Open X-Embodiment 和 RHT20。

## 结果
- 在 SimplerEnv 基准上，论文声称它在 Google Robot 和 WidowX 任务上都达到了最先进水平。
- 在 WidowX 上，ReFineVLA 的平均任务成功率达到 **47.7%**，比次优方法高 **5.0 个百分点**。
- 在更复杂的设置中，它在 **variant aggregation** 上的成功率是 **68.8%**，高 **3.5 个百分点**；在 **visual matching** 上的成功率是 **76.6%**，高 **2.3 个百分点**。
- 在更难的单项任务上，它在 **Move Near** 上提升了 **9.6 个百分点**，在 **Open/Close Drawer** 上提升了 **8.2 个百分点**。
- 给出的文本还报告了注意力图分析：在加入推理感知微调后，模型比只做动作预测的基线更关注语义相关的物体和空间锚点。
- 提供的文本没有包含完整结果表、按数据集拆分的明细或方差指标，所以这里能看到的量化证据只限于上面的主要基准提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17800v1](http://arxiv.org/abs/2604.17800v1)
