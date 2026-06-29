---
source: hn
url: https://www.afterpack.dev/blog/claude-code-source-leak
published_at: '2026-04-01T23:25:29'
authors:
- rvz
topics:
- javascript-security
- code-deobfuscation
- llm-code-analysis
- software-supply-chain
- prompt-exposure
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Obfuscation is not security – AI can deobfuscate any minified JavaScript code

## Summary
## 摘要
这篇文章认为，Anthropic 的 Claude Code 源码其实已经通过一个公开的、经过压缩的 JavaScript 包暴露出来，而现代大语言模型几乎不用费力就能从这类代码里还原结构和敏感细节。核心观点是，压缩并不能保护 JavaScript 免受 AI 辅助的逆向分析。

## 问题
- 文章针对一种常见的安全假设：发布压缩后的 JavaScript 就足以隐藏提示词、逻辑、功能开关和内部产品细节。
- 这之所以重要，是因为 JavaScript CLI、Web 应用、Electron 应用和 React Native 应用都会把客户端可见代码发出来，而 LLM 读取并重建压缩代码的速度远快于人工逆向。
- 在 Claude Code 这个案例里，作者认为 source map 泄露只是补上了注释和文件结构，但核心逻辑、提示词、端点和内部标识符本来就在 npm 包里公开了。

## 方法
- 作者分析了公开的 `@anthropic-ai/claude-code` npm 包，重点看其中的 `cli.js` 文件。作者把它描述为一个 13MB、16,824 行的压缩 JavaScript 文件。
- 作者用一个基于 AST 的提取脚本解析这个包，并提取纯文本内容，例如字符串字面量、提示词、遥测事件名、环境变量、错误消息和端点。
- 接着作者让 Claude 自己分析并反混淆这个压缩包，理由是 LLM 很擅长从压缩或变换后的代码中还原出可读结构。
- 文章把压缩和更强的混淆技术做了对比，然后认为即使是传统的 JavaScript 混淆，现在也很难挡住当前的 AI 模型，因为很多变换都基于模式，而且可以逆转。
- 最后，文章把作者的产品 AfterPack 作为替代方案提出，思路是用不可逆或会破坏信息的变换，再配合加密的 source map 供开发者调试。

## 结果
- AST 解析器在 **1.47 秒** 内处理了完整的 13MB `cli.js` 包。
- 作者称从这个文件里提取出了 **147,992** 个字符串，包括 **1,000+** 个 system prompt、**837** 个遥测事件、**504** 个环境变量和 **3,196** 条错误消息。
- 文章说，npm 包里已经明文暴露了硬编码端点、OAuth URL、一个 DataDog API key 和完整的模型目录，不需要泄露的 source map。
- 被泄露的 source map 被描述为覆盖一个 **1,884 个文件** 的项目树，并暴露了注释、文件名、模块边界和内部实验代号。
- 作为外部背景，作者说 Claude Code 的 clean-room Rust 重写版在 **2 小时内** 达到 **50,000** 个 GitHub stars，后来在大约一天内超过 **100,000** 个 stars，但这些是生态影响，不是反混淆方法的基准结果。
- 文章没有给出和其他逆向工具或模型的对照基准，所以这些量化证据只是一个案例研究，加上对一个目标包的提取计数。

## Problem

## Approach

## Results

## Link
- [https://www.afterpack.dev/blog/claude-code-source-leak](https://www.afterpack.dev/blog/claude-code-source-leak)
