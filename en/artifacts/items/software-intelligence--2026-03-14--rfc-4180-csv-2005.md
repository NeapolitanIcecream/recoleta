---
source: hn
url: https://www.rfc-editor.org/rfc/rfc4180
published_at: '2026-03-14T23:04:40'
authors:
- basilikum
topics:
- csv-format
- mime-type
- data-interoperability
- file-format-spec
- abnf
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# RFC 4180 – CSV (2005)

## Summary
This RFC does not propose a new algorithm; instead, it provides a common convention for the CSV format, which had long been widely used but lacked a formal definition, and it formally registers the `text/csv` MIME type. Its value lies in reducing ambiguous interpretations of CSV across different programs and improving interoperability in data exchange.

## Problem
- CSV was widely used for spreadsheets and data conversion, but there had previously been **no unified, formal specification**, leading different implementations to interpret format details differently.
- IANA had previously **not formally registered a MIME type for CSV**, while different systems had already begun using inconsistent type identifiers, affecting network transmission and software compatibility.
- This inconsistency creates interoperability risks for parsers, import/export tools, and operating systems when handling headers, line breaks, quotes, comma escaping, and related issues.

## Approach
- The document summarizes the CSV conventions that “most implementations roughly follow” and writes them down as a set of **clear textual rules**: one record per line, fields separated by commas, an optional header, and a consistent number of fields.
- It specifies a **quote-handling mechanism**: fields containing commas, line breaks, or double quotes should be enclosed in double quotes; double quotes inside a field are escaped using two double quotes.
- It provides an **ABNF grammar**, formalizing the CSV structure into rules such as `file/header/record/field`, making it easier for implementers to write parsers accordingly.
- It formally registers the **`text/csv`** media type and defines the optional parameters **`charset`** and **`header`** (`present`/`absent`).
- It recommends that implementations adopt a conservative-sending, liberal-receiving strategy, because many real-world CSV implementations still do not fully align.

## Results
- The most central outcome is the **formal registration of the MIME type `text/csv`**, resolving the earlier problem that CSV was common but had no official MIME registration.
- The document provides **7 specific format rules**, covering record line breaks, optional final-line line break, optional header, field separation, quote wrapping, special character handling, and double-quote escaping.
- It gives a complete **ABNF grammar definition**, including formal descriptions such as `file = [header CRLF] record *(CRLF record) [CRLF]`, which can directly guide implementation.
- It defines **2 optional MIME parameters**: `charset` and `header`; the valid values of `header` are **`present`** or **`absent`**.
- The document contains **no experimental data, benchmark tests, or performance metrics**, so there are no reportable results for accuracy, speed, datasets, or baseline comparisons.
- Its strongest concrete claim is that this RFC provides a common definition for CSV and significantly improves the foundation for interoperability across implementations through the registration of `text/csv`.

## Link
- [https://www.rfc-editor.org/rfc/rfc4180](https://www.rfc-editor.org/rfc/rfc4180)
