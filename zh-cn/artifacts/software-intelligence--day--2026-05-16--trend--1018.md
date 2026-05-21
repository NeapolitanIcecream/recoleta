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

# 代码智能体正在作为有边界的工作者接受测试，而不只是代码生成器

## Overview
最强的信号是运行式评估。1GC-7RC、AgentKernelArena 和 TOBench 都在有边界的工作循环中给智能体评分，循环包含工具、运行时检查和资源限制。同一关切也出现在可靠性论文、供应链风险研究和 token 预算报告中。

## Clusters

### 端到端智能体基准
新的基准把智能体当作需要规划、编辑、运行工具并从错误中恢复的工作者来测试。1GC-7RC 在一块 NVIDIA A100 GPU 上给智能体安排七个机器学习任务，不提供互联网访问，每个任务预算为 40–120 分钟。AgentKernelArena 测试 196 个 GPU 内核任务，覆盖 HIP、Triton 和 PyTorch-to-HIP 路径，然后检查编译、正确性、速度和隐藏输入形状。TOBench 加入了多模态工具使用：100 个可执行任务、27 个 Model Context Protocol 服务器，以及针对具体任务的验证器。

结果呈现出有用的差异。使用 Sonnet 4.6 的 Claude Code 在 1GC-7RC 的七个可见基线上都有提升。AgentKernelArena 报告称，许多内核类别的编译率和正确率较高，平均加速最高达到 6.89×，但 PyTorch-to-HIP 内核在未见过的形状上经常失败。TOBench 的结果严格得多：最佳模型的任务成功率为 41.0%，而人类基准为 94.0%。

#### Evidence
- [1GC-7RC: One Graphic Card -- Seven Research Challenges! How Good Are AI Agents at Doing Your Job?](../Inbox/2026-05-16--1gc-7rc-one-graphic-card-seven-research-challenges-how-good-are-ai-agents-at-doing-your-job.md): 定义了 1GC-7RC 任务、计算限制，以及报告的 Sonnet 4.6 结果。
- [AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents](../Inbox/2026-05-16--agentkernelarena-generalization-aware-benchmarking-of-gpu-kernel-optimization-agents.md): 定义了 AgentKernelArena 的任务集、评分、加速结果和未见形状问题。
- [TOBench: A Task-Oriented Omni-Modal Benchmark for Real-World Tool-Using Agents](../Inbox/2026-05-16--tobench-a-task-oriented-omni-modal-benchmark-for-real-world-tool-using-agents.md): 定义了 TOBench 的任务设计，并报告了模型和人类成功率。

### 执行反馈和拒答控制
多篇论文关注如何判断代码生成是否可靠到可以使用。CodeRefuser 会采样程序、运行生成的测试、对输出聚类，并拒绝看起来可能失败的提示。它的校准目标是任务级风险，默认设置检查三个采样解是否全错。

训练阶段的反馈也变得更谨慎。关于扩散代码模型强化学习的研究发现，当大多数生成程序失败时，Pylint 风格的静态分析可能比单元测试通过率更适合作为奖励。在 DiffuCoder 上，静态检查把 HumanEval 从 53.9 提高到 67.1，并把 rollout 时间从 29.3 秒降到 26.5 秒。适度提示有帮助，但较高提示比例可能有害，因此有效信号取决于任务难度和奖励类型。

#### Evidence
- [Task Abstention for Large Language Models in Code Generation](../Inbox/2026-05-16--task-abstention-for-large-language-models-in-code-generation.md): 描述了 CodeRefuser、输出聚类、校准和精确率提升。
- [Beyond Execution: Static-Analysis Rewards and Hint-Conditioned Diffusion RL for Code Generation](../Inbox/2026-05-16--beyond-execution-static-analysis-rewards-and-hint-conditioned-diffusion-rl-for-code-generation.md): 报告了静态分析奖励结果、rollout 时间减少和提示效果。

### 可追踪性和包风险
这一时期的智能体安全工作集中在可追踪动作上，同时也关注更安全的最终回答。溯源论文认为，使用工具的智能体需要记录，以展示设计、部署和监控过程中的因果贡献、执行可追踪性和可能干预点。它的证据基础主要是概念分析和引用的风险数据，但指出了一个具体缺口：多步骤智能体造成的伤害可能涉及开发者、工具作者、平台运营者和部署者。

包幻觉为这一风险提供了一个软件供应链例子。一项复现实验覆盖 Claude Sonnet 4.6、Claude Haiku 4.5、GPT-5.4-mini、Gemini 2.5 Pro 和 DeepSeek V3.2，发现总体幻觉率集中在 4.62% 到 6.10% 之间。最可执行的发现是一组由五个模型共同幻觉出的 127 个不存在的包名，其中包括 109 个 PyPI 名称和 18 个 npm 名称。

#### Evidence
- [Responsible Agentic AI Requires Explicit Provenance](../Inbox/2026-05-16--responsible-agentic-ai-requires-explicit-provenance.md): 概述了显式溯源提案和引用的智能体风险证据。
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): 报告了包幻觉率和共同幻觉出的包名。

### 运行成本和智能体原生工具
实际约束已扩展到模型质量之外。Token 使用正在成为工程团队的一项预算科目。The Pragmatic Engineer 的报告提到两家公司在六个月内 token 支出增长约 10×，一家种子轮基础设施公司的每名开发者月成本从约 200 美元升至约 3,000 美元，还有一家 SaaS 公司通过更改默认模型将成本降低 30%。

工具设计正在代码编辑层作出回应。ane 是一个早期终端编辑器，通过 Language Server Protocol 支持和无头 CLI 命令，让智能体按函数、定义、行或分隔符作用域读取或编辑代码。该项目还没有基准证据，但它的设计目标很明确：通过给智能体提供更窄的代码操作，减少整文件读取和大范围补丁。

#### Evidence
- [Token spend breaks budgets – what next?](../Inbox/2026-05-16--token-spend-breaks-budgets-what-next.md): 报告了 token 支出增长、每名开发者成本和成本控制例子。
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): 描述了 ane 基于 LSP 的窄范围编辑命令，以及缺少定量基准。
