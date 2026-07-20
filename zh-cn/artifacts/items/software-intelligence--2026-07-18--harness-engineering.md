---
source: hn
url: https://github.com/lopopolo/harness-engineering
published_at: '2026-07-18T23:27:36'
authors:
- handfuloflight
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- agent-network
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Harness Engineering

## Summary
## 摘要
Harness 工程通过固定模型和编码代理，同时塑造其上下文、工具、约束与反馈环境，来提升编码代理的表现。该仓库将其描述为一种最后一公里工程，用于让组织的要求和运营知识能够被代理使用。

## 问题
- 通用模型权重不包含组织不断变化的运营状态、本地术语、质量标准、流程、例外历史或权限关系。
- 代理可能在不了解可靠性、安全性、兼容性、可维护性、性能和运营风险等非功能性要求的情况下生成代码。
- 这很重要，因为代理需要组织上下文和结果验证机制，才能对真实系统做出可靠修改；在某些情况下，人们甚至不会直接审查实现代码。

## 方法
- 将模型和编码代理作为黑箱保持不变，然后改进上下文和工具这两个外部杠杆。
- 通过可检索的文档、示例、操作手册、可执行约束和验证检查，将组织要求与决策编码到仓库中。
- 使用 `AGENTS.md` 和论点索引等文件，将任务引导至相关指南、案例和验证流程。
- 将已接受的工作、修正、失败和用户反馈回馈到 harness 中，使后续代理运行能够继承不断积累的组织判断。
- 将部署视为最后一公里层，为代理提供上下文、能力、权限以及结果证据。

## 结果
- 摘录没有报告受控基准测试、数据集、指标或基线比较。
- 摘录声称，让代理接触作者积累的写作和媒体内容，可以使代理输出提升“100x”，但没有提供该数字的测量方法或实验依据。
- 证据最充分支持的是一个设计层面的判断：经过策划的 harness 可以将本地知识和反馈转化为可复用的上下文、工具、示例和检查，从而使组织在代理维护的各类成果中的一致性不断积累。

## Problem

## Approach

## Results

## Link
- [https://github.com/lopopolo/harness-engineering](https://github.com/lopopolo/harness-engineering)
