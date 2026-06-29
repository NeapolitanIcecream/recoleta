---
kind: trend
trend_doc_id: 956
granularity: day
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-12T00:00:00'
topics:
- coding agents
- agent runtimes
- tool-use evaluation
- workflow security
- context compression
- CAD automation
run_id: materialize-outputs
aliases:
- recoleta-trend-956
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-runtimes
- topic/tool-use-evaluation
- topic/workflow-security
- topic/context-compression
- topic/cad-automation
language_code: zh-CN
---

# 在 agent 系统承担更多责任之前，它们需要可检查的执行过程

## Overview
最强信号是，agent 需要可检查的执行过程和更严格的任务证据。DuST 把带执行标签的候选代码当作训练数据，Shepherd 记录实时 agent 状态以便分叉，ComplexMCP 则显示工具型 agent 在有状态软件工作上仍落后于人类。

## Clusters

### Execution feedback as training signal
DuST 将生成的代码样本当作成对监督的来源。基础模型为每个问题采样 64 个候选程序，沙箱为每个候选程序标记通过或失败，混合分组再用 Group Relative Policy Optimization（GRPO）训练同一个模型，让它把正确程序排在错误程序前面。奖励只评估排序质量，但生成效果仍然提升。

在 LiveCodeBench v6 上，Qwen3-30B-Thinking 的 pass@1 从 65.4% 升到 68.5%。它的判断分数从 70.1 的 NDCG 升到 76.3，Best-of-4 准确率从 68.7% 升到 72.6%。这给出了一个明确做法：把推理阶段的测试时扩展数据拿来继续训练。

#### Evidence
- [Primal Generation, Dual Judgment: Self-Training from Test-Time Scaling](../Inbox/2026-05-11--primal-generation-dual-judgment-self-training-from-test-time-scaling.md): Summary gives DuST data construction, GRPO ranking objective, and LiveCodeBench gains.

### Traceable runtime state for meta-agents
Shepherd 把一次 agent 执行变成一个带类型的对象，另一个 agent 可以检查、分叉、回放和修改。每次模型调用、工具调用、文件写入和环境操作都会变成 Git 风格轨迹中的一个事件。分叉使用进程和文件系统的写时复制隔离，因此不同后续路径可以从同一过去状态开始。

报告的系统指标已经足够影响 agent 搜索。对于最大 5.8 GB 的 Terminal-Bench 2.0 镜像，Shepherd 的分叉时间是 134–143 ms。完整文件系统复制在最大镜像上达到 53,462 ms。回放在 Claude Haiku 4.5 上、跨八个任务时的 prompt-cache 命中率也接近 95%。

#### Evidence
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): Summary describes Shepherd's typed trace, fork/replay operations, and performance results.

### Stateful tool and CAD benchmarks expose narrow competence
ComplexMCP 通过 Model Context Protocol（MCP）测试 agent，包含 300 多个工具和 7 个有状态沙箱。表现最好的模型 Gemini-3-Flash 在 47 个任务上的成功率是 55.31%。人类用户通过同一个接口达到 93.61%。失败包括工具检索饱和、跳过环境检查，以及出错后恢复能力差。

BenchCAD 对多模态设计工作施加了类似压力。它包含 17,900 个经过执行验证的 CadQuery 程序，覆盖 106 个工业零件家族。这个基准把 image-to-code 生成、视觉问答、代码问答和编辑任务分开评估。模型读 CAD 代码比从渲染图中推断同样细节更好：最好的 Code QA 大约是 0.838，而 Vision QA 最高只有 0.587。

#### Evidence
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): Summary reports MCP tool scale, stateful sandboxes, human and model success rates, and failure modes.
- [BenchCAD: A Comprehensive, Industry-Standard Benchmark for Programmatic CAD](../Inbox/2026-05-11--benchcad-a-comprehensive-industry-standard-benchmark-for-programmatic-cad.md): Summary reports BenchCAD dataset size, tasks, and QA results.

### Workflow context and compressed memory need stronger checks
JAW 表明，当攻击者控制的内容进入与 token、工具或密钥相关的提示词时，agent 工作流会被劫持。它结合了工作流路径分析、提示词来源追踪、能力检查和负载演化。论文报告了 4,174 个可劫持的 GitHub 工作流和 8 个可劫持的 n8n 模板，影响包括凭证泄露和命令执行。

上下文问题也出现在编码 agent 里。In-Context Autoencoder（ICAE）把观测压缩成连续记忆 token，让 agent 跑得更长，但细节丢失会损害真实问题修复。在 SWE-bench Verified 上，这个压缩系统只解决了 500 个问题里的 7 个，低于未压缩的 Qwen3-8B 基线 19 个，也远低于监督微调模型的 86 个。

#### Evidence
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): Summary gives JAW method, affected workflow types, counts, and reported impacts.
- [On Problems of Implicit Context Compression for Software Engineering Agents](../Inbox/2026-05-11--on-problems-of-implicit-context-compression-for-software-engineering-agents.md): Summary reports ICAE setup and SWE-bench Verified resolution drop.
