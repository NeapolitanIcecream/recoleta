---
kind: trend
trend_doc_id: 139
granularity: day
period_start: '2026-04-04T00:00:00'
period_end: '2026-04-05T00:00:00'
topics:
- coding-agents
- repository-level-generation
- program-repair
- runtime-debugging
- agent-safety
- context-pruning
run_id: materialize-outputs
aliases:
- recoleta-trend-139
tags:
- recoleta/trend
- topic/coding-agents
- topic/repository-level-generation
- topic/program-repair
- topic/runtime-debugging
- topic/agent-safety
- topic/context-pruning
language_code: zh-CN
---

# 编码代理研究越来越看重执行循环、运行时证据和真实动作控制

## Overview
这一天最强的几篇论文，让编码代理的主张更可执行，也更可检查。重点是对代理读取什么、记住什么、运行什么，以及被允许修改什么，进行更具体的控制。EnvGraph 和 LiveCoder把仓库生成和运行时验证、多次尝试中的证据联系起来。DebugHarness把修复推进到实时调试。Squeez 和 AmPermBench则分别聚焦两个操作层面的瓶颈：上下文膨胀和权限覆盖。

## Clusters

### 可执行仓库与跨尝试记忆
仓库级代码生成越来越看重整个项目能否安装、链接、运行，并在多次尝试中保持可用。EnvGraph把运行时故障诊断视为一个结构化归因问题，覆盖外部包和内部引用，并在 RAL-Bench 和 NL2Repo-Bench 上报告了 5.72 到 5.87 个点的功能正确性提升，以及 4.58 到 8.66 个点的非功能质量提升。LiveCoder从另一个角度处理同一瓶颈：它在多次尝试之间保留成功笔记、失败笔记和当前最佳仓库产物。在 RAL-Bench 上，它报告了最高 +22.94 个功能分数点、最高 81.58% 的仓库复用率，以及最高 53.63% 的成本下降。共同的信息很直接：执行反馈现在已经是方法的一部分，不只是评分结果。

#### Evidence
- [Toward Executable Repository-Level Code Generation via Environment Alignment](../Inbox/2026-04-04--toward-executable-repository-level-code-generation-via-environment-alignment.md): EnvGraph 摘要，包含方法和基准提升。
- [Persistent Cross-Attempt State Optimization for Repository-Level Code Generation](../Inbox/2026-04-04--persistent-cross-attempt-state-optimization-for-repository-level-code-generation.md): LiveCoder 摘要，包含跨尝试持久状态和报告的改进。

### 将代理观察裁剪为证据块
工具使用效率正在成为一个可以单独基准测试的子问题。Squeez关注编码代理循环中的一个小步骤：从一次工具输出里只保留下一步操作所需的原文行。它的数据集包含 27 种工具类型的 11,477 个样例，经过 LoRA 微调的 Qwen 3.5 2B 模型在一个含 618 个样例、经人工审查的测试集上，在 0.92 压缩率下达到 0.80 F1。这个结果的价值在于，它让代理的上下文管理可以在线级别衡量，并且用直接的证据保留指标来评估，而不是笼统地谈提示压缩。论文没有展示端到端任务收益，所以现有证据支持的是一个很强的组件结果，还不能说明整个代理都因此变强。

#### Evidence
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md): 摘要给出了任务定义、数据集规模，以及高压缩下的行级结果。

### 修复代理读取的是运行时状态，不只是代码
程序修复工作越来越依赖实时状态。DebugHarness 使用 GDB、pwndbg 和 rr record/replay 来检查运行时内存、逆向追踪故障、测试假设，并在循环中验证补丁。在覆盖 29 个 C/C++ 项目的 200 个真实漏洞的 SEC-bench 上，它报告的解决率约为 90%，高于 PatchAgent 的 57.5% 和 VulnResolver 的 67.5%。这里的具体价值不只是更高的补丁成功率。对于崩溃点和根因相距很远的内存安全故障，这个方法把运行时检查当作主要的缺陷证据来源。

#### Evidence
- [DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair](../Inbox/2026-04-04--debugharness-emulating-human-dynamic-debugging-for-autonomous-program-repair.md): 摘要涵盖了动态调试流程和 SEC-bench 结果。

### 权限门控仍然漏掉许多真实代理动作
代理安全评估越来越具体地指出权限系统会在哪些地方失效。Claude Code auto-mode 研究为含糊的 DevOps 请求构建了 AmPermBench，并在单个动作层级给决策打分。在 253 个会改变状态的动作中，报告的假阴性率为 81.0%。问题很大一部分出在架构上：36.8% 的动作通过 Tier 2 文件编辑路径，而分类器从不检查这一路径，仅这一处就产生了 51 个假阴性。即使权限门会检查动作，仅 Tier 3 的表现仍然很差，假阴性率为 70.3%，假阳性率为 31.9%。这个阶段的风险点很明确：防护栏需要覆盖所有等价的状态变更路径，而不只是 shell 命令。

#### Evidence
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): 摘要提供了基准设计、分层架构和动作级错误率。
