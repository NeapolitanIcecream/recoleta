---
source: hn
url: https://www.custodianlabs.io
published_at: '2026-07-19T22:57:48'
authors:
- sherryf123
topics:
- ai-agents
- code-intelligence
- automated-software-production
- privacy-preserving-ai
- retrieval-augmented-generation
- model-agnostic-infrastructure
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Deploy AI agent in 5 lines of code

## Summary
## 摘要
Custodian Labs 是一个用于部署生产级 AI 智能体的平台，内置 PII 控制、检索、模型切换和托管基础设施。其主要价值在于减少配置工作，同时让敏感数据处于应用控制之下。

## 问题
- 部署智能体通常需要先完成托管、数据库、向量搜索、模型提供商集成、重试逻辑和流式传输支持，之后才能编写应用逻辑。
- 将原始 PII 发送给外部模型会带来隐私和合规风险，而移除 PII 可能削弱上下文和响应质量。

## 方法
- 该平台将部署流程简化为 SDK 和 API 密钥工作流，并声称智能体可以在不到 10 分钟内投入生产环境，且只需五行代码。
- 其 Guardian Layer 可检测已配置的 PII 实体、报告置信度分数，并支持三种策略：将 PII 转换为保持语义的合成等价内容、用带类型标签进行屏蔽，或仅进行检测而不修改文本。
- 通过一行知识库配置，平台可提供检索增强生成和持久化文档记忆，无需直接配置嵌入或向量数据库。
- 在 OpenAI、Anthropic、Mistral 和本地模型之间切换时，智能体逻辑保持不变；Custodian 还对托管和数据库基础设施进行了抽象。

## 结果
- 摘录未报告独立基准测试、准确率测量、延迟结果或基线比较。
- 产品声称部署耗时不到 10 分钟、实现只需五行代码，但未提供可复现的测试条件。
- 文档所述的入门套餐包括 100,000 个 token 和 1,000 次请求；更高档的入门套餐包括 1 million 个 token 和 10,000 次请求。
- 最具体且有力的产品声明是：PII 可以在到达模型之前得到处理，同时通过合成替换、屏蔽或仅检测模式保留上下文。
- 平台表示，其基础技术由 AUT Ventures 和新西兰政府资金支持实现商业化，但摘录未提供相关学术研究的具体信息。

## Problem

## Approach

## Results

## Link
- [https://www.custodianlabs.io](https://www.custodianlabs.io)
