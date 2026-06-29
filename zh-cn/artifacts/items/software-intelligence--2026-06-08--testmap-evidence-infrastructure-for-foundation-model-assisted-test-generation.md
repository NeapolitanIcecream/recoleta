---
source: arxiv
url: https://arxiv.org/abs/2606.10211v1
published_at: '2026-06-08T22:04:51'
authors:
- Hunter Leary
- Luke Hanuska
- Chris Brown
topics:
- test-generation
- foundation-models
- code-intelligence
- software-testing
- dotnet
- evaluation-infrastructure
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# TestMap: Evidence Infrastructure for Foundation-Model-Assisted Test Generation

## Summary
TestMap 是一个开源原型，用于记录在真实 C#/.NET 仓库中由基础模型生成的单元测试证据。它会检查每个候选测试是否能构建、是否通过、是否提升覆盖率或变异信号、是否需要修复，以及是否适合审查。

## Problem
- 基础模型生成的测试可能可以编译并通过，但仍然只检查很弱或错误的行为，所以团队在用它们验证生产代码之前需要证据。
- 构建日志、覆盖率、变异结果、代码指标和 test smell 等信号分散在不同工具里，很难和单个生成测试对应起来。
- 这件事很重要，因为测试生成正在进入日常开发流程，但信任仍然不高：Stack Overflow 2025 报告称 45% 的受访者不信任 AI 工具输出，Google DORA 2025 报告称 30% 的受访者对 AI 生成代码几乎没有信任或完全没有信任。

## Approach
- TestMap 读取仓库，记录提交和项目元数据，使用 Roslyn 打开 .NET 解决方案，并把项目证据存入 SQLite。
- 它会在可行时运行静态分析、基线测试、覆盖率收集、使用 Stryker.NET 的变异测试、代码指标，以及基于 xNose 的 C# test smell 检测。
- 它会把生成的候选测试映射到源方法、相关测试、未覆盖代码、存活突变体、提示词、模型、生成策略、修复预算和执行结果。
- 生成流程会先为目标方法构建一份证据包，必要时创建上下文图，然后通过分阶段规划和测试创建来提示模型。
- 它会保留失败、已修复、低影响和证据为正的候选测试，方便研究者比较模型、提示词、上下文模式、pass@k 预算和修复循环。

## Results
- 摘要没有给出生成测试质量的定量基准结果，例如通过率、覆盖率提升、变异得分提升或开发者接受度。
- TestMap 定义了 9 类证据：仓库、目标、生成、执行、测试影响、质量、失败、修复和策略证据。
- 它定义了 4 种流水线结果：ValidationFailed、Validated、ValidatedLowImpact 和 ValidatedEvidencePositive。
- 该原型面向 C#/.NET 仓库，并使用了 Roslyn、TRX 测试结果、Cobertura 覆盖率报告、Stryker.NET 变异报告、SQLite 和 xNose 等命名工具。
- 论文声称，主要收益是能在生成、验证、修复和测量之间跟踪到候选级别，包括许多流水线会丢弃的失败候选测试。

## Link
- [https://arxiv.org/abs/2606.10211v1](https://arxiv.org/abs/2606.10211v1)
