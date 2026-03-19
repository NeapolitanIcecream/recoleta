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
language_code: en
---

# Show HN: Dropbox Cleaner – prune old Dropbox backups with Bash

## Summary
This is a Bash script for cleaning up old SQL backups in Dropbox, reducing the risk of accidental deletion through a dual rule of “delete by age + always keep at least the newest N copies.” It is designed for scheduled jobs and multi-client deployment scenarios, and relies on dates in filenames rather than Dropbox metadata.

## Problem
- It addresses the problem of database backups continuously accumulating in Dropbox, consuming storage, and making manual cleanup inefficient.
- Traditional time-based deletion can easily remove too many historical copies when backup jobs fail or uploads are interrupted, so a “safety floor” mechanism is needed.
- In many lightweight deployment scenarios, it is not practical to depend on Dropbox metadata, so decisions need to be made solely based on dates in filenames.

## Approach
- The core mechanism is simple: the script first lists backup files in a Dropbox directory, extracts the date from filenames in the format `databasename-YYYY.MM.DD.sql.gz`, and then sorts them from newest to oldest.
- The deletion condition uses a double threshold: **the file age is greater than `KEEP_DAYS`, and it is not among the newest `MIN_FILES`**, so even if there are many old files, it always retains at least the newest N backups.
- It supports `-n` dry-run mode, which does not actually delete files, making it convenient to verify that the rules are correct before going live.
- It is suitable for scheduled execution via cron and also supports separate deployment for multiple clients; it only requires Bash 4+ and authorized configuration of `dropbox_uploader.sh`.

## Results
- The text does not provide benchmarks, experimental data, or formal evaluation results, so there are **no quantitative metrics to report**.
- The clearly stated functional outcome is that it can delete old backups **older than `N` days** while **always keeping the newest `N` copies** as a safety baseline.
- It supports configurable examples: `-k 60 -m 10` means keeping files within **60 days** and retaining at least the newest **10** backups.
- It supports extreme strategies: `-k 0 -m 14` can implement “keep only the newest **14** copies”; `-m 0` can disable the minimum retention count constraint.
- It is suitable for scheduled automation, such as the example cron job that runs once daily at **3:00**; the author emphasizes that it should first be run in dry-run mode for **at least one week** before enabling actual deletion.

## Link
- [https://github.com/cre8llc/Dropbox-Cleaner](https://github.com/cre8llc/Dropbox-Cleaner)
