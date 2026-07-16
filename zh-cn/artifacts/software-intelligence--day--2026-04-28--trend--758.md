---
kind: trend
trend_doc_id: 758
granularity: day
period_start: '2026-04-28T00:00:00'
period_end: '2026-04-29T00:00:00'
topics:
- coding agents
- code editing
- agent harnesses
- software testing
- agent infrastructure
- model efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-758
tags:
- recoleta/trend
- topic/coding-agents
- topic/code-editing
- topic/agent-harnesses
- topic/software-testing
- topic/agent-infrastructure
- topic/model-efficiency
language_code: zh-CN
---

# 编码代理的进展来自模型周边的接口

## 概览
这一时期的基线仍然是可执行评测。最强的主张来自模型外部的部分：SWE-Edit 的读写分离、Agentic Harness Engineering 的 rollout 驱动 harness 编辑，以及 SAFEdit 的测试支撑修复循环。这个方向把上下文、工具、存储、安全提醒和推理成本都当作代理性能中可测量的部分。

## 研究发现

### Code editing interfaces
当文件读取、补丁写入和修复被拆成更小的任务时，仓库代理的收益最大。SWE-Edit 通过 Viewer 处理相关代码块、Editor 执行补丁，把探索性文件内容挡在主推理上下文之外。在 SWE-bench Verified 上，它报告 resolved-rate 从 69.9% 提高到 72.0%，edit success 从 93.4% 提高到 96.9%，总推理成本下降 17.9%。

SAFEdit 把同样的分工用在指令式编辑上。Planner 写编辑计划，Editor 只改目标代码，Verifier 运行真实单元测试，并最多做三轮修复。在 EditBench 上，它报告任务成功率 68.6%，高于其 GPT-4.1 ReAct 基线的 60.0%。Claude Code 的回归报告显示了另一面的运行风险：在一次报告的工作流里，Read 和 Grep 结果中反复出现的恶意软件提醒，让 5 个 Opus 4.7 subagent 里的 3 个拒绝了普通重构任务。

#### 资料来源
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): SWE-Edit design and SWE-bench Verified cost, edit success, and resolved-rate results.
- [SAFEdit: Does Multi-Agent Decomposition Resolve the Reliability Challenges of Instructed Code Editing?](../Inbox/2026-04-28--safedit-does-multi-agent-decomposition-resolve-the-reliability-challenges-of-instructed-code-editing.md): SAFEdit multi-agent edit, verification loop, and EditBench task success results.
- [Regression: malware reminder on every read still causes subagent refusals](../Inbox/2026-04-28--regression-malware-reminder-on-every-read-still-causes-subagent-refusals.md): Claude Code regression report showing subagent refusals and token overhead from repeated system reminders.

### Harness engineering
围绕编码模型的 harness 现在被当作一个可编辑系统来处理，并且有自己的测量指标。Agentic Harness Engineering (AHE) 把 prompts、tools、middleware、skills、sub-agent 设置和 memory 作为文件暴露出来。它用清洗过的 rollout traces 提出改动，记录预期收益和风险，然后在保留编辑前检查结果。经过 10 轮迭代后，AHE 报告 Terminal-Bench 2 的 pass@1 在 89 个任务上从 69.7% 提高到 77.0%。它的冻结 harness 在 SWE-bench-verified 上也比 seed harness 用了更少的 tokens。

Mesa 和那篇代理安全文章也在产品层面处理同样的问题，只是测量更弱。Mesa 给代理提供一个持久的、兼容 POSIX 的文件系统，带有分支、diff、回滚、审计轨迹和作用域挂载。安全文章通过 HTTP proxies 注入凭据，把真实凭据留在 AI SRE 容器外；当应用忽略代理设置时，它还考虑使用 gVisor 的网络拦截。

#### 资料来源
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](../Inbox/2026-04-28--agentic-harness-engineering-observability-driven-automatic-evolution-of-coding-agent-harnesses.md): AHE components, rollout evidence loop, Terminal-Bench 2 results, transfer, and token-use data.
- [Mesa: A Versioned Filesystem for Agents](../Inbox/2026-04-28--mesa-a-versioned-filesystem-for-agents.md): Mesa filesystem features for durable, permissioned, versioned agent work.
- [Proxies, Sandboxes and Agent Security](../Inbox/2026-04-28--proxies-sandboxes-and-agent-security.md): Credential-injection proxy design and sandbox observations for agent security.

### Bug reports from uncovered code
IssueSpecter 把自动化软件修复往前推了一步，让大语言模型 (LLM) 检查当前测试从不执行的代码。SlipCover 找出未覆盖的 Python 片段。GPT-5-mini 生成候选 issue 报告，包含严重性、复现步骤、受影响的操作系统和建议修复。之后的排序步骤再把 issue 筛给人工审查。

报告中的规模足够有用，但噪声仍然很大。在 13 个活跃的 Python 项目中，这个系统生成了 10,467 条 issue 报告。对排名前 130 条报告的人工审查发现了 49 个有效 bug、61 个还需要进一步调查的报告，以及 20 个无效报告。作者还报告说，基于 LLM 的排序在 precision@3 上比基于规则的排序高 50%，在 mean reciprocal rank 上高 41%。

#### 资料来源
- [LLM-Guided Issue Generation from Uncovered Code Segments](../Inbox/2026-04-28--llm-guided-issue-generation-from-uncovered-code-segments.md): IssueSpecter pipeline, manual annotation results, ranking gains, and bug taxonomy coverage.

### Inference cost and observability
软件工程模型里的效率主张很具体。Carbon-Taxed Transformers (CTT) 把 neural architecture search、structured pruning、quantization 和 distillation 结合起来，用于面向代码的模型。它报告内存占用最高减少 49 倍，clone detection 延迟降低 8–10 倍，生成延迟降低 4–7 倍，推理 CO2 排放最高降低 81%。代码生成是最难的情况：pass@1 保留率最高达到 68%。

另一篇关于 observability 的综述认为，生产环境里的 LLM 系统需要把模型内部状态、置信度、行为、运维和基础设施 traces 连成可观察信号。它的证据不够均匀，因为它汇总了多项研究，但运维层面的结论和这些代理论文一致：只有把模型行为和工具、traces 以及基础设施指标连起来，失败和成本才看得见。

#### 资料来源
- [Carbon-Taxed Transformers: A Green Compression Pipeline for Overgrown Language Models](../Inbox/2026-04-28--carbon-taxed-transformers-a-green-compression-pipeline-for-overgrown-language-models.md): CTT compression method and reported memory, latency, CO2, and task-retention results.
- [AI Observability for Large Language Model Systems: A Multi-Layer Analysis of Monitoring Approaches from Confidence Calibration to Infrastructure Tracing](../Inbox/2026-04-28--ai-observability-for-large-language-model-systems-a-multi-layer-analysis-of-monitoring-approaches-from-confidence-calibration-to-infrastructure-tracing.md): Survey of LLM observability layers, examples, and open gaps in cross-layer correlation.
