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
language_code: en
---

# macOS backups with Kopia and Backblaze (2023)

## Summary
This is a practical technical article that explains how to use Kopia with Backblaze B2 on macOS to achieve low-cost, incremental, automated cloud backups. Its core value is using open-source tools to get fast deduplicated backups while keeping the monthly cost extremely low.

## Problem
- The article aims to solve this: how to reliably automate cloud backups on macOS without relying on a heavyweight GUI.
- This matters because personal computer data needs continuous backup, while common cloud storage options may be more expensive and less transparent to configure, and automation with a command-line solution is not always intuitive.
- The author specifically points out that Kopia’s CLI does not directly handle macOS scheduled execution for you, so you need to add automation and health checks yourself.

## Approach
- Use **Kopia** to take **incremental snapshots** of selected directories, relying on its content deduplication mechanism to make subsequent snapshots faster and more space-efficient.
- Store the backup repository in **Backblaze B2**, using its low-cost object storage as the remote backend.
- Configure retention policies, compression, and ignore rules through **snapshot policy**, for example ignoring regenerable directories such as `node_modules/`, `.venv/`, and `__pycache__/`.
- Write a simple shell script to run `kopia snapshot create` for multiple target directories in batch.
- On macOS, use **launchd / LaunchAgent** to trigger the script at a fixed time (the example is 6 PM daily), together with **healthchecks.io** to monitor whether backups complete on schedule.

## Results
- Cost data: the author reports a monthly cost of about **$0.26/month** for backing up **20GB** of data.
- Pricing comparison: Backblaze B2 provides the first **10GB free**, then charges **$0.026/GB/month**; the article says this is less than **one-fifth the cost of S3**.
- Operating experience: the author says they have used this setup for **nearly two years**, with total spending so low that “Backblaze hasn’t even bothered to bill me yet.”
- Performance claim: Kopia’s intelligent content deduplication makes new snapshots “fast and space-efficient,” but the article **does not provide formal benchmarks or quantitative results such as restore speed**.
- Automation outcome: with LaunchAgent + logs + healthchecks.io, you can build a schedulable, observable macOS backup workflow with failure alerting, though this is practical experience rather than a paper-style evaluation.

## Link
- [https://hmarr.com/blog/mac-backups-with-kopia/](https://hmarr.com/blog/mac-backups-with-kopia/)
