---
kind: ideas
granularity: day
period_start: '2026-07-12T00:00:00'
period_end: '2026-07-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- model routing
- security review
- agent memory
- local AI
tags:
- recoleta/ideas
- topic/coding-agents
- topic/model-routing
- topic/security-review
- topic/agent-memory
- topic/local-ai
language_code: zh-CN
---

# 代理部署的运营控制

## 摘要
团队可以通过将代理工作附加到现有审查记录、在范围明确的生产工作负载上评估模型，并把记忆控制作为可观察的产品行为进行测试，更安全地采用代理。现有测量数据有限，因此每次部署都应从范围受限的试验和明确的运营指标开始。

## 面向代码仓库的拉取请求安全审查模型路由
应用安全团队应在拉取请求层面评估和路由模型。Dam Secure 对 10 个拉取请求进行的基准测试显示，成本与质量差异很大：GPT-5.6 Sol 的 F1 为 0.91，每个拉取请求成本 0.70 美元；Grok 4.5 的 F1 为 0.77，成本 0.20 美元；Gemini 3.1 Flash Lite 的 F1 为 0.75，成本约 0.04 美元。测试语料只包含预先植入的访问控制缺陷，因此还需要在各团队使用的编程语言、漏洞类型和审查规范上确认这些排名。

实际部署时，可以重放一组包含已知问题的私有已合并拉取请求，记录召回率、精确率、审查延迟和成本，然后选择达到团队召回率阈值的最低成本模型。对于高风险变更，可以根据涉及的文件、身份验证代码或初始模型的不确定性升级到更高层级。先以影子模式运行路由器，再在最高模型层级限制下开放一部分流量。使用 20 到 50 个有代表性的拉取请求，可以初步检查路由是否降低支出，同时没有增加漏报或噪声评论。

### 资料来源
- [Grok 4.5 and GPT5.6 beat Anthropic for finding security vulnerabilities in PRs](../Inbox/2026-07-12--grok-4-5-and-gpt5-6-beat-anthropic-for-finding-security-vulnerabilities-in-prs.md): 说明了该基准测试仅覆盖拉取请求，并提醒完整代码扫描的排名可能不同。
- [Grok 4.5 and GPT5.6 beat Anthropic for finding security vulnerabilities in PRs](../Inbox/2026-07-12--grok-4-5-and-gpt5-6-beat-anthropic-for-finding-security-vulnerabilities-in-prs.md): 报告了领先模型和低成本模型的 F1、召回率、精确率及每个拉取请求的成本。
- [We taught our platform to learn its own pricing decisions](../Inbox/2026-07-12--we-taught-our-platform-to-learn-its-own-pricing-decisions.md): 介绍了影子运行、受限流量开放、模型层级上限和不包含内容的训练数据。

## 关联工单的编码代理拉取请求与设计决策记录
使用编码代理的工程团队应把工单、拉取请求和 CI 运行记录整合成一份连续的工作记录。工单应包含验收标准和设计约束；代理应在隔离分支或工作区中工作；审查评论和失败检查应让同一代理继续修改。这样，审查者可以在一条可检查的记录中看到需求、实现、测试结果和合并决定。

代码快速生成也会形成审查瓶颈。一名开发者对三个月使用经历的记录显示，原型从几天缩短到几小时完成，但架构决策、代码量和缺少解释增加了精神压力。为每个代理创建的拉取请求添加一份简短的机器生成决策记录，说明变更的边界、数据模型选择、放弃的选项、新增的测试和未解决的不确定性。在有限的工单类型上试行这套流程，并将审查时间、修改轮次、逃逸缺陷和审查者报告的工作量，与类似的人工编写拉取请求进行比较。OneDev 描述了这种连贯的工作流程，但没有提供量化评估，因此必须依靠本地审查指标。

### 资料来源
- [OneDev AI: Coding Agents as Teammates in Issues, Pull Requests, and CI](../Inbox/2026-07-12--onedev-ai-coding-agents-as-teammates-in-issues-pull-requests-and-ci.md): 展示了关联工单、分支、审查评论、CI/CD 检查和合并决定如何保留在正常的开发记录中。
- [OneDev AI: Coding Agents as Teammates in Issues, Pull Requests, and CI](../Inbox/2026-07-12--onedev-ai-coding-agents-as-teammates-in-issues-pull-requests-and-ci.md): 介绍了由审查反馈和 CI/CD 失败触发的代理修改。
- [The cost of AI-assisted development: cognitive fatigue](../Inbox/2026-07-12--the-cost-of-ai-assisted-development-cognitive-fatigue.md): 报告了审查量增加，以及难以还原生成代码实现选择背后的推理过程。

## 代理记忆导出、删除与同意控制的一致性测试
安全团队和采购团队需要针对持久化代理记忆控制建立可执行的检查。当前的产品描述承诺提供隔离存储库、经同意控制的访问、加密、导出、删除、本地文件和可替换模型，但没有提供独立安全审计或检索测量结果。可以建立一套小型一致性测试，写入具有明显特征的记录，通过获授权和未获授权的代理查询这些记录，撤销同意，导出存储内容，删除指定记录，并验证已删除内容不再出现在检索结果、缓存、日志或模型提示中。

同一套测试还应通过将导出内容加载到第二个客户端或模型中来检查可移植性，确认来源信息和访问规则仍然有效。采购方可以在概念验证期间运行测试，供应商则可以为每个版本发布带签名的结果。应从金丝雀记录以及用户、团队和连接器权限矩阵开始；任何跨存储库检索或删除后的记忆都应阻止部署。这样可以把所有权和删除承诺转化为可重复验证、用户可见的行为。

### 资料来源
- [Show HN: Collaborative context-sharing memory platform for agents and teams](../Inbox/2026-07-12--show-hn-collaborative-context-sharing-memory-platform-for-agents-and-teams.md): 列出了隔离团队存储库、同意控制、加密、导出和删除等承诺，同时指出缺少独立验证和部署数据。
- [Show HN: Collaborative context-sharing memory platform for agents and teams](../Inbox/2026-07-12--show-hn-collaborative-context-sharing-memory-platform-for-agents-and-teams.md): 介绍了跨工具的团队记忆和经同意控制的跨代理访问。
- [A Technology for Free Will](../Inbox/2026-07-12--a-technology-for-free-will.md): 提出可移植的纯文本记忆、可替换模型、本地执行和确定性的客户端权限控制，但没有受控安全审计。
