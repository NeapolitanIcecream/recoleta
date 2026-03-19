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
language_code: en
---

# Mechanical Sympathy

## Summary
This article introduces SBE (Simple Binary Encoding), a binary encoding standard for low-latency financial message transmission. Its core goal is to reduce message encoding and decoding overhead to a level close to accessing in-memory structs directly. Its value lies in the fact that systems such as financial market data may process hundreds of thousands to tens of millions of messages per second, so encoding efficiency directly determines system latency, throughput, and hardware cost.

## Problem
- Financial systems need to handle extremely high message rates: exchange market data commonly reaches hundreds of thousands of messages per second, and aggregate feeds such as OPRA can peak at over **10 million messages/second**.
- Traditional representations such as **XML, JSON, FIX tag-value**, as well as some general-purpose binary protocols, consume substantial CPU in parsing, object allocation, copying, and backward access, and are often more expensive than the business logic itself.
- Low-latency scenarios require not only high throughput but also **predictable latency**; garbage collection, non-sequential memory access, and indirect addressing of variable-length fields all undermine this.

## Approach
- SBE uses **schema-driven binary encoding**: first define an XML schema, then generate static stubs in Java/C++/C# with a compiler, and use these stubs to read and write buffers sequentially.
- The core mechanism is simple: design messages with a layout similar to a **C struct**, arrange fixed-length fields in order at static offsets, and place **all variable-length fields at the end of the message**, avoiding backward access and pointer jumps.
- The implementation emphasizes **sequential streaming access, zero-copy, zero extra allocation, and no backward traversal**, to better exploit CPU caches and hardware prefetchers while reducing GC interference in managed languages.
- It supports two decoding modes: high-performance **compile-time generated stubs**, and **on-the-fly dynamic decoding** based on the schema intermediate representation (IR), the latter being suitable for log viewers and packet capture tools.
- Through versioning, trailing extension fields, alignment, and byte-order control, it achieves backward compatibility and hardware-friendly memory layout optimization.

## Results
- The article claims that compared with **Google Protocol Buffers (GPB)**, SBE can achieve about **16–25x** higher throughput, with lower and more stable latency.
- Encoding or decoding a typical market data message takes about **25ns**, while GPB on the same hardware takes about **1000ns**; the author says **XML and FIX tag-value** are “orders of magnitude” slower.
- In the Java benchmark (before optimization), **Car decode**: GPB **462.817 ops/ms** vs SBE **10436.476 ops/ms**, about **22.6x**.
- In the Java benchmark (before optimization), **Car encode**: GPB **326.018 ops/ms** vs SBE **11657.190 ops/ms**, about **35.8x**.
- In the Java benchmark (before optimization), **MarketData decode**: GPB **1148.050 ops/ms** vs SBE **34078.646 ops/ms**, about **29.7x**; **MarketData encode**: GPB **1242.252 ops/ms** vs SBE **29193.600 ops/ms**, about **23.5x**.
- Even after GPB optimization, GPB still lags significantly: **Car decode 619.467 ops/ms**, **Car encode 433.711 ops/ms**, **MarketData decode 2088.998 ops/ms**, **MarketData encode 1316.123 ops/ms**; the article also claims that implementations in all three languages can process typical financial messages in **the tens-of-nanoseconds range**, with C++ only slightly faster than Java and C# somewhat slower.

## Link
- [https://mechanical-sympathy.blogspot.com/](https://mechanical-sympathy.blogspot.com/)
