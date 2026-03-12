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
---

# WebSocket+Huffman vs. SSE+JSON for streaming LLM tokens

## Summary
这篇工作提出一种面向 LLM 流式输出的传输层优化：用 **WebSocket + Huffman 编码的 token ID** 替代常见的 **SSE + JSON 文本流**。其核心目标是减少带宽、降低服务器 CPU 开销，并改善实时补全的感知延迟，但目前仍是基于 mock server 的概念验证。

## Problem
- 现有 LLM 流式链路通常是 **token → text → JSON → UTF-8 → 网络 → 浏览器解析**，存在多层表示与解析开销，导致带宽浪费和额外延迟。
- 服务器端需要把 token 解码成文本再封装传输，这会消耗 CPU，限制高并发场景下的扩展性。
- 这个问题重要，因为代码补全、聊天和高吞吐在线服务都依赖低延迟流式输出；在移动端或弱网环境下，传输效率尤其关键。

## Approach
- 核心方法是：**直接传 token ID，而不是传文本**；再用基于 tokenizer 词表概率构造的 **Huffman 编码**压缩 token 序列，通过 WebSocket 二进制帧发送。
- 客户端在浏览器或 Node.js 侧使用 **Rust → WASM 解码器**进行增量解压与同步，把服务器原本的部分解码工作卸载到客户端。
- 协议层使用带版本、codebook/epoch、payload length、CRC 的 **framed binary messages**，支持周期性 reset、防失步和部分帧解码，适合流式 UI 更新。
- 作者还提出 **自适应 token 分布**：从全局先验开始，根据用户已观测 token 做 Bayesian updating，并在安全边界重建 Huffman 树，以进一步贴近用户特定词汇分布。
- 实现上是可运行原型：Rust Huffman 编码器/解码器、WASM 模块、WebSocket 客户端和 Node.js benchmark harness，但尚未接入真实 LLM 推理后端。

## Results
- 作者声称在 **inline completions (50 tokens)** 上，**WebSocket+Huffman 比 SSE+JSON 快 28.5%**。
- 在 **small completions (100 tokens)** 上，报告 **12.1% 更快**；在 **large completions (5000 tokens)** 上，报告 **6.4% 更快**。
- 带宽方面，作者给出 **60% bandwidth savings**，并举例为 **3 bytes/token vs 8 bytes/token**。
- 文中还声称相对传统 **JSON+SSE**，可实现 **40–60% 带宽降低** 和 **70% 服务器 CPU 降低**，并据此推断服务器可服务 **约 3x 更多用户**。
- 基准测试中，**WS+Huffman 在 5 个场景中赢了 3 个**。
- 但这些结果**来自 mock benchmarks / mock server**，不是实际推理系统端到端实验；作者明确指出尚未修改真实 LLM server，真实世界效果仍待验证。

## Link
- [https://github.com/vidur2/token_entropy_encoder](https://github.com/vidur2/token_entropy_encoder)
