---
kind: trend
trend_doc_id: 939
granularity: week
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-11T00:00:00'
topics:
- "\u7F16\u7801\u4EE3\u7406"
- "\u8F6F\u4EF6\u5DE5\u7A0B\u57FA\u51C6"
- "\u53EF\u6267\u884C\u8BC4\u4F30"
- "\u5F62\u5F0F\u5316\u9A8C\u8BC1"
- "\u4EE3\u7406\u5B89\u5168"
- "\u5DE5\u5177\u4F7F\u7528"
run_id: materialize-outputs
aliases:
- recoleta-trend-939
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u4EE3\u7406"
- "topic/\u8F6F\u4EF6\u5DE5\u7A0B\u57FA\u51C6"
- "topic/\u53EF\u6267\u884C\u8BC4\u4F30"
- "topic/\u5F62\u5F0F\u5316\u9A8C\u8BC1"
- "topic/\u4EE3\u7406\u5B89\u5168"
- "topic/\u5DE5\u5177\u4F7F\u7528"
language_code: zh-CN
---

# 编码代理面临更严格的信任测试：执行轨迹、仓库纪律和行动前检查

## Overview
本周研究把大语言模型（LLM）编码代理视为需要先给出证据才能被信任的系统。最有力的工作通过执行、仓库任务、形式化证明、工具契约和对抗性安全测试来检查生成代码。SWE Atlas、VeriContest 和 RubricRefine 展示了同一个实用标准：有用的代理必须留下可检查的证据，处理常规工程工作，并避免不安全操作。

## Clusters

### 生成代码的可执行证据
执行是检验代码生成主张的主要筛选条件。Semantic Voting 表明，在生成的输入上运行候选程序，比文本层面的投票给出强得多的选择信号：在 18 个 HumanEval+ 和 MBPP+ 设置中，基于执行的选择器比输出模式多数投票高出 19 到 52 个百分点。Sketch-and-Verify 对较弱的代码模型给出相近结论。它要求模型尝试不同的算法草图，再用执行指纹检查候选程序。在 Gemini 3.1 Flash Lite 的 19 个困难 HumanEval+ 案例上，较小的草图设置解决了 19 题中的 11 题；相同候选数量下，平铺采样解决了 19 题中的 5 题。

同样的执行标准也出现在测试工作中。ConCovUp 针对普通单元测试漏掉的并发 C/C++ 行为。它结合静态共享内存分析、LLM 引导的路径推理和运行反馈，在九个真实库上把平均共享内存访问对覆盖率从 Claude Code 基线的 36.6% 提高到 68.1%。

#### Evidence
- [Semantic Voting: Execution-Grounded Consensus for LLM Code Generation](../Inbox/2026-05-09--semantic-voting-execution-grounded-consensus-for-llm-code-generation.md): Semantic Voting 报告称，基于执行的候选选择相比输出模式投票有大幅提升。
- [Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching](../Inbox/2026-05-09--sketch-and-verify-structured-inference-time-scaling-via-program-sketching.md): Sketch-and-Verify 报告称，结构化算法草图加执行检查在相同预算下带来收益。
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): ConCovUp 报告了以执行为依据的并发测试生成，并在真实 C/C++ 库上提高了覆盖率。

### 仓库级基准与放弃修改
仓库工作正在用超出问题修复的标准来衡量。SWE Atlas 覆盖 18 个活跃开源仓库中的 284 个任务，任务包括代码库问答、测试编写和重构。它的评估把程序检查与评分细则结合，覆盖覆盖率、可维护性、约定、清理和代码卫生。报告中的重构回归测试通过率与评分细则通过率相差约 15 到 40 个百分点，说明仅通过测试不足以衡量工程质量。

FixedBench 加入了更严格的维护要求：代理必须知道什么时候不应修改可执行代码。在已经修复的 SWE-bench Verified 问题上，主设置下代理仍在 35% 到 65% 的案例中做了不该做的可执行代码编辑。奖励放弃修改的提示改善了不改代码的行为，但在部分修复仍需继续处理时造成了有害的过度放弃。

#### Evidence
- [SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution](../Inbox/2026-05-08--swe-atlas-benchmarking-coding-agents-beyond-issue-resolution.md): SWE Atlas 定义了仓库问答、测试编写和重构任务，并使用程序化检查和评分细则检查。
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench 衡量代理在已经修复任务上的放弃修改能力，并报告不该编辑的比例和提示带来的权衡。

### 形式化和高风险正确性检查
形式化验证仍是当前模型难以跨越的边界。VeriContest 包含 946 个 Rust/Verus 竞赛编程任务，配有自然语言提示、专家规格、已通过评测的 Rust 代码、已检查证明，以及正向和负向测试。GPT-5.5 在自然语言到代码生成上达到 92.18% pass@1，但端到端验证生成只有 5.29%。所有被评估模型的端到端成绩都低于 6%。

SmartEval 覆盖另一个高风险领域：从自然语言规格生成的 Solidity 智能合约。该基准用五项指标评分细则评估 9,000 个生成合约，指标包括功能完整性、变量保真度、状态机正确性、业务逻辑和代码质量。最弱的指标是业务逻辑保真度，表现较差的合约主要存在逻辑遗漏和状态转换错误。

#### Evidence
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): VeriContest 报告了普通代码生成与端到端验证的 Rust/Verus 程序之间的差距。
- [SmartEval: A Benchmark for Evaluating LLM-Generated Smart Contracts from Natural Language Specifications](../Inbox/2026-05-10--smarteval-a-benchmark-for-evaluating-llm-generated-smart-contracts-from-natural-language-specifications.md): SmartEval 评估生成的 Solidity 合约，并报告业务逻辑和状态转换方面的失效模式。

### 工具契约与对抗性安全测试
使用工具的代理需要在第一次真实操作前接受检查。RubricRefine 根据任务特定契约检查代码模式工具调用，检查内容包括工具选择、输出形状、调用签名、顺序和数据来源。在 M3ToolEval 上，它在七个模型上的平均成功率为 0.86；单轮 CodeAct 为 0.62。细化过程中不会执行候选操作。

安全评估也更具体。MOSAIC-Bench 表明，看起来普通的分阶段工单可以组合成可利用代码。在九个生产级编码代理中，分阶段攻击链达到 53.3% 到 85.9% 的端到端攻击成功率，且只有两次拒绝。MonitoringBench 用 2,644 条成功的 BashArena 攻击轨迹测试监控器，并显示更强的红队攻击会明显降低表面上的监控器捕获率，包括 Opus 4.5 全轨迹监控器在细化攻击上的捕获率从 94.9% 降至 60.3%。

#### Evidence
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): RubricRefine 报告了执行前契约检查，以及多工具任务上的成功率提升。
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench 报告了分阶段漏洞诱导率和可执行的概念验证判定器。
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): MonitoringBench 报告了一个大型破坏轨迹基准，并显示在更强攻击下监控器捕获率下降。
