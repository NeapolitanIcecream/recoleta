---
kind: ideas
granularity: day
period_start: '2026-05-13T00:00:00'
period_end: '2026-05-14T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent evaluation
- software engineering
- verification
- runtime systems
- agent optimization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/verification
- topic/runtime-systems
- topic/agent-optimization
language_code: zh-CN
---

# 代理验证记录

## Summary
完整的代理工作现在需要证据：代理设置了项目，选对了文件，运行了有意义的检查，并保留了现有行为。可执行做法很具体：给代理 PR 添加 trace 包，向 HDL 代理提供可执行 EDA 失败日志，并在要求代理编写语义测试前按模型测试 property-based 提示。

## 包含设置、测试和介入记录的代理 PR trace 包
采用代码代理的软件团队应要求每个代理 PR 包含一个简短的 trace 包：环境设置步骤、检查过的文件、运行过的命令、生成或修改的测试、验证结果、失败诊断，以及任何人工介入记录。这样，评审者在阅读大型补丁前，可以先检查一个稳定的工件。

SWE-Cycle 说明了这件事的重要性。代理在独立的环境设置和测试生成任务上表现明显好于从原始仓库完整解决 issue；摘录中最高的 FullCycle 解决率是 13.50%，而独立环境重建达到 78.12%，独立验证测试生成达到 67.28%。AI Harness Engineering 给出了缺失证据的操作清单，包括 action、tool、context、verification、failure attribution、intervention、entropy 和 outcome trace。1Password 的单体重构展示了生产环境中的做法：工程师构建确定性分析器、manifest、停止规则和评审点后，代理工作得更好，但排序错误仍需要人工控制。

### Evidence
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): SWE-Cycle 报告了独立设置或测试任务与完整原始仓库 issue 解决之间的明显差距。
- [AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents](../Inbox/2026-05-13--ai-harness-engineering-a-runtime-substrate-for-foundation-model-software-agents.md): AI Harness Engineering 定义了用于可审计代理软件工作的 trace 类别和运行时职责。
- [What we learned using AI agents to refactor a monolith](../Inbox/2026-05-13--what-we-learned-using-ai-agents-to-refactor-a-monolith.md): 1Password 描述了在大型 Go 单体重构中使用的确定性分析器、manifest、停止规则和人工评审。

## 面向 HDL 仓库代理的 EDA testbench 日志反馈
在 Verilog 或 SystemVerilog 上测试软件式代码代理的硬件团队，应在大规模采用前加入 EDA 反馈循环。一个可操作版本是：在 Docker 固定的 Verilator 或综合环境中运行代理补丁，返回带有模块层级上下文的失败 testbench 日志，并要求代理在隔离 worktree 中进行一次修复尝试。

Phoenix-bench 报告称，在可执行 EDA 检查下，顶级商业代理只能解决 32.7% 到 38.6% 的仓库级 HDL issue；与 SWE-bench Verified 相比下降 37 到 58 个百分点。失败模式很具体：代理停在症状文件，漏掉通过端口、时钟、复位、参数和实例化模块传播的信号流依赖。文件级 oracle 定位只增加 1.4 个百分点，而一轮 testbench 日志反馈把解决率提高到约 42% 到 45%。低成本的采用测试是建立一个小型内部基准，使用近期 HDL bug，包含 fail-to-pass 和 pass-to-pass 检查；只有目标失败通过且先前通过的测试仍然通过时才计分。

### Evidence
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): Phoenix-bench 总结了仓库级 HDL 任务、EDA 检查、解决率、SWE-bench 迁移降幅，以及 testbench 日志反馈的效果。
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): 论文描述了跨层级信号流失败，并说明文件级定位对许多硬件 bug 来说粒度过粗。

## 面向 Python 库的按模型 property-based testing 提示试验
要求代理为 Python 库编写测试的团队，应先按模型试用 property-based testing 提示，再把该流程加入 CI。具体检查很小：给代理 API 文档、现有测试和一个隐藏的有 bug 版本，要求输出使用 Hypothesis 的 `pbt_test.py` 文件，并按 fail-on-buggy 和 pass-on-fixed 行为给测试计分。

PBT-Bench 在 100 个问题、40 个 Python 库和 365 个注入语义 bug 上隔离评估这项能力。在 PBT 引导提示下，不同模型的召回率为 42.1% 到 83.4%。同一提示让一些模型提升超过 20 个百分点，也让另一些模型变差，包括报告中 DeepSeek V3.2 和 Grok 4.1 Fast 的下降。团队可以用这个模式决定允许哪个模型和提示为文档化不变量生成属性测试，尤其适用于边界情况和输入分布比示例测试更重要的 API。

### Evidence
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): PBT-Bench 定义了任务、基准规模、Hypothesis 输出要求，以及按模型和提示划分的结果。
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): 论文报告了 Hypothesis 脚手架下的召回率范围，以及特定模型的提升或下降。
