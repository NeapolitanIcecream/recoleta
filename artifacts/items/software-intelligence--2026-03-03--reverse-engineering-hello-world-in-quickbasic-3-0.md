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
---

# Reverse engineering "Hello World" in QuickBASIC 3.0

## Summary
这篇文章通过逆向一个由 QuickBASIC 3.0 编译的最小程序 `10 PRINT "Hello, world!"`，重建了 QB30 可执行文件与运行时 `BRUN30.EXE` 的加载、重定位和执行机制。核心价值在于揭示一种资料稀缺的 1987 年 BASIC 编译/运行模型，为分析同类 DOS 软件与游戏提供方法论和结构认知。

## Problem
- 要解决的问题是：**QuickBASIC 3.0 编译出的 EXE 到底如何组织、加载并运行 BASIC 程序**，因为现有文献很少，而且 QB30 与 QB4/4.5 的模型明显不同。
- 这很重要，因为许多历史 DOS 游戏/工具由 QB30 构建；若不了解其二进制结构，就很难逆向分析、修复或保存这些软件。
- 连最简单的 `Hello, world!` 都能让常见工具崩溃或误判，说明 QB30 产物存在非标准/反直觉的装载细节，值得系统拆解。

## Approach
- 作者选取最小样本 `HELLO.EXE`，配合运行时 `BRUN30.EXE`，把它当作“受控实验对象”，先理解最简单程序，再迁移到更复杂的 QB30 软件。
- 核心方法非常直接：**先抓完整执行轨迹，再逐条指令对照内存变化和反汇编推理程序意图**。主要工具是 DOSBox Debug 的 heavy log、内存转储、grep/awk 文本处理，以及 Ghidra/radare2/Spice86 的辅助分析与修补。
- 机制上，作者发现 QB30 的 `HELLO.EXE` 并不是一个“只装少量 P-code 的薄壳”。它会自己完成一系列类似小型操作系统/加载器的工作：划分内存块、复制环境变量、搜索并加载 `BRUN30.EXE`、读取其代码/数据、**手动扫描并应用重定位表**，然后重排内存并把自身大部分代码覆盖掉，以腾出内存给运行时和程序。
- 同时，文章指出静态工具初始失败的原因之一是 EXE 头声明的镜像大小大于文件实际大小；作者因此修补了 Spice86 和 radare2 的相关处理逻辑。

## Results
- 最显著的发现是：一个仅打印 13 个字符的 QB30 `Hello, world!`，**执行大约 8000 条汇编指令**；文中 DOSBox 轨迹统计为 **7905 行**，远超直觉预期。
- 中断调用非常频繁：作者统计 **7905** 条轨迹中有 **291** 条 `int`，约为**每 45 个周期一次中断**；这揭示了 QB30 运行模型高度依赖 DOS/BIOS 服务。
- 真正显示文本非常晚：第一次用于输出字符的 `INT 10h, AH=09h` 调用出现在大约 **第 6399 行附近**；文中还指出程序在显示第一个字母前耗费约 **6400 cycles**，之后每个后续字符约再花 **30 cycles**。
- `HELLO.EXE` 在加载 `BRUN30.EXE` 时，先读取极小片段验证格式和版本，识别到运行时代码大小为 **0x0FE0 paragraphs**；随后把前 **64 KB** 代码段装入内存，并把剩余约 **5 KB** 作为数据单独读取。
- 手工重定位成本极高：作者指出 **cycles 827–2750** 都在扫描 `BRUN30` 的重定位表并修正指针，约占整个执行轨迹的 **25%**。
- 文章还给出多个具体结构性结论：程序早期创建了大小分别为 **0x20、0x10、0x1000 paragraphs** 的内存区；后续用一条 `repe movsw` 复制 **0x7FF8 bytes**（约 **32 KB**）覆盖自身主体代码，只保留前部 **0x99 bytes** 存根继续执行。这些都是对 QB30 装载机制的强证据，而非仅停留在猜测层面。

## Link
- [https://marnetto.net/2026/03/01/brun-hello-world](https://marnetto.net/2026/03/01/brun-hello-world)
