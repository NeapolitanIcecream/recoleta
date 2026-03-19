---
source: hn
url: https://marnetto.net/2026/03/01/brun-hello-world
published_at: '2026-03-03T23:51:15'
authors:
- avadodin
topics:
- reverse-engineering
- quickbasic
- dos-executable
- x86-real-mode
- binary-analysis
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Reverse engineering "Hello World" in QuickBASIC 3.0

## Summary
This is a reverse-engineering article on the output produced by QuickBASIC 3.0, attempting to explain why a single line, `PRINT "Hello, world!"`, generates an unusually complex DOS executable. Through execution tracing, memory dumps, and disassembly, the author reconstructs the loading, relocation, and execution mechanisms of HELLO.EXE and BRUN30.EXE.

## Problem
- The problem to solve is: **how a minimal program compiled by QuickBASIC 3.0 actually works at the binary level**, especially the relationship between `HELLO.EXE` and the runtime `BRUN30.EXE`.
- This matters because documentation on QB30's internal structure is extremely scarce, and understanding its execution model helps with further analysis of DOS software and games built with this system.
- The article also reveals a practical difficulty: common tools are misled by the executable's unusual MZ header information and may even crash, causing conventional static analysis to fail.

## Approach
- The author first uses **DOSBox Debug's heavy log** to record the full execution trace, then analyzes step by step how a program that prints 13 characters expands into about **7905–8000 assembly instructions**.
- By processing traces with `grep`/`awk` and using multiple **full memory dumps**, the author identifies key interrupts, the moments when characters are output, memory block creation, environment variable copying, parameter handling, and other behaviors.
- Combined with disassembly of `HELLO.EXE` and `BRUN30.EXE`, the author finds that QB30 does not simply turn one line of BASIC into minimal P-code; instead, a frontend program first **manually loads the runtime, allocates/repartitions DOS memory blocks, reads BRUN30, and then performs relocation fixups itself**.
- The article also identifies a key mechanism: when `HELLO.EXE` starts, it first skips over a **0x99-byte** stub, then later jumps back to execute that code, using it to overwrite most of its own contents and reclaim memory for the runtime and data area.

## Results
- The most direct finding is that this “Hello, world!” program executes about **8000 assembly instructions**; the specific trace line count given by the author is **7905**.
- Before the program actually displays the first character, it consumes about **6400 cycles/trace steps**; after that, each subsequent character still requires about **30** steps. Output is performed via **INT 10h, AH=09h**, rather than by writing directly to video memory.
- The trace counts a total of **291 `int` instructions**, averaging about one interrupt call every **45** instructions, showing that much of the work is spent on DOS/BIOS-level system interaction rather than directly executing application logic.
- During the runtime loading stage, `HELLO.EXE` first reads a small fragment of BRUN30 to check its format and version (identified in the article as version **5.6**), then allocates DOS memory based on a code size of **0x0FE0 segments**, and loads the first **64 KB** of BRUN30 (skipping the first **0x200 bytes**) separately from the remaining roughly **5 KB** of data.
- The author claims that the most “breakthrough” result is not better performance, but the **first systematic reconstruction of the real loading chain of QB30 Hello World**: including custom memory block headers, environment copying, manual relocation, stack switching, and using `repe movsw` to copy **0x7FF8 bytes (nearly 32 KB)** for self-overwriting to free space.
- The text does not provide quantitative evaluation in terms of standard academic benchmarks such as accuracy, F1, or SOTA; its strongest concrete contribution is a fine-grained, actionable reverse-engineering account of the QB30 executable format and runtime startup process, along with fixes to Spice86/radare2's handling of abnormal EXE size declarations.

## Link
- [https://marnetto.net/2026/03/01/brun-hello-world](https://marnetto.net/2026/03/01/brun-hello-world)
