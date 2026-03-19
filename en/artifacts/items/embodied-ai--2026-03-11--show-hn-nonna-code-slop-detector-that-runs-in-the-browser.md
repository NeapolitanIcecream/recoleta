---
source: hn
url: http://www.babush.me/nonna/
published_at: '2026-03-11T23:45:42'
authors:
- babush
topics:
- code-quality
- static-analysis
- browser-based
- privacy-preserving
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: Nonna – code slop detector that runs in the browser

## Summary
This is a browser-based “code slop detector” called Nonna, used to locally analyze uploaded Python files or archives. The given content looks more like a product page excerpt than a research paper, so the amount of confirmable information is very limited.

## Problem
- It attempts to solve the problem of detecting “code slop,” helping users identify low-quality, redundant, or suspicious patterns in code.
- This matters because code quality issues affect maintainability, review efficiency, and developers’ trust in automatically generated code or large codebases.
- From the page description, it especially emphasizes privacy and ease of use: analysis is completed locally in the browser, without uploading code to a server.

## Approach
- The core mechanism appears to be that users upload `.py` or `.zip`, and the tool analyzes the code locally in the browser, then compares or retrieves against some “pre-indexed corpus.”
- The page includes `Pairs`, `Packages`, and “Loading pre-indexed corpus...,” suggesting it may detect “slop” through code snippet pairing, package-level statistics, or corpus matching.
- Put simply: it is like a frontend-running code checker that compares your Python code against an existing corpus to find suspicious low-quality patterns.
- A clearly visible implementation characteristic is **fully local analysis**: "Files are analyzed locally — nothing is uploaded to a server".

## Results
- The provided text contains **no quantitative experimental results**, with no dataset, metrics, baselines, or precision/recall numbers.
- The strongest concrete claim is that it supports uploading `.py` / `.zip` for analysis.
- Another concrete claim is that analysis is performed locally in the browser, and files are not uploaded to a server.
- The page also states that it loads a “pre-indexed corpus,” indicating that the system relies on an existing corpus for detection, but it does not specify the scale, source, or effectiveness.

## Link
- [http://www.babush.me/nonna/](http://www.babush.me/nonna/)
