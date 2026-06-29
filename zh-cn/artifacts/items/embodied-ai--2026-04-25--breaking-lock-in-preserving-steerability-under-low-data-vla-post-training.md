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
## 总结
DeLock 针对视觉-语言-动作策略低数据后训练中的一个常见失效：模型在少量演示数据上微调后，虽然学会了任务，却不再跟随新指令。它在微调时保留模型预训练得到的视觉对齐，并在测试时加入提示词对比规则，引导动作生成朝向新指令。

## 问题
- 低数据监督微调会导致 **lock-in**：策略过拟合后训练演示，忽略新指令，即使它在预训练中已经学会了相关概念。
- 论文把这个问题分成 **concept lock-in**（对训练过的对象或属性产生固定）和 **spatial lock-in**（对训练过的位置或关系，如左/右、上/下，产生固定）。
- 这很重要，因为收集覆盖广泛的机器人演示成本很高，实际适配通常只能针对每个任务使用 80-100 条演示，而且指令覆盖范围很窄。

## 方法
- **视觉编码器漂移正则化：** 在后训练阶段，DeLock 在视觉编码器权重上加入相对预训练模型的 L2 惩罚，目标为 `L_BC + λ||θ_v - θ_v^pre||^2`，以防止视觉对齐在窄微调分布上塌缩。
- **Contrastive Prompt Guidance (CPG)：** 在测试时，同一个基于 flow 的策略分别接收新提示词 `τ+` 和训练提示词 `τ-`，再把它们的去噪向量场组合为 `v_CPG = v(τ-) + w(v(τ+) - v(τ-))`，从而把动作生成推向新指令。
- 训练提示词起负条件作用，因为它捕捉了后训练偏置；新提示词是正条件。
- 这种方法不依赖额外监督、外部基础模型标签、辅助损失或增强数据集。
- 评估套件包含 8 个任务：4 个 LIBERO 仿真任务，每个任务 100 条演示；4 个 DROID 真实世界任务，每个任务 80 条演示，直接测试 concept lock-in 和 spatial lock-in。

## 结果
- 在 8 任务评估中，每个任务 **20 次试验**，DeLock 在 OOD 位置和新指令测试上表现稳定：**T1 16/20**、**T4 OOD 15/20**、**T2[C] 19/20**、**T3[C] 19/20**、**T4[C] 17/20**、**T5[S] 11/20**、**T6[S] 13/20**、**T7[S] 14/20**、**T8[C+S] 13/20**。
- 与低数据基线 **RETAIN** 相比，DeLock 在表 2 展示的每个新提示词任务上都更好。例子包括：**T2 19/20 vs 0/20**、**T5 11/20 vs 0/20**、**T7 14/20 vs 2/20**、**T8 13/20 vs 1/20**。
- 与高资源参考模型 **π0.5-DROID** 相比，DeLock 在几项报告的真实世界新指令任务上持平或更好：**T4[C] 17/20 vs 18/20**、**T7[S] 14/20 vs 11/20**、**T8[C+S] 13/20 vs 0/20**。论文把这解读为达到或超过了一个使用更多精心筛选后训练数据的最先进通用策略。
- 消融实验表明两部分都重要。去掉视觉正则化会让性能大幅下降，例如 **T2 19/20 → 9/20**、**T8 13/20 → 0/20**。去掉 CPG 后，部分 concept 表现还在，但 spatial lock-in 任务失败：没有 CPG 时 **T5/T6/T7/T8 = 0/20、0/20、0/20、0/20**，而完整 DeLock 对应为 **11/20、13/20、14/20、13/20**。
- 只冻结视觉编码器弱于带正则化的适配：**Frozen-Vis** 在 **T5 2/20**、**T6 11/20**、**T7 8/20**、**T8 4/20**，都低于完整 DeLock 在同样任务上的表现。
- 论文还给出定性证据：标准微调会让视觉-语言注意力塌缩到训练目标上，而 DeLock 会把注意力和去噪轨迹调整到与新提示词一致。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23121v1](http://arxiv.org/abs/2604.23121v1)
