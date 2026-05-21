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
Mono2Sls 将单体 Flask 和 Express 后端自动迁移为可部署的 AWS SAM 无服务器应用。它把静态代码分析与 4 个使用工具的 LLM 代理结合起来，分别规划架构、生成 Lambda 代码、编写 SAM 模板并检查一致性。

## 问题
- 将单体应用迁移到无服务器架构，需要在 API 路由、Lambda 边界、应用代码、IAM、DynamoDB、Cognito、SQS/EventBridge 和 SAM 模板之间做协调一致的修改。
- 手动迁移速度慢且容易出错，因为代码和基础设施之间的小不匹配就可能阻止部署，或破坏 API 行为。
- 通用代码助手通常缺少用于无服务器迁移的稳定跨产物契约，因此处理程序代码、路由、权限和模板资源可能相互偏离。

## 方法
- 静态分析将 HTTP 入口点、文件标签、跨文件调用边、异步提示和 DynamoDB 架构候选项提取到 `analysis_report.json`。
- Architect 代理将这些事实转换为 `blueprint.json`，把业务端点映射到 Lambda 函数，并在需要时选择 Cognito、同步 Lambda 调用、SQS 或 EventBridge。
- Code Developer 代理将 Flask/Express 处理程序重写为 Lambda 处理程序，将身份适配到 Cognito claims，移除全局状态，并添加用于 Lambda 间通信的 SDK 调用。
- SAM Engineer 代理生成 `template.yaml`，其中包含 DynamoDB、Cognito、API Gateway、Lambda、layer、queue 和 event 资源，然后通过验证工具运行 `cfn-lint`。
- Consistency Validator 在生成的代码、SAM 和蓝图之间运行 11 项跨产物检查，然后应用修复并重新验证。

## 结果
- 基准测试涵盖 6 个应用、10,478 行代码、76 个可观察业务端点、24 个 DynamoDB 表；6/6 个应用包含身份验证，4/6 个应用包含异步模式。
- Mono2Sls 报告称，在 6 个基准应用中无需手动修复即可达到 100% 部署成功率。
- 端到端正确率达到 66.1%，商业基线为 53.7% 至 61.2%。
- API 覆盖率 F1 达到 98.7%，商业基线为 88.4%。
- 消融研究报告称，静态分析引导的架构规划使端到端正确率提高 23.4 个百分点。
- 论文还称 AWS 原生身份验证和异步模式的使用更一致，但摘录未提供各模式的详细计数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24550v1](https://arxiv.org/abs/2604.24550v1)
