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
APITestGenie根据自然语言业务需求和OpenAPI规范生成可执行的Web API集成测试。论文显示，这种由需求驱动的方法可以为大多数评估过的需求生成有效测试，包括大型工业API。

## 问题
- 编写API集成测试和验收测试仍然主要依赖人工，速度慢且容易出错，尤其是在预期行为由业务需求描述、而不是由底层API调用描述时。
- 现有API测试工具通常只基于OpenAPI工作，因此缺少需求上下文，也难以生成能够跨多个端点检查业务行为的测试。
- 这对依赖大量API的现代系统很重要，因为这类系统需要能够跟上频繁变更和部署节奏的测试。

## 方法
- APITestGenie接收两个输入：自然语言业务需求和API的OpenAPI规范，然后让LLM使用Axios和Jest生成可直接运行的TypeScript测试。
- 系统使用结构化提示，包含任务上下文、输出质量标准，以及必需的输出格式；该格式包括需求解释、端点选择和可执行测试代码。
- 对于大型API规范，系统会先预处理OpenAPI文件，将其拆分为多个片段，嵌入向量数据库，把需求扩展为相关查询，并通过RAG检索最相关的片段。
- 该流程包含三个模块：测试生成、基于先前执行反馈的可选测试改进，以及在Jest/TypeScript环境中的测试执行。
- 评估使用GPT-4-Turbo，对每条业务需求最多进行三次生成尝试，然后执行脚本并人工检查其语义有效性。

## 结果
- 评估覆盖10个真实世界API和25条业务需求，共进行了75次生成尝试；其中8个API来自汽车行业合作伙伴，覆盖约1,000个在线端点。
- APITestGenie在75次尝试中生成了52个有效测试脚本，对应单次尝试成功率69.3%。
- 在25条业务需求中，有22条在三次尝试内至少得到一个有效脚本，对应需求层面的成功率88.6%；摘要中将其四舍五入为89%。
- 低复杂度API在24次尝试中得到21个有效脚本，即87.5%；8条需求全部至少得到一个有效脚本。高复杂度API在51次尝试中得到31个有效脚本，即60.8%；17条需求中有14条至少得到一个有效脚本。
- 平均生成时间为126秒，平均每次生成成本为0.37欧元。
- 在52个有效脚本中，31个通过，12个暴露出API缺陷，2个因文档信息不足而失败，7个因环境配置问题而失败。论文指出，一些生成的测试发现了此前未知的缺陷，包括跨端点的集成问题。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02039v1](http://arxiv.org/abs/2604.02039v1)
