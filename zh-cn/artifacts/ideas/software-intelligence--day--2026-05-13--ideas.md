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

# Agent verification records

## 摘要
完整的代理工作现在需要证据，证明代理完成了项目搭建、选对了文件、运行了有意义的检查，并保住了原有行为。可行的做法很具体：给代理 PR 加追踪包，给 HDL 代理输入可执行的 EDA 失败日志，并在要求代理写语义测试之前，按模型测试 property-based 提示。

## Agent PR trace packages with setup, test, and intervention records
采用代码代理的软件团队应要求每个代理 PR 都附带一个简短的追踪包：环境搭建步骤、检查过的文件、运行过的命令、生成或修改的测试、验证结果、失败诊断，以及任何人工介入。这会给审阅者一个稳定的材料，让他们先看证据，再花时间读大补丁。

SWE-Cycle 说明了这件事的原因。代理在单独的环境搭建和测试生成任务上，表现可以明显好于从原始仓库完成完整问题修复；在摘录里，最佳 FullCycle 解决率只有 13.50%，而单独的环境重建达到 78.12%，单独的验证测试生成达到 67.28%。AI Harness Engineering 给出了缺失证据的操作清单，包括 action、tool、context、verification、failure attribution、intervention、entropy 和 outcome traces。1Password 的单体重构展示了生产环境里的做法：工程师构建确定性分析器、清单、停止规则和审阅点后，代理表现更好，但顺序错误仍然需要人工控制。

### 资料来源
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): SWE-Cycle reports the sharp gap between isolated setup or test tasks and full raw-repository issue resolution.
- [AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents](../Inbox/2026-05-13--ai-harness-engineering-a-runtime-substrate-for-foundation-model-software-agents.md): AI Harness Engineering defines trace classes and runtime responsibilities for auditable agent software work.
- [What we learned using AI agents to refactor a monolith](../Inbox/2026-05-13--what-we-learned-using-ai-agents-to-refactor-a-monolith.md): 1Password describes deterministic analyzers, manifests, stop rules, and human review during a large Go monolith refactor.

## EDA testbench-log feedback for HDL repository agents
测试 Verilog 或 SystemVerilog 的软件式代码代理的硬件团队，在大规模采用前应该先加一层 EDA 反馈回路。一个可行做法是把代理的补丁放进固定版本的 Docker Verilator 或综合环境里运行，把失败的 testbench 日志连同模块层级上下文返回，再要求它在隔离的 worktree 里修复一次。

Phoenix-bench 报告说，在可执行的 EDA 检查下，顶级商业代理对仓库级 HDL 问题的解决率只有 32.7% 到 38.6%，相比 SWE-bench Verified 下降了 37 到 58 个百分点。失败模式很具体：代理会停在症状文件上，漏掉跨端口、时钟、复位、参数和实例化模块的信号流依赖。文件级 oracle 定位只带来 1.4 个百分点的提升，而一轮 testbench 日志反馈把解决率抬到大约 42% 到 45%。一个低成本的采用测试，是用最近的 HDL bug 做一个小型内部基准，带 fail-to-pass 和 pass-to-pass 检查，只在目标失败通过且之前通过的测试仍然通过时才记分。

### 资料来源
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): Phoenix-bench summarizes repository-level HDL tasks, EDA checks, resolved rates, SWE-bench transfer drops, and the effect of testbench-log feedback.
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): The paper describes cross-hierarchy signal-flow failures and why file-level localization is too coarse for many hardware bugs.

## Model-specific property-based testing prompt trials for Python libraries
让代理为 Python 库写测试的团队，在把流程接入 CI 之前，应先按模型试用 property-based testing 提示。具体检查很简单：给代理 API 文档、现有测试和一个隐藏的有 bug 版本，要求它输出一个使用 Hypothesis 的 `pbt_test.py` 文件，并按 fail-on-buggy 和 pass-on-fixed 的行为给测试评分。

PBT-Bench 在 100 个问题、40 个 Python 库和 365 个注入的语义 bug 上分离了这项能力。在 PBT 引导提示下，不同模型的召回率在 42.1% 到 83.4% 之间。同一个提示让一些模型提升了 20 个百分点以上，也让另一些模型变差，包括文中报告的 DeepSeek V3.2 和 Grok 4.1 Fast 的下降。团队可以用这个模式决定哪个模型和提示可以用来生成已文档化不变量的 property test，尤其适用于边界条件和输入分布比示例型测试更重要的 API。

### 资料来源
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): PBT-Bench defines the task, benchmark size, Hypothesis output requirement, and model-by-prompt results.
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): The paper reports the recall range and model-specific gains or degradations under Hypothesis scaffolding.
