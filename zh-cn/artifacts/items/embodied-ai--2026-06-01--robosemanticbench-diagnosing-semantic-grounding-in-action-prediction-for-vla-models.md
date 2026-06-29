---
source: arxiv
url: https://arxiv.org/abs/2606.02277v1
published_at: '2026-06-01T14:02:37'
authors:
- Bin Yu
- Yao Zhang
- Haishan Liu
- Shijie Lian
- Yuliang Wei
- Xiaopeng Lin
- Zhaolong Shen
- Changti Wu
- Ruina Hu
- Bailing Wang
- Cong Huang
- Kai Chen
topics:
- vision-language-action
- robot-benchmark
- semantic-grounding
- action-prediction
- embodied-evaluation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# RoboSemanticBench: Diagnosing Semantic Grounding in Action Prediction for VLA Models

## Summary
## 摘要
RoboSemanticBench 是一个诊断性基准，用来测试 VLA 模型在选择机器人动作时是否使用了指令语义。论文发现，许多微调后的 VLA 策略可以抓取候选物体，但在选择语义上正确的目标时，表现接近随机水平。

## 问题
- 预训练语言模型或视觉-语言骨干模型中的语义知识，原本应该进入 VLA 模型的机器人动作预测，但模仿学习式微调可能会奖励捷径。
- 常规机器人基准会把运动技能、物体识别和语言理解混在一起，所以较高的任务分数可能掩盖了薄弱的语义目标选择能力。
- 这个问题很重要，因为真实机器人指令可能要求先做算术、常识、事实知识或多步语言理解，再让机器人选出正确物体。

## 方法
- RoboSemanticBench 把多项选择题转换成抓取放置任务：机器人需要回答问题，把答案选项对应到一个可见方块上，再把该方块移动到答案区域。
- 该基准包含三个子集：RSB-Math 用于受控算术，RSB-HardMath 来自 GSM8K 风格的文字题，RSB-General 来自常识题和 MMLU 风格题目。
- 每个子集都有 4 选和 10 选套件，选项到方块的映射和方块布局都经过随机化，以减少固定颜色、字母和位置捷径。
- 论文报告了任务成功率（TSR）、抓取成功率（GSR）和归一化语义落地（nSG）。其中 nSG=0 表示在抓取成功后，目标选择是随机的。
- 作者在经过 100,000 步微调后评估了 GO1、OpenVLA-OFT、DexVLA、TinyVLA、PD-VLA、pi0、pi0.5、GR00T N1.7 和 QwenGR00T，通常批大小为 64。

## 结果
- 在每个模型和套件的 500 个仿真回合中，pi0.5 的平均 TSR 最高，为 21.8%；其后依次是 pi0 的 12.7%、GR00T N1.7 的 12.6%、OpenVLA-OFT 的 11.1%、QwenGR00T 的 10.7%、PD-VLA 的 9.0%、TinyVLA 的 8.6%、DexVLA 的 6.5% 和 GO1 的 2.0%。
- 在 4 选套件中，随机选中目标的概率是 25%；在 10 选套件中是 10%。在按抓取成功率条件化并通过 nSG 计算后，许多模型的表现接近或低于这些水平。
- OpenVLA-OFT（-7.2%）、GO1（-19.4%）、DexVLA（-3.4%）、pi0（-5.7%）、GR00T N1.7（-5.9%）和 QwenGR00T（-7.1%）的平均 nSG 为负。
- 按 nSG 看，pi0.5 是最强模型，平均为 5.2%；PD-VLA 为 3.2%，TinyVLA 接近随机，为 0.2%。
- 在 10 选套件中，pi0.5 在 RSB-Math-10 上达到 12.0% TSR，在 RSB-HardMath-10 上为 16.2%，在 RSB-General-10 上为 19.6%；其他几个模型都低于 9%。
- ReasoningVLA 将 QwenGR00T 的平均 TSR 从 10.7% 提高到 16.0%，六个套件都有提升，但论文指出这仍然没有解决语义落地问题；QwenGR00T 的联合训练把平均 TSR 降到了 8.2%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.02277v1](https://arxiv.org/abs/2606.02277v1)
