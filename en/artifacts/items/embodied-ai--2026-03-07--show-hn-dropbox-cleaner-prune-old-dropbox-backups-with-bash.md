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
language_code: en
---

# Show HN: Dropbox Cleaner – prune old Dropbox backups with Bash

## Summary
This is a Bash script for cleaning up old SQL backups in Dropbox, safely deleting old files through a dual rule of “retention days + minimum number of backups to keep.” It is designed for scheduled operations scenarios, with a focus on avoiding accidental deletion of too many backups when backups are interrupted or uploads fail.

## Problem
- The problem it solves is: how to automatically delete overly old database backups in Dropbox while ensuring that not too many recent backups that may still be needed are removed.
- This is important because backups that accumulate over time consume storage and increase management burden, while simple time-based deletion can lead to too few restore points when backup jobs fail.
- This tool is specifically aimed at backup cleanup scenarios that rely only on dates in filenames, without additional Dropbox metadata support.

## Approach
- The core mechanism is very simple: it extracts the date from the backup filename (format such as `databasename-YYYY.MM.DD.sql.gz`) and uses that to calculate file age, without relying on Dropbox metadata.
- The script first uses Dropbox-Uploader to list files, then sorts them from newest to oldest by time.
- It sets two thresholds: `KEEP_DAYS` means only files older than N days are deleted, and `MIN_FILES` means the newest N backups are kept no matter what.
- The actual deletion condition is: `age > KEEP_DAYS AND not in newest MIN_FILES`, so even if uploads stop, at least the specified number of newest backups are retained.
- It supports dry-run, cron scheduled execution, and multi-client deployment, making it suitable for routine automated operations.

## Results
- The text **does not provide benchmark data, experimental datasets, or quantitative evaluation results**, so there are no precise performance metrics to report.
- The most specific result-oriented claim given is that the deletion condition is explicitly “older than `KEEP_DAYS` and not among the newest `MIN_FILES`,” which by policy guarantees that **at least N** of the newest backups are retained.
- Example configurations include: keep **60 days** and retain at least **10 backups** (`-k 60 -m 10`).
- It also supports a “keep only the newest few backups” mode; for example, `-k 0 -m 14` means keeping only the newest **14** backups.
- It is recommended to run via cron every night at **3:00**, and to use dry-run (`-n`) during the first week to verify behavior before enabling actual deletions.

## Link
- [https://github.com/cre8llc/Dropbox-Cleaner](https://github.com/cre8llc/Dropbox-Cleaner)
