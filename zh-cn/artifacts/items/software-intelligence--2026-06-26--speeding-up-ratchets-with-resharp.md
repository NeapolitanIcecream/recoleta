---
source: hn
url: https://danverbraganza.com/writings/ratchets-run-faster-with-resharp
published_at: '2026-06-26T23:13:00'
authors:
- nvader
topics:
- code-intelligence
- agentic-coding
- software-quality
- rust
- regex-engine
- developer-tools
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# Speeding Up Ratchets with Resharp

## Summary
## 摘要
Ratchets v0.4.0 将 Rust 的 regex crate 替换为 Resharp，并且在 Sculptor 代码库上运行速度约快 15%。这次变更还为基于正则表达式的规则加入了完整的环视支持，这些规则用于 agentic coding 工作流。

## 问题
- Ratchet 系统会阻止禁用代码模式的新实例，同时允许现有技术债随时间减少，这帮助团队添加规则，而无需一次性迁移整个代码库。
- 编码 agent 可能产生风格违规，或添加 `# pyrefly: ignore` 这类快速抑制，因此团队需要低成本检查来引导 agent，而不用写很长的提示词或使用 agent-as-judge。
- Rust 中广泛使用的 `regex` crate 缺少完整的环视支持，这限制了一些 Ratchets 规则，尤其是注释风格规则。

## 方法
- Ratchets 使用 2 种机制检测禁用模式：tree-sitter 抽象语法树查询和正则表达式。
- tree-sitter 处理需要理解语法的检查，因为格式或换行可能导致正则计数出错。
- 对于更容易用文本表达的模式，例如注释风格，正则规则仍然有用。
- 作者在 Ratchets v0.4.0 中将 Rust 的 `regex` crate 替换为 Resharp，以支持环视断言。
- 在文中描述的 agent 工作流中，编码 agent 会看到 ratchet 失败，而规划 agent 可以决定什么时候允许提高 ratchet 计数。

## 结果
- 在 Sculptor 代码库上，将 `regex` 替换为 Resharp 后，Ratchets 运行速度约快 15%。
- 文中比较的是更换引擎前后的 Ratchets，并称没有其他代码变更。
- Ratchets v0.4.0 是破坏性发布，因为它更换了正则表达式引擎。
- 文章报告了 1 个被测代码库 Sculptor，但没有提供绝对运行时间、规则数量、多次运行方差或硬件细节。
- 除速度之外，最强的具体主张是功能层面的：Resharp 加入了 Rust `regex` crate 未提供的完整环视支持。

## Problem

## Approach

## Results

## Link
- [https://danverbraganza.com/writings/ratchets-run-faster-with-resharp](https://danverbraganza.com/writings/ratchets-run-faster-with-resharp)
