---
source: hn
url: https://news.ycombinator.com/item?id=47226046
published_at: '2026-03-02T23:59:47'
authors:
- iamalizaidi
topics:
- software-architecture
- adr-enforcement
- github-action
- code-review
- developer-tooling
relevance_score: 0.01
run_id: materialize-outputs
---

# Spotify's take on ADRs is great, but how do you enforce them at scale?

## Summary
这是一项面向工程团队的开源工具实践：通过在 PR 触及受保护文件时自动贴出相关 ADR，把“写过但没人看”的架构决策真正嵌入代码评审流程。核心价值不在新增文档，而在以最合适的时机主动呈现已有决策，从而提升架构约束执行力。

## Problem
- 团队即使按照 Spotify 的建议编写了 ADR，文件通常仍静置在 `docs/adr/` 中，开发者在开 PR 前不会主动查阅。
- 真正的缺口不是“缺少文档”，而是“缺少在改动相关代码时的即时决策提示”，导致架构约束难以在日常开发中被遵守。
- 现有替代方式如 CODEOWNERS 更偏向分配评审人，Danger.js 往往需要写代码规则；两者都没有直接用简洁 Markdown ADR 在评审时解释“为什么这样审”。

## Approach
- 用普通 Markdown 编写 ADR/决策文件，并在其中声明受保护文件范围、状态、严重级别等元数据，兼容已有 ADR 写法。
- 在 GitHub Action 或 CLI 中扫描 PR 改动；一旦命中文件匹配规则，就自动把相关决策作为 PR 评论贴出来。
- 规则匹配支持 glob、正则、基于内容的规则和布尔逻辑，因此不仅能按路径触发，也能按更复杂条件触发。
- 通过严重级别（Critical / Warning / Info）对决策进行分层，关键违规场景可阻塞 PR，从“提醒”升级为“执行约束”。
- 设计上强调工程可用性：CLI 可接入任意 CI；评论幂等更新避免刷屏；无外部网络调用以保护代码与元数据隐私。

## Results
- 文中**没有提供正式基准实验、公开数据集评测或对比数值指标**，因此不存在论文式 SOTA 结果。
- 最强的具体工程声明是：可处理 **3000+ 文件** 的 PR 而**不会 OOM**，说明其在大规模代码评审场景下具备可用性。
- 工具宣称具备 **109 个测试**，并包含 **ReDoS protection** 与 **path traversal protection**，强调规则引擎与文件处理的健壮性与安全性。
- 功能层面的可验证主张包括：支持 **3 档严重级别**（Critical / Warning / Info），其中 Critical 可用于**阻塞 PR**。
- 兼容性主张包括：既可作为**单步 GitHub Action**使用，也可通过 **`npx decision-guardian` CLI** 接入 GitLab、Jenkins、CircleCI、pre-commit hooks 等环境。
- 相对基线的定位是：相比 **CODEOWNERS**，它补充“为什么要审”；相比 **Danger.js**，它用 **Markdown 而非代码** 来维护规则，使非 JavaScript 工程师也能维护架构决策。

## Link
- [https://news.ycombinator.com/item?id=47226046](https://news.ycombinator.com/item?id=47226046)
