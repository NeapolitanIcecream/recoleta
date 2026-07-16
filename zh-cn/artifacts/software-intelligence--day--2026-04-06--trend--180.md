---
kind: trend
trend_doc_id: 180
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
topics:
- coding-agents
- reinforcement-learning
- software-testing
- program-repair
- verification
- workflow-automation
run_id: materialize-outputs
aliases:
- recoleta-trend-180
tags:
- recoleta/trend
- topic/coding-agents
- topic/reinforcement-learning
- topic/software-testing
- topic/program-repair
- topic/verification
- topic/workflow-automation
language_code: zh-CN
---

# 软件代理研究正在收敛到可验证的训练循环和硬控制闸门

## 概览
这一天最清楚的工作，是让软件代理更容易评分、更容易重跑，也更容易在检查失败时被拦住。Atomic-skill RL、Agent-CoEvo 和 Nidus 分别在训练目标、仓库修复和工程治理三个位置收紧控制环。和前几天相比，重点更少放在证明代理能在真实环境中行动，更多放在建立训练和验证设置，让这些动作可以被测量。

## 研究发现

### Execution-scored RL for engineering agents
强化学习之所以更可用，是因为训练目标更窄，环境更快。*Scaling Coding Agents via Atomic Skills* 把软件工作拆成五个可验证技能，并报告在十个任务上的平均提升为 18.7%，其中 SWE-bench Verified 从 0.507 提升到 0.585。*SandMLE* 把同样的先执行后评估逻辑用到机器学习工程：合成任务把运行时间从约 200 秒降到 15 秒以内，然后在 MLE-bench-lite 上把 Any Medal 率提高 20.3%，达到 66.9%。共同模式很直接：让每一步都便宜、容易评分，然后再扩展 on-policy RL。

#### 资料来源
- [Scaling Coding Agents via Atomic Skills](../Inbox/2026-04-06--scaling-coding-agents-via-atomic-skills.md): Atomic-skill RL setup and cross-task gains for coding agents
- [Synthetic Sandbox for Training Machine Learning Engineering Agents](../Inbox/2026-04-06--synthetic-sandbox-for-training-machine-learning-engineering-agents.md): Synthetic sandbox design, 13x speedup, and MLE gains

### Behavior-first evaluation at repository and service level
仓库级代理现在看的是它们能否修复行为，而不只是补上文件。*Agent-CoEvo* 同时搜索代码补丁和测试补丁，再用通过/失败矩阵给它们评分。它在 SWE-bench Lite 上报告 41.33% resolved，在 SWT-bench Lite 上报告 46.4% resolved，测试质量也高于列出的基线。在微服务里，*Mirage* 在测试期间把模型留在依赖调用链中，在 110 个场景里达到 99% 的状态码一致性和 99% 的响应形状一致性。两篇论文都把模型放进可执行反馈环路里，让行为在发生时就被检查。

#### 资料来源
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Joint code-test search and benchmark results on SWE-bench Lite and SWT-bench Lite
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): Runtime dependency simulation and fidelity metrics for microservice testing

### Deterministic and solver-checked control layers
另一条线是在任务已经足够清楚、可以编译或验证之后，收紧运行时模型的自由度。*Compiled AI* 先生成一个小代码工件，验证后再确定性运行。它在 BFCL 上达到 96% 的任务完成率，大约 17 次事务后回本，P50 延迟为 4.5 ms，且可复现率为 100%。*Nidus* 把治理往前推了一步：每次变更都要对照一个由求解器支持的活规范检查，论文还报告了一个自托管的 100,000 行系统，每次提交都有证明义务。今天最强的系统不要求模型自己保持谨慎，而是把它绑定到代码、测试或形式化检查上。

#### 资料来源
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Compiled workflow generation, validation pipeline, and cost/latency results
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): Solver-checked living specification and self-hosting evidence
