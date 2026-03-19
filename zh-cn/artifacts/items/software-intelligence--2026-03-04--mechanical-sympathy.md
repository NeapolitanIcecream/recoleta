---
source: hn
url: https://mechanical-sympathy.blogspot.com/
published_at: '2026-03-04T22:59:58'
authors:
- p0u4a
topics:
- binary-encoding
- low-latency-systems
- financial-messaging
- code-generation
- protocol-design
relevance_score: 0.32
run_id: materialize-outputs
language_code: zh-CN
---

# Mechanical Sympathy

## Summary
本文介绍了面向低延迟金融消息传输的二进制编解码标准 SBE（Simple Binary Encoding），核心目标是把消息编解码开销压到接近内存结构体访问的水平。其价值在于金融行情等系统每秒可处理数十万到上千万条消息，编码效率会直接决定系统延迟、吞吐与硬件成本。

## Problem
- 金融系统需要处理极高消息速率：交易所行情常见每秒数十万到数十万级消息，像 OPRA 聚合行情峰值可超过 **1000 万条/秒**。
- 传统表示方式如 **XML、JSON、FIX tag-value**，以及部分通用二进制协议，在解析、对象分配、拷贝和回溯访问上消耗大量 CPU，常常比业务逻辑本身更贵。
- 低延迟场景不仅要求高吞吐，还要求**可预测延迟**；垃圾回收、非顺序内存访问、变量字段间接寻址都会破坏这一点。

## Approach
- SBE 采用**模式驱动的二进制编码**：先定义 XML schema，再由编译器生成 Java/C++/C# 的静态 stub，用这些 stub 直接对 buffer 进行顺序读写。
- 核心机制很简单：把消息设计成类似 **C struct** 的布局，固定长度字段按静态偏移顺序排列，**可变长字段统一放在消息末尾**，避免回溯和指针跳转。
- 实现上强调**顺序流式访问、零拷贝、零额外分配、无回溯**，以更好利用 CPU cache 和硬件预取器，并降低托管语言中的 GC 干扰。
- 支持两种解码方式：高性能的**编译期生成 stub**，以及基于 schema 中间表示（IR）的**on-the-fly 动态解码**，后者适合日志查看器和抓包工具。
- 通过版本号、尾部扩展字段、对齐与字节序控制，实现向后兼容和贴近硬件的内存布局优化。

## Results
- 文中声称 SBE 相比 **Google Protocol Buffers (GPB)** 可达到约 **16–25 倍**更高吞吐，并具有更低且更稳定的延迟。
- 典型市场数据消息的编码或解码时间约为 **25ns**，而同硬件上的 GPB 约为 **1000ns**；作者称 **XML 和 FIX tag-value** 还要“慢几个数量级”。
- Java 基准（优化前）中，**Car decode**：GPB **462.817 ops/ms** vs SBE **10436.476 ops/ms**，约 **22.6x**。
- Java 基准（优化前）中，**Car encode**：GPB **326.018 ops/ms** vs SBE **11657.190 ops/ms**，约 **35.8x**。
- Java 基准（优化前）中，**MarketData decode**：GPB **1148.050 ops/ms** vs SBE **34078.646 ops/ms**，约 **29.7x**；**MarketData encode**：GPB **1242.252 ops/ms** vs SBE **29193.600 ops/ms**，约 **23.5x**。
- 即使在 GPB 优化后，GPB 仍明显落后：**Car decode 619.467 ops/ms**、**Car encode 433.711 ops/ms**、**MarketData decode 2088.998 ops/ms**、**MarketData encode 1316.123 ops/ms**；文中同时声称三种语言实现都能把典型金融消息处理做到**几十纳秒级**，且 C++ 仅略快于 Java，C# 稍慢。

## Link
- [https://mechanical-sympathy.blogspot.com/](https://mechanical-sympathy.blogspot.com/)
