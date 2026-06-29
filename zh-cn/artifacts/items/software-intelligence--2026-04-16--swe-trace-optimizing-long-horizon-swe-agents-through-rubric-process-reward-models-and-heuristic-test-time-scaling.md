---
source: arxiv
url: http://arxiv.org/abs/2604.14820v1
published_at: '2026-04-16T09:41:47'
authors:
- Hao Han
- Jin Xie
- Xuehao Ma
- Weiquan Zhu
- Ziyao Zhang
- ZhiLiang Long
- Hongkai Chen
- Qingwen Ye
topics:
- software-engineering-agents
- process-reward-model
- test-time-scaling
- swe-bench
- long-horizon-reasoning
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-TRACE: Optimizing Long-Horizon SWE Agents Through Rubric Process Reward Models and Heuristic Test-Time Scaling

## Summary
## 摘要
SWE-TRACE 是一个面向软件工程智能体的训练与推理流程，目标是让长链路的 bug 修复轨迹更短、更容易学习，也更便宜。它把筛选后的监督数据、逐步奖励信号和推理时的引导式搜索结合起来。

## 问题
- 长链路 SWE 智能体会在重复探索、反复调用工具和噪声很大的调试轨迹上浪费 token，这会削弱监督训练效果。
- 强化学习里，最终测试通过或失败只是稀疏奖励，智能体几乎拿不到关于哪些中间动作有帮助的信号。
- 常见的测试时缩放方法会采样很多完整轨迹再重新排序，这会抬高仓库级任务的延迟和算力开销。

## 方法
- 通过筛选超过 1,000 个 GitHub 仓库来构建一个可执行的大规模训练集，保留其中 77 个可以编译并运行测试的仓库，生成约 140K 个候选 bug 实例，再把它们过滤到 60K 个高质量样本。
- 使用面向测试的 bug 合成：把测试映射到相关函数，只在与测试相关的代码区域注入 bug，并在生成时结合相关测试进行条件约束，让问题和修复保持可执行、可验证。
- 用 LLM 多任务级联蒸馏更短的监督轨迹：在每一步生成局部定位、检查、编辑、验证、总结等模式下的动作候选，再用 oracle 验证器选出下一步最佳动作，并压缩掉冗余步骤。
- 训练时使用基于 rubric 的过程奖励模型，对进展、补丁方向、有用信息增量、token 成本和冗余动作提供密集的逐步反馈，而不是只依赖最终执行奖励。
- 在推理时复用这个过程奖励模型，尽早给动作候选打分并剪掉较弱的候选，还在上下文过长时用它保留高价值的历史步骤记忆缓冲区。

## 结果
- 面向测试的 bug 合成把 25 个仓库上的基准构建成功率从 35.0% 提高到 50.7%，过滤后的样本从 20,638 增加到 24,995。
- 该数据流程在 77 个仓库中生成了约 140K 个候选 bug 问题，并保留了 60K 个过滤后的训练实例。
- 论文声称在标准 SWE 基准上取得了最先进的提升，包括 SWE-bench Verified，并称该方法在减少 token 使用和推理延迟的同时，也提升了 4B 和 30B 模型的表现。
- 给出的摘要片段没有包含主要基准表或 SWE-bench Verified 的准确解决率数字，所以这里无法给出数据构建之外的核心定量结论。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14820v1](http://arxiv.org/abs/2604.14820v1)
