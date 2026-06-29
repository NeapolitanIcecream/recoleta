---
kind: trend
trend_doc_id: 1665
granularity: day
period_start: '2026-06-28T00:00:00'
period_end: '2026-06-29T00:00:00'
topics:
- AI agents
- credential security
- coding agents
- agent workspaces
- model routing
- software economics
run_id: materialize-outputs
aliases:
- recoleta-trend-1665
tags:
- recoleta/trend
- topic/ai-agents
- topic/credential-security
- topic/coding-agents
- topic/agent-workspaces
- topic/model-routing
- topic/software-economics
language_code: zh-CN
---

# 代理产品正在围绕有边界的访问和可见监督展开

## Overview
今天的语料把代理视为运营工具，它们需要更安全的凭据、更清晰的工作界面和更严格的监督。DevFortress 提供了最强的风险证据；Iris 和 Notion 展示了产品模式：把小而有边界的工作分配给代理，同时让审查和权限保持可见。

## Clusters

### 代理执行的凭据安全
最高风险项是凭据暴露。DevFortress 文章认为，代理、Model Context Protocol (MCP) 服务器、CI/CD 工具、IDE 插件和云集成通常靠近可复用的密钥运行。文中引用的事件数据很具体：2025 年公共 GitHub 上暴露了 28,649,024 个新密钥，2022 年泄露的凭据中有 64% 到 2026 年 1 月仍处于活动状态，MCP 配置文件中发现了 24,008 个唯一密钥。

提出的控制措施是凭据别名化。代理和集成拿到别名，真实凭据留在受控基础设施中。产品声明包括会话监控、限定范围的凭据、签名载荷、防重放检查，以及两秒内隔离或撤销。事件规模方面的证据很强，但摘录中没有该产品本身的第三方基准、误报率或延迟分布。

#### Evidence
- [AI Agent Credential Crisis: Six Months of Incidents](../Inbox/2026-06-28--ai-agent-credential-crisis-six-months-of-incidents.md): 摘要给出了凭据别名化方案、事件指标、MCP 密钥数量，以及评估证据的限制。

### 团队工具中的代理工作
两篇材料都把代理放进现有协作界面中，作为可分配任务的同事。CrewAI 的 Iris 通过 Slack 工作：工程师标记 `@Iris`，代理可以创建 Linear issue、运行 Claude Code、打开 GitHub pull request，并在线程中回报结果。具体例子很小但有用：一个两行的空白字符修复原本需要九个手动步骤，最后约三分钟完成，并为报告的换行问题添加了测试。

Notion 的 /Dev 产品在工作区层面采用同一思路。用户可以在页面、评论或聊天中 @mention 代理。Notion Workers 在 Notion 管理的基础设施上运行隔离代码，用于同步、自定义工具、webhook 和外部 API 调用。产品声明集中在共享权限、审查点和代理可见的工作区数据；摘录没有给出可靠性或延迟数字。

#### Evidence
- [My coworker Iris isn't a person](../Inbox/2026-06-28--my-coworker-iris-isn-t-a-person.md): 摘要给出了 Iris 工作流、三分钟示例，以及缺少基准证据这一点。
- [/Dev/Notion](../Inbox/2026-06-28--dev-notion.md): 摘要描述了 Notion 代理、Workers、权限、审查流程，以及缺少定量结果。

### 编码代理的操作者控制
编码代理的使用正在围绕人的注意力来组织。Mux 是一个范围很窄的工具，面向在 tmux 中运行多个 Claude Code 会话的人。它读取 Claude Code 状态文件，将它们匹配到实时窗格，并打开一个 fzf 覆盖层，把等待中的会话排在工作中或空闲会话前面。有用的动作很直接：按 Enter 跳到被阻塞的会话。

The Usefulness of AI Agents 这篇文章通过个人使用经验得出类似的操作规则。作者称，当编码代理被限制在一两个文件内、编码前被要求说明计划，并且超过 100 行或多个文件的变更需要先过关时，结果更好。这个判断是定性的。代理帮助完成了较小的原型和设置工作；研究输出看起来连贯，但作为研究偏弱。

#### Evidence
- [Mux – A tmux overlay for managing Claude Code sessions](../Inbox/2026-06-28--mux-a-tmux-overlay-for-managing-claude-code-sessions.md): 摘要解释了 Mux 状态跟踪、排序覆盖层、一键跳转，以及缺少基准数据。
- [The Usefulness of AI Agents](../Inbox/2026-06-28--the-usefulness-of-ai-agents.md): 摘要给出了作者对编码代理的限制性规则，以及对代理实用性的定性评估。

### 模型充足条件下的路由和产品价值
Role-model 和 Comparative Advantage in Software 都把通用模型视为一种需要产品层约束的资源。Role-model 提出一种开放协议，按任务、能力、策略、模态、成本、本地性和观测到的端点行为来路由 AI 请求。它的 RouterDecision 记录所选端点、回退项、排除项和选择理由。摘录给出了设计和运行时声明，但没有路由质量或延迟测量。

Comparative Advantage in Software 给出了同一约束的商业版本。如果客户可以要求大型语言模型 (LLM) 创建工具，付费软件就需要更清楚的存在理由。文章指出两个杠杆：减少完成任务所需的 token，或通过持久状态、评估、类型化数据和纠错工作流提高正确性。餐厅运营提供了具体例子：自动化采购需要精确状态和审批，因为采购可能影响约 30% 的收入。

#### Evidence
- [Role-model: protocol for assigning the right AI model for the right job](../Inbox/2026-06-28--role-model-protocol-for-assigning-the-right-ai-model-for-the-right-job.md): 摘要说明了 Role-model 按任务和能力感知的路由协议、决策产物，以及缺少定量结果。
- [Comparative Advantage in Software](../Inbox/2026-06-28--comparative-advantage-in-software.md): 摘要给出了 token 成本和正确性论点、餐厅示例，以及 30% 收入这一声明。
