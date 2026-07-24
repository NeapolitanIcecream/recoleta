---
kind: ideas
granularity: day
period_start: '2026-07-23T00:00:00'
period_end: '2026-07-24T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent evaluation
- reliability harnesses
- human oversight
- neuro-symbolic reasoning
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/reliability-harnesses
- topic/human-oversight
- topic/neuro-symbolic-reasoning
language_code: zh-CN
---

# 面向模糊智能体工作的评估与审查控制

## 摘要
将澄清、形式化验证和专家审查安排在错误变得难以逆转的决策点，能够更精确地测试智能体的可靠性。最有价值的改进涉及智能体何时提问、策略结论是否具有可执行的推导，以及哪些中间产物确实会触发审查。

## 在不可逆的实现决策之前设置澄清检查点
编码智能体基准的设计者应评估智能体是否会在作出依赖某项隐藏约束的实现决策之前询问该约束，而不应只奖励提问数量或需求覆盖率。ICAE-Bench 发现，恢复更多约束并不会自动提高通过率；pAI-Econ-claude 则将人的决策权集中在代价高昂、难以逆转的选择上。综合这些观察，可以为每项隐藏需求标注其最后责任检查点，例如 API、模式或架构的选择，并将及时澄清与最终测试成功和不必要的中断分开评分。可以进行一次小规模的 ICAE-Bench 重放实验，对比不受限制的提问与基于检查点访问模拟用户的方式，测量增强测试结果和实现返工量。

### 资料来源
- [ICAE-Bench: Evaluating Coding Agents as Interactive Project Builders](../Inbox/2026-07-23--icae-bench-evaluating-coding-agents-as-interactive-project-builders.md): ICAE-Bench 评估了 480 个模糊的项目构建任务，并报告了智能体在隐藏约束、边界情况和长周期集成方面持续失败。
- [pAI-Econ-claude: A Gated Human-in-the-Loop Multi-Agent Architecture for AI-Assisted Economic Theory Development](../Inbox/2026-07-23--pai-econ-claude-a-gated-human-in-the-loop-multi-agent-architecture-for-ai-assisted-economic-theory-development.md): 该门控工作流将人的判断分配给代价高昂、难以逆转的决策；在五个匹配任务中，盲评者有四个任务更偏好该工作流，但其中一个任务丢失了一个重要机制。

## 用于安全策略任务验证的可执行证明轨迹
安全基准维护者和合规团队可以要求智能体同时提交操作性答案，以及基于独立编写的策略模型得出的形式化推导。Tencent WorkBuddy Bench 已按领域区分验证方式，并纳入安全任务；Euclid-MCP 则可以重新运行 Horn 子句推理并公开证明树。组合后的评估能够区分“看起来正确”的答案与有既定规则支持的答案：基准验证器将执行所提交的查询，把结论与任务结果进行比较，并检查推导是否使用了所需的策略子句。对权限、阈值或日期进行反事实修改，可以低成本地检查答案是否经过硬编码。该方法测试的是可审计性，而不是假定智能体将自然语言转换为逻辑的过程正确；Euclid-MCP 没有报告这一步骤的数值基线比较。

### 资料来源
- [Tencent WorkBuddy Bench: A Multi-Domain Coding-Agent Benchmark with Contamination-Resistant Task Construction](../Inbox/2026-07-23--tencent-workbuddy-bench-a-multi-domain-coding-agent-benchmark-with-contamination-resistant-task-construction.md): WorkBuddy Bench 按领域使用不同的验证工具，并有意避免提供覆盖整个套件的汇总分数。
- [Euclid-MCP: A Model Context Protocol Server for Deterministic Logical Reasoning via Prolog](../Inbox/2026-07-23--euclid-mcp-a-model-context-protocol-server-for-deterministic-logical-reasoning-via-prolog.md): Euclid-MCP 通过 MCP 暴露确定性的 SWI-Prolog 推理，并提供证明轨迹和推导日志。

## 在长期研究工作流中由提示触发专家审查
运行智能体辅助经济研究的团队可以在工作流接触高风险产物时触发专家审查，例如均衡声明、福利主张、反例或规范模型选择，而不是对所有阶段统一审查，或依赖智能体记住此前的警告。pAI-Econ-claude 的门控机制提高了可审计性，但消耗了基线使用额度的 4.6 至 18 倍。另一方面，基于提示锚定的工作记忆能够在上下文压缩期间可靠地提供限定范围的信息；在最强的自主控制条件下，智能体在 114 轮中没有发起任何记忆调用。一项匹配研究应植入已知的证明、前提和理论沿袭缺陷，然后比较始终启用的门控、自主审查和由产物触发的审查在缺陷拦截、审查者调用次数和 token 使用量上的表现。目前的证据尚未表明基于提示的路由能够保持 pAI-Econ-claude 的质量收益，因此这种比较才是与决策直接相关的测试。

### 资料来源
- [pAI-Econ-claude: A Gated Human-in-the-Loop Multi-Agent Architecture for AI-Assisted Economic Theory Development](../Inbox/2026-07-23--pai-econ-claude-a-gated-human-in-the-loop-multi-agent-architecture-for-ai-assisted-economic-theory-development.md): 定向门控将平均失败严重程度从 1.58 降至 1.16，并将平均实用性从 2.60 提高到 3.10，但完整工作流需要配对基线额度的 4.6 至 18 倍。
- [Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents](../Inbox/2026-07-23--delivery-not-storage-cue-anchored-working-memory-as-a-harness-property-for-coding-agents.md): 自主记忆在 114 轮中产生了 0 次调用，而确定性的提示触发式交付经受住了反复的上下文压缩，并且在报告的编码运行中没有记录误触发。
