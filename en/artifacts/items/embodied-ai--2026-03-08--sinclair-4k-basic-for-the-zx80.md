---
source: hn
url: https://troypress.com/sinclair-4k-basic-for-the-zx80/
published_at: '2026-03-08T23:23:07'
authors:
- punkpeye
topics:
- tiny-basic
- retro-computing
- basic-interpreter
- memory-optimization
- tokenization
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Sinclair 4K Basic for the ZX80

## Summary
This article reviews the Sinclair ZX80's 4K BASIC, focusing on its efficient design under extremely limited memory through keyboard-level keyword tokenization, special character encoding, and compact variable management. Its significance lies in showing how early home computer languages made system-level trade-offs around the harsh constraint of 1KB RAM.

## Problem
- The problem to solve was how to provide a usable BASIC interpreter and interactive programming environment on extremely constrained hardware with only **1KB RAM**.
- This mattered because memory had to store not only programs but also the screen display; the larger the program, the smaller the visible screen, directly affecting programmability and user experience.
- At the same time, it still had to balance parsing efficiency, input convenience, and basic graphics/string-processing capability, without relying on abundant memory like larger systems could.

## Approach
- The core mechanism was to **convert BASIC keywords directly into tokens at the keyboard input stage**, rather than entering characters first and having the interpreter parse them later; this reduced storage overhead and sped up syntax processing.
- The ZX80 also used a **custom non-ASCII character set**, with high-value character codes directly representing complete keywords, further saving screen RAM.
- **Syntax checking** was performed during input, and erroneous lines could not be saved; this reduced later parsing burden, but also limited editing flexibility, and each line could contain only one statement.
- In variable management, it did not reserve fixed slots for all variables, but instead used a **symbol table supporting long variable names**; this was more memory-efficient than static allocation.
- String processing relied on a small set of primitive functions, such as **CODE()** to get the first character code and **TL$()** to remove the first character, achieving character-by-character parsing with minimal functionality.

## Results
- The article **does not provide formal experimental metrics or benchmark results**; it is mainly a historical/technical commentary on the implementation.
- The clearest quantitative constraint is that the machine shipped with only **1KB RAM**, and with a full **32×24** screen display, only **384 bytes** of memory remained available to the programmer.
- Conversely, if a program reached **990 bytes**, the screen would be reduced to only **1 line of visible characters**, showing that program storage and display directly competed for the same RAM.
- Compared with some contemporary Tiny BASIC/Level I BASIC designs, the ZX80 supported **integer variable names of arbitrary length** (subject to RAM limits), **26 string variables A$–Z$**, and numeric or string arrays, reflecting a more flexible memory organization.
- The trade-offs were also clear: it lacked **INKEY$**, had no **DATA/READ**, no **LEN**, and usually required explicit assignment forms like **LET X=X+1**, which limited the kinds of programs that could be written, especially games.

## Link
- [https://troypress.com/sinclair-4k-basic-for-the-zx80/](https://troypress.com/sinclair-4k-basic-for-the-zx80/)
