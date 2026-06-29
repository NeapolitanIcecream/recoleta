---
kind: trend
trend_doc_id: 1018
granularity: day
period_start: '2026-05-16T00:00:00'
period_end: '2026-05-17T00:00:00'
topics:
- code agents
- agent benchmarks
- execution feedback
- GPU kernels
- code safety
- token cost
- supply-chain risk
run_id: materialize-outputs
aliases:
- recoleta-trend-1018
tags:
- recoleta/trend
- topic/code-agents
- topic/agent-benchmarks
- topic/execution-feedback
- topic/gpu-kernels
- topic/code-safety
- topic/token-cost
- topic/supply-chain-risk
language_code: zh-CN
---

# 代码 agent 正在按有边界的工人来测试，而不是按代码生成器来测试

## Overview
最强的信号是操作层面的评估。1GC-7RC、AgentKernelArena 和 TOBench 都在有工具、运行时检查和资源限制的封闭工作循环里给 agent 打分。同样的关注也出现在可靠性论文、供应链风险研究和 token 预算报告中。

## Clusters

### End-to-end agent benchmarks
新的基准把 agent 当作必须规划、编辑、运行工具并从错误中恢复的工人。1GC-7RC 给 agent 七个机器学习任务，运行在一块 NVIDIA A100 GPU 上，没有互联网访问，任务时限为 40 到 120 分钟。AgentKernelArena 测试 196 个 GPU kernel 任务，覆盖 HIP、Triton 和 PyTorch-to-HIP 路径，然后检查编译、正确性、速度和隐藏输入形状。TOBench 增加了多模态工具使用：100 个可执行任务、27 个 Model Context Protocol 服务器，以及针对任务的验证器。

结果很有用，但不一致。Claude Code 搭配 Sonnet 4.6 在 1GC-7RC 的所有七个可见基线之上都有提升。AgentKernelArena 在许多 kernel 类别上报告了很高的编译率和正确率，平均加速最高到 6.89×，但 PyTorch-to-HIP kernel 常常在未见过的形状上失败。TOBench 更严格：最佳模型的任务成功率是 41.0%，而人类基准是 94.0%。

#### Evidence
- [1GC-7RC: One Graphic Card -- Seven Research Challenges! How Good Are AI Agents at Doing Your Job?](../Inbox/2026-05-16--1gc-7rc-one-graphic-card-seven-research-challenges-how-good-are-ai-agents-at-doing-your-job.md): Defines 1GC-7RC tasks, compute limits, and reported Sonnet 4.6 results.
- [AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents](../Inbox/2026-05-16--agentkernelarena-generalization-aware-benchmarking-of-gpu-kernel-optimization-agents.md): Defines AgentKernelArena task set, scoring, speedups, and unseen-shape issue.
- [TOBench: A Task-Oriented Omni-Modal Benchmark for Real-World Tool-Using Agents](../Inbox/2026-05-16--tobench-a-task-oriented-omni-modal-benchmark-for-real-world-tool-using-agents.md): Defines TOBench task design and reports model and human success rates.

### Execution feedback and refusal controls
几篇论文都在研究什么时候代码生成已经足够可信，可以拿来使用。CodeRefuser 采样程序，运行生成的测试，把输出聚类，然后拒绝那些看起来很可能失败的提示。它的校准目标是任务级风险，默认设置检查三个采样解是否全部错误。

训练阶段的反馈也在变得更谨慎。扩散式代码强化学习研究发现，当大多数生成程序都会失败时，类似 Pylint 的静态分析可能比单元测试通过率更适合作为奖励。以 DiffuCoder 为例，静态检查把 HumanEval 从 53.9 提高到 67.1，并把 rollout 时间从 29.3 秒降到 26.5 秒。适度提示有帮助，但较高的提示比例可能会拖累表现，所以有效信号取决于任务难度和奖励类型。

#### Evidence
- [Task Abstention for Large Language Models in Code Generation](../Inbox/2026-05-16--task-abstention-for-large-language-models-in-code-generation.md): Describes CodeRefuser, output clustering, calibration, and precision gains.
- [Beyond Execution: Static-Analysis Rewards and Hint-Conditioned Diffusion RL for Code Generation](../Inbox/2026-05-16--beyond-execution-static-analysis-rewards-and-hint-conditioned-diffusion-rl-for-code-generation.md): Reports static-analysis reward results, rollout-time reduction, and hint effects.

### Traceability and package risk
这段时间的 agent 安全工作重点是可追踪的行动，而不只是更安全的最终答案。provenance 论文认为，使用工具的 agent 需要记录，显示因果贡献、执行可追踪性，以及在设计、部署和监控中的可能干预点。它的证据基础主要是概念论证和引用的风险数据，但它指出了一个具体缺口：多步骤 agent 造成的危害，可能涉及开发者、工具作者、平台运营方和部署方。

包幻觉给这个风险提供了一个软件供应链例子。对 Claude Sonnet 4.6、Claude Haiku 4.5、GPT-5.4-mini、Gemini 2.5 Pro 和 DeepSeek V3.2 的复现研究发现，总体幻觉率集中在 4.62% 到 6.10% 之间。最可操作的发现是五个模型共同幻觉出的 127 个不存在的包名，其中包括 109 个 PyPI 包名和 18 个 npm 包名。

#### Evidence
- [Responsible Agentic AI Requires Explicit Provenance](../Inbox/2026-05-16--responsible-agentic-ai-requires-explicit-provenance.md): Summarizes the explicit provenance proposal and cited agent-risk evidence.
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): Reports package hallucination rates and shared hallucinated package names.

### Operating cost and agent-native tooling
现实约束已经不只是模型质量。Token 用量正在变成工程团队的预算项。The Pragmatic Engineer 的报告引用了两家公司的数据，它们在六个月内 token 支出都增长了约 10 倍；一家种子期基础设施公司从每名开发者每月约 200 美元涨到约 3,000 美元；另一家 SaaS 公司通过更换默认模型把成本削减了 30%。

工具设计也在代码编辑层面作出回应。ane 是一款早期终端编辑器，借助 Language Server Protocol 支持和无头 CLI 命令，让 agent 读取或编辑函数、定义、行或分隔符作用域。这个项目还没有基准证据，但它的设计目标很明确：用更窄的代码操作减少整文件读取和大范围补丁。

#### Evidence
- [Token spend breaks budgets – what next?](../Inbox/2026-05-16--token-spend-breaks-budgets-what-next.md): Reports token-spend growth, per-developer costs, and cost-control examples.
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): Describes ane's LSP-backed narrow editing commands and lack of quantitative benchmarks.
