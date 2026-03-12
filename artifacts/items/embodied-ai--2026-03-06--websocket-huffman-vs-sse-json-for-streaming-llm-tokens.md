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
---

# WebSocket+Huffman vs. SSE+JSON for streaming LLM tokens

## Summary
这篇工作提出一种面向LLM流式输出的传输层优化：用 **WebSocket + Huffman 编码的 token ID** 替代 **SSE + JSON 文本**。核心目标是在不改变生成内容的前提下，降低带宽、服务器CPU和交互延迟，但当前证据主要来自概念验证与模拟基准。

## Problem
- 现有LLM流式输出通常走 **text → JSON → UTF-8 → SSE/HTTP**，存在表示层冗余，既浪费带宽，也增加解析与编码开销。
- 服务端需要把 token 转成文本并封装为 JSON，再由客户端反向解析，这会增加服务器CPU负担，并限制高并发扩展能力。
- 这很重要，因为代码补全、聊天和移动端场景对**低延迟、低带宽、高并发**非常敏感；但标准API通常只返回文本而非 token ID，使优化难以落地。

## Approach
- 核心方法很简单：**不传文本，改传 token ID**，并对 token ID 使用基于 tokenizer 词表分布的 **Huffman 编码**，直接在“语义符号层”而不是字节层压缩。
- 客户端用 **Rust → WASM** 解码器在浏览器或 Node.js 中增量解码 bitstream，再做 detokenize/显示，从而把部分 token→text 解码成本转移到客户端。
- 传输层使用 **WebSocket 二进制帧**，帧中包含 version、codec id、codebook epoch、payload length 和 CRC；支持周期性 reset、防失步和部分帧解码。
- 编码分布可从全局语料先验开始，并结合用户历史 token 做**贝叶斯更新**，周期性重建 Huffman 树，以适应用户主题/语言风格并提高长期会话压缩率。
- 实现上提供 Rust Huffman 库、约 **160KB** 的 WASM 模块、Node.js 示例和对比基准；但**尚未接入真实LLM推理后端**，当前主要依赖 mock server 模拟。

## Results
- 作者声明在 mock benchmark 中，相比 **SSE+JSON**，**WebSocket+Huffman** 可实现 **40–60% 带宽下降**，文中最具体数字是 **60% bandwidth savings（3 vs 8 bytes/token）**。
- 在时延/速度方面，作者报告：**50 tokens 内联补全快 28.5%**，**100 tokens 小补全快 12.1%**，**5000 tokens 大补全快 6.4%**。
- 文中还声称可带来 **约70% server CPU reduction**，并据此推断“**单服务器可服务约3倍用户**”；但这些结论来自概念验证环境，而非真实在线推理系统。
- 对比结论上，作者称 **WS+Huffman 在 5 个场景中赢了 3 个**，说明收益更偏向短补全、频繁交互和带宽敏感场景，而非所有负载都占优。
- 重要限制：**没有真实LLM服务器集成**、**标准API不返回 token IDs**、**多模型支持需构建时固化 tokenizer**、**尚无真实线上测试**；因此结果更像“协议开销可显著下降”的证据，而不是已被生产验证的系统收益。

## Link
- [https://github.com/vidur2/token_entropy_encoder](https://github.com/vidur2/token_entropy_encoder)
