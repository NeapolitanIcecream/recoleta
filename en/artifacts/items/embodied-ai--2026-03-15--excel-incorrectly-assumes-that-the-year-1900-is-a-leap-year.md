---
source: hn
url: https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year
published_at: '2026-03-15T23:34:35'
authors:
- susam
topics:
- excel-date-system
- leap-year-bug
- backward-compatibility
- spreadsheet-software
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Excel incorrectly assumes that the year 1900 is a leap year

## Summary
This article explains that Excel intentionally preserves the incorrect setting that “1900 was a leap year,” mainly to remain compatible with the Lotus 1-2-3 date serial system. It discusses the system-wide compatibility costs of fixing this error and why Microsoft chose to keep the status quo.

## Problem
- The issue addressed is: explaining why Excel **incorrectly treats 1900 as a leap year**, and whether this historical error should be corrected.
- This matters because Excel’s date system is widely used in worksheets, formulas, and cross-software data exchange; changing the underlying date rules would affect a large number of existing files and calculation results.
- The actual current impact is very limited: mainly that dates **before March 1, 1900** may return incorrect results in functions such as `WEEKDAY`.

## Approach
- The core mechanism is simple: Excel **continued the Lotus 1-2-3 date serial design**, treating 1900 as a leap year to preserve compatibility with serial dates and historical files.
- Microsoft did not propose a new algorithm, but instead made an **engineering tradeoff that prioritizes compatibility**: accepting a known historical error to avoid breaking existing workbooks and cross-program date interoperability.
- The article argues for this choice by comparing the consequences of “fixing the error” versus “maintaining the status quo”: the former would cause widespread date shifts, changes in function outputs, and broken compatibility, while the latter leaves only a rare edge-case issue.
- The article also explicitly limits the scope of the error: **only the year 1900** is handled incorrectly in this special way; Excel correctly handles other leap-year rules, including century years like 2100 that are not leap years.

## Results
- No experimental data or benchmarks are provided, so there are **no quantitative results** to report.
- The strongest conclusion in the article is that if this behavior were corrected, **nearly all dates in existing Excel worksheets would be reduced by 1 day**, requiring substantial manual repair of related formulas.
- The article also states that after correction, some functions (such as **`WEEKDAY`**) would return different values for historical dates, causing some worksheet formulas to behave differently.
- Another explicit conclusion is that fixing the issue would **break compatibility between Excel and other programs that use the same serial date system**.
- If the status quo is maintained, the article indicates there is only **1 main known problem**: `WEEKDAY` returns incorrect results for dates **before March 1, 1900**, and this usage scenario is “rare.”

## Link
- [https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year)
