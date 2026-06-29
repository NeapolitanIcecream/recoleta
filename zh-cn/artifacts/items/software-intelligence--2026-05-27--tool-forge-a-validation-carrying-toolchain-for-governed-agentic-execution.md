---
source: arxiv
url: https://arxiv.org/abs/2605.28000v1
published_at: '2026-05-27T05:45:58'
authors:
- Swanand Rao
topics:
- agentic-tooling
- mcp
- tool-routing
- code-generation
- software-governance
- multi-agent-software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Tool Forge: A Validation-Carrying Toolchain for Governed Agentic Execution

## Summary
## 摘要
Tool Forge 是一个开源工具链，用于把自然语言的工具请求转成经过验证的智能体工具，并通过 MCP 以更少的模式上下文路由这些工具。

## 问题
- 智能体需要工具来调用 API、编辑文件和运行工作流，但生成的工具可能缺少验证、依赖配置有误、测试薄弱，或凭据需求不清楚。
- 当模型上下文里加载每个完整 schema 时，工具目录越大，token 成本和选择噪声就越高。
- 这对生产环境中的智能体系统很重要，因为工具执行会影响安全性、可靠性、可审计性、延迟和成本。

## 方法
- Tool Forge 把每个工具看作一个胶囊，里面包含意图、契约、代码、依赖、测试、文档、验证证据、生命周期状态、凭据和路由元数据。
- 生成流程会把意图转换为能力契约，在有文档时用文档来约束 API 细节，生成代码或工具包，应用确定性的脚手架，运行审查和测试，然后在沙箱里验证执行结果。
- Router 提供一组精简的 MCP 接口，用于搜索、解析、描述、调用和列出配置文件，然后只为选中的工具加载完整 schema。
- 治理配置会按审批状态、凭据映射、租户、生命周期状态和任务会话来过滤工具。

## 结果
- Router 基准测试：83 个用例，覆盖 lite、realistic 和 adversarial 套件；总体 micro-F1 为 0.908。
- Token 暴露：与朴素的全目录 schema 暴露相比，估计的任务流工具上下文减少了 99.49%。
- 端到端生成探针：在 L1 smoke、L2 realistic 和 L3 adversarial 本地工具任务中，25 个请求的工具包全部生成成功。
- 工件模式评分：相对确定性接受模式，micro-F1 为 0.940。
- 现场沙箱验证：25 个生成的工具里有 23 个通过。
- 报告的失败包括否定处理、语义上容易混淆的工具和边界情况验证；作者把这个基准结果描述为一个早期的开源系统结果，而不是与当前最先进方法的比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28000v1](https://arxiv.org/abs/2605.28000v1)
