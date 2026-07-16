---
kind: trend
trend_doc_id: 1870
granularity: day
period_start: '2026-07-12T00:00:00'
period_end: '2026-07-13T00:00:00'
topics:
- coding agents
- model routing
- security review
- agent memory
- local AI
run_id: materialize-outputs
aliases:
- recoleta-trend-1870
tags:
- recoleta/trend
- topic/coding-agents
- topic/model-routing
- topic/security-review
- topic/agent-memory
- topic/local-ai
language_code: zh-CN
---

# 代理产品正成为运营系统，但证据仍然有限

## 概览
代理产品正被设计成受控的运营系统。OneDev 将编码工作固定在议题、拉取请求和持续集成（CI）中；Avriz 通过影子测试和流量上限控制学习型模型路由；Mango 将记忆和权限保存在用户设备上。实测证据并不均衡。最强的基准测试也只覆盖 10 个合成拉取请求，而大多数产品声明缺乏比较评估。

## 研究发现

### 受监督的编码工作流
OneDev 将代理置于现有的软件流程中：议题保存需求，隔离工作区承载执行过程，关联的拉取请求记录评审和 CI 结果。这种设计让代理的工作可检查，也能在构建失败后触发修改。文章没有提供实测评估。

代码生成速度提高后，人工评审负担也会增加。一篇为期三个月的第一人称记录称，原型可在数小时内完成，但开发者仍需持续做架构决策，承受 mental fatigue，并且难以还原生成代码为何采用特定形式。这些报告共同表明，评审能力和决策节奏会限制编码代理的处理能力。

#### 资料来源
- [OneDev AI: Coding Agents as Teammates in Issues, Pull Requests, and CI](../Inbox/2026-07-12--onedev-ai-coding-agents-as-teammates-in-issues-pull-requests-and-ci.md): 概述 OneDev 从议题到拉取请求的工作流、受控工作区、CI 反馈，以及缺乏量化评估的情况。
- [The cost of AI-assisted development: cognitive fatigue](../Inbox/2026-07-12--the-cost-of-ai-assisted-development-cognitive-fatigue.md): 报告更快的原型开发、架构层面的疲劳、评审盲点，以及缺乏受控证据的情况。

### 成本感知的模型选择
模型选择正逐渐成为针对具体工作负载的运行决策。Dam Secure 在 10 个合成拉取请求上测试了 10 个模型，这些请求中植入了访问控制缺陷，并对每个模型重复测试 5 次。GPT-5.6 Sol 的召回率为 100%，F1 为 0.91，每个拉取请求的成本为 $0.70。Grok 4.5 的 F1 为 0.77，成本为 $0.20；Gemini 3.1 Flash Lite 的 F1 为 0.75，成本约为 $0.04。数据集规模小且为私有数据，限制了更广泛的结论，尤其是对完整代码扫描的结论。

Avriz 在实时使用编码代理时处理同一成本问题。它的上下文赌博机使用 11 个不含内容的特征和从计费数据得到的奖励，在 5 个模型层级之间进行选择。学习得到的路由在通过覆盖率门槛前保持影子模式，之后也只能在模型层级上限下获得受限的流量比例。报告提供了实现细节，但没有报告总体节省或质量提升。

#### 资料来源
- [Grok 4.5 and GPT5.6 beat Anthropic for finding security vulnerabilities in PRs](../Inbox/2026-07-12--grok-4-5-and-gpt5-6-beat-anthropic-for-finding-security-vulnerabilities-in-prs.md): 提供基准测试设计、工作负载范围、召回率、F1 和成本结果。
- [We taught our platform to learn its own pricing decisions](../Inbox/2026-07-12--we-taught-our-platform-to-learn-its-own-pricing-decisions.md): 详细说明 Avriz 的特征、五层学习器、延迟奖励、部署门槛，以及缺失的总体结果。

### 代理记忆与用户控制
持久化上下文正被视为一种带有明确所有权规则的数据。Mango 提议采用本地执行、纯文本记忆、可替换模型，以及由客户端确定性控制的权限，用于跨已登录服务执行操作。xysq 面向使用团队的隔离保险库，这些保险库从 Slack、Drive、Notion 和其他工具收集上下文；访问需要获得同意，并支持加密、导出和删除。

这些设计说明了记忆存储在哪里，以及谁有权批准使用记忆。它们的证据来自架构说明和产品宣传。Mango 没有受控安全审计，xysq 也没有提供部署指标、检索评估或对其隐私声明的独立验证。

#### 资料来源
- [A Technology for Free Will](../Inbox/2026-07-12--a-technology-for-free-will.md): 概述 Mango 的本地执行、可移植记忆、模型选择、客户端安全措施、示例和评估缺口。
- [Show HN: Collaborative context-sharing memory platform for agents and teams](../Inbox/2026-07-12--show-hn-collaborative-context-sharing-memory-platform-for-agents-and-teams.md): 描述 xysq 的隔离团队保险库、同意控制、加密、导出和删除声明，以及缺乏指标的情况。
