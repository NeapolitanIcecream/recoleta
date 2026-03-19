---
source: hn
url: https://thenewstack.io/risk-mitigation-agentic-ai/
published_at: '2026-03-12T22:58:27'
authors:
- chhum
topics:
- agentic-ai
- api-testing
- contract-testing
- mocking-sandbox
- enterprise-ai-risk
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Before you let AI agents loose, you'd better know what they're capable of

## Summary
这篇文章讨论企业在部署自治型 AI agent 之前，必须先清楚其真实能力与风险边界。核心观点是：通过**契约驱动的测试、共享 mock/sandbox 和可观测性**，在生产前验证 agent 会做什么，从而降低失控、注入攻击和不可逆操作风险。

## Problem
- 企业级 agent 不只是生成文本，还会**浏览网页、调用 API、执行代码、修改文件**，早期错误可能级联放大，且事后难以审计“做了什么、何时做、为何做”。
- agent 消费外部网页、邮件、文档时，容易遭受**prompt injection**，在接入内部系统后可能导致**数据外泄、权限升级、破坏性操作**。
- 由于 agentic AI 仍很新，企业缺少成熟最佳实践；如果没有能力目录、沙箱和测试反馈环，组织就**不知道 agent 实际能做什么**，也无法安全放权。

## Approach
- 核心方法是把**“行为当作规范”**：不要只看设计意图，而要在生产前通过测试观察系统真实行为，验证 agent 在工具链中的实际动作模式。
- 采用**contract-first** 思路：用 OpenAPI 等正式规范定义 API 能力，再基于规范自动生成 mock endpoint，让 agent 先在**安全 sandbox** 中与真实结构一致的接口交互。
- 用 **Microcks + OpenAPI + Bruno** 等开源工具维护**共享、版本化的示例数据**和 mock，使 API 提供方、使用方、测试方围绕同一契约协作，避免 mock 与真实服务漂移。
- 通过**契约测试**持续对真实端点发请求，检查是否仍符合契约、是否破坏向后兼容；做到从 synthetic mock 切换到 production 时，接口结构仍稳定一致。
- 进一步把 mock API 暴露成 **MCP tool**，让 LLM/agent 在受控环境中调用工具，先理解企业 API 菜单与能力边界，再逐步过渡到生产使用。

## Results
- **BNP Paribas**：法国零售银行业务线中 **32 个 squad**、**500+ 开发与测试人员** 使用 Microcks，平台每周处理 **250 万+ API 调用**。
- 在 BNP 案例中，通过对主机系统后端 API 做 mock，使团队并行开发与测试，**开发和测试周期缩短了三分之二（约 66%）**。
- 大型采用者（如 **Amadeus**）据称通过前移 mocking 与 contract testing 获得了**显著开发速度提升**，但文中未提供更细粒度对比数字。
- Microcks 的轻量本地二进制启动时间**低于 200 毫秒**，并提供 Java、Node、Go、.NET 的 Testcontainers 绑定，用于在本地运行完整集成测试。
- 文中没有给出 agent 安全性的标准化 benchmark 分数；最强的具体主张是：**共享 sandbox + 契约测试** 能降低因不真实 mock、依赖耦合和生产直连导致的风险，并让团队在真实上线前理解 agent 能力边界。

## Link
- [https://thenewstack.io/risk-mitigation-agentic-ai/](https://thenewstack.io/risk-mitigation-agentic-ai/)
