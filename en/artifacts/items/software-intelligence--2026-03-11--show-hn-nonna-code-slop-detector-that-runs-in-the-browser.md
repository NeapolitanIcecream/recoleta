---
source: hn
url: http://www.babush.me/nonna/
published_at: '2026-03-11T23:45:42'
authors:
- babush
topics:
- code-analysis
- browser-based
- privacy-preserving
- python-tools
- local-inference
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# Show HN: Nonna – code slop detector that runs in the browser

## Summary
This is a browser-based "code slop detector" called Nonna, used to locally analyze uploaded Python files or archives. Its core value is that detection can be completed without uploading code to a server, placing greater emphasis on privacy-friendly, lightweight code quality analysis.

## Problem
- The problem it aims to solve is: how to detect "slop" in code (understandable as low-quality, redundant, or suspicious patterns) without sending source code to a remote service.
- This matters because code analysis often involves private repositories, commercial source code, or sensitive logic, and developers typically care about privacy and the risk of data leakage.
- The existing excerpt does not explain the strict definition of "slop," the scope of detection, or details about applicable scenarios.

## Approach
- The tool runs as a browser application, and users can upload `.py` or `.zip` files for analysis.
- The analysis process runs locally, and the text explicitly states "nothing is uploaded to a server," meaning it does not rely on server-side code uploads.
- The system loads a "pre-indexed corpus," suggesting that it may perform pairing, package-level, or similarity-related analysis by comparing the target code against a pre-indexed corpus.
- The interface shows "Pairs" and "Packages," indicating that it may support organizing detection results by file pairs or package level, but the excerpt provides no algorithmic details.

## Results
- The provided excerpt **does not give any quantitative results**: there are no numbers for datasets, accuracy, recall, false positive rate, speed, or comparisons with baseline methods.
- The strongest concrete claims are: it supports uploading `.py` / `.zip` for analysis, and **all analysis is completed locally in the browser**, with code **not uploaded to the server**.
- It also states "Loading pre-indexed corpus...," indicating that the system has a ready-to-use pre-indexed corpus capability, but it does not explain its scale or effectiveness.

## Link
- [http://www.babush.me/nonna/](http://www.babush.me/nonna/)
