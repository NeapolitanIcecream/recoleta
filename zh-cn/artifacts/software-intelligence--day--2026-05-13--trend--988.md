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

# 代码代理正在按完整、可验证的工作评分

## Overview
这一时期最清晰的信号是：代码代理正在按完整、可检查的工作来评分。SWE-Cycle 和 Phoenix-bench 把环境设置、测试和领域工具链纳入分数。CRANE 显示，在保护工具调用格式时，模型编辑可以提高代理通过率。

## Clusters

### 端到端软件工作
SWE-Cycle 让部分进展与完整解决问题单之间的差距变得可见。它要求代理在原始仓库中重建环境、实现修复，并编写验证测试。摘录中最高的 FullCycle 解决率为 13.50%，尽管单独的环境重建达到 78.12%，单独的测试生成达到 67.28%。

AI Harness Engineering 从系统角度解释这种模式。它把代理表现视为模型、运行时 harness 和仓库环境共同作用的结果。该文提出的 trace package 记录动作、工具使用、上下文、验证、失败归因、干预、熵和结果，因此成功补丁必须带有其生成过程的证据。

#### Evidence
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): SWE-Cycle 任务设计、FullCycle 评估和报告的解决率。
- [AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents](../Inbox/2026-05-13--ai-harness-engineering-a-runtime-substrate-for-foundation-model-software-agents.md): Harness 职责、trace 类别和以验证为重点的评估协议。

### 领域工具链暴露迁移限制
Phoenix-bench 在可执行的电子设计自动化（EDA）检查下，用 Verilog 和 SystemVerilog 维护任务测试软件式代理。顶级商业代理只解决 32.7% 到 38.6% 的任务。相同代理相比 SWE-bench Verified 低 37 到 58 个百分点。

失败模式很具体。硬件 bug 会通过实例化模块之间的端口、时钟、复位、参数和信号流传播。文件级 oracle 只增加 1.4 个百分点，因为代理仍会修改错误的模块。一轮 testbench 日志反馈把解决率提高到约 42% 到 45%，说明可执行失败证据比只有文件名更有用。

#### Evidence
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): Phoenix-bench 构建、EDA 评估、解决率、迁移下降和诊断干预。

### 验证技能正在成为单独目标
PBT-Bench 单独考察基于性质的测试（PBT）：代理必须推断文档化的不变量，并编写能触达语义 bug 的 Hypothesis 输入生成器。该基准覆盖 100 个问题、40 个 Python 库和 365 个注入 bug。在 PBT 引导提示下，各模型召回率为 42.1% 到 83.4%。

提示带来的提升不均衡。Qwen 3.6 Plus 提升 24.5 个百分点，Qwen 3.5-30B-A3B 提升 22.9 个百分点，Step 3.5 Flash 提升 20.3 个百分点。DeepSeek V3.2 和 Grok 4.1 Fast 在相同提示结构下召回率下降。这使测试设计能力成为可衡量的代理技能，并且提示适配因模型而异。

#### Evidence
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): PBT-Bench 设计、规模、评分方法、召回率范围和特定模型的提示效果。

### 代理可靠性正在产品表面之下被调优
CRANE 使用 Thinking 检查点中的推理方向编辑 Qwen Instruct 检查点，然后抑制会扰动工具分隔符、JSON schema token 和 chat template 的更新。在 Roo-Eval 上，30B 版本达到 66.2% pass@1，Instruct 基线为 46.7%；80B 版本达到 81.5%，基线为 72.8%。

其他工作在调优周边机制。CANTANTE 根据系统级分数为每个代理的提示分配贡献分，并报告在 MBPP、GSM8K 和 HotpotQA 上的最佳平均排名。SkillOps 将可复用代理技能维护为带有验证器和兼容性链接的类型化契约，使用 200 个技能的库在 ALFWorld 上达到 79.5% 的任务成功率。1Password 的单体重构展示了同一经验在生产中的版本：工程师提供确定性分析器、清单、停止规则和审查点后，代理才发挥作用。

#### Evidence
- [CRANE: Constrained Reasoning Injection for Code Agents via Nullspace Editing](../Inbox/2026-05-13--crane-constrained-reasoning-injection-for-code-agents-via-nullspace-editing.md): CRANE 方法以及 Roo-Eval、SWE-bench-Verified 和 Terminal-Bench 结果。
- [CANTANTE: Optimizing Agentic Systems via Contrastive Credit Attribution](../Inbox/2026-05-13--cantante-optimizing-agentic-systems-via-contrastive-credit-attribution.md): CANTANTE 每代理贡献分分配和基准结果。
- [SkillOps: Managing LLM Agent Skill Libraries as Self-Maintaining Software Ecosystems](../Inbox/2026-05-13--skillops-managing-llm-agent-skill-libraries-as-self-maintaining-software-ecosystems.md): SkillOps 契约表示、维护操作和 ALFWorld 结果。
- [What we learned using AI agents to refactor a monolith](../Inbox/2026-05-13--what-we-learned-using-ai-agents-to-refactor-a-monolith.md): 1Password 生产重构设置、确定性工具、结果和失败案例。
