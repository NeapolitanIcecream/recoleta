---
source: hn
url: https://devarch.ai
published_at: '2026-06-01T23:22:35'
authors:
- ChicagoDave
topics:
- code-intelligence
- ai-coding-agents
- software-guardrails
- automated-testing
- domain-driven-design
- developer-workflow
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Without Intelligent Guardrails, Claude Code Is Pure Chaos

## Summary
## 摘要
DevArch 为 Claude Code 添加自动工程护栏，让 AI 辅助开发在跨会话时也能保留项目上下文、测试质量、架构决策和领域边界。

## 问题
- Claude Code 能让单个开发者更快推进工作，但摘要说，速度也会带来架构不一致、测试薄弱，以及跨会话的上下文丢失。
- 这个问题重要，因为使用 AI 代理的小团队仍然需要可长期保留的决策、清晰的模块边界，以及能证明真实行为而不是浅层检查的测试。
- 目标用户是领域专家、开发者或 QA 角色，他们想用 Claude Code 运行更多软件交付流程。

## 方法
- DevArch 通过 directives、agents、skills 和生命周期 hooks 接入 Claude Code，这些规则会自动运行，不需要开发者手动调用。
- 会话开始 hooks 恢复上下文，预会话审计暴露阻塞项，工作摘要记录状态，架构决策记录保留已批准的决策。
- 在实现前，系统会推动领域驱动设计工作，例如 bounded contexts、ubiquitous language、domain events、aggregates 和 value objects。
- 在编写副作用代码和跨边界状态修改之前，agents 会要求结构化声明，例如 owner、shared state status、promise、alternatives、behavior、timing、reason 和 rejection conditions。
- 测试检查会把基于行为推导的测试评为 RED、YELLOW 或 GREEN，并拒绝同义反复式断言、只做 mock 的检查，以及只验证返回值的测试。

## 结果
- 摘要没有给出基准测试、用户研究、缺陷率下降、吞吐量指标，也没有和原生 Claude Code 做比较。
- 它声称每个阶段都有工具调用预算告警，分别在 70%、90% 和 100% 触发。
- 它声称每个会话都有一个唯一的 6 位十六进制 ID，这样同一仓库里的并发 Claude Code 会话就不会在 gate 文件、预算跟踪或文件变更状态上冲突。
- 它声称 hooks 提供给 2 种 shell 环境，Bash 和 PowerShell，覆盖 Windows、macOS 和 Linux。
- 它声称每个重要决策都可以变成一条带有上下文、理由和后果的 ADR，但摘要没有给出这个流程的数量、采用率或质量指标。

## Problem

## Approach

## Results

## Link
- [https://devarch.ai](https://devarch.ai)
