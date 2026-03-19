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
language_code: en
---

# Mechanical Sympathy

## Summary
SBE (Simple Binary Encoding) is a binary message encoding scheme designed for low-latency financial systems, focused on solving slow encoding/decoding in high-frequency trading and market data processing. Its core value is that, while preserving the ability to express structured messages, it can push encoding/decoding latency down to the tens-of-nanoseconds range.

## Problem
- Financial market data throughput is extremely high: exchanges commonly produce **hundreds of thousands of messages per second**, and aggregate sources such as **OPRA can peak at over 10 million messages per second**; traditional encodings become a system bottleneck.
- Many systems still use representations such as **ASCII/FIX/XML/JSON**; parsing and transformation often consume more CPU than the business logic itself, resulting in high latency and large jitter.
- Low-latency trading is equally sensitive to **predictability**; frequent allocation, backtracking during parsing, copying, and non-sequential memory access harm tail latency and throughput.

## Approach
- Uses a **schema-first** approach: first define an XML message schema, then use a compiler to generate dedicated stubs for **Java/C++/C#**, and use those stubs to read and write messages directly on the buffer.
- The design enforces **sequential streaming access**: fixed-length fields are laid out at static offsets, repeating groups are expanded sequentially, and **variable-length fields (such as strings) are placed uniformly at the end of the message**, avoiding backtracking and indirect addressing.
- Uses **allocation-free** and **copy-free** mechanisms: flyweight stubs reuse objects and directly wrap memory, direct buffers, or memory-mapped files, reducing GC and extra copying.
- Through a memory layout close to a **C struct**, word alignment, default little-endian encoding, and direct buffer access, the machine-level behavior of generated code is made to approach hand-written high-performance implementations as closely as possible.
- Also supports **on-the-fly decoding**: the compiler generates an intermediate representation (IR) and binary schema metadata, making it suitable for dynamic decoding scenarios such as log viewers and packet capture tools.

## Results
- The author claims SBE can achieve overall throughput of about **16–25× that of Google Protocol Buffers (GPB)**, while also delivering “very low and predictable” latency.
- Encoding/decoding latency for typical market data messages is about **~25ns**, while GPB on the same hardware is about **~1000ns**; the article also notes that **XML and FIX tag-value** are several orders of magnitude slower.
- In the Java benchmark (**Car Decode**), SBE achieves **10436.476 ops/ms**, while optimized GPB achieves **619.467 ops/ms**, about **16.8×**.
- In the Java benchmark (**Car Encode**), SBE achieves **11657.190 ops/ms**, while optimized GPB achieves **433.711 ops/ms**, about **26.9×**.
- In the Java benchmark (**MarketData Decode**), SBE achieves **34078.646 ops/ms**, while optimized GPB achieves **2088.998 ops/ms**, about **16.3×**.
- In the Java benchmark (**MarketData Encode**), SBE achieves **29193.600 ops/ms**, while optimized GPB achieves **1316.123 ops/ms**, about **22.2×**.

## Link
- [https://mechanical-sympathy.blogspot.com/](https://mechanical-sympathy.blogspot.com/)
