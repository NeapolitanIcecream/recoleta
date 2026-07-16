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

# 受控的代码代理运作

## 摘要
代码代理已经适合在工程工作流里做更窄的运行测试：固定预算的验收运行、安装前的包名检查，以及与 token 支出挂钩的受限代码编辑试点。共同点是对代理的动作、产出和成本做可测的控制。

## Repository acceptance runs for code agents with time limits and hidden checks
工程团队可以先用一小组内部任务测试代码代理，再扩大上线范围：一个隔离工作区、固定的时间和 token 预算、除非任务需要否则不接入网络、用于迭代的可见测试，以及用于验收的隐藏检查。运行过程应记录命令、编辑、失败、重试、最终得分和成本。

最近的基准测试指向同一种运行方式。1GC-7RC 给代理 7 个机器学习任务，数据准备被锁定，本地数据，1 张 A100 GPU，无网络，预算为 40 到 120 分钟。AgentKernelArena 通过编译、正确性、计时和隐藏输入形状来控制 GPU 内核任务。TOBench 用可执行任务、MCP 工具、工作区状态和任务专用验证器评估使用工具的代理，而最佳报告模型在 94.0% 的人类基准下达到 41.0% 的任务成功率。

一个可操作的内部版本可以先从一个团队的 10 到 20 个重复性工作开始：依赖升级、修复失败测试、小型特性开关、数据管道补丁，或模型训练改进。验收规则要足够简单，能直接放进 CI。若代理只通过可见检查、做了大范围修改，或为了完成小任务花费过多，团队应在进入生产评审队列前就看到这一点。

### 资料来源
- [1GC-7RC: One Graphic Card -- Seven Research Challenges! How Good Are AI Agents at Doing Your Job?](../Inbox/2026-05-16--1gc-7rc-one-graphic-card-seven-research-challenges-how-good-are-ai-agents-at-doing-your-job.md): 1GC-7RC describes fixed-budget ML coding-agent tasks with locked preparation, no internet, one A100 GPU, deterministic metrics, and repeated runs.
- [AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents](../Inbox/2026-05-16--agentkernelarena-generalization-aware-benchmarking-of-gpu-kernel-optimization-agents.md): AgentKernelArena uses an isolated workspace and gated compilation, correctness, timing, and unseen-shape evaluation for GPU-kernel agents.
- [TOBench: A Task-Oriented Omni-Modal Benchmark for Real-World Tool-Using Agents](../Inbox/2026-05-16--tobench-a-task-oriented-omni-modal-benchmark-for-real-world-tool-using-agents.md): TOBench provides executable tool-use tasks with task-specific verifiers and reports a large gap between current agents and humans.

## Package-name checks for AI-generated install commands and imports
接受代理生成代码的团队，应在合并前对 `pip install`、`npm install`、导入、锁定文件和生成的安装脚本中的新包名加一层检查。检查可以查询 PyPI 和 npm，对照已批准的依赖列表，并要求人工审查那些不存在或在仓库里从未使用过的名称。

原因很具体，是供应链暴露。对 Claude Sonnet 4.6、Claude Haiku 4.5、GPT-5.4-mini、Gemini 2.5 Pro 和 DeepSeek V3.2 的复现发现，整体包名幻觉率集中在 4.62% 到 6.10% 之间。研究还发现有 127 个不存在的包名被这五个模型全部幻觉出来，其中 109 个来自 PyPI，18 个来自 npm。这些共享名称可以作为拒绝列表的起始数据，但真正的控制点是生成代码提出依赖时做注册表验证。

这可以作为一个很小的 CI 或 pre-commit 增补，失败条件也很清楚：先阻止未知包名，直到人工确认注册表条目、所有者、注册时长，以及加入它的理由。

### 资料来源
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): The package-hallucination study reports 4.62% to 6.10% hallucination rates across five code-capable models and identifies 127 nonexistent names shared by all five.
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): The paper frames nonexistent package suggestions in install commands and imports as a slopsquatting attack surface for PyPI and npm.

## Scoped code-editing pilots tied to token-spend reporting
工程平台团队可以跑一个为期两周的试点，把选定的代理编辑都限制在符号级或函数级的读取和编辑命令里，然后把 token 用量、编辑大小、审查时间和回滚率与正常的整文件代理会话对比。试点应优先选择 Language Server Protocol 支持较好的语言，以及目标函数或定义已知的任务。

成本压力已经很明显。The Pragmatic Engineer 的报道提到，有公司在六个月内看到 token 支出约增长 10 倍，一家种子阶段基础设施公司从每位开发者每月约 200 美元涨到约 3,000 美元，而一家 SaaS 公司通过更换默认模型把成本降了 30%。代理编辑工具开始在代码操作层面处理同一个问题。`ane` 提供无头 CLI 命令，可以读取或编辑单个函数体、函数名、函数定义、行、缓冲区或分隔符作用域，并返回统一 diff。

这个测试要保持范围收紧：选一个仓库，把常见补丁任务转到受限操作上，看看代理是否还会通读整个文件并产出大范围补丁。如果 token 支出下降，而且审查失败没有增加，团队就得到了一条可以直接用于代理会话的编辑策略。

### 资料来源
- [Token spend breaks budgets – what next?](../Inbox/2026-05-16--token-spend-breaks-budgets-what-next.md): The token-spend report gives concrete examples of fast-growing coding-agent costs and savings from changing default models.
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): The ane summary describes LSP-backed headless commands for narrow reads and edits, with unified diffs for agent use.
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): The source text describes ane exec, language-server integration, minimal token usage, and support for Rust, Go, TypeScript/JavaScript, and Python.
