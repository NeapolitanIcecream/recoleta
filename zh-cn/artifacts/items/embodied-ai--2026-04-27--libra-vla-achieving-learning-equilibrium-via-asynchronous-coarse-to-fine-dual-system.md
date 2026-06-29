---
source: arxiv
url: https://arxiv.org/abs/2604.24921v1
published_at: '2026-04-27T19:02:46'
authors:
- Yifei Wei
- Linqing Zhong
- Yi Liu
- Yuxiang Lu
- Xindong He
- Maoqing Yao
- Guanghui Ren
topics:
- vision-language-action
- generalist-robot-policy
- robot-manipulation
- hierarchical-control
- diffusion-policy
- asynchronous-inference
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System

## Summary
## 摘要
Libra-VLA 是一个用于机器人操作的视觉-语言-动作策略，它把动作生成分成粗粒度离散意图和连续细粒度控制。论文声称，在 LIBERO 和 LIBERO-Plus 上，它的成功率更高，同时更少运行成本较高的 VLM 规划器。

## 问题
- 许多 VLA 策略把图像和语言直接映射为高频电机指令，这让同一个模型同时处理语义推理和精细控制。
- 这很重要，因为操作任务有自然层级：机器人先需要一个大致方向或目标，然后需要精确的姿态调整来完成接触和对齐。
- 先前的时间层级方法缩短了长任务，但它们仍然把每个低层步骤保留为从语言-视觉特征到连续动作的困难映射。

## 方法
- Libra-VLA 将策略分解为 `P(fine action | coarse action, observation) * P(coarse action | observation, instruction)`。
- 语义规划器使用 InternVL2.5-2B VLM，并行接一个粗动作头，从量化后的归一化动作中预测离散的宏方向 token。
- 动作细化器使用扩散 Transformer 和 SigLIP 视觉编码器，把粗意图转换为连续机器人动作。
- 训练时把粗 token 的交叉熵和细动作的扩散 MSE 结合起来，并使用一种课程学习方式，从真实粗 token 逐步切换到规划器预测的 token。
- 推理时，规划器会预测更长的粗粒度时域到 FIFO 意图缓冲区；在 `M=2`、动作块大小为 `5` 时，它会预测 `10` 个粗步骤，而细化器按控制频率运行。

## 结果
- 在 LIBERO 上，Libra-VLA 报告的平均成功率为 `97.2%`，高于 pi0.5 的 `96.9%`、GE-Act 的 `96.5%` 和 DD-VLA 的 `96.3%`。
- LIBERO 套件分项得分为 `98.6%` Spatial、`99.4%` Object、`98.0%` Goal 和 `92.8%` Long。
- 在 LIBERO-Plus 的 zero-shot 迁移上，Libra-VLA 报告的平均成功率为 `79.5%`，高于 OpenVLA-OFT 的 `69.6%` 和 pi0-Fast 的 `61.6%`。
- LIBERO-Plus zero-shot 类别得分为 `68.9%` Camera、`48.8%` Robot、`92.7%` Language、`97.9%` Light、`93.4%` Background、`86.3%` Noise 和 `77.5%` Layout。
- 论文说明，仿真和真实世界实验都没有使用大规模机器人数据预训练；摘要没有给出真实世界成功率数字。
- 论文声称，动作分解粒度和性能之间存在倒 U 形关系，规划器和细化器的学习难度平衡时表现最好；摘要没有给出这一结论的消融数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24921v1](https://arxiv.org/abs/2604.24921v1)
