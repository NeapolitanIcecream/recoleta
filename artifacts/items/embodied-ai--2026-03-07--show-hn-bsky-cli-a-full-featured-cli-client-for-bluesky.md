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
relevance_score: 0.0
run_id: materialize-outputs
---

# Show HN: Bsky-CLI – A full-featured CLI client for Bluesky

## Summary
这是一个用 TypeScript 编写的 Bluesky 命令行客户端，目标是提供接近完整平台功能的 CLI 使用体验。它更像一个开发者工具/产品发布，而不是研究论文，也未提供实验性评测结果。

## Problem
- 它要解决的问题是：Bluesky 缺少一个便于脚本化、终端操作和多账户管理的全功能命令行客户端。
- 这很重要，因为开发者、重度用户和 CI/自动化场景需要在不依赖图形界面的情况下完成发帖、检索、交互和账户管理。
- 现有摘要中还暗示了易部署与跨平台使用需求，包括全局安装、独立二进制和环境变量配置。

## Approach
- 核心方法很直接：把 Bluesky 常见操作封装成一组统一的 CLI 子命令，如时间线、发帖、回复、点赞、转发、搜索、通知、资料更新等。
- 通过多种安装方式支持使用，包括 npm/yarn/pnpm/bun、Homebrew，以及 macOS/Linux/Windows 独立二进制，降低部署门槛。
- 通过配置优先级机制实现自动化友好：`CLI 参数 > 环境变量 > 配置文件`，并支持从环境变量直接认证，适合脚本和 CI。
- 通过 `--profile/-p` 支持多账户隔离管理，让用户能在个人/工作账户之间切换。
- 提供 shell 补全、测试/构建命令和从源码构建流程，说明其定位是可维护、可扩展的开发者工具。

## Results
- 文本**没有提供任何定量实验结果**，没有数据集、基线方法、准确率、延迟、吞吐或用户研究数字可供比较。
- 给出的最强具体主张是“full-featured CLI client for Bluesky”，并列出了大量已支持命令：如 `timeline/tl`、`stream`、`thread`、`post`、`reply`、`quote`、`delete`、`like`、`repost`、`bookmarks`、`follow/unfollow`、`search`、`profile-update`、`notifs`、`invite-codes`、`app-password`、`report`、`mod-list` 等。
- 兼容性方面，明确要求 `Node.js >= 22`，并提供 macOS、Linux、Windows 的独立二进制发布。
- 账户与自动化能力方面，支持多 profile 管理，以及基于环境变量的认证和配置覆盖规则，适合脚本化操作。
- 路线图/未完成功能也被明确列出，包括私信、列表管理、starter packs、moderation lists、post labels、自动 alt-text、OAuth 登录支持和 Docker BuildKit 二进制构建。

## Link
- [https://github.com/harveyrandall/bsky-cli](https://github.com/harveyrandall/bsky-cli)
