---
source: arxiv
url: https://arxiv.org/abs/2605.13632v1
published_at: '2026-05-13T14:58:29'
authors:
- Yiran Ling
- Qing Lian
- Jinghang Li
- Qing Jiang
- Tianming Zhang
- Xiaoke Jiang
- Chuanxiu Liu
- Jie Liu
- Lei Zhang
topics:
- vision-language-action
- interactive-robot-policy
- embodied-reasoning
- robot-data-scaling
- ood-generalization
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Guide, Think, Act: Interactive Embodied Reasoning in Vision-Language-Action Models

## Summary
## 总结
GTA-VLA 让用户用点、框或手绘轨迹等视觉线索引导机器人 VLA 策略，然后在动作前的推理中使用这些线索。本文关注在视觉歧义和分布外变化下的失败恢复，同时保留自主执行能力。

## 问题
- 现有 VLA 策略常把图像和语言输入直接映射为动作，在光照、相机位姿、物体身份或杂乱程度与训练数据不同的时候容易失效。
- 具身 Chain-of-Thought 方法会暴露中间推理，但摘录中说它们没有一种让人类在执行过程中直接修正错误空间定位的方法。
- 这很重要，因为很多操作失败都来自选错物体、抓取点、接触区域或运动路径，而用户往往只需要一个简单的空间线索就能修正。

## 方法
- GTA-VLA 在策略输入中加入一个可选的空间先验：主摄像头图像上的二维可供性点、边界框或轨迹。
- 以 Qwen3-VL-2B 为骨干模型生成包含任务推理、视觉定位和机器人运动推理的空间-视觉推理序列。
- 模型把这些推理 token 的隐藏状态传给 Flow-Matching 动作头，由它预测连续动作片段。
- 推理以较低频率运行，动作头则用缓存的推理状态以更高控制频率运行，从而降低控制过程中自回归推理的成本。
- 作者基于大约 306K 条真实世界操作轨迹构建了 Interact-306K，并从现有机器人数据中加入合成的空间指导和推理监督。

## 结果
- 在域内的 SimplerEnv WidowX 基准上，GTA-VLA 报告成功率为 81.2%，并称这是当前最优表现。
- 摘录中的表格显示，OpenVLA 在 SIMPLER-Env Bridge 任务上的平均成功率为 14.6%，各任务分数分别为 Spoon 4.2%、Carrot 0.0%、Cube 8.3% 和 Eggplant 45.8%。
- 在 LIBERO 上，摘录中的表格显示 OpenVLA 在 Spatial、Object、Goal 和 Long 任务上的平均成功率为 76.5%；OpenVLA-OFT 的平均成功率为 95.3%。
- 论文提出了 SimplerEnv-Plus，包含相机变化、光照变化、未见过的物体和语言扰动等 OOD 变化。
- 在 OOD 视觉变化和空间歧义下，论文声称一次视觉交互就能提升任务成功率，优于现有方法，但摘录没有给出具体的 OOD 提升数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13632v1](https://arxiv.org/abs/2605.13632v1)
