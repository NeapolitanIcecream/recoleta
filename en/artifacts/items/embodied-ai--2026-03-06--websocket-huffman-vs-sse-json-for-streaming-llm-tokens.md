---
source: hn
url: https://github.com/vidur2/token_entropy_encoder
published_at: '2026-03-06T23:47:08'
authors:
- vidur2
topics:
- llm-streaming
- websocket
- huffman-coding
- bandwidth-optimization
- wasm
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# WebSocket+Huffman vs. SSE+JSON for streaming LLM tokens

## Summary
This work proposes a transport-layer optimization for LLM streaming outputs: replacing **SSE + JSON text** with **WebSocket + Huffman-encoded token IDs**. The core goal is to reduce bandwidth, server CPU, and interaction latency without changing the generated content, but the current evidence mainly comes from a proof of concept and simulated benchmarks.

## Problem
- Existing LLM streaming outputs typically follow **text → JSON → UTF-8 → SSE/HTTP**, which introduces representation-layer redundancy, wasting bandwidth and increasing parsing and encoding overhead.
- The server has to convert tokens into text and wrap them in JSON, after which the client parses them back, increasing server CPU load and limiting scalability under high concurrency.
- This matters because code completion, chat, and mobile scenarios are highly sensitive to **low latency, low bandwidth, and high concurrency**; however, standard APIs usually return text rather than token IDs, making this optimization difficult to deploy.

## Approach
- The core method is simple: **send token IDs instead of text**, and apply **Huffman encoding** to the token IDs based on the tokenizer vocabulary distribution, compressing directly at the “semantic symbol layer” rather than the byte layer.
- The client uses a **Rust → WASM** decoder to incrementally decode the bitstream in the browser or Node.js, then detokenize/display it, shifting part of the token→text decoding cost to the client.
- The transport layer uses **WebSocket binary frames**, with frames containing version, codec id, codebook epoch, payload length, and CRC; it supports periodic reset, desynchronization prevention, and partial-frame decoding.
- The coding distribution can start from a global corpus prior and combine it with the user’s historical tokens for **Bayesian updating**, periodically rebuilding the Huffman tree to adapt to the user’s topic/language style and improve compression over long conversations.
- The implementation provides a Rust Huffman library, a roughly **160KB** WASM module, Node.js examples, and comparative benchmarks; however, it is **not yet integrated with a real LLM inference backend** and currently relies mainly on a mock server simulation.

## Results
- The author claims that in mock benchmarks, compared with **SSE+JSON**, **WebSocket+Huffman** achieves a **40–60% reduction in bandwidth**; the most specific figure given is **60% bandwidth savings (3 vs 8 bytes/token)**.
- In terms of latency/speed, the author reports: **28.5% faster for 50-token inline completions**, **12.1% faster for 100-token small completions**, and **6.4% faster for 5000-token large completions**.
- The writeup also claims **about 70% server CPU reduction**, and based on that infers that a “**single server could serve about 3x more users**”; however, these conclusions come from a proof-of-concept environment rather than a real online inference system.
- In the comparative conclusion, the author says **WS+Huffman won in 3 of 5 scenarios**, indicating that the gains are more skewed toward short completions, frequent interactions, and bandwidth-sensitive scenarios rather than all workloads.
- Important limitations: **no real LLM server integration**, **standard APIs do not return token IDs**, **multi-model support requires the tokenizer to be fixed at build time**, and **there is still no real production testing**; therefore, the results are better interpreted as evidence that “protocol overhead can be significantly reduced,” rather than as production-validated system gains.

## Link
- [https://github.com/vidur2/token_entropy_encoder](https://github.com/vidur2/token_entropy_encoder)
