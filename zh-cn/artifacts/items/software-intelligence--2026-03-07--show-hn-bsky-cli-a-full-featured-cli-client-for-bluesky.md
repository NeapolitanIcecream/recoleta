---
source: hn
url: https://github.com/harveyrandall/bsky-cli
published_at: '2026-03-07T22:55:36'
authors:
- harveyrandall
topics:
- cli-tool
- bluesky
- typescript
- developer-tools
- social-media-client
relevance_score: 0.19
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Bsky-CLI – A full-featured CLI client for Bluesky

## Summary
这是一个用 TypeScript 编写的 Bluesky 全功能命令行客户端，面向终端用户、脚本和 CI 场景。它把 Bluesky 的常见社交操作统一到一个可安装、可多账号管理、可跨平台分发的 CLI 工具中。

## Problem
- 解决的问题是：如何在命令行中完整访问和操作 Bluesky，而不依赖图形界面或零散脚本。
- 这很重要，因为开发者、自动化脚本和 CI 工作流需要可编排、可复用、可环境变量配置的社交平台接口。
- 现有摘录强调“full-featured CLI client”，说明目标是覆盖发帖、时间线、互动、资料管理、通知等高频功能。

## Approach
- 核心方法是构建一个统一的 `bsky` 命令，把 Bluesky 的主要能力映射成子命令，如时间线、发帖、回复、引用、点赞、转发、关注、搜索、通知和资料更新。
- 认证机制支持交互式登录、命令行传参、标准输入和环境变量，并明确配置优先级为“CLI 参数 > 环境变量 > 配置文件”，便于脚本化使用。
- 通过 `--profile` / `-p` 支持多账号配置，让用户在个人和工作账号之间切换。
- 提供 macOS、Linux、Windows 独立二进制，以及 npm/yarn/pnpm/bun/Homebrew 多渠道安装，降低使用门槛。
- 还提供 shell 补全、测试/构建脚本与从源码构建方式，增强开发和贡献体验。

## Results
- 功能覆盖上，摘录列出了 **30+ 个命令/子命令**，包括 timeline、stream、thread、post、reply、quote、delete、like、repost、bookmarks、follow、search、profile、notification、app-password、report、mod-list 等，体现出较完整的 Bluesky CLI 能力。
- 平台与分发上，支持 **4 种 JavaScript 包管理器安装**（npm、yarn、pnpm、bun）以及 **1 种 Homebrew 安装**，并提供 **3 大桌面平台** 独立二进制（macOS、Linux、Windows）。
- 运行环境要求为 **Node.js >= 22**；同时支持源码构建、全局链接、类型检查、测试运行和覆盖率命令，但摘录**没有提供具体测试覆盖率数值**。
- 账号管理上，明确支持 **多 profile** 使用方式，可在同一工具中管理多个 Bluesky 账号。
- 路线图/待支持功能列出 **6 项**：Direct messages、List creation and management、Starter packs、Moderation lists、Post labels、Auto alt-text for images and videos，以及 OAuth login support，说明当前仍在扩展中。
- 摘录**没有给出基准测试、性能指标、用户研究或与其他 Bluesky 客户端的定量对比结果**；最强的具体主张是其“full-featured”定位、跨平台分发和较广的命令覆盖面。

## Link
- [https://github.com/harveyrandall/bsky-cli](https://github.com/harveyrandall/bsky-cli)
