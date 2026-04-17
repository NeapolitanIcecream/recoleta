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
SnapFlow 将基于 flow-matching 的 VLA 动作生成从 10 次去噪压缩到 1 步，并通过一种自蒸馏训练方法保持或略微提高任务成功率。论文关注 \(\pi\)0.5 和 SmolVLA 这类大型机器人策略的推理延迟。

## 问题
- 基于 flow-matching 的 VLA 通过迭代去噪生成动作，通常使用 10 个 Euler 步，这部分时间占据了推理的大头。对 \(\pi\)0.5 来说，去噪在端到端 274 ms 中约占 241 ms，也就是 80% 的延迟。
- 直接把步数降到 1 并不可靠，因为模型训练时学的是用于多步积分的局部速度预测，不是从噪声到动作的单次大跨度跳转。
- 这对机器人控制很关键，因为边缘部署和实时场景的控制周期预算很紧。论文举了 3 Hz 控制的例子，其中 330 ms 必须同时覆盖感知和动作生成。

## 方法
- SnapFlow 训练同一个 flow-matching VLA 同时完成两件事：用于局部速度预测的标准 flow matching，以及用于直接 1 步动作生成的 consistency 风格捷径目标。
- 这个捷径目标是一个两步 Euler 估计，由模型自己在时间 1 和 0.5 的边际速度预测构成，而不是使用论文认为会导致轨迹漂移的条件速度。
- 训练时将原始 flow-matching loss 和捷径 loss 混合，使模型在保留速度估计能力的同时，学会准确的单步跳转。
- 一个零初始化的 target-time embedding 用来告诉网络当前应当像原始的局部去噪器一样工作，还是像新的单步生成器一样工作，同时不需要改动主体架构。
- 该方法可以直接用于现有的 flow-matching VLA，不需要外部教师模型，只训练动作专家和新的 target-time embedding；论文报告训练约 30k steps，在一张 A800 上约需 12 小时。

## 结果
- 在 \(\pi\)0.5 (3B) 上，覆盖 4 个 LIBERO suite、40 个任务和 400 个 episode，1 步的 SnapFlow 平均成功率达到 **98.75%**，10 步基线为 **97.75%**，直接 1 步的朴素做法为 **96.75%**。
- 在 A800 上测得的 \(\pi\)0.5 延迟中，端到端时间从 **274 ms** 降到 **83 ms**，端到端加速 **3.3x**；去噪部分加速为 **9.6x**。
- 在 \(\pi\)0.5 的离线 LIBERO 指标上，MSE 从 **0.01169** 改善到 **0.00773**（**-33.9%**），标准差从 **0.05412** 降到 **0.02964**（**-45.2%**），P95 MSE 从 **0.02357** 降到 **0.01664**（**-29.4%**），余弦相似度从 **0.9885** 提高到 **0.9916**。
- 各个 \(\pi\)0.5 LIBERO suite 的成功率变化为：Spatial **98.0% -> 99.0%**，Object **100.0% -> 100.0%**，Goal **96.0% -> 99.0%**，Long-10 **97.0% -> 97.0%**。
- 在 SmolVLA (500M) 上，SnapFlow 将 PushT MSE 从 **0.468** 降到 **0.429**（**-8.3%**），将余弦相似度从 **0.765** 提高到 **0.818**（**+6.9%**），并带来 **3.56x** 的端到端加速。
- 在长时程任务的 action-step sweep 中，SnapFlow 在不同执行时域下都保持优势；摘要报告在 **n_act = 5** 时成功率为 **93%**，基线为 **90%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05656v1](http://arxiv.org/abs/2604.05656v1)
