---
source: hn
url: https://news.ycombinator.com/item?id=47226046
published_at: '2026-03-02T23:59:47'
authors:
- iamalizaidi
topics:
- adr-enforcement
- github-action
- code-review
- architecture-governance
- developer-workflow
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# Spotify's take on ADRs is great, but how do you enforce them at scale?

## Summary
这是一款将架构决策记录（ADR）在拉取请求阶段自动“贴脸提示”的开源工具，通过 GitHub Action/CLI 在代码触及受保护文件时自动展示相关决策。它试图解决 ADR 写了但在真正改代码时没人看的执行落地问题。

## Problem
- 团队虽然编写了 ADR，但它们通常沉睡在 `docs/adr/` 中，开发者在提交 PR 前往往不会主动查阅。
- 真正需要看到架构决策的时机，不是在入职培训或规划会议，而是在有人修改受这些决策约束的代码时。
- 仅靠 `CODEOWNERS` 只能指定评审人，不能解释“为什么这里必须这样改”，因此难以把架构约束嵌入日常开发流程。

## Approach
- 使用兼容现有 ADR 的纯 Markdown 格式编写决策，并在其中声明状态、严重级别以及受保护文件范围。
- 通过 GitHub Action 或 CLI 在 CI 中检测 PR 改动；一旦修改命中规则，就自动把对应 ADR 作为评论发布到 PR。
- 规则匹配支持 glob、正则、基于内容的规则和布尔逻辑，以便把“代码变更”映射到“应被提醒的架构决策”。
- 对严重级别进行分层（Critical / Warning / Info）；关键级别可用于阻塞 PR，从“提醒”升级到“强制执行”。
- 工具强调工程可落地性：可在 GitHub 之外通过 CLI 接入 GitLab/Jenkins/CircleCI/pre-commit，且无外部网络调用。

## Results
- 文本未提供标准基准数据、离线评测或对照实验结果，因此**没有量化研究指标**可报告。
- 工程性声明包括：可处理 **3000+ files** 的 PR 而不会 OOM。
- 质量与安全声明包括：包含 **109 tests**，并具备 **ReDoS protection** 与 **path traversal protection**。
- 功能性对比声明：相较 `CODEOWNERS`，它不仅分配评审，还解释相关架构原因；相较 `Danger.js`，它不要求写代码，使用 Markdown 即可维护决策。
- 部署与采用声明：工具为 **MIT licensed**，支持单步 GitHub Action 或 `npx decision-guardian` CLI，定位为低接入成本的 ADR 执行方案。

## Link
- [https://news.ycombinator.com/item?id=47226046](https://news.ycombinator.com/item?id=47226046)
