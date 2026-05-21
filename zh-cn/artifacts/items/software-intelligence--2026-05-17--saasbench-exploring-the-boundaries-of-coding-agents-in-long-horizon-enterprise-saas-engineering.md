---
source: arxiv
url: https://arxiv.org/abs/2605.17526v1
published_at: '2026-05-17T16:15:56'
authors:
- Qingnan Ren
- Shun Zou
- Shiting Huang
- Ziao Zhang
- Kou Shi
- Zhen Fang
- Yiming Zhao
- Yu Zeng
- Qisheng Su
- Lin Chen
- Yong Wang
- Zehui Chen
- Xiangxiang Chu
- Feng Zhao
topics:
- coding-agents
- software-engineering-benchmark
- saas-development
- full-stack-generation
- agent-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering

## Summary
## 摘要
SaaSBench 测试编码代理能否根据较长的产品需求构建可部署的企业 SaaS 系统。论文发现，当前代理经常在环境搭建、配置和跨组件集成上失败；报告的最佳 Pass@1 为 20.68%。

## 问题
- 现有编码基准主要关注代码片段、仓库编辑或简单项目生成，因此漏掉了企业 SaaS 工作的复杂性。
- 真实 SaaS 产品需要前端、后端、数据库、身份认证、部署和业务流程协同工作；某一层失败可能阻塞其余部分。
- 扁平的单元测试或端到端评分可能过度惩罚下游失败，也可能看不出具体失败的是哪项工程能力。

## 方法
- SaaSBench 包含 30 个任务，覆盖 6 个 SaaS 领域，基于真实开源 SaaS 仓库和有市场依据的产品类别构建。
- 每个任务包含一份较长的 PRD、一个歧义消解知识库、标准化 Docker 运行环境和基于 DAG 的测试套件。
- 该基准的 PRD 平均有 4,362.7 行，包含 5,370 个可执行验证节点、6,167 条前置依赖边、8 种编程语言、6 种数据库类型和 13 个前端/后端框架。
- 评估按依赖顺序运行验证节点，并将被阻塞的检查标记为 skipped dependency，而不是直接失败。
- 评分使用二元检查、加权部分得分检查，以及针对页面布局质量等情况的 LLM-as-judge 检查。

## 结果
- 总体最佳结果来自使用 Claude Opus 4.7 的 Claude Code：SaaSBench 上 Pass@1 为 20.68%，节点覆盖率为 18.50%。
- OpenHands 的最佳结果来自 Claude Opus 4.7：Pass@1 为 18.12%，节点覆盖率为 18.24%。
- 在不同代理后端中，Claude Code 的平均 Pass@1 为 11.64%，OpenHands 的平均 Pass@1 为 9.26%。
- 在 Claude Code 下，Claude Opus 4.7 之后结果最强的是 GLM 5.1，Pass@1 为 13.60%；DeepSeek V4 Pro 次之，Pass@1 为 13.19%。
- 在 OpenHands 下，Claude Opus 4.7 之后结果最强的是 DeepSeek V4 Pro，Pass@1 为 10.97%；GLM 5.1 次之，Pass@1 为 10.23%。
- 论文报告称，超过 95% 的任务失败发生在代理进入深层业务逻辑之前，主要出现在系统搭建、集成、过早停止或重复调试循环期间。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17526v1](https://arxiv.org/abs/2605.17526v1)
