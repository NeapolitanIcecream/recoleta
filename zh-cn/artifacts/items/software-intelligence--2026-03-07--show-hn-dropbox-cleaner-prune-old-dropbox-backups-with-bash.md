---
source: hn
url: https://github.com/cre8llc/Dropbox-Cleaner
published_at: '2026-03-07T23:09:14'
authors:
- e-gockel
topics:
- bash-automation
- backup-cleanup
- dropbox
- cron-jobs
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Dropbox Cleaner – prune old Dropbox backups with Bash

## Summary
这是一个用于清理 Dropbox 中旧 SQL 备份的 Bash 脚本，通过“按天数删除 + 至少保留最新 N 份”的双重规则降低误删风险。它面向定时任务和多客户部署场景，依赖文件名中的日期而非 Dropbox 元数据。

## Problem
- 解决 Dropbox 中数据库备份持续累积、占用存储且人工清理低效的问题。
- 传统按时间直接删除容易在备份任务失败或上传中断时删掉过多历史副本，因此需要一个“安全下限”机制。
- 在很多轻量部署场景中，无法方便依赖 Dropbox 元数据，所以需要仅基于文件名日期完成判断。

## Approach
- 核心机制很简单：脚本先列出 Dropbox 目录中的备份文件，从文件名 `databasename-YYYY.MM.DD.sql.gz` 提取日期，再按从新到旧排序。
- 删除条件是双重门槛：**文件年龄大于 `KEEP_DAYS`，且不在最新 `MIN_FILES` 之内**，因此即使旧文件很多，也始终保留至少 N 份最新备份。
- 支持 `-n` dry-run 预演，不真正删除文件，方便上线前验证规则是否正确。
- 适合 cron 定时执行，也支持多客户端分别部署；只需 Bash 4+ 和 `dropbox_uploader.sh` 授权配置。

## Results
- 文本未提供基准测试、实验数据或正式评测结果，因此**没有可报告的定量指标**。
- 明确宣称的功能结果是：可删除**超过 `N` 天**的旧备份，同时**始终保留最新 `N` 份**作为安全底线。
- 支持可配置示例：`-k 60 -m 10` 表示保留 **60 天**内文件，并至少保留最新 **10** 份备份。
- 支持极端策略：`-k 0 -m 14` 可实现“只保留最新 **14** 份”；`-m 0` 则可关闭最小保留数约束。
- 适用于定时自动化，如示例 cron 为每天 **3:00** 运行一次；作者强调应先以 dry-run 模式运行**至少一周**后再启用真实删除。

## Link
- [https://github.com/cre8llc/Dropbox-Cleaner](https://github.com/cre8llc/Dropbox-Cleaner)
