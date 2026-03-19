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
- wasm
- token-compression
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# WebSocket+Huffman vs. SSE+JSON for streaming LLM tokens

## Summary
This work proposes a transport-layer optimization for LLM streaming output: use **WebSocket + Huffman-encoded token IDs** instead of the common **SSE + JSON text stream**. Its core goal is to reduce bandwidth, lower server CPU overhead, and improve perceived latency for real-time completions, but it is currently still a proof of concept based on a mock server.

## Problem
- Existing LLM streaming pipelines are typically **token → text → JSON → UTF-8 → network → browser parsing**, which introduces overhead from multiple representation and parsing layers, leading to bandwidth waste and additional latency.
- The server has to decode tokens into text and then package them for transport, which consumes CPU and limits scalability in high-concurrency scenarios.
- This problem matters because code completion, chat, and high-throughput online services all depend on low-latency streaming output; transport efficiency is especially important on mobile devices or weak network connections.

## Approach
- The core method is: **send token IDs directly instead of text**; then compress the token sequence using **Huffman coding** constructed from tokenizer vocabulary probabilities, and send it through WebSocket binary frames.
- The client uses a **Rust → WASM decoder** in the browser or on the Node.js side for incremental decompression and synchronization, offloading part of the server’s original decoding work to the client.
- At the protocol layer, it uses **framed binary messages** with version, codebook/epoch, payload length, and CRC, supporting periodic reset, desynchronization prevention, and partial-frame decoding, making it suitable for streaming UI updates.
- The author also proposes **adaptive token distribution**: starting from a global prior, performing Bayesian updating based on tokens already observed by the user, and rebuilding the Huffman tree within safety bounds to better match user-specific vocabulary distributions.
- In implementation terms, it is a runnable prototype: a Rust Huffman encoder/decoder, a WASM module, a WebSocket client, and a Node.js benchmark harness, but it has not yet been connected to a real LLM inference backend.

## Results
- The author claims that for **inline completions (50 tokens)**, **WebSocket+Huffman is 28.5% faster than SSE+JSON**.
- For **small completions (100 tokens)**, it reports **12.1% faster**; for **large completions (5000 tokens)**, it reports **6.4% faster**.
- In terms of bandwidth, the author reports **60% bandwidth savings**, with an example of **3 bytes/token vs 8 bytes/token**.
- The article also claims that compared with traditional **JSON+SSE**, it can achieve **40–60% lower bandwidth usage** and **70% lower server CPU usage**, and on that basis infers that a server could support **about 3x more users**.
- In the benchmark tests, **WS+Huffman won 3 out of 5 scenarios**.
- However, these results come from **mock benchmarks / mock server**, not end-to-end experiments on an actual inference system; the author explicitly notes that no real LLM server has yet been modified, so real-world effects still need validation.

## Link
- [https://github.com/vidur2/token_entropy_encoder](https://github.com/vidur2/token_entropy_encoder)
