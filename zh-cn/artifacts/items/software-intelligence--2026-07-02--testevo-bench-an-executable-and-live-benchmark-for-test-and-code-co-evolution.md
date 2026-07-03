---
source: arxiv
url: https://arxiv.org/abs/2607.02469v1
published_at: '2026-07-02T17:35:20'
authors:
- Jiale Amber Wang
- Kaiyuan Wang
- Pengyu Nie
topics:
- coding-agents
- code-intelligence
- software-testing
- test-generation
- test-update
- benchmarking
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# TestEvo-Bench: An Executable and Live Benchmark for Test and Code Co-Evolution

## Summary
## 摘要
TestEvo-Bench 是一个可执行、带时间戳的基准，用于测试编码智能体能否在真实代码变更后更新或新增测试。它包含从 152 个开源项目挖掘出的 746 个 Java 测试生成任务和 509 个测试更新任务。

## 问题
- 现有测试生成基准常使用固定的代码快照，因此无法检查智能体是否理解代码变更引入的新行为。
- 许多测试更新数据集依赖 diff 或静态依赖信号，缺少足够的构建和运行时上下文，难以验证生成的测试是否能编译、运行，并覆盖已变更的行为。
- 这个问题重要，因为代码智能体需要在软件变更期间维护回归测试。过时或缺失的测试会让开发者看不到行为变更。

## 方法
- 该基准从 Java Maven 仓库中挖掘相邻提交，保留能够构建且测试通过的提交对，并记录方法级代码 diff 和测试 diff。
- 它使用运行时依赖追踪和跨版本执行，将每个测试关联到已变更的生产方法。
- 测试生成要求智能体添加一个测试，该测试在新版本上通过，在旧版本上失败。
- 测试更新从新代码加恢复后的旧测试开始，然后要求智能体编辑这些测试，使其通过并覆盖已变更的行为。
- 运行器报告成功、通过和失败类别、使用 JaCoCo 的焦点行覆盖率，以及使用 Universal Mutator 的 mutation score。

## 结果
- 数据集从 59,950 条候选协同演化记录开始，最终保留来自 152 个仓库的 13,868 条已分类记录。
- 发布的快照包含 746 个测试生成任务，覆盖 1,961 个目标方法；还包含 509 个测试更新任务，覆盖 1,138 个目标方法。
- 在测试生成上，Claude Code + Claude Opus 4.7 和 Gemini CLI + Gemini 3.1 Pro 都达到 77.5% Success；它们的 Redundant 率为 19.9%，MutOnPass 分别为 56.6% 和 55.0%。
- 在测试更新上，Gemini CLI + Gemini 3.1 Pro 达到 74.6% Success，高于 Claude Code + Claude Opus 4.7 的 74.4%；MutOnPass 分别为 44.9% 和 44.6%。
- SWE-Agent 在生成任务上较低：搭配 Claude Opus 4.7 为 66.1%，搭配 Gemini 3.1 Pro 为 68.6%；harness failures 分别占 14.1% 和 10.1%。
- 两个轨道的完整评估约需 72 个机器小时。论文报告称，在较新的任务和单任务成本上限下，成功率更低，但摘录未给出这些降幅的具体数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02469v1](https://arxiv.org/abs/2607.02469v1)
