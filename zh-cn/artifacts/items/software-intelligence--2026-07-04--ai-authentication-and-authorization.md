---
source: hn
url: https://fusionauth.io/articles/ai/ai-authentication-authorization
published_at: '2026-07-04T23:10:55'
authors:
- mooreds
topics:
- ai-authentication
- authorization
- rag-security
- mcp
- agent-security
- identity-management
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# AI Authentication and Authorization

## Summary
## 摘要
文章认为，AI 系统应从人类身份继承权限，并用确定性检查执行访问控制。文章通过一个银行支持场景，讨论了 RAG、通过 MCP 或 API 访问工具，以及多代理工作流。

## 问题
- 如果检索在访问检查运行前把未授权的文本块发送给模型，RAG 系统可能泄露受限文档。
- AI 工具和代理可以更新记录、读取文件、调用外部服务和安排会议，因此每个操作都需要明确的用户、代理身份、权限和审计记录。
- 仅靠提示词做访问控制并不安全，因为模型可能产生幻觉或临场编造，而身份层必须返回固定的是或否决策。

## 方法
- 通过身份提供商认证人类用户，然后把用户声明带入 RAG、工具和代理请求。
- 对 RAG，在文档块上存储访问元数据，运行向量检索，通过细粒度授权过滤结果，并且只把已授权的文本块发送给 LLM。
- 对工具，使用带 OAuth 2.1 授权码流程的 MCP，或使用带访问令牌、API 密钥和网关控制的现有 API。
- 对代理，给每个代理分配自己的身份，把工作拆分给权限范围有限的子代理，并使用带委托声明的已签名 JWT 来保留从人类到代理的身份链。
- 使用审计日志、短期凭证、实体授权，并清理特定工作流的代理实体，以减少过期访问权限。

## 结果
- 文章没有提供基准评估、准确率指标、延迟数字、安全测试结果或生产事故对比。
- 文章围绕 3 个 AI 用例组织指导内容：RAG、通过 MCP 或 API 使用工具，以及代理系统。
- 代理示例把一个银行工作流拆分为 4 个代理：协调代理、文档代理、业务服务代理和日历代理。
- JWT 示例使用 300 秒的令牌生命周期，并使用与 RFC 8693 中 OAuth Token Exchange 语义一致的 `act` 声明。
- 审计日志示例记录了一个具体操作：文档代理从一个文件夹收集了 4 份文档，并记录 actor、delegator、human user、role 和 scope 字段。

## Problem

## Approach

## Results

## Link
- [https://fusionauth.io/articles/ai/ai-authentication-authorization](https://fusionauth.io/articles/ai/ai-authentication-authorization)
