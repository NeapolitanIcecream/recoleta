---
source: hn
url: https://marnetto.net/2026/03/01/brun-hello-world
published_at: '2026-03-03T23:51:15'
authors:
- avadodin
topics:
- reverse-engineering
- dos-binaries
- quickbasic
- runtime-loader
- binary-analysis
relevance_score: 0.27
run_id: materialize-outputs
language_code: en
---

# Reverse engineering "Hello World" in QuickBASIC 3.0

## Summary
This article reconstructs the loading, relocation, and execution mechanisms of QB30 executables and the runtime `BRUN30.EXE` by reverse engineering a minimal program compiled with QuickBASIC 3.0: `10 PRINT "Hello, world!"`. Its core value lies in revealing a poorly documented 1987 BASIC compilation/runtime model, providing methodology and structural insight for analyzing similar DOS software and games.

## Problem
- The problem to solve is: **how exactly does an EXE compiled by QuickBASIC 3.0 organize, load, and run a BASIC program**, since existing documentation is scarce and the QB30 model is clearly different from QB4/4.5.
- This matters because many historical DOS games and tools were built with QB30; without understanding their binary structure, it is difficult to reverse engineer, repair, or preserve such software.
- Even the simplest `Hello, world!` can crash common tools or trigger incorrect interpretations, showing that QB30 outputs contain nonstandard or counterintuitive loading details worth systematically dissecting.

## Approach
- The author selects the minimal sample `HELLO.EXE`, together with the runtime `BRUN30.EXE`, and treats it as a "controlled experimental subject": first understand the simplest program, then transfer that understanding to more complex QB30 software.
- The core method is very direct: **first capture the complete execution trace, then infer the program’s intent instruction by instruction by comparing memory changes with the disassembly**. The main tools are DOSBox Debug heavy logs, memory dumps, grep/awk text processing, and auxiliary analysis and patching with Ghidra/radare2/Spice86.
- Mechanistically, the author finds that QB30’s `HELLO.EXE` is not a "thin wrapper carrying only a small amount of P-code." It performs a series of tasks itself, much like a small operating system/loader: partitioning memory blocks, copying environment variables, searching for and loading `BRUN30.EXE`, reading its code/data, **manually scanning and applying the relocation table**, then rearranging memory and overwriting most of its own code to free space for the runtime and program.
- At the same time, the article points out that one reason static tools initially failed is that the EXE header declares an image size larger than the actual file size; the author therefore patched the relevant handling logic in Spice86 and radare2.

## Results
- The most striking finding is that a QB30 `Hello, world!` that prints only 13 characters **executes about 8,000 assembly instructions**; the DOSBox trace in the article counts **7,905 lines**, far beyond intuitive expectations.
- Interrupt calls are very frequent: the author counts **291** `int` instructions out of **7,905** trace lines, about **one interrupt every 45 cycles**; this reveals that the QB30 runtime model relies heavily on DOS/BIOS services.
- Actual text output occurs very late: the first `INT 10h, AH=09h` call used to print a character appears around **line 6399**; the article also notes that the program spends about **6400 cycles** before displaying the first letter, and then about **30 cycles** for each subsequent character.
- When loading `BRUN30.EXE`, `HELLO.EXE` first reads a tiny fragment to verify format and version, identifies the runtime code size as **0x0FE0 paragraphs**, then loads the first **64 KB** code segment into memory and reads the remaining roughly **5 KB** separately as data.
- Manual relocation is very costly: the author states that **cycles 827–2750** are spent scanning `BRUN30`’s relocation table and fixing pointers, accounting for about **25%** of the entire execution trace.
- The article also presents several specific structural conclusions: early in execution, the program creates memory regions of **0x20**, **0x10**, and **0x1000 paragraphs**; later it uses a `repe movsw` instruction to copy **0x7FF8 bytes** (about **32 KB**) and overwrite its own main code body, leaving only the first **0x99 bytes** of stub code to continue execution. These are strong pieces of evidence for the QB30 loading mechanism, rather than mere speculation.

## Link
- [https://marnetto.net/2026/03/01/brun-hello-world](https://marnetto.net/2026/03/01/brun-hello-world)
