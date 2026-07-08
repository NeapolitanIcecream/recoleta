---
source: arxiv
url: https://arxiv.org/abs/2607.04816v1
published_at: '2026-07-06T08:50:05'
authors:
- Yifu Xiong
- Wenhao Yu
- Jiaxuan Lin
- Bojun Zou
- Jiahao Li
- Lu Zhang
- Yanyong Zhang
- Jianmin Ji
topics:
- vision-language-action
- robot-manipulation
- latent-actions
- action-conditioning
- context-gating
- libero
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# CAC-VLA: Context-Gated Action Conditioning for Vision-Language-Action Models

## Summary
## 摘要
CAC-VLA 在视觉-语言-动作机器人策略中加入了潜在动作预测和门控动作条件化。它报告在 LIBERO 监督微调上的平均成功率为 98.3%，在 LIBERO-Plus 监督微调上的平均成功率为 89.5%。

## 问题
- 标准 VLA 策略把视觉-语言特征传给动作专家，因此动作专家必须从主要为感知和语言训练的特征中推断动作结构和低层机器人命令。
- 以往的动作推理方法通常会加入独立模块，用来生成动作计划、参考轨迹或动作先验，这会增加系统复杂度。
- 这个问题很重要，因为指令理解与运动控制之间的连接出现小误差，也可能导致操作失败，尤其是在长时程任务或视觉条件发生偏移时。

## 方法
- CAC-VLA 训练 VLM 查询 token，根据当前图像和语言指令预测潜在动作。
- 这些潜在动作是来自有序动作 tokenizer 的原始潜变量，由未来机器人动作片段编码得到，并带有可配置的潜在动作时程。
- 机器人不会直接执行这些潜在动作。连续动作专家把它们作为条件，同时仍然生成最终动作块。
- 交叉注意力模块为每个专家层检索潜在动作信息，context gate 按通道控制残差更新强度。
- 训练期间，冻结的 tokenizer 提供潜在目标和条件 token；推理期间，tokenizer 被移除，由 VLM 预测的潜在动作对专家进行条件化。

## 结果
- 在 LIBERO 上，CAC-VLA 报告平均成功率为 98.3%，其中 Spatial 为 98.4%，Object 为 99.8%，Goal 为 99.6%，Long 为 95.4%。它总体排名第二，低于 ACoT-VLA 的 98.5%。
- 在 LIBERO Object 和 Goal 上，CAC-VLA 报告了列表中的最高分：Object 为 99.8%，Goal 为 99.6%。
- 在 LIBERO-Plus 监督微调上，CAC-VLA 报告平均成功率为 89.5%，相比之下 ACoT-VLA 为 88.0%，复现的 π0.5 基线为 85.7%。
- 在 LIBERO-Plus 监督微调上，CAC-VLA 报告 Camera 为 91.2%，Robot 为 78.4%，Language 为 83.3%，Light 为 97.5%，Background 为 97.1%，Noise 为 95.4%，Layout 为 87.8%。
- 在 LIBERO-Plus 零样本迁移上，CAC-VLA 报告平均成功率为 83.8%，相比之下复现的 π0.5 为 81.5%，OpenVLA-OFT 为 69.6%，RIPT-VLA 为 68.4%。
- 摘录称消融实验支持潜在动作时程和 context gate 的作用，但提供的消融表被截断，没有包含所有定量比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.04816v1](https://arxiv.org/abs/2607.04816v1)
