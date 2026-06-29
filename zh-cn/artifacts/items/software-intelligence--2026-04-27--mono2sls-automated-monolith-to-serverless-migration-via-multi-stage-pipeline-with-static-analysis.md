---
source: arxiv
url: https://arxiv.org/abs/2604.24550v1
published_at: '2026-04-27T14:44:07'
authors:
- Xingyan Chen
- Yuxin Su
- Zishan Su
- Yang Yu
- Zibin Zheng
topics:
- serverless-migration
- code-intelligence
- multi-agent-systems
- software-modernization
- aws-sam
- static-analysis
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Mono2Sls: Automated Monolith-to-Serverless Migration via Multi-Stage Pipeline with Static Analysis

## Summary
## 摘要
Mono2Sls 将单体式 Flask 和 Express 后端自动迁移为可部署的 AWS SAM 无服务器应用。它把静态代码分析和四个使用工具的 LLM 代理结合起来，由这些代理负责架构规划、生成 Lambda 代码、编写 SAM 模板和检查一致性。

## 问题
- 将单体应用迁移到无服务器架构，需要在 API 路由、Lambda 边界、应用代码、IAM、DynamoDB、Cognito、SQS/EventBridge 和 SAM 模板之间同步修改。
- 人工迁移速度慢，也容易出错，因为代码和基础设施之间只要有一点不匹配，就可能阻止部署或破坏 API 行为。
- 通用代码助手通常缺少面向无服务器迁移的稳定跨工件约定，因此处理器代码、路由、权限和模板资源容易彼此脱节。

## 方法
- 静态分析提取 HTTP 入口点、文件标签、跨文件调用边、异步线索和 DynamoDB 模式候选项，写入 `analysis_report.json`。
- Architect 代理把这些事实转成 `blueprint.json`，将业务端点映射到 Lambda 函数，并在需要时选择 Cognito、同步 Lambda 调用、SQS 或 EventBridge。
- Code Developer 代理把 Flask/Express 处理器改写为 Lambda 处理器，将身份信息改为使用 Cognito 声明，移除全局状态，并为 Lambda 间通信添加 SDK 调用。
- SAM Engineer 代理生成 `template.yaml`，其中包含 DynamoDB、Cognito、API Gateway、Lambda、layer、queue 和 event 资源，然后通过验证工具运行 `cfn-lint`。
- Consistency Validator 在生成的代码、SAM 和 blueprint 之间执行 11 项跨工件检查，之后应用修复并重新验证。

## 结果
- 基准测试覆盖 6 个应用、10,478 行代码、76 个可观测业务端点、24 个 DynamoDB 表，6/6 个应用包含身份验证，4/6 个应用包含异步模式。
- Mono2Sls 在这 6 个基准应用上实现了 100% 的部署成功率，且无需人工修复。
- 端到端正确率达到 66.1%，商业基线为 53.7% 到 61.2%。
- API 覆盖率 F1 达到 98.7%，商业基线为 88.4%。
- 消融研究显示，静态分析引导的架构规划为端到端正确率带来 23.4 个百分点的提升。
- 论文还声称，这个系统对 AWS 原生身份验证和异步模式的使用更一致，但摘录没有给出各模式的详细计数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24550v1](https://arxiv.org/abs/2604.24550v1)
