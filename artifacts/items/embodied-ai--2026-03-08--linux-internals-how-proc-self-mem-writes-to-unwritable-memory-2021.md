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
---

# Linux Internals: How /proc/self/mem writes to unwritable memory (2021)

## Summary
本文解释了 Linux 中 `/proc/self/mem` 的一个少见但有意保留的特性：它可以把数据写入进程中原本“不可写”的虚拟内存页。核心意义在于说明内核并不必须受用户态页权限的直接约束，因为它可以通过重新映射物理页来绕过这些限制。

## Problem
- 文章要解决的问题是：为什么通过 `/proc/*/mem` 写内存时，即使目标虚拟页被标记为只读或代码段不可写，写入仍然能成功。
- 这很重要，因为它关系到 Linux 内核、MMU、页表权限、Copy-on-Write 与调试/JIT 等系统机制之间的真实边界。
- 它也回答了一个更深层的问题：CPU 的写保护机制在多大程度上真的能限制内核访问内存。

## Approach
- 作者先用一个最小化实验演示现象：对 `mmap(PROT_READ)` 的只读页和 libc 的 `getchar` 代码页，通过 `/proc/self/mem` 直接写入数据。
- 然后分析 x86-64 上两个相关硬件机制：`CR0.WP`（内核写保护）和 `CR4.SMAP`（限制内核访问用户空间），说明它们看似相关但不是关键原因。
- 关键实现路径是 Linux 内核中的 `mem_rw() -> access_remote_vm() -> get_user_pages_remote() -> kmap() -> copy_to_user_page()`。
- 真正实现“打穿”语义的核心机制是 `get_user_pages_remote()` 使用 `FOLL_FORCE`：即使目标 VMA 没有 `VM_WRITE`，也继续解析并获取对应物理页。
- 之后内核把该物理页映射到自己的可写虚拟地址空间，再用类似 `memcpy` 的方式写入；因此它不是“直接写原用户虚拟地址”，而是“通过内核自己的 RW 映射写同一物理页”。

## Results
- 实验结果显示，对一个 `PROT_READ` 映射页写入 4 字节 `0x40 0x41 0x41 0x41` 后，程序成功读回 `mymap[0] = 0x41414140`，证明只读页被成功修改。
- 对 libc 的 `getchar` 入口写入 1 字节 `0xCC`（x86-64 断点指令）后，再次调用 `getchar` 触发 `SIGTRAP`，证明可执行代码页也被成功补丁化。
- 文章没有给出基准测试、吞吐量、准确率或大规模数据集指标；其“结果”主要是机制验证与内核源码级解释，而非传统论文中的定量评测。
- 它明确声称，这种行为是**有意设计**而非漏洞，并被 Julia JIT 编译器、rr 调试器等项目实际使用。
- 它还指出，私有映射（如 libc 的 `MAP_PRIVATE` 场景）上的写入会遵守 CoW 语义：写入效果只在当前进程可见，而不会直接污染共享底层映射。

## Link
- [https://offlinemark.com/an-obscure-quirk-of-proc/](https://offlinemark.com/an-obscure-quirk-of-proc/)
