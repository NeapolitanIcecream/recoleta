---
source: hn
url: https://hmarr.com/blog/mac-backups-with-kopia/
published_at: '2026-03-13T23:24:38'
authors:
- chmaynard
topics:
- backup
- macos
- kopia
- backblaze-b2
- incremental-snapshots
relevance_score: 0.01
run_id: materialize-outputs
---

# macOS backups with Kopia and Backblaze (2023)

## Summary
这是一篇关于在 macOS 上用 **Kopia + Backblaze B2** 搭建低成本云备份的实践文章，不是学术论文。作者重点说明了如何做增量去重备份、如何用 `launchd` 定时执行，以及这一方案为什么便宜且实用。

## Problem
- 解决的问题是：如何在 **macOS 上不依赖图形界面**，自动、稳定地把重要目录备份到云端。
- 这很重要，因为个人数据需要可恢复、可持续、低成本的异地备份；若只手动备份，容易忘记执行，也缺少监控。
- 作者特别针对 Kopia CLI 在 macOS 上“**自动化调度不够直观**”这一实际使用痛点给出配置方法。

## Approach
- 使用 **Kopia** 对指定目录做 **增量快照**，并利用 **去重** 降低重复数据带来的存储和上传开销。
- 将备份仓库存放在 **Backblaze B2**，利用其较低的存储价格替代更贵的对象存储方案。
- 通过 **snapshot policy** 配置保留策略、压缩、忽略路径等，例如保留最近 10 个版本、48 个小时级快照、7 个日级快照、4 个周级快照、24 个月级快照、3 个年级快照。
- 编写一个 shell 脚本批量执行 `kopia snapshot create` 备份多个目录。
- 在 macOS 上用 **LaunchAgent / launchd** 按固定时间（示例中为每天 18 点）自动运行脚本，并通过日志与 **healthchecks.io** 进行失败监控。

## Results
- 最核心的量化结果是成本：作者称 **20GB 数据每月仅约 $0.26**。
- 文中给出的 B2 定价依据是：**前 10GB 免费**，之后 **$0.026/GB/月**；并声称这低于 **S3 的五分之一**。
- 作者表示该方案已使用 **将近两年**，总花费低到 **Backblaze 甚至还没有向他收费**。
- 性能方面没有正式基准测试或实验表格；最具体的经验性结论是 **增量快照 + 智能去重** 使新快照“更快且更节省空间”。
- 自动化效果上，文章提供了可直接复用的 `launchd` 配置与脚本流程，用于实现 **每日自动备份** 与失败告警，但没有系统化成功率/恢复时间等实验数据。

## Link
- [https://hmarr.com/blog/mac-backups-with-kopia/](https://hmarr.com/blog/mac-backups-with-kopia/)
