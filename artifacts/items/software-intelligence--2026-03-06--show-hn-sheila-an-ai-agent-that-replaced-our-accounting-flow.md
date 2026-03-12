---
source: hn
url: https://soapbox.pub/blog/announcing-sheila/
published_at: '2026-03-06T23:08:29'
authors:
- knewter
topics:
- ai-agent
- workflow-automation
- accounting-automation
- code-intelligence
- human-in-the-loop
relevance_score: 0.87
run_id: materialize-outputs
---

# Show HN: Sheila, an AI agent that replaced our accounting flow

## Summary
Sheila 是一个面向真实业务的会计 AI 代理，作者称其已替代 Soapbox 的整套承包商付款与记账流程。文章的核心贡献不在新模型，而在于展示了一种通过细粒度工具脚本 + 自然语言工作流文档 + 人在回路迭代，构建可生产代理的工程方法。

## Problem
- 要让 AI 代理真正接管**端到端业务流程**很难；很多平台强调自主、多代理和演示效果，但缺少能在生产中稳定运行的单个代理。
- 会计/付款流程涉及多系统集成与高风险操作，包括收发票、记账、法币/比特币支付、归档、报税与费用上报，手工处理耗时且容易出错。
- 这之所以重要，是因为若 AI 代理不能在这种高约束、高责任的流程中可靠工作，“AI agent platform” 的价值就很难落地到真实企业运营。

## Approach
- 用 **OpenCode** 在空项目中自底向上构建，而不是先写复杂的多步骤硬编码流程；作者认为 v1 方案“脆弱且不灵活”，因此在 v2 改为工具化设计。
- 把能力拆成**50+ 个细粒度脚本**，每个脚本只做一件事，例如读邮件、查余额、发起支付、上传文件、写表格，并逐个测试。
- 用一份约 **600 行的 `AGENTS.md`** 以自然语言描述工作流；当用户下达“process invoices”之类指令时，代理读取说明并串联合适脚本完成流程。
- 保持**human-in-the-loop**：代理在终端中执行，作者实时监督；她可以起草邮件或准备付款，但关键动作在发出前对人可见。
- 核心机制可用最简单的话概括为：**把复杂会计流程拆成很多可靠小工具，再让 LLM 按说明书把它们按顺序调用，并通过人类反复测试修正。**

## Results
- 作者声称 Sheila 已经**替代 Soapbox 的整个 accounting flow**，覆盖承包商发票处理、法币支付（ACH/wire via Mercury）、比特币支付（Kraken/Lightning/Boltz）、记账、费用追踪、P&L 和 1099 报告等完整流程。
- 文章给出的具体工程规模包括：**v2 使用 50+ 个脚本**、工作流说明文档约 **600 行**，并经过“**数百次**”人机迭代测试与修正。
- 交互结果上，用户只需在终端询问“**what's the status?**”，代理即可汇总哪些已完成、哪些待处理、哪些需要关注，表明其具备跨系统流程状态整合能力。
- **没有提供标准基准数据或正式定量指标**；没有报告处理时延、成功率、错误率、节省工时百分比，也没有与其他 agent framework 的可复现实验对比。
- 最强的具体主张是：相较于作者此前的 v1“复杂代码流”，v2 的“细粒度脚本 + AGENTS.md + 人类监督”在真实生产会计场景中更稳定、更灵活，并且已被实际用于公司运营。
- 文章还声称这种模式具有可迁移性：只需替换集成脚本，就可复用到其他业务流程；代码已**以 AGPL 开源**。

## Link
- [https://soapbox.pub/blog/announcing-sheila/](https://soapbox.pub/blog/announcing-sheila/)
