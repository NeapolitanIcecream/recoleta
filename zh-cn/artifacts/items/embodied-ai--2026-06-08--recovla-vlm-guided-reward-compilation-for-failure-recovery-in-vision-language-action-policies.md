---
source: arxiv
url: https://arxiv.org/abs/2606.09630v1
published_at: '2026-06-08T15:29:09'
authors:
- Haodi Hu
- Chung-Ta Huang
- Jing Liu
- Ye Wang
- Kei Suzuki
- Matthew Brand
- Toshiaki Koike-Akino
topics:
- vision-language-action
- robot-failure-recovery
- residual-rl
- vlm-reward-compilation
- sim2real
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies

## Summary
## 摘要
ReCoVLA 在保持基础 vision-language-action 策略冻结的同时，为失败后的机器人操作状态训练恢复策略。VLM 先识别失败类型和恢复阶段，再由奖励编译器构建 residual-RL 在仿真中使用的奖励，之后进行零样本实物部署。

## 问题
- VLA 操作策略在落到分布外状态后可能失效，比如物体掉落、放错容器、失去抓取，或接触密集步骤没有完成。
- 对整个 VLA 做微调需要恢复演示，也可能破坏已有技能；通用 RL 奖励常常过于稀疏，或把奖励项的激活顺序设错。
- 这个问题很重要，因为机器人即使能完成标准任务，也需要在执行出错时进行针对性纠正。

## 方法
- 基础 VLA 保持冻结。恢复阶段里，residual policy 在 VLA 动作上叠加纠正动作。
- Qwen3-VL-8B-Instruct 分析回放图像和指令，输出结构化描述：失败类别、恢复阶段、活动实体、置信度和奖励掩码。
- 一个确定性编译器把这个描述映射到仿真器奖励项，包括距离进展、抓取状态、放置进展和关节闭合进展。
- 阶段门控只在前置条件满足后才激活奖励项，比如先抓住物体，再启用放置奖励。
- residual policies 在仿真中用 PPO、基于 VLA 潜在特征训练，然后在真实机器人上由 VLM 检测到已知失败类别时选用。

## 结果
- 在三个 Fetch 任务的仿真中，ReCoVLA 把无恢复 π0.5 基线的平均成功率从 36.7% 提高到 66.7%；平均 Q-score 从 0.56 提高到 0.83。
- 在物理零样本 sim-to-real 测试中，ReCoVLA 的平均成功率达到 61.7%，平均 Q-score 达到 0.75；报告称比基线高 18.3 个百分点、Q-score 高 0.21。
- 带阶段门控的方法优于 VLM 选择但不门控的奖励消融：M3 的仿真成功率为 48.3%，比 ReCoVLA 低 18.4 个百分点。
- 任务级仿真提升包括工具箱整理从 25% 提高到 60%，蔬菜分类从 30% 提高到 65%。
- 在 OpenVLA 上，同样的恢复设计把基础策略的平均仿真成功率从 23.3% 提高到 45.0%。
- 在 OOD 物体替换中，无恢复基线的成功率为 10.0%、Q-score 为 0.22；ReCoVLA 的成功率为 53.3%、Q-score 为 0.65。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09630v1](https://arxiv.org/abs/2606.09630v1)
