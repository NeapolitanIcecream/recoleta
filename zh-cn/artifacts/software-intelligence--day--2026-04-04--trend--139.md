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

# 编码代理研究正在按执行循环、运行时证据和真实动作控制来评判

## 概览
这一天最强的论文把编码代理的主张做得更可执行，也更可检查。重点是对代理读什么、记什么、运行什么、以及允许改什么进行具体控制。EnvGraph 和 LiveCoder 把仓库生成和运行时验证、以及多次尝试证据绑定起来。DebugHarness 把修复推进到实时调试。Squeez 和 AmPermBench 收窄了两个运维瓶颈：上下文膨胀和权限覆盖。

## 研究发现

### 可执行仓库与多次尝试记忆
仓库级代码生成现在要看整个项目能否安装、链接、运行，并且经得起反复尝试。EnvGraph 把运行时失败诊断当作一个跨外部包和内部引用的结构化归因问题，在 RAL-Bench 和 NL2Repo-Bench 上分别报告了 5.72 到 5.87 个百分点的功能正确性提升，以及 4.58 到 8.66 个百分点的非功能质量提升。LiveCoder 从另一个角度处理同一个瓶颈：它在多次尝试之间保留成功记录、失败记录和最好的仓库产物。在 RAL-Bench 上，它报告最高 +22.94 个功能分、最高 81.58% 的仓库复用率，以及最高 53.63% 的成本降低。这里传达的信息很直接：执行反馈已经进入方法本身，而不只是计分板。

#### 资料来源
- [Toward Executable Repository-Level Code Generation via Environment Alignment](../Inbox/2026-04-04--toward-executable-repository-level-code-generation-via-environment-alignment.md): EnvGraph summary with approach and benchmark gains.
- [Persistent Cross-Attempt State Optimization for Repository-Level Code Generation](../Inbox/2026-04-04--persistent-cross-attempt-state-optimization-for-repository-level-code-generation.md): LiveCoder summary with persistent cross-attempt state and reported improvements.

### 把代理观察剪成证据块
工具使用效率也开始有了自己的可评测子问题。Squeez 关注编码代理循环里的一个小步骤：从一次工具输出中只保留下一步动作需要的原文行。它的数据集包含 11,477 个样本，覆盖 27 种工具类型；经过 LoRA 微调的 Qwen 3.5 2B 模型在一个经过审核的 618 样本测试集上，以 0.92 压缩率达到 0.80 F1。这个结果有意义，因为它把代理上下文管理细化到行级，用直接的证据保留指标来衡量，而不是笼统地谈提示压缩。论文没有展示端到端任务收益，所以现有证据支持的是一个强的组件结果，而不是完整代理的胜利。

#### 资料来源
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md): Summary gives task definition, dataset scale, and line-level results under heavy compression.

### 修复代理在读运行时状态，而不只是代码
程序修复工作正在更紧地依赖运行时状态。DebugHarness 使用 GDB、pwndbg 和 rr 的 record/replay 来检查运行时内存、向后追踪故障、验证假设，然后在循环中确认补丁。它在覆盖 29 个 C/C++ 项目、200 个真实世界漏洞的 SEC-bench 上报告约 90% 的修复率，高于 PatchAgent 的 57.5% 和 VulnResolver 的 67.5%。这里的具体价值不只是更高的补丁率。这个方法把运行时检查当作内存安全故障的主要证据来源，尤其适用于崩溃位置和根因相距很远的情况。

#### 资料来源
- [DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair](../Inbox/2026-04-04--debugharness-emulating-human-dynamic-debugging-for-autonomous-program-repair.md): Summary covers dynamic debugging workflow and SEC-bench results.

### 权限门控仍然漏掉很多真实代理动作
代理安全评估也在更具体地看权限系统在哪些地方失效。Claude Code auto-mode 研究为含糊的 DevOps 请求构建了 AmPermBench，并在单个动作层面评分。253 个会改变状态的动作里，报告的假阴性率是 81.0%。问题很大一部分来自架构：36.8% 的动作经过了分类器根本不检查的 Tier 2 文件编辑，只这一层就产生了 51 个假阴性。即使网关确实检查了动作，Tier 3-only 的表现仍然很弱，假阴性率 70.3%，假阳性率 31.9%。这给这个时期一个明确的风险主题：防护栏需要覆盖等价的状态变更路径，而不只是 shell 命令。

#### 资料来源
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): Summary provides benchmark design, tiered architecture, and action-level error rates.
