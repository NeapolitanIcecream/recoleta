---
source: arxiv
url: https://arxiv.org/abs/2606.05960v1
published_at: '2026-06-04T09:58:55'
authors:
- Anlan Yu
- Zaishu Chen
- Zhiqing Hong
- Daqing Zhang
topics:
- world-models
- robot-data-scaling
- imitation-learning
- industrial-logistics
- synthetic-recovery-data
- embodied-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Towards a Data Flywheel for Embodied Intelligence in Logistics

## Summary
## 总结
论文提出一个物流数据飞轮，把日常仓库操作、机器人日志、演示和失败案例转成具身策略的训练数据。其具体成果是 WM-DAgger，它使用条件于动作的世界模型为模仿学习生成恢复轨迹。

## 问题
- 物流机器人在吞吐量和可靠性约束下要处理长尾包裹操作场景，而实验室演示覆盖不了足够多的失败或恢复行为。
- 依赖人工参与的 DAgger 式恢复标注在工业规模下成本很高。
- 现有运行数据类型杂，需要先对齐成观测-动作-结果序列，才能训练世界模型或策略。

## 方法
- 用少量专家演示和约 5 分钟的游玩数据训练一个条件于动作的世界模型。
- 通过预测机器人动作下未来的手眼视角观测，生成候选视频-动作恢复轨迹。
- 用纠正动作合成，将专家轨迹扰动到附近的分布外状态，并引导动作回到专家行为。
- 用一致性引导过滤，拒绝那些末帧与匹配的真实演示帧不一致的生成 rollout。
- 将过滤后的合成恢复数据与真实演示合并，用于训练模仿策略；后续工作会加入未标注的运行视频、自动化日志和部署反馈。

## 结果
- 软袋推动（5-shot）：5 条真实演示加 1,500 条生成轨迹达到 93.3% 成功率，而标准 BC 为 26.7%，DMD 为 40.0%。
- 软袋推动（20-shot）：使用 20 条真实演示和 1,500 条生成轨迹时，WM-DAgger 达到 96.7%，BC 为 30.0%，DMD 为 56.7%。
- 抓取与放置（见过）：WM-DAgger 为 84.4%，BC 为 11.1%，DMD 为 32.2%。
- 抓取与放置（未见过）：WM-DAgger 为 70.0%，BC 为 5.0%，DMD 为 11.8%。
- 投票插入和毛巾折叠在 WM-DAgger 下分别达到 73.3% 和 46.7% 的成功率，BC 分别为 13.3% 和 0.0%。
- WM-DAgger 之外更广泛的物流飞轮是提出中的工作；摘录没有给出生产规模部署指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05960v1](https://arxiv.org/abs/2606.05960v1)
