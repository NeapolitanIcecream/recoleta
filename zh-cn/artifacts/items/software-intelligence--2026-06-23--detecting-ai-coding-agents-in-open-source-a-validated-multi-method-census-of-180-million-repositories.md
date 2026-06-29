---
source: arxiv
url: https://arxiv.org/abs/2606.24429v1
published_at: '2026-06-23T11:05:42'
authors:
- Arsham Khosravani
- Audris Mockus
topics:
- ai-coding-agents
- open-source-mining
- software-supply-chain
- code-intelligence
- repository-metadata
- agent-detection
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Detecting AI Coding Agents in Open Source: A Validated Multi-Method Census of 180 Million Repositories

## Summary
## 摘要
本文衡量了 1.8 亿多个 Git 仓库中的 AI 编码代理痕迹，并显示只依赖单一信号的研究会漏掉大部分活动。论文的主要结论是，提交、拉取请求、作者和配置文件信号会识别出不同的代理群体和工作类型。

## 问题
- AI 编码代理留下的痕迹常常很弱或不一致，因此开源研究可能低估 AI 辅助代码的规模。
- 可靠检测会影响软件供应链审计、普及率测量，以及代码质量或项目速度研究。
- 以往基于机器人账号、拉取请求或配置文件的普查只覆盖一个渠道。

## 方法
- 作者使用 World of Code 快照 V2412、V2510 和 V2604，覆盖 2024 年 12 月至 2026 年 4 月，以及 1.8 亿多个仓库。
- 他们定义了四类痕迹：集中式机器人账号、提交消息签名、人类作者名模式，以及仅存在于配置文件中的痕迹。
- 他们扫描作者映射、提交消息和文件到项目的映射；解析人类别名；将机器人身份单独保留；并在统计采用情况前对项目去分叉。
- 他们用 495 个人工标签验证每个检测器单元，报告带 Wilson 置信区间的单元级精确率，并将其提交普查与 AIDev 拉取请求普查进行比较。

## 结果
- 在 V2510 中，多方法 Claude Code 检测发现 850,157 个提交。仅使用机器人账号查找发现 28,154 个提交，相对召回差距为 30 倍；并集仍然只是下限。
- 在 V2510 中，Copilot SWE Agent 在 85,739 个项目中有 1,127,201 个提交，Claude Code 在 17,295 个项目中有 850,157 个提交，Devin 有 215,998 个提交，Jules 有 209,911 个提交。
- 在 V2604 中，可归因于提交的代理产生 1,772,677 个提交。Claude Code 贡献 886,122 个提交，占 50%；Replit 贡献 314,779 个，Jules 贡献 215,804 个，Aider 贡献 196,132 个。
- 可归因于提交的 AI 代理在 2026 年 3 月峰值时每月超过 320,000 个提交。在包含 AI 归因提交的项目中，AI 份额从 2025 年 12 月非机器人活动的 1.6% 上升到 2026 年 3 月的 6.7%。
- V2604 配置文件普查发现 1,699,950 次配置文件出现。Claude 在 21,078 个项目中占 888,177 次，GitHub Copilot 占 211,166 次，Codex 占 134,810 次。
- 与 AIDev 相比，拉取请求普查会漏掉 79% 通过提交检测到的 Claude Code 采用者，而基于提交的普查会漏掉几乎所有 Codex 采用者。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24429v1](https://arxiv.org/abs/2606.24429v1)
