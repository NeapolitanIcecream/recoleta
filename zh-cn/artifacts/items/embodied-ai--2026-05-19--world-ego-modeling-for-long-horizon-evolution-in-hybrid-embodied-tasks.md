---
source: arxiv
url: https://arxiv.org/abs/2605.19957v1
published_at: '2026-05-19T15:10:27'
authors:
- Zuyao Lin
- Jianhui Zhang
- Peidong Jia
- Xiaoguang Zhao
- Shanghang Zhang
- Xingyu Chen
topics:
- embodied-world-model
- robot-world-model
- long-horizon-rollout
- navigation-manipulation
- video-diffusion
- robot-data-benchmark
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# World-Ego Modeling for Long-Horizon Evolution in Hybrid Embodied Tasks

## Summary
## 摘要
WEM 将长时程具身视频预测拆成场景级世界状态和机器人/物体自我状态。它面向导航与操作交错的混合任务，因为单一视频生成器往往会丢失场景一致性或受指令条件约束的接触动力学。

## 问题
- 现有具身世界模型把持久的场景结构、视角变化、机器人运动和接触动力学混在一条预测路径里，这会损害长时程滚动预测。
- 混合任务需要在多条指令下同时保持导航中的场景一致性和操作中的物理过程；现有基准多聚焦于短期操作或单提示生成。
- 这很重要，因为世界模型会用于规划、策略模拟和合成机器人数据。

## 方法
- WEM 为每一步预测两个潜在状态：一个世界状态来自视觉历史和过去指令，一个自我状态来自当前指令和最近上下文。
- 它从三种方式定义 world-ego 划分，然后默认使用语义划分：机器人和被操作的物体属于 ego，背景和未活动的物体属于 world。
- 一个冻结的 Qwen3-VL-2B-Instruct 状态预测器使用 256 个查询，分成 192 个 world 查询和 64 个 ego 查询，并带有角色条件注意力。
- 一个 Wan2.2-TI2V-5B 扩散 Transformer 被拆成一个共享的前置专家，再加 world 和 ego 两个专家。预测出的语义掩码把视频 token 路由到对应专家，并在解码前重新合并。
- 训练使用视频潜变量的 flow matching，以及用于 world-ego 掩码的 BCE 和 Dice 损失。

## 结果
- 论文引入了 HTEWorld：12.5 万个训练视频片段，超过 450 万帧，细粒度动作标注，300 条评测轨迹，以及超过 2000 条指令。
- HTEWorld 使用来自 WorldArena 的 16 项指标 EWMScore，并增加 6 项用于多轮和混合导航-操作评测的指标。
- 在边界消融中，语义 world-ego 划分比基于运动的划分高 2.12 个 EWMScore 点，比基于意图的划分高 2.79 分。
- 文中报告 WEM 在 HTEWorld 上优于微调后的 Cosmos-Predict 2.5 2B/14B 和 WoW-7B，但摘录没有给出绝对分数或完整基线差距。
- 论文还说 WEM 在现有仅操作基准上保持有竞争力，但摘录没有提供这些基准的分数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19957v1](https://arxiv.org/abs/2605.19957v1)
