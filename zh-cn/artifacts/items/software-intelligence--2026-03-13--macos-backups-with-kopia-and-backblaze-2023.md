---
source: hn
url: https://hmarr.com/blog/mac-backups-with-kopia/
published_at: '2026-03-13T23:24:38'
authors:
- chmaynard
topics:
- macos-backup
- kopia
- backblaze-b2
- incremental-backup
- deduplication
relevance_score: 0.1
run_id: materialize-outputs
language_code: zh-CN
---

# macOS backups with Kopia and Backblaze (2023)

## Summary
这是一篇实践型技术文章，介绍如何在 macOS 上用 Kopia 配合 Backblaze B2 实现低成本、增量式、自动化云备份。核心价值在于用开源工具获得快速去重备份，并把月成本压到极低。

## Problem
- 文章要解决的是：如何在 macOS 上不用重型 GUI，也能稳定地自动执行云端备份。
- 这件事重要，因为个人电脑数据需要持续备份，而常见云存储方案可能更贵、配置不透明，命令行方案的自动化也不直观。
- 作者特别指出，Kopia 的 CLI 本身不直接替你完成 macOS 定时调度，因此需要补上自动运行与健康检查这一环。

## Approach
- 使用 **Kopia** 对指定目录做 **incremental snapshots**，并依赖其内容去重机制，让后续快照更快且更省空间。
- 将备份仓库存储到 **Backblaze B2**，利用其低价对象存储作为远程后端。
- 通过 **snapshot policy** 配置保留策略、压缩和忽略规则，例如忽略 `node_modules/`、`.venv/`、`__pycache__/` 等可再生成目录。
- 编写一个简单 shell 脚本，批量对多个目标目录执行 `kopia snapshot create`。
- 在 macOS 上使用 **launchd / LaunchAgent** 按固定时间（示例为每天 18 点）触发该脚本，并配合 **healthchecks.io** 监控备份是否按时完成。

## Results
- 成本数据：作者备份 **20GB** 数据时，月成本约 **$0.26/month**。
- 定价对比：Backblaze B2 提供前 **10GB 免费**，之后 **$0.026/GB/month**；文中称这低于 **S3 的五分之一**。
- 运行经验：作者表示该方案已使用 **近两年**，总花费低到“Backblaze 甚至还没来得及收费”。
- 效果主张：Kopia 的内容智能去重使新增快照“快速且空间高效”，但文中**没有提供正式基准测试或恢复速度等量化实验结果**。
- 自动化结果：通过 LaunchAgent + 日志 + healthchecks.io，可以形成可调度、可观测、失败可告警的 macOS 备份流程，但这属于实践经验而非论文式评测。

## Link
- [https://hmarr.com/blog/mac-backups-with-kopia/](https://hmarr.com/blog/mac-backups-with-kopia/)
