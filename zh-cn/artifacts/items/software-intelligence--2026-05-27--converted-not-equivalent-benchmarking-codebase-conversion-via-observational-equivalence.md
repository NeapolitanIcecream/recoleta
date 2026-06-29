---
source: arxiv
url: https://arxiv.org/abs/2605.29054v1
published_at: '2026-05-27T19:57:15'
authors:
- Linxin Song
- Jiefeng Chen
- Yue Huang
- Bhavana Dalvi Mishra
- Chi Wang
- Jieyu Zhao
- Jinsung Yoon
- Tomas Pfister
topics:
- codebase-conversion
- code-agents
- code-intelligence
- software-engineering-benchmarks
- pytorch-to-jax
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Converted, Not Equivalent: Benchmarking Codebase Conversion via Observational Equivalence

## Summary
## 摘要
T2J-Bench 测试将 PyTorch 训练代码库转换为 JAX 后，是否能保留可观察到的训练行为，而不只是能运行。经过 355 次盲测尝试，表现最好的系统在 pass@1 下的通过率仍低于 30%，说明当前代码代理与目标之间差距很大。

## 问题
- 代码代理常常接受那些在本地能跑通、却破坏用户所需训练行为的转换，例如梯度、优化器更新、奖励项或短期训练轨迹。
- 以往的转换基准往往只看最终结果或浅层执行检查，容易漏掉训练管线内部的语义漂移。
- 这对软件现代化很重要，因为转换后的机器学习代码库可能看起来可用，实际却产生不同的训练动态。

## 方法
- 论文提出 T2J-Bench，一个用于把完整的 PyTorch 训练代码库转换为 JAX 的基准。
- 每个任务都使用从源代码库推导出的固定等价契约，并限制 seed、精度、小数据集、batch size 和 replay 步数等配置。
- 验证器按三个顺序阶段运行：Spec 检查接口和 schema；Numeric 检查输出、loss、梯度和任务特定张量；Behavioral 在固定随机种子下检查短期训练动态。
- 数据集包含 45 个数据点，覆盖 15 个模型家族，任务类型包括 SFT、DPO 和 PPO。
- 代理收到一个冻结的最小约束提示词，用来定义公开训练接口，但不透露评测器内部实现。

## 结果
- 在 T2J-Bench 上，pass@1 表现最好的受控模型是 Claude Opus 4.7，整体通过率为 28.9%；表现最好的原生代码代理是带 Opus 4.7 的 Claude Code，pass@1 为 26.7%。
- 在 pass@3 下，共享脚手架中的 Claude Opus 4.7 达到 46.7% 的整体通过率，而带 Opus 4.7 的 Claude Code 达到 42.2%；超过一半任务仍未解决。
- Spec 通过率远高于端到端通过率：带 Opus 4.7 的 Claude Code 在 pass@1 下的 Spec 通过率为 91.1%，但经过 Numeric 和 Behavioral 检查后，整体只有 26.7%。
- Numeric 检查是主要失败点：对 pass@1 下最强的受控模型，Spec 为 84.4%，在 Spec 条件下的 Numeric 为 39.5%，在 Numeric 条件下的 Behavioral 为 86.7%，整体为 28.9%。
- token 花费和成功率没有稳定对应关系：平均每次尝试的 token 数相差 4.7 倍，整体通过率只相差 2.2 倍。
- 所有被评测系统都高估了自己的成功率，相比固定验证器高出 66.6 到 97.8 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29054v1](https://arxiv.org/abs/2605.29054v1)
