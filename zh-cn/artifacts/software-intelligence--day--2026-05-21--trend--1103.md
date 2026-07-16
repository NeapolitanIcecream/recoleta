---
kind: trend
trend_doc_id: 1103
granularity: day
period_start: '2026-05-21T00:00:00'
period_end: '2026-05-22T00:00:00'
topics:
- coding agents
- software engineering
- agent evaluation
- test generation
- trajectory training
- self-evolving agents
- pull requests
run_id: materialize-outputs
aliases:
- recoleta-trend-1103
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/test-generation
- topic/trajectory-training
- topic/self-evolving-agents
- topic/pull-requests
language_code: zh-CN
---

# Coding agents are being judged by the evidence they leave behind

## 概览
当前重点是：coding-agent 工作正在把进展绑定到可检查的证据上。P2T 组织修复步骤，SWE-Mutation 测试生成的测试能否抓住真实 bug，MOSS 在源代码更新前重放生产故障。

## 研究发现

### Trajectory evidence for training coding agents
P2T 将开发者补丁当作私有筛选数据，然后构建由事实、里程碑、编辑和验证步骤组成的过程图。学生代理只能看到经过约束的轨迹前缀。这针对监督微调中的一个常见失败：复制包含重复文件查看、循环或没有依据的推理的长教师轨迹。

报告的提升很实际。在 SWE-bench Verified 上，P2T 相比按结果过滤的监督微调，Pass@1 最高提升 10.8 个点，同时把平均推理成本每个实例降低约 15 美元。ACC 走了另一条长上下文训练路线。它把完成的 Search、软件工程和 SQL 代理运行整理成问答样例，样例来自分散的工具输出。用这些整理后的上下文对 Qwen3-30B-A3B-Thinking 做微调后，MRCR 从 50.19 提升到 68.28，GraphWalks 从 69.92 提升到 77.51。

#### 资料来源
- [From Patches to Trajectories: Privileged Process Supervision for Software-Engineering Agents](../Inbox/2026-05-21--from-patches-to-trajectories-privileged-process-supervision-for-software-engineering-agents.md): P2T summary, method, and SWE-bench results.
- [ACC: Compiling Agent Trajectories for Long-Context Training](../Inbox/2026-05-21--acc-compiling-agent-trajectories-for-long-context-training.md): ACC trajectory compilation method and long-context benchmark gains.

### Generated tests face harder checks
SWE-Mutation 把可执行测试和有用测试区分开来。每个问题都配有从 golden fix 生成的变异体，生成的测试必须复现原始 bug、通过修复版本，并发现有缺陷的变体。差距很大：DeepSeek-V3.1 配合 Mini-Swe-Agent 在 Python 测试生成上达到 88.20% Pass@1，但验证只有 10.20%，变异体检测只有 36.15%。

VeriScale 对基于 Lean 的可验证代码生成施加了类似压力。它把 Verina 扩展成 VerinaPlus，加入更多预期案例、非预期输入和对抗性非预期输出。在更强的测试集下，GPT-5.5 SpecGen 从 68.78% 降到 44.44%，CodeGen 从 96.83% 降到 86.24%。共同结论很直接：测试集需要对抗性覆盖，而不只是能运行的样例。

#### 资料来源
- [SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?](../Inbox/2026-05-21--swe-mutation-can-llms-generate-reliable-test-suites-in-software-engineering.md): SWE-Mutation benchmark design and model results.
- [VeriScale: Adversarial Test-Suite Scaling for Verifiable Code Generation](../Inbox/2026-05-21--veriscale-adversarial-test-suite-scaling-for-verifiable-code-generation.md): VeriScale test-suite scaling method and score drops.

### Production failures are becoming update inputs
MOSS 测试一个已部署代理能否在反复出现面向用户的失败后修复自己的源代码。它把薄弱或缺失的对话块分批处理，按顺序执行定位、规划、编辑、审查、评估和裁定阶段，然后在 trial-worker 容器里测试候选镜像。升级仍然需要通过 `moss evo apply` 获取用户同意，再结合健康探针和回滚机制。

在 OpenClaw 上，一次演化周期把四个任务的平均评分从 0.25 提高到 0.61，没有人工代码编辑。修复范围很大：MOSS 会修改 harness 代码，也会修改提示、技能和记忆，所以路由、hook 顺序、会话状态、分发和并发中的故障都能修。

#### 资料来源
- [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](../Inbox/2026-05-21--moss-self-evolution-through-source-level-rewriting-in-autonomous-agent-systems.md): MOSS design, deployment safeguards, and OpenClaw score change.

### Review records and patch structure matter
两项研究说明，最终通过或合并标签对 coding agent 来说太粗了。agentic pull-request 研究检查了 11,048 个已关闭 PR，并手工编码了 717 个案例。在被拒绝的 PR 中，只有 35.7% 是明确的代理失败；其余由工作流约束和未知原因构成。在已合并的 PR 中，15.4% 包含明确的审查反馈或审查者直接应用的提交。

Refactoring Runaway 直接看补丁本身。在 3,691 个有效的 Java 代理补丁中，纠缠式重构出现在 21.43% 的代理补丁里，并且与较低的可编译性有关。RefUntangle 会检查重构是否必要且安全，然后移除或修复有风险的部分。平均编译成功率从 19.34% 升到 38.33%，此前未解决的补丁中有 2.79% 通过了全部测试。

#### 资料来源
- [Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study](../Inbox/2026-05-21--why-are-agentic-pull-requests-merged-or-rejected-an-empirical-study.md): Agentic PR dataset, manual coding, and merge/rejection findings.
- ["Refactoring Runaway": Understanding and Mitigating Tangled Refactorings in Coding Agents for Issue Resolution](../Inbox/2026-05-21--refactoring-runaway-understanding-and-mitigating-tangled-refactorings-in-coding-agents-for-issue-resolution.md): Tangled refactoring study and RefUntangle results.
