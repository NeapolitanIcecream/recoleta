---
source: hn
url: https://github.com/cre8llc/Dropbox-Cleaner
published_at: '2026-03-07T23:09:14'
authors:
- e-gockel
topics:
- bash-script
- backup-cleanup
- dropbox
- cron-automation
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Dropbox Cleaner – prune old Dropbox backups with Bash

## Summary
这是一个用于清理 Dropbox 中旧 SQL 备份的 Bash 脚本，通过“保留天数 + 最少保留份数”双重规则安全删除旧文件。它面向定时运维场景，重点是避免因备份中断或上传失败而误删过多备份。

## Problem
- 解决的问题是：如何自动删除 Dropbox 中过旧的数据库备份，同时确保不会把最近仍需要的备份删得太多。
- 这很重要，因为长期累积的备份会占用存储并增加管理负担，而简单按时间删除在备份任务失败时可能导致恢复点不足。
- 该工具特别针对只依赖文件名日期、没有额外 Dropbox 元数据支持的备份清理场景。

## Approach
- 核心机制非常简单：从备份文件名中提取日期（格式如 `databasename-YYYY.MM.DD.sql.gz`），据此计算文件年龄，而不依赖 Dropbox 元数据。
- 脚本先用 Dropbox-Uploader 列出文件，再按时间从新到旧排序。
- 它设置两个阈值：`KEEP_DAYS` 表示仅删除超过 N 天的文件，`MIN_FILES` 表示无论如何都保留最新的 N 份备份。
- 真正删除的条件是：`age > KEEP_DAYS AND not in newest MIN_FILES`，因此即使上传停止，也至少保留指定数量的最新备份。
- 支持 dry-run、cron 定时执行和多客户端部署，适合日常自动化运维。

## Results
- 文本**没有提供基准数据、实验数据集或定量评测结果**，因此没有可报告的精确性能指标。
- 给出的最具体结果性声明是：删除条件明确为“超过 `KEEP_DAYS` 且不属于最新 `MIN_FILES`”，从策略上保证**至少保留 N 份**最新备份。
- 示例配置包括：保留 **60 天**且至少保留 **10 份**（`-k 60 -m 10`）。
- 还支持“只保留最新若干份”的模式，例如 `-k 0 -m 14` 表示仅保留最新 **14** 份备份。
- 推荐每晚 **3:00** 通过 cron 运行，并建议首周使用 dry-run（`-n`）验证行为后再启用真实删除。

## Link
- [https://github.com/cre8llc/Dropbox-Cleaner](https://github.com/cre8llc/Dropbox-Cleaner)
