---
source: hn
url: https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year
published_at: '2026-03-15T23:34:35'
authors:
- susam
topics:
- spreadsheet-compatibility
- date-serialization
- leap-year-bug
- legacy-software
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Excel incorrectly assumes that the year 1900 is a leap year

## Summary
This article explains that Excel’s incorrect treatment of the year 1900 as a leap year is not merely a defect, but a historical design choice retained for compatibility with Lotus 1-2-3. It discusses the costs and benefits of correcting this behavior and concludes that keeping the status quo is more reasonable.

## Problem
- The issue to be addressed is: explaining why Excel incorrectly treats 1900 as a leap year, and why this historical error has not been fixed.
- This matters because the date serial system affects large numbers of spreadsheets, formula results, and compatibility with other software.
- If handled improperly, changing this behavior would shift dates throughout existing documents and disrupt established workflows.

## Approach
- The core mechanism is simple: Excel inherited Lotus 1-2-3’s date serial system and treats 1900 as a leap year to preserve file and date-calculation compatibility.
- The article uses a compatibility tradeoff analysis rather than proposing a new algorithm: it compares the system-wide effects of “fixing the error” versus “preserving historical behavior.”
- It points out that after a fix, nearly all dates in existing worksheets would decrease by 1 day, and related date formulas might also require manual adjustment.
- At the same time, results from functions like `WEEKDAY` would change, and Excel would lose compatibility with other software that uses the same date serial system.
- Therefore, Microsoft chose to preserve this special case and accept only a more limited problem: weekday values may be incorrect for dates before March 1, 1900.

## Results
- The article does not provide experimental data, benchmark tests, or standard evaluation metrics, so there are no quantitative results to report.
- The strongest concrete conclusion is that if this issue were corrected, **nearly all** dates in current Excel worksheets and other documents would **decrease by 1 day**.
- Another specific impact is that the `WEEKDAY` function returns incorrect values for dates **before March 1, 1900**; Microsoft says this issue is relatively rare because most users do not use dates in that range.
- The article explicitly states that, aside from **1900**, Excel handles other leap years correctly, including cases like **2100**, which is a century year but not a leap year.
- The central claim is not a performance breakthrough but a product decision: to maintain compatibility with Lotus 1-2-3 and related date systems, preserving this historical behavior has a lower overall cost than fixing it.

## Link
- [https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year)
