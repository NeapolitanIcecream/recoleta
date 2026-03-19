---
source: hn
url: https://offlinemark.com/an-obscure-quirk-of-proc/
published_at: '2026-03-08T22:50:55'
authors:
- medbar
topics:
- linux-kernel
- virtual-memory
- procfs
- memory-protection
- x86-64
relevance_score: 0.27
run_id: materialize-outputs
language_code: en
---

# Linux Internals: How /proc/self/mem writes to unwritable memory (2021)

## Summary
This article explains why `/proc/self/mem` in Linux can write to user-space memory that is supposedly “unwritable,” and shows that this is not a vulnerability but semantics intentionally provided by the kernel. The core conclusion is: the kernel does not write directly through the original user virtual address, but instead bypasses the write protection on that virtual address by resolving the page tables and remapping the physical page.

## Problem
- The article addresses the question: why does writing memory through `/proc/*/mem` still succeed even when the target page is marked read-only.
- This matters because it relates to understanding the Linux kernel, the MMU, page permissions, Copy-on-Write, and more broadly “whether hardware can actually restrict the kernel.”
- It also directly affects real system behavior and tool implementations, since projects such as the Julia JIT and rr debugger intentionally rely on this “punch through” semantics.

## Approach
- The author first presents a reproducible experiment: write data to an anonymous page mapped with `PROT_READ`, then write `0xcc` to the code page of libc’s `getchar`; if subsequent execution triggers `SIGTRAP`, that proves the code page write succeeded.
- The article then analyzes two relevant hardware mechanisms on x86-64: `CR0.WP` (kernel write protection) and `CR4.SMAP` (restricting kernel access to user-space memory), explaining that they seem at first glance as though they would prevent such writes.
- It then dives into the Linux kernel implementation: the write path for `/proc/*/mem` enters `mem_rw()`, which then calls `access_remote_vm()`.
- The key mechanism is that `get_user_pages_remote()` uses `FOLL_FORCE`, which ignores the target VMA’s unwritable restriction during page-table traversal and, when necessary, triggers a simulated page fault to handle CoW.
- The kernel then uses `kmap()` to map the target physical page into its own writable kernel virtual address space, and uses `copy_to_user_page()` (essentially similar to `memcpy`) to complete the write, thereby bypassing the permission checks on the original user virtual address.

## Results
- In the experiment, after writing 4 bytes `0x40 0x41 0x41 0x41` to a `PROT_READ` mapped page, the program successfully reads back `mymap[0] = 0x41414140`, proving that the read-only page was modified.
- In the experiment, after writing `0xcc` to the first byte of libc’s `getchar` function, calling `getchar` again triggers `SIGTRAP`, proving that the executable code page was also successfully patched.
- The article does not provide benchmark results, accuracy metrics, or large-scale evaluation data; its main “results” are mechanism-level conclusions that can be validated and demonstrated by running the code.
- Mechanistic conclusion 1: the “punch through” semantics of `/proc/*/mem` mainly come from `get_user_pages_remote(..., FOLL_FORCE)` forcibly bypassing unwritable VMAs.
- Mechanistic conclusion 2: what actually performs the write is not a forced write through the original user virtual address, but rather “locate the physical page via the page tables -> map it into the kernel RW address space -> memcpy,” so `CR0.WP` is not the decisive obstacle.
- Mechanistic conclusion 3: memory permissions are bound to the virtual mapping used to access a physical page, rather than to the physical page itself.

## Link
- [https://offlinemark.com/an-obscure-quirk-of-proc/](https://offlinemark.com/an-obscure-quirk-of-proc/)
