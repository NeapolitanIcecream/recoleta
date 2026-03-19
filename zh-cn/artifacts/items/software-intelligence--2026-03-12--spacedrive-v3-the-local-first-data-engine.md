---
source: hn
url: https://spacedrive.com/blog/spacedrive-v3-launch
published_at: '2026-03-12T22:57:04'
authors:
- raybb
topics:
- local-first
- data-engine
- agent-memory
- prompt-injection-defense
- vector-search
- rust
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Spacedrive v3: The local-first data engine

## Summary
Spacedrive v3 是一个本地优先的数据引擎，目标是在不移动原始数据的前提下，把多源个人/团队数据统一索引并可搜索。其核心卖点不是文件管理，而是在 AI 使用前先对数据做本地安全筛查、质量分类和信任分层。

## Problem
- 传统跨平台文件管理器产品面太大，涉及多操作系统文件语义、权限、缩略图、拖放等，导致难以稳定交付。
- 现有本地数据工具通常把原始内容直接送入 LLM/Agent 上下文，缺少对提示注入（prompt injection）和低质量噪声内容的预处理。
- 用户希望统一搜索邮件、笔记、书签、日历、联系人、GitHub、Slack、编码会话等数据，同时保持本地控制与隐私边界，这对 AI 场景尤其重要。

## Approach
- 把每个数据源建模为一个 repository：原始数据留在原处，Spacedrive 仅维护该源对应的 SQLite 数据库和向量索引，实现统一检索。
- 在进入搜索索引前，对每条记录执行四阶段处理流水线：安全筛查、内容分类、适配器专用处理、搜索索引。
- 安全筛查阶段使用 Meta 的 Prompt Guard 2 在本地 CPU 上运行，对注入内容隔离，对边界样本加安全元数据；内容分类阶段为记录打质量分、噪声标签和类别标签，影响搜索排序与 Agent 可见性。
- 通过 repository trust tiers 和可见性控制，将数据源划分为 authored/collaborative/external 等信任等级，并支持 private/shared/agent-excluded，限制 Agent 跨源访问。
- 系统架构为纯 Rust 核心库，基于 SQLite、LanceDB、FastEmbed、BLAKE3 等构建，本地单二进制运行；通过脚本式 adapter 接入 11 类数据源，并与 Spacebot 直接作为 crate 集成。

## Results
- 文章没有提供标准学术基准上的检索、分类或 Agent 安全性的定量实验结果，也没有给出与其他系统的统一 benchmark 对比。
- 明确给出的性能数字是：Prompt Guard 2 本地 CPU 推理 **每个 chunk 少于 50ms**，用于索引前的注入筛查。
- 启动时支持 **11 个 adapters**：Gmail、Apple Notes、Chrome Bookmarks、Chrome History、Safari History、Obsidian、OpenCode、Slack Export、macOS Contacts、macOS Calendar、GitHub，并支持 UTC 归一化日期与增量同步游标。
- 工程规模与成熟度信号：核心实现约 **183k 行 Rust**（指 v2 架构背景），当前架构包含 **68 个测试**；项目历史上累计 **37,000 GitHub stars**、**600,000 downloads**、**$2M seed**，说明需求验证较强但不代表技术效果 benchmark。
- 相比 v1/v2，作者宣称 v3 的突破在于聚焦“可搜索的数据索引层”而非跨平台文件管理/实时同步，并把注入防护、内容分类、信任分层作为一等能力，而不是可选附加功能。

## Link
- [https://spacedrive.com/blog/spacedrive-v3-launch](https://spacedrive.com/blog/spacedrive-v3-launch)
