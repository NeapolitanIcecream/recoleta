---
kind: ideas
granularity: day
period_start: '2026-07-22T00:00:00'
period_end: '2026-07-23T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- program repair
- code optimization
- test generation
- repository context
tags:
- recoleta/ideas
- topic/coding-agents
- topic/program-repair
- topic/code-optimization
- topic/test-generation
- topic/repository-context
language_code: zh-CN
---

# 代码优化与生成式测试的可执行控制

## 摘要
通过结合互补的可执行信号，性能优化和测试生成工作流可以提高模型输出的可靠性：使用运行时性能分析来优先处理静态优化匹配，使用语义变异来检验验收测试，并在行为级验证之前采用确定性的项目脚手架。

## 按性能分析器结果为静态优化匹配排序
性能工程师可以在整个代码仓库中运行 MoST 风格的已验证 Semgrep 规则，然后根据采样性能分析器报告的运行时占比和调用上下文对匹配结果排序。MoST 提供了可跨语言和架构复用的候选转换，但静态匹配无法表明某个位置是否对已部署工作负载重要；PerfAgent 表明，性能分析器反馈可以帮助代理跨越抽象层，并更频繁地达到接近专家水平的加速效果。具体做法是只向编码代理提供影响最大的规则匹配，对每个正确补丁重新进行性能分析，并保留最快的结果，而不是最后提交的结果。一项低成本检查是，在相同的优化任务上比较按性能分析器排序和未排序的规则匹配，衡量每次尝试编辑带来的成功加速效果以及验证成本。

### 资料来源
- [PerfAgent: Profiler-Guided Iterative Refinement for Repository-Level Code Optimization](../Inbox/2026-07-22--perfagent-profiler-guided-iterative-refinement-for-repository-level-code-optimization.md): PerfAgent 通过性能分析器引导的迭代验证，将 GSO 上与专家匹配的补丁比例从 19.6% 提高到 39.2%，并将 SWE-fficiency-Lite 上的比例从 26% 提高到 74%。
- [Multi-Source and Cross-Scenario Strategy-Guided Code Optimization](../Inbox/2026-07-22--multi-source-and-cross-scenario-strategy-guided-code-optimization.md): MoST 将多来源优化策略转换为经过验证的 Semgrep 规则；与 SemOpt 相比，其生成的开发者精确匹配补丁多出 24.44%–180.00%。

## 通过变异强化性能补丁的验收测试
在认定最快的候选补丁正确之前，接受代理生成优化的维护者应使用合理但错误的性能补丁来检验受影响的测试集。PerfAgent 能够高效地选出通过定向测试的最快补丁，但其失败分析指出，测试范围过窄可能遗漏边界情况。CoHarden 说明了通过测试并不意味着测试具有足够的区分能力：严格的复现测试使修复成功率提高了 8.5 个百分点，宽松测试没有带来提升，而错位测试使其下降了 3.6 个百分点。优化循环可以生成语义变异体，例如删除边界检查、修改回退路径或不安全地复用缓存，然后扩展选择性测试集，直到其能够拒绝这些变异体。对之前接受的补丁分别在启用和不启用这种强化的情况下重新运行，可以揭示额外的变异步骤是否能捕获基于依赖关系的选择性测试所遗漏的回归问题。

### 资料来源
- [PerfAgent: Profiler-Guided Iterative Refinement for Repository-Level Code Optimization](../Inbox/2026-07-22--perfagent-profiler-guided-iterative-refinement-for-repository-level-code-optimization.md): PerfAgent 指出，测试范围不足可能导致看似快速的补丁悄然破坏边界情况或下游路径。
- [Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes](../Inbox/2026-07-22--beyond-fail-to-pass-iterative-hardening-of-co-generated-bug-reproduction-tests-and-fixes.md): 严格测试使 Resolved 提高了 8.5 个百分点；宽松测试没有带来收益，错位测试则使 Resolved 降低了 3.6 个百分点。

## 对生成式 BDD 胶水代码进行编译与变异检查
维护 Java BDD 测试套件的团队可以将胶水代码验收分为三个关卡：确定性的框架脚手架、编译与静态修复，以及基于变异的行为检查。AutoGlue 会检索场景和代码仓库上下文，但其生成的实现中只有 46.1% 可以直接使用，而且执行验证受到步骤级预言机薄弱的限制。CATGen 表明，固定的骨架和静态分析修复可以低成本地消除许多项目集成失败；CoHarden 则表明，可执行测试仍可能接受看似合理但错误的实现。对于每个生成的步骤定义，流水线都应修改 API 调用、参数或被省略的操作，并要求外层场景拒绝这些变体。首次评估可以将编译率、直接可用率和存活变异体数量与 AutoGlue 当前的生成工作流进行比较。

### 资料来源
- [Bridging Behavior and Implementation: Automated Java Glue Code Generation for Behavior-Driven Development](../Inbox/2026-07-22--bridging-behavior-and-implementation-automated-java-glue-code-generation-for-behavior-driven-development.md): AutoGlue 为 1,307 个 Java BDD 步骤中的 46.1% 生成了可直接使用的代码，但执行验证受到环境依赖和薄弱步骤级预言机的限制。
- [Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation](../Inbox/2026-07-22--context-matters-improving-the-practical-reliability-of-llm-based-unit-test-generation.md): CATGen 的确定性骨架和静态分析修复使工业项目的编译成功率提高了 24.72%–38.05%，同时将 token 使用量降低了 66.83%–83.86%。
- [Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes](../Inbox/2026-07-22--beyond-fail-to-pass-iterative-hardening-of-co-generated-bug-reproduction-tests-and-fixes.md): CoHarden 区分了严格测试和宽松测试：后者虽然满足 fail-to-pass，却仍会接受合理但错误的修复。
