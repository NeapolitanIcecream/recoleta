---
source: arxiv
url: http://arxiv.org/abs/2604.23121v1
published_at: '2026-04-25T03:18:07'
authors:
- Suning Huang
- Jiaqi Shao
- Ke Wang
- Qianzhong Chen
- Jiankai Sun
- Yanjiang Guo
- Mac Schwager
- Jeannette Bohg
topics:
- vision-language-action
- robot-foundation-models
- low-data-post-training
- instruction-following
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training

## Summary
## 概要
DeLock 处理视觉-语言-动作策略在低数据后训练中的一个常见失效：模型在狭窄的演示集上微调后，机器人学会了任务，但不再遵循新指令。它在微调时保留模型预训练得到的视觉 grounding，并在测试时加入提示词对比规则，把动作生成引导到新指令上。

## 问题
- 低数据监督微调会导致**锁定**：策略过拟合到后训练演示，即使已经从预训练中学到了相关概念，也会忽略新指令。
- 论文将其分为**概念锁定**（固着于训练过的物体或属性）和**空间锁定**（固着于训练过的位置或关系，如左/右、上/下）。
- 这很重要，因为收集覆盖面广的机器人演示成本很高，所以实际适配通常每个任务只有 80-100 条演示，指令覆盖也很窄。

## 方法
- **视觉编码器漂移正则化：**在后训练期间，DeLock 相对预训练模型的视觉编码器权重加入 L2 惩罚，目标为 `L_BC + λ||θ_v - θ_v^pre||^2`，以防视觉 grounding 塌缩到狭窄的微调分布上。
- **Contrastive Prompt Guidance (CPG)：**在测试时，用新提示 `τ+` 和训练过的提示 `τ-` 运行同一个基于 flow 的策略，然后将它们的去噪向量场组合为 `v_CPG = v(τ-) + w(v(τ+) - v(τ-))`，把动作生成推向新指令。
- 训练过的提示充当负条件，因为它编码了后训练偏置；新提示是正条件。
- 该方法不依赖额外监督、外部 foundation model 标签、辅助损失或扩增数据集。
- 评测包含 8 个任务：4 个 LIBERO 仿真任务，每个 100 条演示；4 个 DROID 真实世界任务，每个 80 条演示。这些任务都直接用于测试概念锁定和空间锁定。

## 结果
- 在这组 **8 个任务**、**每个任务 20 次试验**的评测中，DeLock 在 OOD 位置和新指令测试上表现很强：**T1 16/20**、**T4 OOD 15/20**、**T2[C] 19/20**、**T3[C] 19/20**、**T4[C] 17/20**、**T5[S] 11/20**、**T6[S] 13/20**、**T7[S] 14/20**、**T8[C+S] 13/20**。
- 与低数据基线 **RETAIN** 相比，DeLock 在 Table 2 展示的每个新提示任务上都更好。例子包括：**T2 19/20 vs 0/20**、**T5 11/20 vs 0/20**、**T7 14/20 vs 2/20**、**T8 13/20 vs 1/20**。
- 与高资源参考 **π0.5-DROID** 相比，DeLock 在若干已报告的真实世界新指令任务上达到或超过其表现：**T4[C] 17/20 vs 18/20**、**T7[S] 14/20 vs 11/20**、**T8[C+S] 13/20 vs 0/20**。论文将此描述为达到或超过了一个使用更多精筛后训练数据的最新通用策略。
- 消融实验表明两部分都重要。去掉视觉正则化后，性能明显下降，例如 **T2 19/20 → 9/20**、**T8 13/20 → 0/20**。去掉 CPG 后，模型在部分概念任务上还保留一些表现，但在空间锁定任务上失效：没有 CPG 时 **T5/T6/T7/T8 = 0/20, 0/20, 0/20, 0/20**，而完整 DeLock 分别为 **11/20, 13/20, 14/20, 13/20**。
- 冻结视觉编码器弱于带正则的适配：**Frozen-Vis** 在 **T5 2/20**、**T6 11/20**、**T7 8/20**、**T8 4/20**，都低于完整 DeLock 在相同任务上的结果。
- 论文还给出定性证据，说明标准微调会让视觉-语言注意力塌缩到训练目标上，而 DeLock 会按照新提示改变注意力和去噪轨迹。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23121v1](http://arxiv.org/abs/2604.23121v1)
