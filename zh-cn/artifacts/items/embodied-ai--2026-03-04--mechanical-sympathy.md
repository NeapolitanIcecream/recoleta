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
- protocol-design
- code-generation
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Mechanical Sympathy

## Summary
SBE（Simple Binary Encoding）是一种面向低延迟金融系统的二进制消息编码方案，重点解决高频交易和市场数据处理中编解码过慢的问题。其核心价值是在保持结构化消息表达能力的同时，把编解码延迟压到几十纳秒量级。

## Problem
- 金融市场数据吞吐极高：交易所常见每秒**数十万到数十万级消息**，聚合源如 **OPRA 峰值可超过 1000 万条/秒**，传统编码会成为系统瓶颈。
- 许多系统仍使用 **ASCII/FIX/XML/JSON** 等表示，解析和转换常常比业务逻辑本身更耗 CPU，导致延迟高且抖动大。
- 低延迟交易对**可预测性**同样敏感；频繁分配、回溯解析、拷贝和非顺序内存访问会破坏尾延迟与吞吐表现。

## Approach
- 使用 **schema-first** 方式：先定义 XML 消息 schema，再由编译器生成 **Java/C++/C#** 的专用 stubs，用这些 stubs 直接在 buffer 上读写消息。
- 设计上强制**顺序流式访问**：固定长度字段按静态 offset 排列，重复组顺序展开，**可变长字段（如字符串）统一放在消息末尾**，避免回溯和间接寻址。
- 采用 **allocation-free** 与 **copy-free** 机制：flyweight stubs 复用对象，直接包装内存/直接缓冲区/映射文件，减少 GC 与额外复制。
- 通过接近 **C struct** 的内存布局、字对齐、little-endian 默认编码和直接缓冲访问，把生成代码的机器级表现尽量逼近手写高性能实现。
- 额外支持 **on-the-fly decoding**：编译器生成中间表示（IR）和二进制 schema 元数据，便于日志查看器、抓包工具等动态解码场景使用。

## Results
- 作者声称 SBE 的总体吞吐可达到 **Google Protocol Buffers（GPB）的约 16–25 倍**，并具有“很低且可预测”的延迟。
- 典型市场数据消息的编解码延迟约为 **~25ns**，而同硬件上 GPB 约为 **~1000ns**；文中还指出 **XML 和 FIX tag-value** 会比这更慢几个数量级。
- Java 基准（**Car Decode**）中，SBE 为 **10436.476 ops/ms**，优化后 GPB 为 **619.467 ops/ms**，约 **16.8×**。
- Java 基准（**Car Encode**）中，SBE 为 **11657.190 ops/ms**，优化后 GPB 为 **433.711 ops/ms**，约 **26.9×**。
- Java 基准（**MarketData Decode**）中，SBE 为 **34078.646 ops/ms**，优化后 GPB 为 **2088.998 ops/ms**，约 **16.3×**。
- Java 基准（**MarketData Encode**）中，SBE 为 **29193.600 ops/ms**，优化后 GPB 为 **1316.123 ops/ms**，约 **22.2×**。

## Link
- [https://mechanical-sympathy.blogspot.com/](https://mechanical-sympathy.blogspot.com/)
