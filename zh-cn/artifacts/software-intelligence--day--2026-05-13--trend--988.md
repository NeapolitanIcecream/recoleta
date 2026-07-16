---
kind: trend
trend_doc_id: 988
granularity: day
period_start: '2026-05-13T00:00:00'
period_end: '2026-05-14T00:00:00'
topics:
- coding agents
- agent evaluation
- software engineering
- verification
- runtime systems
- agent optimization
run_id: materialize-outputs
aliases:
- recoleta-trend-988
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/verification
- topic/runtime-systems
- topic/agent-optimization
language_code: zh-CN
---

# 代码代理正在按完整、可验证的工作来评分

## 概览
这一时期最清楚的信号是：代码代理正在按完整、可检查的工作来评分。SWE-Cycle 和 Phoenix-bench 把环境搭建、测试和领域工具链纳入评分。CRANE 表明，在保护工具调用格式时，模型编辑可以提高代理通过率。

## 研究发现

### End-to-end software work
SWE-Cycle 让部分进展和完整问题解决之间的差距变得清楚。它要求代理在一个原始仓库里重建环境、实现修复并编写验证测试。摘录中最好的 FullCycle 解决率是 13.50%，而单独的环境重建达到 78.12%，单独的测试生成达到 67.28%。

AI Harness Engineering 对这种模式给出系统层面的解释。它把代理性能看作模型、运行时 harness 和仓库环境共同作用的结果。它提出的 trace 包记录动作、工具使用、上下文、验证、失败归因、干预、熵和结果，因此一个成功的补丁必须附带它是如何产生的证据。

#### 资料来源
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): SWE-Cycle task design, FullCycle evaluation, and reported solve rates.
- [AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents](../Inbox/2026-05-13--ai-harness-engineering-a-runtime-substrate-for-foundation-model-software-agents.md): Harness responsibilities, trace classes, and verification-focused evaluation protocol.

### Domain toolchains expose transfer limits
Phoenix-bench 在可执行的电子设计自动化（EDA）检查下，测试面向软件风格的代理处理 Verilog 和 SystemVerilog 维护任务的能力。表现最好的商业代理只解决了 32.7% 到 38.6% 的任务。和 SWE-bench Verified 相比，这些代理低了 37 到 58 个百分点。

失败模式很具体。硬件 bug 会沿着端口、时钟、复位、参数以及实例化模块之间的信号流传播。文件级 oracle 只带来 1.4 个百分点的提升，因为代理还是会改错模块。加入一轮 testbench 日志反馈后，解决率升到大约 42% 到 45%，说明可执行的失败证据比单看文件名更有用。

#### 资料来源
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): Phoenix-bench construction, EDA evaluation, resolved rates, transfer drop, and diagnostic interventions.

### Verification skills are becoming separate targets
PBT-Bench 把基于性质的测试（PBT）单独拎出来：代理必须推断一个文档里写明的不变量，并编写能触发语义 bug 的 Hypothesis 输入生成器。这个基准覆盖 100 个问题、40 个 Python 库和 365 个注入的 bug。在 PBT 引导提示下，不同模型的召回率范围是 42.1% 到 83.4%。

提示带来的收益并不均匀。Qwen 3.6 Plus 提升 24.5 个百分点，Qwen 3.5-30B-A3B 提升 22.9 个百分点，Step 3.5 Flash 提升 20.3 个百分点。DeepSeek V3.2 和 Grok 4.1 Fast 在同样的 scaffolding 下召回率下降。这说明测试设计能力可以作为可测量的代理技能，而且模型和提示之间要匹配。

#### 资料来源
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): PBT-Bench design, scale, scoring method, recall ranges, and model-specific prompt effects.

### Agent reliability is being tuned below the product surface
CRANE 用 Thinking checkpoints 的推理方向编辑 Qwen Instruct checkpoints，然后抑制会干扰工具分隔符、JSON schema tokens 和 chat templates 的更新。在 Roo-Eval 上，它在 30B 时达到 66.2% pass@1，而 Instruct baseline 是 46.7%；在 80B 时达到 81.5%，baseline 是 72.8%。

其他工作在调整周边机制。CANTANTE 根据系统级分数给每个代理分配提示归因，并报告在 MBPP、GSM8K 和 HotpotQA 上的最佳平均排名。SkillOps 把可复用的代理技能维护为带验证器和兼容性链接的类型化契约，在 200 个技能的库上把 ALFWorld 任务成功率做到 79.5%。1Password 的单体重构展示了同样教训在生产环境中的版本：在工程师提供确定性分析器、清单、停止规则和审查点后，代理才帮上忙。

#### 资料来源
- [CRANE: Constrained Reasoning Injection for Code Agents via Nullspace Editing](../Inbox/2026-05-13--crane-constrained-reasoning-injection-for-code-agents-via-nullspace-editing.md): CRANE method and Roo-Eval, SWE-bench-Verified, and Terminal-Bench results.
- [CANTANTE: Optimizing Agentic Systems via Contrastive Credit Attribution](../Inbox/2026-05-13--cantante-optimizing-agentic-systems-via-contrastive-credit-attribution.md): CANTANTE per-agent credit assignment and benchmark results.
- [SkillOps: Managing LLM Agent Skill Libraries as Self-Maintaining Software Ecosystems](../Inbox/2026-05-13--skillops-managing-llm-agent-skill-libraries-as-self-maintaining-software-ecosystems.md): SkillOps contract representation, maintenance actions, and ALFWorld result.
- [What we learned using AI agents to refactor a monolith](../Inbox/2026-05-13--what-we-learned-using-ai-agents-to-refactor-a-monolith.md): 1Password production refactor setup, deterministic tooling, results, and failure cases.
