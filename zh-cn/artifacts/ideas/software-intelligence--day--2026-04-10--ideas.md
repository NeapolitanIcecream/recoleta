---
kind: ideas
granularity: day
period_start: '2026-04-10T00:00:00'
period_end: '2026-04-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- repo-generation
- secure-code
- human-in-the-loop
- evaluation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repo-generation
- topic/secure-code
- topic/human-in-the-loop
- topic/evaluation
language_code: zh-CN
---

# 编码代理控制门

## 摘要
近期最清楚的变化，是围绕编码代理增加更明确的控制点：仓库生成前先放合同工件，给代码生成加安全评分并配上受限编辑工具，以及在需求含糊时先做澄清。证据更支持具体构建和流程调整，而不是更大的自治承诺。

## 面向多文件绿色开发的先合同仓库生成
为新的内部工具和小型产品模块构建一个先写合同的仓库生成器。这个做法的关键变化是，让代理在写文件前先写一份可机器检查的规格：需要的模块、文件映射、API、类型签名和状态定义。Contract-Coding 给出了这样做的直接理由。在 Greenfield-5 上，它报告 Gomoku 和 Plane Battle 的成功率都是 100%，City Sim 为 87%，Snake++ 为 80%，Roguelike 为 47%，并且在这个集合里最难的任务上明显优于 OpenHands、MetaGPT、ChatDev 和 FLOW。速度结果也对想缩短迭代周期的产品团队有用：Hierarchical Execution Graph 让 Roguelike 的成功率保持在 47%，同时把运行时间从 510 秒降到 232 秒。

最先会用到它的是那些生成新的多文件服务、管理工具、游戏原型或迁移脚手架的团队，因为这类任务里跨文件一致性比本地语法更容易出错。一个简单的测试方法是：拿十个现在通常要经过多轮代理修复的绿色项目任务，加上一份必须在代码生成前审批或自动检查的合同工件，然后测文件级一致性、重跑次数和到可通过仓库的耗时。同一组证据也说明了它的边界：当任务可以拆成明确接口和模块边界时，这种方法最有用。带有密集策略逻辑或业务规则冲突的任务，仍然需要合同之上的另一层控制。

### 资料来源
- [Contract-Coding: Towards Repo-Level Generation via Structured Symbolic Paradigm](../Inbox/2026-04-10--contract-coding-towards-repo-level-generation-via-structured-symbolic-paradigm.md): Repo-level results, benchmark comparisons, and runtime gains support a contract-first build for multi-file generation.
- [Can Coding Agents Be General Agents?](../Inbox/2026-04-10--can-coding-agents-be-general-agents.md): The Odoo case shows where explicit structure still struggles once policy constraints and interdependent business decisions accumulate.

## 带补丁式编辑和审批门的安全偏置代码生成
给代码生成加上一层安全评分，再配上受限编辑工具。DeepGuard 给出了一条具体的模型侧路径：聚合多个 Transformer 层的安全信号，然后在推理时加一个很便宜的偏置，让模型更偏向安全 token，同时几乎不损失功能正确性。在五个代码 LLM 上，它把安全且正确的生成率平均比 SVEN 提高了 11.9%；在 Qwen2.5-Coder-3B 上，它把 sec-pass@1 从 70.47% 提到 80.76%，同时把 pass@1 保持在接近基础模型的水平。

这足够支持一个窄一些的产品方案，面向把内部编码代理放进常见安全敏感代码库的团队：Web 处理程序、认证流程、文件操作、数据库访问和依赖拼接。Zup 的部署论文给出了工具侧的补充。它的内部代理依赖定向字符串替换编辑、分层 shell 限制、审计日志，以及在更高自治之前的审批模式。实际落地可以这样做：把高风险文件路由到安全强化过的模型路径，保持编辑为补丁式，并在早期阶段要求 shell 和写入操作先审批。一个便宜的检查方法是，回放几百个已接受的代理任务，带上安全审查标签，然后在扩展权限前比较漏洞发现、通过率和人工返工。

### 资料来源
- [DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation](../Inbox/2026-04-10--deepguard-secure-code-generation-via-multi-layer-semantic-aggregation.md): Provides the concrete secure-code gain and the mechanism that preserves correctness while improving security.
- [Building an Internal Coding Agent at Zup: Lessons and Open Questions](../Inbox/2026-04-10--building-an-internal-coding-agent-at-zup-lessons-and-open-questions.md): Shows the surrounding tool controls that make a security-hardened coding agent usable in production.

## 面向编码代理的先澄清工单分流
在含糊的编码任务前加一个明确的澄清关卡，并把它当作产品功能来评估。HiL-Bench 显示，这个缺口已经大到值得单独做一套流程。在 SQL 任务上，完整信息下能拿到 86% 到 91% pass@3 的模型，在必须决定何时调用 `ask_human()` 时会掉到 5% 到 38%。在 SWE 任务上，完整信息下能到 64% 到 88% 的模型，在选择性升级求助时会掉到 2% 到 12%。没有任何模型在 SWE 上的 blocker recall 超过 50%。问题也不是少见边缘情况。这个基准包含 1,131 个经过人工验证的 blocker，平均每个任务 3.8 个，类型包括缺失信息、含糊请求和矛盾信息。

实现方式很直接：在涉及需求不清、隐藏策略选择或仓库上下文不完整的工单上，执行前先做 blocker 检查。代理应该暴露候选 blocker，提出有针对性的问题，并在问题没有得到回答时暂停。评估也不能只看成败。Ask-F1、blocker recall 和 question precision 应该和任务完成率一起出现在内部评分卡上。旁边的日志研究从另一个角度指向同一个操作问题。代理会漏掉非功能性要求，后续由人工补救：在 58.4% 的仓库里，人工修改日志的次数比代理更多，代理对建设性日志请求的遵守失败率是 67%，而 72.5% 的生成后日志修复由人工完成。把代理接进 issue-to-PR 流程的团队，在开始编码前需要正式的澄清步骤，而不只是一个模型很少用好的聊天框。

### 资料来源
- [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](../Inbox/2026-04-10--hil-bench-human-in-loop-benchmark-do-agents-know-when-to-ask-for-help.md): Quantifies how badly agents perform when they must decide when to ask for clarification.
- [Do AI Coding Agents Log Like Humans? An Empirical Study](../Inbox/2026-04-10--do-ai-coding-agents-log-like-humans-an-empirical-study.md): Shows a related failure in observability requirements where humans repair what agents omit or mis-handle.
