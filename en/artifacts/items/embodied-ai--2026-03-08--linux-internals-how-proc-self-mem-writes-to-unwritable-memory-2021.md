---
source: hn
url: https://offlinemark.com/an-obscure-quirk-of-proc/
published_at: '2026-03-08T22:50:55'
authors:
- medbar
topics:
- linux-kernel
- procfs
- virtual-memory
- mmu
- copy-on-write
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Linux Internals: How /proc/self/mem writes to unwritable memory (2021)

## Summary
This article explains a rare but intentionally preserved feature of `/proc/self/mem` in Linux: it can write data into virtual memory pages in a process that are originally marked as “unwritable.” The core significance is that the kernel does not have to be directly constrained by user-space page permissions, because it can bypass those restrictions by remapping physical pages.

## Problem
- The article addresses the question of why writes through `/proc/*/mem` can still succeed even when the target virtual page is marked read-only or the code segment is non-writable.
- This matters because it concerns the real boundary between system mechanisms such as the Linux kernel, the MMU, page table permissions, Copy-on-Write, and debugging/JIT.
- It also answers a deeper question: to what extent the CPU’s write-protection mechanisms can actually restrict the kernel’s access to memory.

## Approach
- The author first demonstrates the phenomenon with a minimal experiment: writing directly through `/proc/self/mem` to a read-only page created with `mmap(PROT_READ)` and to the `getchar` code page in libc.
- Then the article analyzes two related hardware mechanisms on x86-64: `CR0.WP` (kernel write protection) and `CR4.SMAP` (restricting kernel access to user space), explaining that although they seem relevant, they are not the key reason.
- The key implementation path in the Linux kernel is `mem_rw() -> access_remote_vm() -> get_user_pages_remote() -> kmap() -> copy_to_user_page()`.
- The core mechanism that enables the “punch through” semantics is that `get_user_pages_remote()` uses `FOLL_FORCE`: even if the target VMA does not have `VM_WRITE`, it still resolves and obtains the corresponding physical page.
- After that, the kernel maps that physical page into its own writable virtual address space and writes to it using a `memcpy`-like method; therefore, it is not “writing directly to the original user virtual address,” but rather “writing the same physical page through the kernel’s own RW mapping.”

## Results
- The experimental results show that after writing 4 bytes `0x40 0x41 0x41 0x41` to a `PROT_READ` mapped page, the program successfully reads back `mymap[0] = 0x41414140`, proving that the read-only page was successfully modified.
- After writing 1 byte `0xCC` (the x86-64 breakpoint instruction) to the entry of libc’s `getchar`, calling `getchar` again triggers `SIGTRAP`, proving that the executable code page was also successfully patched.
- The article does not provide benchmark tests, throughput, accuracy, or large-scale dataset metrics; its “results” are mainly mechanism validation and kernel source-level explanation rather than the quantitative evaluation typical of a traditional paper.
- It explicitly states that this behavior is **intentional design**, not a vulnerability, and is actually used by projects such as the Julia JIT compiler and the rr debugger.
- It also points out that writes on private mappings (such as libc in a `MAP_PRIVATE` scenario) still obey CoW semantics: the effects of the write are visible only to the current process and do not directly contaminate the shared underlying mapping.

## Link
- [https://offlinemark.com/an-obscure-quirk-of-proc/](https://offlinemark.com/an-obscure-quirk-of-proc/)
