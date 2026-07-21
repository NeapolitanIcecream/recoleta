---
source: arxiv
url: https://arxiv.org/abs/2607.17786v1
published_at: '2026-07-20T10:20:32'
authors:
- Tuan Duong Trinh
- Naveed Akhtar
- Basim Azam
topics:
- robot-foundation-model
- vision-language-action
- robot-robustness
- adversarial-attacks
- latent-reasoning
- robot-safety
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Reasoning as a Double-Edged Sword: Architecture and Cross-Stage Robustness in Vision-Language-Action Models

## Summary
## 摘要
该论文检验了显式推理是否能提高视觉-语言-动作（VLA）策略的鲁棒性，发现鲁棒性取决于推理架构。在所报告的 LIBERO 和 SimplerEnv 实验中，潜在迭代推理尤其脆弱，而运行时推理监控器在自适应攻击下失效。

## 问题
- 论文考察了增加推理阶段是否能帮助 VLA 模型吸收扰动，还是会放大扰动；这一问题关系到在传感器、计算或指令出现错误时部署通用机器人策略的可行性。
- 论文还检验了公开的推理轨迹是否能支持运行时安全监控，而不只是提升任务性能。

## 方法
- 作者比较了三个经过 LIBERO 微调的 VLA：不进行推理的 OpenVLA-OFT、使用文本思维链的 DeepThinkVLA，以及采用 12 步潜在迭代循环的 RD-VLA。
- 作者分别在视觉、推理和动作阶段注入随机扰动与对抗性扰动，在 LIBERO 和 SimplerEnv 上使用高斯噪声、FGSM、PGD-10、Square Attack 和文本实体替换。
- 作者将 RD-VLA 的推理递归深度从 K=4 调整到 K=12，以检验其脆弱性是否会随推理步骤呈乘法增长。
- 作者在自适应攻击和匹配误报率校准下，评估了计划-动作一致性监控器和动作异常监控器。

## 结果
- 在 LIBERO 的 sigma=0.2 高斯视觉噪声下，DeepThinkVLA、OpenVLA-OFT 和 RD-VLA 的成功率分别为 92.7%、89.0% 和 14.8%；RD-VLA 相比其无扰动性能下降了 74.3 个百分点。
- 在 epsilon=8/255 的白盒 PGD-10 攻击下，DeepThinkVLA、OpenVLA-OFT 和 RD-VLA 的成功率分别为 49.8%、18.2% 和 0.0%，由此在该运行点得到所报告的排序：DeepThinkVLA > OpenVLA-OFT >> RD-VLA。
- RD-VLA 在 K=8 到 K=12 之间的放大效应几乎没有变化：rho(12)/rho(8)=1.005，而乘法预测值为 2.0。因此，作者将观察到的脆弱性归因于编码器和递归固定点输出的结构性属性，而不是迭代过程中的累积效应；同时作者指出，K=4 条件属于分布外情况。
- 计划-动作一致性探针的检测 AUC 从朴素破坏下的 0.996 降至自适应攻击下的 0.493，约等于随机水平。
- 在匹配误报率校准下，将一致性探针与动作异常探针结合，并未在任何 PGD-10 单元格中使防御后的任务成功率超过未防御条件。
- 结论仅适用于所测试的架构、模拟操纵基准、扰动类别和输出级监控器；所提供的摘录不完整，无法据此证明其能迁移到物理世界，也无法证明防御措施存在普遍的不可能性结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.17786v1](https://arxiv.org/abs/2607.17786v1)
