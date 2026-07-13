---
source: hn
url: https://onedev.io/blogs/ai-teammates
published_at: '2026-07-12T23:44:18'
authors:
- timplant
topics:
- coding-agents
- software-engineering
- pull-request-automation
- ci-cd
- multi-agent-workflows
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# OneDev AI: Coding Agents as Teammates in Issues, Pull Requests, and CI

## Summary
## 摘要
OneDev AI 将编码代理嵌入议题、工作区、拉取请求和 CI/CD，使其能在团队现有工作流中实现、审查和修改软件。文章认为，这种连接式工作流可以改善可追溯性、控制能力和自动化，但没有提供实测评估。

## 问题
- 外部编码代理聊天会将需求、实现、审查和交付分开，导致上下文和责任更难保持连贯。
- 团队需要持久的规格说明、受控的执行环境和可重复的检查，让代理能够在没有临时指令的情况下处理软件开发。
- 这个问题很重要，因为 AI 生成的变更仍然需要审查、CI/CD 验证，以及记录变更原因的清晰记录。

## 方法
- 将议题作为事实来源，其中包含需求、验收标准、附件、评论和设计上下文。
- 让 AI 用户创建隔离工作区、检查代码仓库、在议题分支上修改代码，并打开关联的拉取请求。
- 将拉取请求审查与议题关联，使代理能够留下代码行评论、回应修改要求，并在 CI/CD 失败后修改代码。
- 使用项目规则将议题分配给代理、要求代理进行审查，并在规定的审查和 CI/CD 检查通过后允许自动合并。

## 结果
- 文章没有提供定量结果、基准分数、数据集或基线比较。
- 文章最具体的主张是，OneDev 将议题、Git 代码仓库、工作区、拉取请求、审查、软件包、代码搜索和 CI/CD 连接在一个端到端流程中。
- 代理可以实现分配给它们的议题、打开拉取请求、审查变更、回应反馈，并在构建失败后继续工作。
- 受控工作区和权限规则提供隔离的执行环境，并限制代理可以操作的位置。
- 关联议题会在实现和验收过程中保留原始需求及其讨论记录。

## Problem

## Approach

## Results

## Link
- [https://onedev.io/blogs/ai-teammates](https://onedev.io/blogs/ai-teammates)
