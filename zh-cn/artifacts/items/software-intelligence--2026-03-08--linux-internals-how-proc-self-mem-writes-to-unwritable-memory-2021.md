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
language_code: zh-CN
---

# Linux Internals: How /proc/self/mem writes to unwritable memory (2021)

## Summary
本文解释了 Linux 中 `/proc/self/mem` 为何能够写入本应“不可写”的用户态内存，并说明这不是漏洞而是内核有意提供的语义。核心结论是：内核并不直接按原用户虚拟地址写，而是通过页表解析与重新映射物理页来绕过该虚拟地址上的写保护。

## Problem
- 文章要解决的问题是：为什么通过 `/proc/*/mem` 写内存时，即使目标页被标记为只读，写入仍然会成功。
- 这很重要，因为它关系到对 Linux 内核、MMU、页权限、Copy-on-Write 以及“硬件到底能否限制内核”的理解。
- 它也直接影响实际系统行为与工具实现，例如 Julia JIT 和 rr debugger 会主动依赖这种“punch through”语义。

## Approach
- 作者先给出一个可复现实验：向 `PROT_READ` 的匿名页写入数据，再向 libc 的 `getchar` 代码页写入 `0xcc`，若后续执行触发 `SIGTRAP`，就证明写代码页成功。
- 然后分析 x86-64 上两个相关硬件机制：`CR0.WP`（内核写保护）和 `CR4.SMAP`（限制内核访问用户态内存），说明它们表面上似乎会阻止这种写入。
- 接着深入 Linux 内核实现：`/proc/*/mem` 的写路径进入 `mem_rw()`，再调用 `access_remote_vm()`。
- 关键机制是 `get_user_pages_remote()` 使用 `FOLL_FORCE`，在页表遍历时忽略目标 VMA 的不可写限制，并在需要时触发模拟缺页来处理 CoW。
- 随后内核通过 `kmap()` 把目标物理页映射到自己的可写内核虚拟地址空间，再用 `copy_to_user_page()`（本质上类似 `memcpy`）完成写入，因此绕开了原用户虚拟地址上的权限检查。

## Results
- 实验中，对一个 `PROT_READ` 映射页写入 4 字节 `0x40 0x41 0x41 0x41` 后，程序成功读回 `mymap[0] = 0x41414140`，证明只读页被改写。
- 实验中，向 libc 的 `getchar` 函数首字节写入 `0xcc` 后，再次调用 `getchar` 触发了 `SIGTRAP`，证明可执行代码页也被成功打补丁。
- 文章没有提供基准测试、准确率或大规模评测数据；其主要“结果”是机制层面的可验证结论与可运行演示。
- 机制性结论 1：`/proc/*/mem` 的“punch through”语义主要来自 `get_user_pages_remote(..., FOLL_FORCE)` 对不可写 VMA 的强制穿透。
- 机制性结论 2：真正完成写入的不是对原用户虚拟地址强写，而是“页表定位物理页 -> 映射进内核 RW 地址空间 -> memcpy”，因此 `CR0.WP` 并不是决定性障碍。
- 机制性结论 3：内存权限是绑定在“访问该物理页所用的虚拟映射”上的，而不是绑定在物理页本身上。

## Link
- [https://offlinemark.com/an-obscure-quirk-of-proc/](https://offlinemark.com/an-obscure-quirk-of-proc/)
