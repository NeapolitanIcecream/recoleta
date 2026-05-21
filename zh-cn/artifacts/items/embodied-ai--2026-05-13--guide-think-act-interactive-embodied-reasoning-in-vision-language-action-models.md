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
## 摘要
GTA-VLA 允许用户用点、框或绘制轨迹等视觉提示来引导机器人 VLA 策略，并在行动前把这些提示用于推理。论文目标是在视觉歧义和分布外偏移下恢复失败，同时保留自主执行能力。

## 问题
- 现有 VLA 策略通常把图像和语言输入直接映射到动作；当光照、相机位姿、物体身份或杂物情况不同于训练数据时，这种方式可能失败。
- 具身 Chain-of-Thought 方法会展示中间推理，但摘录称，这些方法缺少一种直接方式，让人类在执行过程中纠正错误的空间定位。
- 这一点很重要，因为许多操作失败来自选错物体、抓取点、接触区域或运动路径，而用户通常可以用一个简单的空间提示来修正。

## 方法
- GTA-VLA 在策略输入中加入一个可选的空间先验：主相机图像上的 2D 可供性点、边界框或轨迹。
- Qwen3-VL-2B 骨干生成一段空间-视觉推理序列，包含任务推理、视觉定位和机器人运动推理。
- 模型把这些推理 token 的隐藏状态传给 Flow-Matching 动作头，由动作头预测连续动作片段。
- 推理以较低频率运行，动作头则使用缓存的推理状态以较高控制频率运行，从而降低控制期间自回归推理的成本。
- 作者基于约 306K 条真实世界操作轨迹构建 Interact-306K，并从现有机器人数据中加入合成空间引导和推理监督。

## 结果
- 在域内 SimplerEnv WidowX 基准上，GTA-VLA 报告成功率为 81.2%，并声称达到当前最佳性能。
- 摘录表格列出 OpenVLA 在 SIMPLER-Env Bridge 任务上的平均成功率为 14.6%，各任务分数为 Spoon 4.2%、Carrot 0.0%、Cube 8.3%、Eggplant 45.8%。
- 在 LIBERO 上，摘录表格列出 OpenVLA 在 Spatial、Object、Goal 和 Long 任务上的平均成功率为 76.5%；OpenVLA-OFT 的平均成功率为 95.3%。
- 论文引入 SimplerEnv-Plus，其中包含相机变化、光照变化、未见物体和语言扰动等 OOD 变化。
- 在 OOD 视觉偏移和空间歧义下，论文称一次视觉交互能比现有方法提高任务成功率，但摘录没有给出具体的 OOD 提升数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13632v1](https://arxiv.org/abs/2605.13632v1)
