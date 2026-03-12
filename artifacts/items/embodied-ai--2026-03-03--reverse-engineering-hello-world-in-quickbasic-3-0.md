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
---

# Reverse engineering "Hello World" in QuickBASIC 3.0

## Summary
这是一篇针对 QuickBASIC 3.0 编译产物的逆向分析文章，试图解释为什么一句 `PRINT "Hello, world!"` 会生成一个异常复杂的 DOS 可执行程序。作者通过执行跟踪、内存转储和反汇编，重建了 HELLO.EXE 与 BRUN30.EXE 的装载、重定位和运行机制。

## Problem
- 要解决的问题是：**QuickBASIC 3.0 编译的最小程序到底如何在二进制层面工作**，尤其是 `HELLO.EXE` 与运行时 `BRUN30.EXE` 之间的关系。
- 这很重要，因为 QB30 的内部结构资料极少，弄清它的执行模型有助于后续分析大量使用该系统构建的 DOS 软件和游戏。
- 文章还揭示了一个实践难点：常见工具会被该可执行文件的异常 MZ 头信息误导甚至崩溃，导致常规静态分析失效。

## Approach
- 作者先用 **DOSBox Debug 的 heavy log** 记录完整执行轨迹，把一个打印 13 个字符的程序拆成约 **7905–8000 条汇编指令**逐步分析。
- 通过 `grep`/`awk` 处理 trace 与多次 **全内存转储**，定位关键中断、字符输出时刻、内存块创建、环境变量复制和参数处理等行为。
- 结合对 `HELLO.EXE` 与 `BRUN30.EXE` 的反汇编，作者发现 QB30 不是简单把一行 BASIC 变成极小 P-code，而是由前端程序先**手工装载运行时、分配/重划 DOS 内存块、读取 BRUN30、再自行完成重定位修复**。
- 文中还识别出一个关键机制：`HELLO.EXE` 启动时先跳过前面 **0x99 字节**的 stub，稍后再回跳执行这段代码，用它把自身大部分内容覆盖掉，以回收内存给运行时和数据区使用。

## Results
- 最直接的发现是：这个“Hello, world!” 程序执行大约 **8000 条汇编指令**；作者给出的具体 trace 行数为 **7905**。
- 程序在真正显示首字符前，大约先消耗了 **6400 个周期/trace steps**；之后每个后续字符还需要约 **30** 个步骤。输出通过 **INT 10h, AH=09h** 完成，而不是直接写显存。
- Trace 中共统计到 **291 次 `int` 指令**，平均大约每 **45** 条指令就有一次中断调用，说明大量工作在做 DOS/BIOS 级系统交互而非直接执行业务逻辑。
- 运行时装载阶段，`HELLO.EXE` 先读取 BRUN30 的小片段检查格式和版本（文中指出版本为 **5.6**），再依据代码大小 **0x0FE0 段**申请 DOS 内存，并把 BRUN30 的前 **64 KB**（跳过前 **0x200 字节**）与剩余约 **5 KB** 数据分开装入内存。
- 作者声称其中最“突破性”的结果不是性能提升，而是**首次系统性重建了 QB30 Hello World 的真实装载链路**：包括自建内存块头、环境复制、手工重定位、切换栈、以及通过 `repe movsw` 复制 **0x7FF8 字节（近 32 KB）**来自我覆盖释放空间。
- 文本没有给出标准学术基准上的准确率、F1、SOTA 等量化评测；最强的具体贡献是对 QB30 可执行格式与运行时启动流程给出了细粒度、可操作的逆向结论，并顺带修补了 Spice86/radare2 对异常 EXE 大小声明的处理问题。

## Link
- [https://marnetto.net/2026/03/01/brun-hello-world](https://marnetto.net/2026/03/01/brun-hello-world)
