---
source: arxiv
url: https://arxiv.org/abs/2605.06125v1
published_at: '2026-05-07T12:31:09'
authors:
- Ye Shang
- Quanjun Zhang
- Haichuan Hu
- Chunrong Fang
- Liang Xiao
- Zhenyu Chen
topics:
- test-evolution
- coding-agents
- software-testing
- code-intelligence
- benchmarking
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution

## Summary
## 摘要
TEBench 是一个项目级基准，用于评测编码代理在生产代码提交后更新测试的能力。它很重要，因为当前代理只能找到约一半受影响的测试，而过时或缺失的测试会让已变更的行为得不到检查。

## 问题
- 现有测试演化基准把受影响的测试方法作为输入，因此跳过了在整个仓库中搜索的环节。
- 真实提交可能会破坏测试，让通过的测试在语义上过时，或加入完全没有测试覆盖的行为。
- 测试演化效果差会让测试套件通过，但不再检查提交所改变的行为。

## 方法
- 任务输入是一个仓库和一个改变生产代码的提交；输出是一个测试补丁。
- TEBench 将每个实例标注为 Test-Breaking、Test-Stale、Test-Missing，或这些类型的组合。
- 数据集来自 Defects4J Java 项目，并经过静态过滤、执行检查和质量过滤。
- 评估将测试识别与补丁质量分开：对受影响测试使用 precision、recall 和 F1，对更新使用可执行性、覆盖重叠和 token 级修改相似度。
- 论文评测了 Claude Code、Codex CLI 和 OpenCode 上的七种代理配置，另加一个启发式基线。

## 结果
- TEBench 包含来自 10 个 Java 项目的 314 个任务实例，起点是 67,670 个初始提交和 14 个 Maven Defects4J 项目。
- 最终数据集覆盖 172 个 Test-Breaking 任务、207 个 Test-Stale 任务和 199 个 Test-Missing 任务；标签可以重叠。
- 七种代理配置的识别 F1 分数为 45.7% 到 49.4%，彼此差距小于 4 个百分点。
- Test-Stale 最难，平均 F1 约为 36%，因为代理主要跟随执行失败信号，会漏掉需要语义更新但仍能通过的测试。
- 穷尽式结构依赖分析的召回率也只有 66%，约三分之一受影响测试不在直接依赖追踪范围内。
- 论文报告称，代理补丁通常可以编译和运行，但其编辑内容与开发者编写的真实答案差异很大。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06125v1](https://arxiv.org/abs/2605.06125v1)
