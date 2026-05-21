---
source: arxiv
url: https://arxiv.org/abs/2605.06445v1
published_at: '2026-05-07T15:44:40'
authors:
- Francesco Dente
- Dario Satriani
- Paolo Papotti
topics:
- software-foundation-models
- code-intelligence
- backend-code-generation
- llm-agents
- software-benchmarks
- multi-agent-software-engineering
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Constraint Decay: The Fragility of LLM Agents in Backend Code Generation

## Summary
## 摘要
这篇论文表明，当后端代码必须遵守数据库、ORM 和架构要求时，LLM 编码智能体的失败率会高得多。主要结果是测得一种“约束衰减”效应：从宽松任务到完全指定的任务，能力较强的智能体在断言通过率上下降约 30 个百分点。

## 问题
- 生产后端必须匹配 API 契约，也必须遵守结构规则，包括分层代码、指定数据库和指定 ORM。
- 许多代码生成基准奖励可运行的行为，却忽略代码是否符合这些结构规则。
- 这对软件工程智能体很重要，因为生成的服务可能通过简单功能检查，但仍然难以维护、集成或部署。

## 方法
- 作者固定一个基于 RealWorld Conduit API 的 OpenAPI 3.0 契约：覆盖 articles、comments、users、profiles 和 tags 的 19 个端点。
- 他们在 8 个 Web 框架上创建 80 个从零开始的后端生成任务：Flask、FastAPI、Django、aiohttp、Express、Fastify、Hono 和 Koa。
- 他们在 L0 到 L3 各层级改变结构约束：仅 Web 框架，然后加入 Clean Architecture、SQLite 或 PostgreSQL，以及使用 SQLAlchemy 或 Sequelize 的 ORM。
- 他们用一套共享的 HTTP 行为测试评估生成的服务，其中包含 32 个请求和 291 个断言；随后用静态验证器检查架构、数据库和 ORM 使用是否合规。
- 他们测试 Mini-SWE-Agent 和 OpenHands，使用的模型包括 GPT-5-mini、GPT-5.2、Qwen3-Coder-Next、Qwen3-235B-A22B、MiniMax-M2.5 和 Kimi-K2.5。

## 结果
- 在 L0 A% 高于 50 的较强配置中，从 L0 到 L3，断言通过率下降约 30 个百分点，相当于相对基线性能损失 40%。
- OpenHands + Qwen3-Coder-Next 报告的降幅最大：从 L0 的 73.0 A% 降至 L3 的 27.6 A%，下降 45.5 个百分点。OpenHands + MiniMax-M2.5 是报告中最强的 L3 配置：L3 达到 78.6 A%，但 pass@1 只有 8.3%。
- 数据库要求造成最大的边际损失：PostgreSQL 损失 19.3 ± 2.5 个 A% 点，SQLite 损失 14.3 ± 2.5 个点。Clean Architecture 损失 9.1 ± 1.6 个点。
- 在配对分析中，ORM 要求增加的边际损失很小：SQLAlchemy 损失 1.5 ± 2.1 个 A% 点，Sequelize 损失 0.6 ± 2.2 个点。
- 论文报告称，验证器强制执行最多只会让任一单独 A% 分数变化 2.7 个点，因此衰减主要来自行为失败，而非静态检查惩罚。
- 在现有 RealWorld 仓库上的 20 个功能实现任务中，pass@1 仍然较低：GPT-5.2 搭配 Mini-SWE-Agent 达到 50.0%，搭配 OpenHands 达到 55.0%；GPT-5-mini 分别达到 15.0% 和 48.3%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06445v1](https://arxiv.org/abs/2605.06445v1)
