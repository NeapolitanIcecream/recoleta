---
source: hn
url: https://daniel.haxx.se/blog/2026/03/09/10k-curl-downloads-per-year/
published_at: '2026-03-09T23:02:13'
authors:
- donutshop
topics:
- open-source-metrics
- software-measurement
- curl
- ecosystem-analytics
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# 10K Curl Downloads per Year

## Summary
This article criticizes the Linux Foundation “Insights” method for measuring the influence of open source projects, arguing that its statistics for curl’s annual downloads are severely distorted. Using data from multiple real distribution channels, the author shows that a single aggregated metric can significantly underestimate the true scale of usage.

## Problem
- The problem the article addresses is: **whether the “download count” metric provided by open source project platforms is trustworthy, and why distortions in such a metric are dangerous**.
- This matters because numbers from foundations or scoring platforms may be used to “grade” project health, influence, and resource allocation, but incorrect metrics can mislead communities, users, and decision-makers.
- Using curl as an example, the article points out that the claimed annual download count of **10,467** is completely inconsistent with how the project is actually distributed.

## Approach
- The author does not propose a new algorithm, but instead uses a **counterexample audit** approach, taking one specific metric in Linux Foundation Insights and breaking it down.
- The core mechanism is simple: directly compare the platform’s claimed annual curl download count with the public/known scale of curl across multiple real distribution channels.
- The compared channels include: official release tarball downloads, Docker image pulls, quay.io image pulls, git repository clones, as well as OS preinstallation, Linux/BSD package-manager distribution, and indirect distribution through libcurl being embedded in applications and devices.
- The argument is that if a “download count” definition cannot cover these main distribution paths, then it does not represent the project’s true adoption, but is merely a partial count from some narrow source.

## Results
- Linux Foundation Insights claims that curl was downloaded **10,467** times in the past year.
- The author’s data from the official site is that curl release tarballs are downloaded from curl.se at about **250,000/month**, or about **3,000,000/year**, already far higher than 10,467.
- In the Docker channel, curl images are pulled about **400,000–700,000/day**; quay.io is “roughly the same,” implying a combined total of about **800,000–1,400,000/day**, or about **292 million–511 million/year**.
- curl’s git repository is cloned about **32,000/day**, or about **11.68 million/year**.
- There are also important but unquantified forms of distribution: installation via Linux/BSD distributions, default preinstallation on Windows and macOS, and libcurl being embedded in large numbers of applications, games, devices, cars, TVs, printers, and services. The article does not provide a single unified total, but its strongest conclusion is: **the figure 10,467 underestimates curl’s true distribution scale by multiple orders of magnitude**.

## Link
- [https://daniel.haxx.se/blog/2026/03/09/10k-curl-downloads-per-year/](https://daniel.haxx.se/blog/2026/03/09/10k-curl-downloads-per-year/)
