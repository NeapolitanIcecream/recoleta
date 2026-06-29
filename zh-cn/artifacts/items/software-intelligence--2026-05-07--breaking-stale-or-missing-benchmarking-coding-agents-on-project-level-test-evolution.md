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
TEBench 是一个项目级基准，用来评测代码代理在生产代码提交后更新测试的能力。它之所以重要，是因为现有代理只能找出大约一半受影响的测试，而过时或缺失的测试会让变更后的行为得不到检查。

## 问题
- 现有的测试演化基准把受影响的测试方法直接作为输入，因此跳过了在整个仓库中查找测试的过程。
- 真实的提交可能会让测试失败，让仍然通过的测试在语义上变得过时，或者为新增行为带来缺失测试。
- 测试演化做得不好，会让测试套件继续通过，但它已经不再检查这次提交改动的行为。

## 方法
- 任务输入是一个仓库和一个会修改生产代码的提交；输出是一个测试补丁。
- TEBench 将每个实例标注为 Test-Breaking、Test-Stale、Test-Missing，或这些类型的组合。
- 数据集来自 Defects4J 的 Java 项目，经过静态过滤、执行检查和质量过滤后得到。
- 评估把测试识别和补丁质量分开，用受影响测试的 precision、recall 和 F1，以及更新结果的可执行性、覆盖重叠和 token 级修改相似度来衡量。
- 论文评测了 Claude Code、Codex CLI 和 OpenCode 上的七种代理配置，以及一个启发式基线。

## 结果
- TEBench 包含来自 10 个 Java 项目的 314 个任务实例，来源于 67,670 个起始提交和 14 个 Maven Defects4J 项目。
- 最终数据集包含 172 个 Test-Breaking 任务、207 个 Test-Stale 任务和 199 个 Test-Missing 任务；这些标签可以重叠。
- 七种代理配置的识别 F1 在 45.7% 到 49.4% 之间，相差不到 4 个百分点。
- Test-Stale 最难，平均 F1 约为 36%，因为代理主要依赖执行失败信号，漏掉了那些通过了运行但需要语义更新的测试。
- 穷尽式结构依赖分析的召回率只有 66%，仍有大约三分之一的受影响测试无法通过直接依赖追踪找到。
- 论文指出，代理生成的补丁通常能编译并运行，但它们的修改与开发者写出的真实答案差异很大。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06125v1](https://arxiv.org/abs/2605.06125v1)
