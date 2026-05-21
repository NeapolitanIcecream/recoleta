---
kind: ideas
granularity: day
period_start: '2026-05-16T00:00:00'
period_end: '2026-05-17T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- code agents
- agent benchmarks
- execution feedback
- GPU kernels
- code safety
- token cost
- supply-chain risk
tags:
- recoleta/ideas
- topic/code-agents
- topic/agent-benchmarks
- topic/execution-feedback
- topic/gpu-kernels
- topic/code-safety
- topic/token-cost
- topic/supply-chain-risk
language_code: zh-CN
---

# 受控的代码代理操作

## Summary
代码代理适合先在工程工作流中做范围较窄的运行测试：固定预算验收运行、安装前包名检查，以及与 token 支出绑定的限定范围代码编辑试点。共同点是围绕代理的动作、输出和成本建立可衡量的控制。

## 带时间限制和隐藏检查的代码代理仓库验收运行
工程团队在大范围推出代码代理之前，可以先用一小组内部任务测试它们：一个隔离工作区，固定时间和 token 预算，除非任务需要否则不允许联网，用可见测试支持迭代，用隐藏检查决定是否验收。每次运行都应记录命令、编辑、失败、重试、最终得分和成本。

近期基准测试显示出相同的运行方式。1GC-7RC 给代理提供七个 ML 任务，包含锁定的数据准备、本地数据、一块 A100 GPU、无互联网访问，以及 40 到 120 分钟的预算。AgentKernelArena 通过编译、正确性、计时和隐藏输入形状来约束 GPU kernel 工作。TOBench 用可执行任务、MCP 工具、工作区状态和任务专用验证器评估使用工具的代理；报告中的最佳模型任务成功率为 41.0%，人类基准为 94.0%。

一个实用的内部版本可以从一个团队的 10 到 20 个重复性工作开始：依赖升级、失败测试修复、小型功能开关、数据流水线补丁，或模型训练改进。验收规则应足够简单，可以在 CI 中运行。如果代理只通过可见检查、进行大范围编辑，或为完成小任务花费过高，团队可以在它进入生产评审队列之前发现这些问题。

### Evidence
- [1GC-7RC: One Graphic Card -- Seven Research Challenges! How Good Are AI Agents at Doing Your Job?](../Inbox/2026-05-16--1gc-7rc-one-graphic-card-seven-research-challenges-how-good-are-ai-agents-at-doing-your-job.md): 1GC-7RC 描述了固定预算的 ML 编码代理任务，包括锁定准备流程、无互联网访问、一块 A100 GPU、确定性指标和重复运行。
- [AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents](../Inbox/2026-05-16--agentkernelarena-generalization-aware-benchmarking-of-gpu-kernel-optimization-agents.md): AgentKernelArena 为 GPU-kernel 代理使用隔离工作区，并采用编译、正确性、计时和未见形状评估的分级流程。
- [TOBench: A Task-Oriented Omni-Modal Benchmark for Real-World Tool-Using Agents](../Inbox/2026-05-16--tobench-a-task-oriented-omni-modal-benchmark-for-real-world-tool-using-agents.md): TOBench 提供带任务专用验证器的可执行工具使用任务，并报告了当前代理与人类之间的较大差距。

## 面向 AI 生成安装命令和 import 的包名检查
接受代理代码的团队应在合并前增加新包名检查，覆盖 `pip install`、`npm install`、import、lockfile 和生成的 setup 文件。该检查可以查询 PyPI 和 npm，与已批准的依赖列表比较，并要求人工评审不存在或从未在仓库中使用过的名称。

原因是具体的软件供应链暴露面。一项对 Claude Sonnet 4.6、Claude Haiku 4.5、GPT-5.4-mini、Gemini 2.5 Pro 和 DeepSeek V3.2 的复现实验发现，整体包幻觉率集中在 4.62% 到 6.10% 之间。研究还发现 127 个不存在的包名被五个模型全部幻觉生成，其中包括 109 个 PyPI 名称和 18 个 npm 名称。这些共享名称可作为拒绝列表的种子数据，但主要控制点是在生成代码提出依赖时进行注册表验证。

这是一个小型 CI 或 pre-commit 增补，失败模式明确：阻止未知包名，直到人工确认注册表条目、所有者、存在时间和添加原因。

### Evidence
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): 包幻觉研究报告称，五个具备代码能力的模型的幻觉率为 4.62% 到 6.10%，并识别出 127 个被五个模型共同生成的不存在名称。
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): 该论文将安装命令和 import 中不存在的包建议描述为 PyPI 和 npm 的 slopsquatting 攻击面。

## 与 token 支出报告绑定的限定范围代码编辑试点
工程平台团队可以运行一个为期两周的试点，要求选定的代理编辑通过符号级或函数级读写命令完成，然后将 token 使用量、编辑规模、评审时间和回滚率与常规整文件代理会话比较。试点应聚焦于 Language Server Protocol 支持较好的语言，以及目标函数或定义已知的任务。

成本压力已经显现。The Pragmatic Engineer 的报告提到，一些公司在六个月内 token 支出增长约 10 倍，一家种子轮基础设施公司的人均月支出从约 200 美元升至约 3,000 美元，还有一家 SaaS 公司通过更改默认模型将成本降低 30%。代理编辑工具开始在代码操作层面处理同一问题。`ane` 提供无头 CLI 命令，可读取或编辑单个函数体、函数名、函数定义、行、缓冲区或分隔符作用域，并返回 unified diff。

有用的测试范围很窄：选择一个仓库，将常见补丁任务路由到限定范围的操作，并衡量代理是否停止读取整文件和生成大范围补丁。如果 token 支出下降且评审失败没有增加，团队就有一条可用于代理会话的具体编辑策略。

### Evidence
- [Token spend breaks budgets – what next?](../Inbox/2026-05-16--token-spend-breaks-budgets-what-next.md): token 支出报告给出了编码代理成本快速增长的具体例子，以及通过更改默认模型节省成本的例子。
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): ane 摘要描述了由 LSP 支持的无头命令，用于窄范围读取和编辑，并为代理使用返回 unified diff。
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): 源文本描述了 ane exec、language-server 集成、低 token 使用量，以及对 Rust、Go、TypeScript/JavaScript 和 Python 的支持。
