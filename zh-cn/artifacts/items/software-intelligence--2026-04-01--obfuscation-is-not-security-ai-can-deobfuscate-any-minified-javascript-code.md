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
这篇文章认为，Anthropic 的 Claude Code 源码早已通过一个公开的压缩 JavaScript 包暴露出来，而现代 LLM 几乎不费力就能从这类代码中还原结构和敏感细节。核心观点是：压缩并不能阻止 AI 辅助的 JavaScript 逆向分析。

## 问题
- 文章针对一种常见的安全假设：发布压缩后的 JavaScript，就足以隐藏提示词、逻辑、功能开关和内部产品细节。
- 这一点很重要，因为 JavaScript CLI、Web 应用、Electron 应用和 React Native 应用都会向客户端交付可见代码，而 LLM 读取和重构压缩代码的速度远快于人工逆向。
- 以 Claude Code 为例，作者认为，泄露的 source map 补充了注释和文件结构，但核心逻辑、提示词、端点和内部标识符本来就已经在 npm 包中公开了。

## 方法
- 作者分析了公开的 `@anthropic-ai/claude-code` npm 包，重点查看其中打包后的 `cli.js` 文件，文中称它是一个 13MB、16,824 行的压缩 JavaScript 文件。
- 作者使用一个基于 AST 的简单提取脚本来解析该包，并提取其中的明文内容，例如字符串字面量、提示词、遥测事件名称、环境变量、错误信息和端点。
- 随后，作者让 Claude 自己分析并反混淆这个压缩包，并认为 LLM 很擅长从压缩或转换过的代码中还原可读结构。
- 文章将压缩与更强的混淆技术做了对比，接着认为即便是传统的 JavaScript 混淆，在当前 AI 模型面前也已经不够有效，因为很多变换都是基于模式且可逆的。
- 最后一部分介绍了作者的产品 AfterPack，作为一种替代方案，依赖不可逆或会销毁信息的变换，并为开发调试提供加密的 source map。

## 结果
- AST 解析器在 **1.47 秒** 内处理完了整个 13MB 的 `cli.js` 包。
- 作者称，从该文件中提取出了 **147,992 个字符串**，其中包括 **1,000+ 条系统提示词**、**837 个遥测事件**、**504 个环境变量** 和 **3,196 条错误信息**。
- 文章称，这个 npm 包以明文形式暴露了硬编码端点、OAuth URL、一个 DataDog API key，以及完整的模型目录，而不需要用到泄露的 source map。
- 文中称，泄露的 source map 覆盖了一个包含 **1,884 个文件** 的项目树，并暴露了注释、文件名、模块边界和内部实验代号。
- 作为外部背景，作者称 Claude Code 的一个 clean-room Rust 重写版本在 **2 小时** 内获得了 **50,000 个 GitHub stars**，随后在大约一天内超过 **100,000+ stars**，但这些属于生态反应，不是该反混淆方法的基准结果。
- 文章没有给出与其他逆向工具或模型的受控基准对比，因此量化证据主要是一项单案例研究，加上对一个目标包的提取计数。

## Problem

## Approach

## Results

## Link
- [https://www.afterpack.dev/blog/claude-code-source-leak](https://www.afterpack.dev/blog/claude-code-source-leak)
