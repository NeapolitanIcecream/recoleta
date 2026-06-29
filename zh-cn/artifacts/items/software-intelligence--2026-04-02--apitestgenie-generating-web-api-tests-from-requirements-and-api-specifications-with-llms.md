---
source: arxiv
url: http://arxiv.org/abs/2604.02039v1
published_at: '2026-04-02T13:43:56'
authors:
- "Andr\xE9 Pereira"
- Bruno Lima
- "Jo\xE3o Pascoal Faria"
topics:
- llm-test-generation
- api-testing
- openapi
- requirements-to-code
- retrieval-augmented-generation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# APITestGenie: Generating Web API Tests from Requirements and API Specifications with LLMs

## Summary
## 摘要
APITestGenie 根据自然语言业务需求和 OpenAPI 规范生成可执行的 Web API 集成测试。论文表明，这种以需求为驱动的设置可以为大多数评估需求产出有效测试，也包括大型工业 API。

## 问题
- 编写 API 集成测试和验收测试仍然主要依赖人工，过程缓慢且容易出错，尤其是在预期行为由业务需求而不是底层 API 调用来描述时。
- 现有 API 测试工具往往只基于 OpenAPI，因此缺少需求上下文，也难以生成能够检查跨多个端点的业务行为的测试。
- 对依赖大量 API 且需要测试随频繁变更和部署同步更新的现代系统来说，这个问题很重要。

## 方法
- APITestGenie 接收两个输入：用自然语言写成的业务需求和 API 的 OpenAPI 规范，然后让 LLM 生成可直接运行的 TypeScript 测试，使用 Axios 和 Jest。
- 系统使用结构化提示词，包含任务上下文、输出质量标准，以及要求的输出格式，格式中包括需求解析、端点选择和可执行测试代码。
- 对于大型 API 规范，系统会预处理 OpenAPI 文件，将其拆分为多个块，把这些块嵌入向量数据库，把需求扩展为相关查询，再用 RAG 检索最相关的块。
- 工作流包含三个模块：测试生成、基于先前执行反馈的可选测试改进，以及在 Jest/TypeScript 环境中执行测试。
- 评估使用 GPT-4-Turbo，每个业务需求进行三次生成尝试，然后执行脚本并手动检查语义有效性。

## 结果
- 在 10 个真实世界 API 和 25 条业务需求上进行评估，共有 75 次生成尝试；其中 8 个 API 来自汽车行业合作伙伴，覆盖约 1,000 个在线端点。
- APITestGenie 在 75 次尝试中生成了 52 个有效测试脚本，单次尝试成功率为 69.3%。
- 25 条业务需求中有 22 条在三次尝试内至少生成了一个有效脚本，需求级成功率为 88.6%；摘要将其四舍五入为 89%。
- 低复杂度 API 在 24 次尝试中得到 21 个有效脚本，成功率为 87.5%，8 条中的 8 条需求都至少生成了一个有效脚本。高复杂度 API 在 51 次尝试中得到 31 个有效脚本，成功率为 60.8%，17 条需求中有 14 条至少生成了一个有效脚本。
- 平均生成时间为 126 秒，平均每次生成成本为 €0.37。
- 在 52 个有效脚本中，31 个通过，12 个暴露出 API 缺陷，2 个因为文档不足而失败，7 个因为环境配置问题而失败。论文指出，部分生成测试发现了此前未知的缺陷，包括跨端点集成问题。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02039v1](http://arxiv.org/abs/2604.02039v1)
