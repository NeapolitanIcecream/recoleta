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
ReFineVLA 在视觉-语言-动作策略的微调中加入教师生成的自然语言推理说明，让机器人模型不仅学习动作，也学习这些动作背后的明确理由。论文称，这种方法提高了模型在 Google Robot 和 WidowX 配置下模拟操作基准中的泛化能力和任务成功率。

## 问题
- 标准 VLA 策略通常直接学习从图像和指令到动作的映射，没有显式的逐步推理。
- 在长时程、组合式或分布外的操作任务中，机器人需要考虑物体关系、任务上下文和动作顺序，缺少这类推理会损害可解释性和泛化能力。
- 论文认为，这一点对通用机器人策略很重要，因为跨环境和跨具身形态的成功不只取决于反应式动作预测。

## 方法
- 该方法用教师撰写的推理说明增强机器人演示数据。对于每个观测-动作对，Gemini 等专家教师模型会生成文本，解释观测内容、情境分析、空间推理和任务规划。
- 它在一个加入推理数据的数据集上微调预训练 VLA 主干模型，该数据集约有 125,000 条轨迹，来自 BridgeData-v2 和 Google RT-1 机器人数据。
- 训练使用联合损失：标准动作预测损失加上按调节系数加权的推理生成损失，因此模型会同时学习预测动作和生成推理说明。
- 为了保留基础模型的预训练能力，它冻结了大部分参数，只更新后部 transformer blocks 和 policy head，而不是对整个模型进行微调。
- 具体实现的模型以 SpatialVLA 为起点，这是一个 35 亿参数的 VLA，基于 PaliGemma 2，并在 Open X-Embodiment 和 RHT20 上完成预训练。

## 结果
- 在 SimplerEnv 基准上，论文称该方法在 Google Robot 和 WidowX 任务中达到当前最优表现。
- 在 WidowX 上，ReFineVLA 的平均任务成功率达到 **47.7%**，比第二好的方法高 **5.0 个百分点**。
- 在更多样化的设置中，它报告在 **variant aggregation** 上取得 **68.8%** 的成功率，提升 **3.5 个百分点**；在 **visual matching** 上取得 **76.6%** 的成功率，提升 **2.3 个百分点**。
- 在更难的单项任务上，它报告 **Move Near** 提升 **9.6 个百分点**，**Open/Close Drawer** 提升 **8.2 个百分点**。
- 摘要还提到注意力图分析：经过面向推理的微调后，模型比只学习动作的基线更关注语义相关的物体和空间锚点。
- 这里提供的文本不包含完整结果表、按数据集划分的细项结果或方差指标，因此目前能看到的定量证据仅限于上述基准的主要提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17800v1](http://arxiv.org/abs/2604.17800v1)
