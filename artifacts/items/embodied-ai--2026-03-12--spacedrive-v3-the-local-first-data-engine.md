---
source: hn
url: https://spacedrive.com/blog/spacedrive-v3-launch
published_at: '2026-03-12T22:57:04'
authors:
- raybb
topics:
- local-first
- search-index
- prompt-injection-defense
- data-integration
- agent-memory
relevance_score: 0.08
run_id: materialize-outputs
---

# Spacedrive v3: The local-first data engine

## Summary
Spacedrive v3 是一个本地优先的数据引擎，用统一索引把分散在邮件、笔记、浏览器、Slack、文件等处的数据变成可搜索知识层。其核心卖点不是文件管理，而是在本地先做安全筛查、质量分类和结构化处理，再把数据提供给搜索与 AI 代理。

## Problem
- 现有文件管理器/本地数据工具要么产品面太大、跨平台实现过重，难以稳定交付；要么把原始内容直接喂给搜索和 LLM，缺乏安全边界。
- 当邮件、Slack 等外部内容进入 AI 检索语料时，恶意文本可能通过提示注入操纵代理；文中称这是 OWASP 的 #1 LLM 漏洞。
- 用户需要在不把数据交给云端的前提下，从一个入口检索所有个人与工作数据，同时区分不同来源的信任级别与隐私权限。

## Approach
- 将每个数据源抽象为一个 repository：数据保留在原处，Spacedrive 仅在本地保存 SQLite 数据库、向量索引、元数据、哈希和提取文本。
- 设计四阶段处理流水线：1) 用 Prompt Guard 2 做本地注入筛查；2) 做内容质量/噪声/类别分类；3) 做适配器专属处理；4) 仅将通过前几阶段的记录写入 FTS5 与 LanceDB 索引。
- 用 trust tiers 和仓库级可见性控制隔离不同数据源，例如 authored、collaborative、external，并支持 private/shared/agent-excluded。
- 采用脚本化适配器体系接入异构数据源；启动时提供 11 个适配器，并支持 UTC 归一化时间和基于 cursor 的增量同步。
- 架构上使用纯 Rust 核心库，CLI、桌面端和 Spacebot 都是薄客户端；单二进制、无服务器依赖、完全本地运行。

## Results
- 这是产品发布说明而非学术论文，**没有给出标准数据集上的定量 benchmark 或对比实验结果**。
- 文中给出的最明确性能数字是：Prompt Guard 2 在本地 CPU 上对每个 chunk 的筛查时间 **低于 50ms**。
- 项目历史影响力指标：过去四年获得 **37,000 GitHub stars**、**600,000 downloads**；v1 alpha 曾被下载约 **500,000** 次；曾完成 **$2M** 种子轮融资。
- 工程规模声明：v2 曾包含 **183k 行 Rust 代码**；v3 当前架构有 **68 个测试** 覆盖各子系统；启动时支持 **11 个适配器**。
- 核心产品性主张是相对现有本地数据工具的差异化：在进入搜索/AI 之前，所有内容先经过注入防护、质量分类与信任分级，而不是“原样进入 LLM 上下文”。

## Link
- [https://spacedrive.com/blog/spacedrive-v3-launch](https://spacedrive.com/blog/spacedrive-v3-launch)
