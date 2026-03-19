---
source: hn
url: https://news.ycombinator.com/item?id=47255521
published_at: '2026-03-04T23:35:11'
authors:
- martinZak
topics:
- privacy-tools
- browser-based
- json-parsing
- personal-data
- google-takeout
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# TakeoutReader – Turn your Google Takeout JSON into a readable report

## Summary
TakeoutReader is a browser-based tool that converts the raw JSON files exported by Google Takeout into readable reports. It primarily addresses the problem that personal data export files are difficult to understand, and it emphasizes privacy because the data never leaves the local browser.

## Problem
- A Google Takeout export produces a large number of JSON files containing millisecond-level timestamps, GPS coordinates, and nested structures that ordinary users can hardly read directly.
- Although users can obtain their own data, they lack visualization and structured organization, making information such as search history, location records, and YouTube activity difficult to truly understand and use.
- This matters because "data portability" is only truly valuable when users can understand, search, and summarize their data, and it also involves highly sensitive personal privacy data.

## Approach
- The core method is simple: parse Google Takeout JSON files in the browser and convert raw fields, timestamps, and coordinates into human-readable reports.
- The tool organizes multiple categories of Google data sources, such as search history, location data, and YouTube activity, and presents scattered nested structures in a unified way.
- Mechanistically, it uses pure frontend/local processing: no server uploads, no account required, and no cloud storage.
- The author also mentioned being able to further explain the parsing approach and the data structures Google uses, indicating that the system focuses on specialized parsing and report generation for the Takeout format.

## Results
- The text **does not provide quantitative experimental results**; it gives no dataset size, processing speed, accuracy, or baseline comparison with other tools.
- The strongest concrete claim is that it can turn "hundreds of JSON files" from an "unreadable" state into a "clean, readable" report.
- The explicitly supported data types include search history, location data, YouTube activity, and more.
- The explicit privacy claim is: **data never leaves the browser**, meaning no server upload, no account, and no persistent storage.

## Link
- [https://news.ycombinator.com/item?id=47255521](https://news.ycombinator.com/item?id=47255521)
