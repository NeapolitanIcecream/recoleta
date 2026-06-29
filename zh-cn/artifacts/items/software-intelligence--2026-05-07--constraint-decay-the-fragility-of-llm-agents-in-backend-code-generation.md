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
## 总结
论文表明，当后端代码必须遵守数据库、ORM 和架构要求时，LLM 编码代理的失败率会高得多。核心结果是作者测得的“约束衰减”效应：能力较强的代理从宽松任务到完全指定任务，断言通过率平均下降约 30 个百分点。

## 问题
- 生产环境中的后端既要符合 API 合约，也要遵守结构性规则，包括分层代码、指定数据库和必需的 ORM。
- 许多代码生成基准只看功能是否可用，忽略代码是否符合这些结构性规则。
- 这对软件工程代理很重要，因为生成的服务即使能通过简单功能检查，仍然可能难以维护、集成或部署。

## 方法
- 作者固定了一个基于 RealWorld Conduit API 的 OpenAPI 3.0 合约：涵盖 articles、comments、users、profiles 和 tags 的 19 个端点。
- 他们在 8 个 Web 框架上创建了 80 个全新后端生成任务：Flask、FastAPI、Django、aiohttp、Express、Fastify、Hono 和 Koa。
- 他们按 L0 到 L3 四个层级变化结构约束：只要求 Web 框架，然后加入 Clean Architecture、SQLite 或 PostgreSQL，以及使用 SQLAlchemy 或 Sequelize 的 ORM。
- 他们用一套共享的 HTTP 行为测试集评估生成的服务，这套测试包含 32 个请求和 291 个断言，然后用静态验证器检查架构、数据库和 ORM 的合规性。
- 他们测试了 Mini-SWE-Agent 和 OpenHands，所用模型包括 GPT-5-mini、GPT-5.2、Qwen3-Coder-Next、Qwen3-235B-A22B、MiniMax-M2.5 和 Kimi-K2.5。

## 结果
- 在 L0 的 A% 高于 50 的能力较强配置中，断言通过率从 L0 到 L3 下降约 30 个百分点，相当于相对基线性能损失 40%。
- OpenHands + Qwen3-Coder-Next 的下降幅度最大：L0 为 73.0 A%，L3 为 27.6 A%，下降 45.5 个百分点。OpenHands + MiniMax-M2.5 是报告中最强的 L3 配置：L3 达到 78.6 A%，但 pass@1 只有 8.3%。
- 数据库要求带来最大的边际损失：PostgreSQL 使 A% 下降 19.3 ± 2.5 个点，SQLite 下降 14.3 ± 2.5 个点。Clean Architecture 使 A% 下降 9.1 ± 1.6 个点。
- 在配对分析中，ORM 要求带来的边际损失很小：SQLAlchemy 使 A% 下降 1.5 ± 2.1 个点，Sequelize 下降 0.6 ± 2.2 个点。
- 论文报告称，验证器强制检查对任何单个 A% 分数的影响最多只有 2.7 个点，所以这种衰减主要来自行为失败，而不是静态检查惩罚。
- 在基于现有 RealWorld 仓库的 20 个功能实现任务中，pass@1 仍然很低：GPT-5.2 在 Mini-SWE-Agent 下达到 50.0%，在 OpenHands 下达到 55.0%；GPT-5-mini 分别为 15.0% 和 48.3%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06445v1](https://arxiv.org/abs/2605.06445v1)
