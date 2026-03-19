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
language_code: en
---

# macOS backups with Kopia and Backblaze (2023)

## Summary
This is a practical article about building a low-cost cloud backup setup on macOS with **Kopia + Backblaze B2**, not an academic paper. The author focuses on how to do incremental deduplicated backups, how to schedule them with `launchd`, and why this setup is cheap and practical.

## Problem
- The problem it addresses is: how to automatically and reliably back up important directories to the cloud on **macOS without relying on a graphical interface**.
- This matters because personal data needs recoverable, sustainable, low-cost offsite backups; if backups are only done manually, it is easy to forget to run them and there is also a lack of monitoring.
- The author specifically provides a configuration method for the real-world pain point that automation scheduling with the Kopia CLI on macOS is **not very intuitive**.

## Approach
- Use **Kopia** to take **incremental snapshots** of specified directories, and use **deduplication** to reduce the storage and upload overhead caused by duplicate data.
- Store the backup repository in **Backblaze B2**, using its lower storage pricing instead of more expensive object storage options.
- Use **snapshot policy** to configure retention, compression, ignored paths, etc., for example keeping the latest 10 versions, 48 hourly snapshots, 7 daily snapshots, 4 weekly snapshots, 24 monthly snapshots, and 3 annual snapshots.
- Write a shell script to batch-execute `kopia snapshot create` to back up multiple directories.
- On macOS, use **LaunchAgent / launchd** to automatically run the script at a fixed time (18:00 daily in the example), and use logs plus **healthchecks.io** for failure monitoring.

## Results
- The most important quantitative result is cost: the author says **20GB of data costs only about $0.26 per month**.
- The B2 pricing basis given in the article is: **the first 10GB are free**, and after that **$0.026/GB/month**; it also claims this is **less than one-fifth the cost of S3**.
- The author says this setup has been used for **nearly two years**, with total spending so low that **Backblaze has not even bothered to bill him**.
- On performance, there are no formal benchmarks or experimental tables; the most specific experiential conclusion is that **incremental snapshots + intelligent deduplication** make new snapshots “faster and more space-efficient.”
- For automation, the article provides directly reusable `launchd` configuration and a script workflow to achieve **daily automatic backups** and failure alerts, but it does not provide systematic experimental data such as success rates or recovery times.

## Link
- [https://hmarr.com/blog/mac-backups-with-kopia/](https://hmarr.com/blog/mac-backups-with-kopia/)
