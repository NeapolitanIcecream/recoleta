---
source: arxiv
url: http://arxiv.org/abs/2604.05656v1
published_at: '2026-04-07T09:56:03'
authors:
- Wuyang Luan
- Junhui Li
- Weiguang Zhao
- Wenjian Zhang
- Tieru Wu
- Rui Ma
topics:
- vision-language-action
- flow-matching
- robot-inference-acceleration
- self-distillation
- generalist-robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# SnapFlow: One-Step Action Generation for Flow-Matching VLAs via Progressive Self-Distillation

## Summary
## 摘要
SnapFlow 通过一种自蒸馏方法，把基于 flow matching 的 VLA 动作生成从 10 步去噪压到 1 步，同时保持甚至略微提升任务成功率。论文针对的是 \(\pi\)0.5 和 SmolVLA 这类大规模机器人策略的推理延迟。

## 问题
- 基于 flow matching 的 VLA 用迭代去噪生成动作，通常要做 10 次 Euler 步，这部分占了大多数推理时间。对 \(\pi\)0.5 来说，去噪大约占端到端 274 ms 中的 241 ms，也就是 80% 的延迟。
- 直接把步数降到 1 步并不稳定，因为模型训练时学的是适合多步积分的局部速度，而不是从噪声到动作的一次大跳跃。
- 这会影响机器人控制，因为边缘端和实时场景的控制周期预算很紧。论文举了 3 Hz 控制作为例子，此时 330 ms 需要同时覆盖感知和动作生成。

## 方法
- SnapFlow 让同一个 flow-matching VLA 同时做两件事：用标准 flow matching 做局部速度预测，再用一致性风格的捷径目标直接生成 1 步动作。
- 这个捷径目标是一个两步 Euler 估计，由模型在时间 1 和 0.5 的边际速度预测构造出来，而不是用论文认为会造成轨迹漂移的条件速度。
- 训练时把原始 flow-matching 损失和捷径损失混合起来，这样模型在保留速度估计能力的同时，学习准确的一步跳转。
- 一个零初始化的目标时间嵌入告诉网络当前该像原来的局部去噪器工作，还是像新的单步生成器工作，而不改主干架构。
- 这个方法可以直接接到现有的 flow-matching VLA 上，不需要外部教师模型。论文报告只训练动作专家和新的目标时间嵌入，大约 30k 步、在一张 A800 上约 12 小时。

## 结果
- 在 \(\pi\)0.5（3B）上，覆盖 4 个 LIBERO 套件、40 个任务和 400 个 episode，SnapFlow 在 1 步时达到 **98.75%** 平均成功率，10 步基线是 **97.75%**，朴素 1 步是 **96.75%**。
- 在 A800 上测 \(\pi\)0.5 延迟时，端到端时间从 **274 ms** 降到 **83 ms**，端到端加速为 **3.3x**；去噪加速报告为 **9.6x**。
- 在 \(\pi\)0.5 的离线 LIBERO 指标上，MSE 从 **0.01169** 降到 **0.00773**（**-33.9%**），标准差从 **0.05412** 降到 **0.02964**（**-45.2%**），P95 MSE 从 **0.02357** 降到 **0.01664**（**-29.4%**），余弦相似度从 **0.9885** 升到 **0.9916**。
- \(\pi\)0.5 在各个 LIBERO 套件上的成功率变化分别是：Spatial **98.0% -> 99.0%**，Object **100.0% -> 100.0%**，Goal **96.0% -> 99.0%**，Long-10 **97.0% -> 97.0%**。
- 在 SmolVLA（500M）上，SnapFlow 将 PushT 的 MSE 从 **0.468** 降到 **0.429**（**-8.3%**），把余弦相似度从 **0.765** 提到 **0.818**（**+6.9%**），并带来 **3.56x** 的端到端加速。
- 在长时程任务的动作步数扫描中，SnapFlow 在不同执行时长下都保持优势；摘要报告在 **n_act = 5** 时成功率为 **93%**，基线是 **90%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05656v1](http://arxiv.org/abs/2604.05656v1)
