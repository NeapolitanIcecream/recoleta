---
source: hn
url: https://www.sepo.sh/
published_at: '2026-07-19T22:40:04'
authors:
- liangqiyao99
topics:
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
- agent-memory
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Self-evolving repo for team and coding agent collaboration

## Summary
## 总结
Sepo 将 GitHub 仓库转变为一个结构化工作空间，让编码代理能够回答问题、实施变更、审查拉取请求，并在人类监督下持续迭代。它的主要贡献是持久且可追踪的代理工作记录，以及结合项目特定规则与记忆的工作方式。

## 问题
- 在长期任务中，编码代理的工作可能难以追踪、验证，也难以在人类与代理之间协调。
- 团队需要一份共享记录，保存请求、决策、审查和代码变更，以便后续代理运行能够利用项目上下文，而不是重复之前的工作。

## 方法
- 用户在 GitHub issue、拉取请求或讨论中提及 `@sepo-agent`；代理会在线程中回复，并将工作记录为相互关联的 issue、拉取请求和评论。
- `/implement`、`/review`、`/fix-pr` 和 `/orchestrate` 等命令支持实施、基于规则的审查、修复，以及反复执行的实施—审查—修复循环。
- 系统将代理工作存储在 `agent/memory` 分支中，从讨论和审查中提炼项目规则，并使用这些规则指导后续实施。
- 大型任务可以拆分为子 issue；定时任务可以检查仓库并提出改进建议，之后由人类审查并批准合并。

## 结果
- 所提供材料没有报告定量基准、准确率指标、任务完成率、延迟评估，也没有与其他编码代理系统进行比较。
- 材料给出了具体的工作流描述：单个 issue 可以触发实施—审查—修复循环，大型 issue 可以拆分为多个子 issue，代理变更则以 GitHub issue 和拉取请求的形式保持有序。
- 设置过程被描述为 3 个步骤：创建或安装仓库模板，安装 GitHub App 并添加模型凭据，然后在 issue 中提及代理。
- 示例审查在检查规则项目和测试时发现了缺失的重试保护措施，但摘录没有说明生成的代码是否通过了独立评估。

## Problem

## Approach

## Results

## Link
- [https://www.sepo.sh/](https://www.sepo.sh/)
