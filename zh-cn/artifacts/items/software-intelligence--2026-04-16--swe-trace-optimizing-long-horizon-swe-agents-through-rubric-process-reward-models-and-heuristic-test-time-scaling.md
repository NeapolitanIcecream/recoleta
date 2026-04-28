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
SWE-TRACE 是一套面向软件工程代理的训练与推理流程，目标是让长程错误修复轨迹更短、更容易学习、运行成本更低。它把筛选后的监督数据、步骤级奖励信号和推理时的引导式搜索结合在一起。

## 问题
- 长程 SWE 代理会把 token 浪费在冗余探索、重复工具调用和噪声调试轨迹上，这会削弱监督训练效果。
- 对强化学习来说，最终测试通过或失败属于稀疏奖励，因此代理几乎得不到关于哪些中间动作有帮助的信号。
- 常见的 test-time scaling 方法会采样许多完整轨迹再重新排序，这会提高仓库级任务上的延迟和计算成本。

## 方法
- 通过筛查 1,000 多个 GitHub 仓库来构建一个大型可执行训练集，保留其中 77 个能够构建并运行测试的仓库，生成约 14 万个候选 bug 实例，再过滤到 6 万个高质量样本。
- 使用测试感知的 bug 合成：将测试映射到相关函数，只在与测试关联的代码区域中注入 bug，并在生成时以相关测试为条件，使问题和修复保持可执行且可验证。
- 用 LLM 多任务级联蒸馏更短的监督轨迹：在每一步为 localize、inspect、edit、validate 和 summarize 等模式生成动作候选，再用 oracle verifier 选择最佳下一步动作，并压缩掉冗余步骤。
- 训练时使用基于 rubric 的过程奖励模型，在进展、补丁方向、有用信息增益、token 成本和冗余动作等方面提供密集的步骤级反馈，而不是只依赖最终执行奖励。
- 在推理阶段复用该过程奖励模型，及早为较弱的动作候选打分并剪枝；当上下文变得过长时，也用它来维护一个保存高价值历史步骤的 memory buffer。

## 结果
- 测试感知 bug 合成把 25 个仓库上的基准构建成功率从 35.0% 提高到 50.7%，过滤后的样本数从 20,638 增加到 24,995。
- 该数据流程在 77 个仓库上产生了约 14 万个候选 bug 问题，并保留了 6 万个过滤后的训练实例。
- 论文声称该方法在标准 SWE 基准上取得了 state-of-the-art 提升，包括 SWE-bench Verified，并表示它在降低 token 使用量和推理延迟的同时，也提升了 4B 和 30B 模型的表现。
- 当前提供的摘录不包含主要基准表，也没有给出 SWE-bench Verified 的确切 resolution rate 数字，因此除数据构建外，这里的核心定量结论还无法核实。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14820v1](http://arxiv.org/abs/2604.14820v1)
