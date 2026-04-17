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

# 编码代理控制闸门

## Summary
近期最明确的变化，是在编码代理周围加入更显式的控制点：在仓库生成前加入契约工件，把安全评分层与受限编辑工具配套使用，以及为含糊任务加入必需的澄清步骤。现有证据更支持具体的产品构建和工作流调整，而不是更宽泛的自主性主张。

## 面向多文件绿地工作的契约优先仓库生成
为绿地内部工具和小型产品模块构建一种契约优先的仓库生成器。关键改动是让代理在写文件之前，先写出可机器校验的规格：所需模块、文件映射、API、类型签名和状态定义。Contract-Coding给出了这样做的具体理由。在 Greenfield-5 上，它在 Gomoku 和 Plane Battle 上报告了 100% 成功率，在 City Sim 上为 87%，在 Snake++ 上为 80%，在 Roguelike 上为 47%；在这组任务里最难的任务上，它明显领先 OpenHands、MetaGPT、ChatDev 和 FLOW。速度结果对想缩短迭代周期的产品团队也有价值：Hierarchical Execution Graph 在把 Roguelike 成功率维持在 47% 的同时，将运行时间从 510s 降到 232s。

第一批用户会是那些生成新的多文件服务、管理工具、游戏原型或迁移脚手架的团队，因为这些场景里跨文件一致性比局部语法更容易出问题。一个低成本测试很简单：选取十个当前需要代理多轮修复的绿地任务，加入一个必须在代码生成前获批或自动检查通过的契约工件，然后衡量文件级一致性、重跑次数，以及仓库达到可通过状态所需的总时间。同样的证据也显示出它的弱点：当任务可以被收敛为明确的接口和模块边界时，这种方法最有效。涉及密集策略逻辑或业务规则冲突的任务，仍然需要在契约之上再加一层控制。

### Evidence
- [Contract-Coding: Towards Repo-Level Generation via Structured Symbolic Paradigm](../Inbox/2026-04-10--contract-coding-towards-repo-level-generation-via-structured-symbolic-paradigm.md): 仓库级结果、基准对比和运行时收益支持在多文件生成中采用契约优先的构建方式。
- [Can Coding Agents Be General Agents?](../Inbox/2026-04-10--can-coding-agents-be-general-agents.md): Odoo 案例显示，一旦策略约束和相互依赖的业务决策开始累积，显式结构仍然会遇到困难。

## 带有补丁式编辑和审批闸门的安全偏置代码生成
在代码生成中加入安全评分层，并与受限编辑工具配套使用。DeepGuard 展示了一条具体的模型侧路径：聚合多个 transformer 层中的安全信号，再在推理时施加一种低成本偏置，让模型更倾向于选择安全 token，同时不过多牺牲功能正确性。在五个代码 LLM 上，它相对 SVEN 将安全且正确的生成率平均提高了 11.9%；在 Qwen2.5-Coder-3B 上，它把 sec-pass@1 从 70.47% 提高到 80.76%，同时让 pass@1 保持接近基础模型水平。

这已经足以支持一个范围收窄的产品方案，面向那些要把内部编码代理投放到存在常规安全暴露代码库中的团队：Web 处理器、认证流程、文件操作、数据库访问和依赖胶水代码。Zup 的部署论文补上了工具侧的部分。他们的内部代理依赖定向字符串替换编辑、分层 shell 限制、审计日志，以及在扩大自主性之前先使用审批模式。一个实际的上线方式是：让高风险文件走安全加固的模型路径，把编辑保持为基于补丁的形式，并在早期阶段对 shell 和写入操作要求审批。低成本验证方法是回放几百个已接受的代理任务，配上安全审查标签，在扩大访问范围之前比较漏洞发现、通过率和人工返工。

### Evidence
- [DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation](../Inbox/2026-04-10--deepguard-secure-code-generation-via-multi-layer-semantic-aggregation.md): 提供了安全代码收益的具体结果，以及在提升安全性的同时保持正确性的机制。
- [Building an Internal Coding Agent at Zup: Lessons and Open Questions](../Inbox/2026-04-10--building-an-internal-coding-agent-at-zup-lessons-and-open-questions.md): 展示了让安全加固编码代理能够在生产环境中可用的配套工具控制。

## 面向编码代理的澄清优先工单分流
在含糊的编码任务前加入显式澄清闸门，并把它作为产品能力来评分。HiL-Bench 表明，这个差距已经大到需要单独设计一套工作流。在 SQL 任务上，模型在信息完整时可达到 86% 到 91% 的 pass@3，但当它们必须自己决定何时调用 `ask_human()` 时，会降到 5% 到 38%。在 SWE 任务上，模型在信息完整时可达到 64% 到 88%，而在需要选择性升级求助时会降到 2% 到 12%。没有任何模型在 SWE 上超过 50% 的 blocker recall。这不是少见的边缘情况。该基准包含 1,131 个经人工验证的 blocker，平均每个任务 3.8 个，覆盖信息缺失、请求含糊和信息冲突。

这里的构建方式很直接：对于涉及不清晰需求、隐藏策略选择或不完整仓库上下文的工单，在执行前加入必需的 blocker 检查。代理应当列出候选 blocker，提出有针对性的问题，并在这些问题没有得到回答时暂停。这也需要超出 pass/fail 的评估。Ask-F1、blocker recall 和 question precision 应当与任务完成率一起进入内部评分卡。旁边那项日志研究从另一个角度指向了同样的运营问题。代理会漏掉非功能性预期，后续清理由人来完成：在 58.4% 的仓库中，人类比代理更频繁地修改日志；代理在 67% 的情况下未能遵守建设性的日志请求；72.5% 的生成后日志修复由人类完成。把代理部署到 issue-to-PR 工作流中的团队，需要在编码前设置一个正式的澄清步骤，而不只是放一个模型很少能有效使用的聊天框。

### Evidence
- [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](../Inbox/2026-04-10--hil-bench-human-in-loop-benchmark-do-agents-know-when-to-ask-for-help.md): 量化了代理在必须决定何时请求澄清时表现有多差。
- [Do AI Coding Agents Log Like Humans? An Empirical Study](../Inbox/2026-04-10--do-ai-coding-agents-log-like-humans-an-empirical-study.md): 展示了可观测性要求中的相关失败：代理遗漏或处理不当的部分，往往由人类补修。
