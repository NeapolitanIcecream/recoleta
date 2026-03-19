---
source: hn
url: https://news.ycombinator.com/item?id=47255521
published_at: '2026-03-04T23:35:11'
authors:
- martinZak
topics:
- privacy-tools
- browser-based
- data-parsing
- google-takeout
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# TakeoutReader – Turn your Google Takeout JSON into a readable report

## Summary
TakeoutReader is a browser-side tool that parses raw JSON files exported from Google Takeout into readable reports. It focuses on solving the problem that personal data exports are difficult to understand, while emphasizing that data always remains in the local browser.

## Problem
- Google Takeout exports typically contain large numbers of JSON files, millisecond-level timestamps, GPS coordinates, and nested structures that ordinary users can hardly read directly.
- Although users can export their own data, they lack an easy way to view content such as search history, location records, and YouTube activity.
- Privacy is critical: if parsing depends on server uploads, users’ sensitive personal data faces additional risk.

## Approach
- Parse and organize multiple types of JSON data in Google Takeout into a unified, human-readable report.
- Perform processing directly in the browser, avoiding server uploads, account registration, or cloud storage.
- Provide structured extraction for common Google data types, such as search history, location data, and YouTube activity.
- Convert raw fields, such as timestamps, coordinates, and nested objects, into display formats that are easier to understand.

## Results
- The text does not provide formal paper experiments, benchmark data, or quantitative evaluation results.
- The explicit product claim is: **data never leaves the browser**, meaning no server uploads, no accounts, and no storage.
- Supported content for generating readable reports includes search history, location data, YouTube activity, and more, but no coverage or parsing accuracy figures are given.
- Compared with directly reading “hundreds of JSON files,” the core improvement is turning unreadable raw exports into consumable reports, but no quantitative comparison with other tools is provided.

## Link
- [https://news.ycombinator.com/item?id=47255521](https://news.ycombinator.com/item?id=47255521)
